#!/usr/bin/env python3
"""Pinned Kokoro ONNX assets and a reusable CPU synthesis worker."""

import argparse
import hashlib
import json
import multiprocessing
import re
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_CACHE = ROOT / ".kokoro-models"
_MODEL = None


def asset_path(settings, kind):
    filename = settings[kind + "_file"]
    digest = settings[kind + "_sha256"]
    if Path(filename).name != filename or len(digest) != 64:
        raise ValueError(f"Invalid Kokoro {kind} asset settings")
    target = MODEL_CACHE / digest / filename
    if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == digest:
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    url = ("https://github.com/thewh1teagle/kokoro-onnx/releases/download/"
           f"{settings['release']}/{filename}")
    temporary = target.with_suffix(".download")
    print(f"Downloading Kokoro {kind}: {filename}", flush=True)
    try:
        with urllib.request.urlopen(url, timeout=60) as source, temporary.open("wb") as output:
            shutil.copyfileobj(source, output)
        if hashlib.sha256(temporary.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Kokoro {kind} checksum does not match pinned config")
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    return target


def voice_names(settings):
    # The upstream voice pack is an NPZ archive. Listing keys needs no ML runtime.
    with zipfile.ZipFile(asset_path(settings, "voices")) as archive:
        names = sorted(Path(name).stem for name in archive.namelist() if name.endswith(".npy"))
    if len(names) < 10 or not all(re.fullmatch(r"[a-z][fm]_[a-z0-9_]+", n) for n in names):
        raise ValueError("Kokoro returned an unexpected or empty voice pack")
    return names


def _generate(plan, target, model_path, voices_path):
    global _MODEL
    import numpy as np
    import onnxruntime as ort
    import soundfile as sf
    from kokoro_onnx import Kokoro

    if _MODEL is None:
        # CPU only, with bounded threading on standard GitHub-hosted runners.
        options = ort.SessionOptions()
        options.intra_op_num_threads = 2
        options.inter_op_num_threads = 1
        session = ort.InferenceSession(model_path, sess_options=options,
                                       providers=["CPUExecutionProvider"])
        _MODEL = Kokoro.from_session(session, voices_path)
    speed = 1 + int(plan["rate"][:-1]) / 100
    samples, sample_rate = _MODEL.create(
        plan["text"], voice=plan["voice"], speed=speed, lang=plan["language"],
    )
    samples = np.asarray(samples)
    if samples.size == 0 or not np.isfinite(samples).all():
        raise ValueError("Kokoro returned empty or non-finite audio")
    gain = 1 + int(plan["volume"][:-1]) / 100
    sf.write(target, np.clip(samples * gain, -1, 1), sample_rate, subtype="PCM_16")
    subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", target],
                   check=True, stdout=subprocess.DEVNULL)


class KokoroSynthesizer:
    """Load the model once; kill the worker on timeout so retries cannot overlap."""

    def __init__(self, settings):
        self.settings = settings
        self.pool = None
        self.paths = None

    def generate(self, plan, target, timeout):
        if self.paths is None:
            self.paths = tuple(str(asset_path(self.settings, kind)) for kind in ("model", "voices"))
        if self.pool is None:
            self.pool = multiprocessing.get_context("spawn").Pool(1)
        try:
            self.pool.apply_async(_generate, (plan, str(target), *self.paths)).get(timeout=timeout)
        except multiprocessing.TimeoutError as exc:
            self.close()
            raise TimeoutError(f"Kokoro synthesis exceeded {timeout}s") from exc
        except Exception:
            self.close()
            raise

    def close(self):
        if self.pool is not None:
            self.pool.terminate()
            self.pool.join()
            self.pool = None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", required=True)
    parser.parse_args()
    settings = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))["kokoro"]
    for kind in ("model", "voices"):
        print(asset_path(settings, kind))
