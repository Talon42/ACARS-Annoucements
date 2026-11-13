# Edge and Kokoro voice catalog

Run **Actions > Refresh TTS Voices > Run workflow** to update both engines together.
The weekly refresh runs on the default branch. Select kokoro for a manual branch refresh; both engines refresh weekly after merge.

**Available voices:** 376 (322 Edge, 54 Kokoro)

Set tts_engine in config.json to edge or kokoro. Role defaults are in `roles.<role>.voices.<engine>`.
A templates.json voice override must belong to the selected engine.

Kokoro entries come from the voice pack configured in config.json, so the list matches the installed model assets.
This generator currently supports American and British English Kokoro voices; other voices are listed for reference.
Kokoro model weights: Apache-2.0. See https://huggingface.co/hexgrad/Kokoro-82M.

| Engine | Short name | Gender | Locale | Friendly name | Supported by generator |
| --- | --- | --- | --- | --- | --- |
| edge | af-ZA-AdriNeural | Female | af-ZA | Microsoft Adri Online (Natural) - Afrikaans (South Africa) | Yes |
| edge | af-ZA-WillemNeural | Male | af-ZA | Microsoft Willem Online (Natural) - Afrikaans (South Africa) | Yes |
| edge | am-ET-AmehaNeural | Male | am-ET | Microsoft Ameha Online (Natural) - Amharic (Ethiopia) | Yes |
| edge | am-ET-MekdesNeural | Female | am-ET | Microsoft Mekdes Online (Natural) - Amharic (Ethiopia) | Yes |
| edge | ar-AE-FatimaNeural | Female | ar-AE | Microsoft Fatima Online (Natural) - Arabic (United Arab Emirates) | Yes |
| edge | ar-AE-HamdanNeural | Male | ar-AE | Microsoft Hamdan Online (Natural) - Arabic (United Arab Emirates) | Yes |
| edge | ar-BH-AliNeural | Male | ar-BH | Microsoft Ali Online (Natural) - Arabic (Bahrain) | Yes |
| edge | ar-BH-LailaNeural | Female | ar-BH | Microsoft Laila Online (Natural) - Arabic (Bahrain) | Yes |
| edge | ar-DZ-AminaNeural | Female | ar-DZ | Microsoft Amina Online (Natural) - Arabic (Algeria) | Yes |
| edge | ar-DZ-IsmaelNeural | Male | ar-DZ | Microsoft Ismael Online (Natural) - Arabic (Algeria) | Yes |
| edge | ar-EG-SalmaNeural | Female | ar-EG | Microsoft Salma Online (Natural) - Arabic (Egypt) | Yes |
| edge | ar-EG-ShakirNeural | Male | ar-EG | Microsoft Shakir Online (Natural) - Arabic (Egypt) | Yes |
| edge | ar-IQ-BasselNeural | Male | ar-IQ | Microsoft Bassel Online (Natural) - Arabic (Iraq) | Yes |
| edge | ar-IQ-RanaNeural | Female | ar-IQ | Microsoft Rana Online (Natural) - Arabic (Iraq) | Yes |
| edge | ar-JO-SanaNeural | Female | ar-JO | Microsoft Sana Online (Natural) - Arabic (Jordan) | Yes |
| edge | ar-JO-TaimNeural | Male | ar-JO | Microsoft Taim Online (Natural) - Arabic (Jordan) | Yes |
| edge | ar-KW-FahedNeural | Male | ar-KW | Microsoft Fahed Online (Natural) - Arabic (Kuwait) | Yes |
| edge | ar-KW-NouraNeural | Female | ar-KW | Microsoft Noura Online (Natural) - Arabic (Kuwait) | Yes |
| edge | ar-LB-LaylaNeural | Female | ar-LB | Microsoft Layla Online (Natural) - Arabic (Lebanon) | Yes |
| edge | ar-LB-RamiNeural | Male | ar-LB | Microsoft Rami Online (Natural) - Arabic (Lebanon) | Yes |
| edge | ar-LY-ImanNeural | Female | ar-LY | Microsoft Iman Online (Natural) - Arabic (Libya) | Yes |
| edge | ar-LY-OmarNeural | Male | ar-LY | Microsoft Omar Online (Natural) - Arabic (Libya) | Yes |
| edge | ar-MA-JamalNeural | Male | ar-MA | Microsoft Jamal Online (Natural) - Arabic (Morocco) | Yes |
| edge | ar-MA-MounaNeural | Female | ar-MA | Microsoft Mouna Online (Natural) - Arabic (Morocco) | Yes |
| edge | ar-OM-AbdullahNeural | Male | ar-OM | Microsoft Abdullah Online (Natural) - Arabic (Oman) | Yes |
| edge | ar-OM-AyshaNeural | Female | ar-OM | Microsoft Aysha Online (Natural) - Arabic (Oman) | Yes |
| edge | ar-QA-AmalNeural | Female | ar-QA | Microsoft Amal Online (Natural) - Arabic (Qatar) | Yes |
| edge | ar-QA-MoazNeural | Male | ar-QA | Microsoft Moaz Online (Natural) - Arabic (Qatar) | Yes |
| edge | ar-SA-HamedNeural | Male | ar-SA | Microsoft Hamed Online (Natural) - Arabic (Saudi Arabia) | Yes |
| edge | ar-SA-ZariyahNeural | Female | ar-SA | Microsoft Zariyah Online (Natural) - Arabic (Saudi Arabia) | Yes |
| edge | ar-SY-AmanyNeural | Female | ar-SY | Microsoft Amany Online (Natural) - Arabic (Syria) | Yes |
| edge | ar-SY-LaithNeural | Male | ar-SY | Microsoft Laith Online (Natural) - Arabic (Syria) | Yes |
| edge | ar-TN-HediNeural | Male | ar-TN | Microsoft Hedi Online (Natural) - Arabic (Tunisia) | Yes |
| edge | ar-TN-ReemNeural | Female | ar-TN | Microsoft Reem Online (Natural) - Arabic (Tunisia) | Yes |
| edge | ar-YE-MaryamNeural | Female | ar-YE | Microsoft Maryam Online (Natural) - Arabic (Yemen) | Yes |
| edge | ar-YE-SalehNeural | Male | ar-YE | Microsoft Saleh Online (Natural) - Arabic (Yemen) | Yes |
| edge | az-AZ-BabekNeural | Male | az-AZ | Microsoft Babek Online (Natural) - Azerbaijani (Azerbaijan) | Yes |
| edge | az-AZ-BanuNeural | Female | az-AZ | Microsoft Banu Online (Natural) - Azerbaijani (Azerbaijan) | Yes |
| edge | bg-BG-BorislavNeural | Male | bg-BG | Microsoft Borislav Online (Natural) - Bulgarian (Bulgaria) | Yes |
| edge | bg-BG-KalinaNeural | Female | bg-BG | Microsoft Kalina Online (Natural) - Bulgarian (Bulgaria) | Yes |
| edge | bn-BD-NabanitaNeural | Female | bn-BD | Microsoft Nabanita Online (Natural) - Bangla (Bangladesh) | Yes |
| edge | bn-BD-PradeepNeural | Male | bn-BD | Microsoft Pradeep Online (Natural) - Bangla (Bangladesh) | Yes |
| edge | bn-IN-BashkarNeural | Male | bn-IN | Microsoft Bashkar Online (Natural) - Bangla (India) | Yes |
| edge | bn-IN-TanishaaNeural | Female | bn-IN | Microsoft Tanishaa Online (Natural) - Bengali (India) | Yes |
| edge | bs-BA-GoranNeural | Male | bs-BA | Microsoft Goran Online (Natural) - Bosnian (Bosnia) | Yes |
| edge | bs-BA-VesnaNeural | Female | bs-BA | Microsoft Vesna Online (Natural) - Bosnian (Bosnia and Herzegovina) | Yes |
| edge | ca-ES-EnricNeural | Male | ca-ES | Microsoft Enric Online (Natural) - Catalan | Yes |
| edge | ca-ES-JoanaNeural | Female | ca-ES | Microsoft Joana Online (Natural) - Catalan | Yes |
| edge | cs-CZ-AntoninNeural | Male | cs-CZ | Microsoft Antonin Online (Natural) - Czech (Czech) | Yes |
| edge | cs-CZ-VlastaNeural | Female | cs-CZ | Microsoft Vlasta Online (Natural) - Czech (Czech) | Yes |
| edge | cy-GB-AledNeural | Male | cy-GB | Microsoft Aled Online (Natural) - Welsh (United Kingdom) | Yes |
| edge | cy-GB-NiaNeural | Female | cy-GB | Microsoft Nia Online (Natural) - Welsh (United Kingdom) | Yes |
| edge | da-DK-ChristelNeural | Female | da-DK | Microsoft Christel Online (Natural) - Danish (Denmark) | Yes |
| edge | da-DK-JeppeNeural | Male | da-DK | Microsoft Jeppe Online (Natural) - Danish (Denmark) | Yes |
| edge | de-AT-IngridNeural | Female | de-AT | Microsoft Ingrid Online (Natural) - German (Austria) | Yes |
| edge | de-AT-JonasNeural | Male | de-AT | Microsoft Jonas Online (Natural) - German (Austria) | Yes |
| edge | de-CH-JanNeural | Male | de-CH | Microsoft Jan Online (Natural) - German (Switzerland) | Yes |
| edge | de-CH-LeniNeural | Female | de-CH | Microsoft Leni Online (Natural) - German (Switzerland) | Yes |
| edge | de-DE-AmalaNeural | Female | de-DE | Microsoft Amala Online (Natural) - German (Germany) | Yes |
| edge | de-DE-ConradNeural | Male | de-DE | Microsoft Conrad Online (Natural) - German (Germany) | Yes |
| edge | de-DE-FlorianMultilingualNeural | Male | de-DE | Microsoft FlorianMultilingual Online (Natural) - German (Germany) | Yes |
| edge | de-DE-KatjaNeural | Female | de-DE | Microsoft Katja Online (Natural) - German (Germany) | Yes |
| edge | de-DE-KillianNeural | Male | de-DE | Microsoft Killian Online (Natural) - German (Germany) | Yes |
| edge | de-DE-SeraphinaMultilingualNeural | Female | de-DE | Microsoft SeraphinaMultilingual Online (Natural) - German (Germany) | Yes |
| edge | el-GR-AthinaNeural | Female | el-GR | Microsoft Athina Online (Natural) - Greek (Greece) | Yes |
| edge | el-GR-NestorasNeural | Male | el-GR | Microsoft Nestoras Online (Natural) - Greek (Greece) | Yes |
| edge | en-AU-NatashaNeural | Female | en-AU | Microsoft Natasha Online (Natural) - English (Australia) | Yes |
| edge | en-AU-WilliamMultilingualNeural | Male | en-AU | Microsoft WilliamMultilingual Online (Natural) - English (Australia) | Yes |
| edge | en-CA-ClaraNeural | Female | en-CA | Microsoft Clara Online (Natural) - English (Canada) | Yes |
| edge | en-CA-LiamNeural | Male | en-CA | Microsoft Liam Online (Natural) - English (Canada) | Yes |
| edge | en-GB-LibbyNeural | Female | en-GB | Microsoft Libby Online (Natural) - English (United Kingdom) | Yes |
| edge | en-GB-MaisieNeural | Female | en-GB | Microsoft Maisie Online (Natural) - English (United Kingdom) | Yes |
| edge | en-GB-RyanNeural | Male | en-GB | Microsoft Ryan Online (Natural) - English (United Kingdom) | Yes |
| edge | en-GB-SoniaNeural | Female | en-GB | Microsoft Sonia Online (Natural) - English (United Kingdom) | Yes |
| edge | en-GB-ThomasNeural | Male | en-GB | Microsoft Thomas Online (Natural) - English (United Kingdom) | Yes |
| edge | en-HK-SamNeural | Male | en-HK | Microsoft Sam Online (Natural) - English (Hongkong) | Yes |
| edge | en-HK-YanNeural | Female | en-HK | Microsoft Yan Online (Natural) - English (Hong Kong SAR) | Yes |
| edge | en-IE-ConnorNeural | Male | en-IE | Microsoft Connor Online (Natural) - English (Ireland) | Yes |
| edge | en-IE-EmilyNeural | Female | en-IE | Microsoft Emily Online (Natural) - English (Ireland) | Yes |
| edge | en-IN-NeerjaExpressiveNeural | Female | en-IN | Microsoft Neerja Online (Natural) - English (India) (Preview) | Yes |
| edge | en-IN-NeerjaNeural | Female | en-IN | Microsoft Neerja Online (Natural) - English (India) | Yes |
| edge | en-IN-PrabhatNeural | Male | en-IN | Microsoft Prabhat Online (Natural) - English (India) | Yes |
| edge | en-KE-AsiliaNeural | Female | en-KE | Microsoft Asilia Online (Natural) - English (Kenya) | Yes |
| edge | en-KE-ChilembaNeural | Male | en-KE | Microsoft Chilemba Online (Natural) - English (Kenya) | Yes |
| edge | en-NG-AbeoNeural | Male | en-NG | Microsoft Abeo Online (Natural) - English (Nigeria) | Yes |
| edge | en-NG-EzinneNeural | Female | en-NG | Microsoft Ezinne Online (Natural) - English (Nigeria) | Yes |
| edge | en-NZ-MitchellNeural | Male | en-NZ | Microsoft Mitchell Online (Natural) - English (New Zealand) | Yes |
| edge | en-NZ-MollyNeural | Female | en-NZ | Microsoft Molly Online (Natural) - English (New Zealand) | Yes |
| edge | en-PH-JamesNeural | Male | en-PH | Microsoft James Online (Natural) - English (Philippines) | Yes |
| edge | en-PH-RosaNeural | Female | en-PH | Microsoft Rosa Online (Natural) - English (Philippines) | Yes |
| edge | en-SG-LunaNeural | Female | en-SG | Microsoft Luna Online (Natural) - English (Singapore) | Yes |
| edge | en-SG-WayneNeural | Male | en-SG | Microsoft Wayne Online (Natural) - English (Singapore) | Yes |
| edge | en-TZ-ElimuNeural | Male | en-TZ | Microsoft Elimu Online (Natural) - English (Tanzania) | Yes |
| edge | en-TZ-ImaniNeural | Female | en-TZ | Microsoft Imani Online (Natural) - English (Tanzania) | Yes |
| edge | en-US-AnaNeural | Female | en-US | Microsoft Ana Online (Natural) - English (United States) | Yes |
| edge | en-US-AndrewMultilingualNeural | Male | en-US | Microsoft AndrewMultilingual Online (Natural) - English (United States) | Yes |
| edge | en-US-AndrewNeural | Male | en-US | Microsoft Andrew Online (Natural) - English (United States) | Yes |
| edge | en-US-AriaNeural | Female | en-US | Microsoft Aria Online (Natural) - English (United States) | Yes |
| edge | en-US-AvaMultilingualNeural | Female | en-US | Microsoft AvaMultilingual Online (Natural) - English (United States) | Yes |
| edge | en-US-AvaNeural | Female | en-US | Microsoft Ava Online (Natural) - English (United States) | Yes |
| edge | en-US-BrianMultilingualNeural | Male | en-US | Microsoft BrianMultilingual Online (Natural) - English (United States) | Yes |
| edge | en-US-BrianNeural | Male | en-US | Microsoft Brian Online (Natural) - English (United States) | Yes |
| edge | en-US-ChristopherNeural | Male | en-US | Microsoft Christopher Online (Natural) - English (United States) | Yes |
| edge | en-US-EmmaMultilingualNeural | Female | en-US | Microsoft EmmaMultilingual Online (Natural) - English (United States) | Yes |
| edge | en-US-EmmaNeural | Female | en-US | Microsoft Emma Online (Natural) - English (United States) | Yes |
| edge | en-US-EricNeural | Male | en-US | Microsoft Eric Online (Natural) - English (United States) | Yes |
| edge | en-US-GuyNeural | Male | en-US | Microsoft Guy Online (Natural) - English (United States) | Yes |
| edge | en-US-JennyNeural | Female | en-US | Microsoft Jenny Online (Natural) - English (United States) | Yes |
| edge | en-US-MichelleNeural | Female | en-US | Microsoft Michelle Online (Natural) - English (United States) | Yes |
| edge | en-US-RogerNeural | Male | en-US | Microsoft Roger Online (Natural) - English (United States) | Yes |
| edge | en-US-SteffanNeural | Male | en-US | Microsoft Steffan Online (Natural) - English (United States) | Yes |
| edge | en-ZA-LeahNeural | Female | en-ZA | Microsoft Leah Online (Natural) - English (South Africa) | Yes |
| edge | en-ZA-LukeNeural | Male | en-ZA | Microsoft Luke Online (Natural) - English (South Africa) | Yes |
| edge | es-AR-ElenaNeural | Female | es-AR | Microsoft Elena Online (Natural) - Spanish (Argentina) | Yes |
| edge | es-AR-TomasNeural | Male | es-AR | Microsoft Tomas Online (Natural) - Spanish (Argentina) | Yes |
| edge | es-BO-MarceloNeural | Male | es-BO | Microsoft Marcelo Online (Natural) - Spanish (Bolivia) | Yes |
| edge | es-BO-SofiaNeural | Female | es-BO | Microsoft Sofia Online (Natural) - Spanish (Bolivia) | Yes |
| edge | es-CL-CatalinaNeural | Female | es-CL | Microsoft Catalina Online (Natural) - Spanish (Chile) | Yes |
| edge | es-CL-LorenzoNeural | Male | es-CL | Microsoft Lorenzo Online (Natural) - Spanish (Chile) | Yes |
| edge | es-CO-GonzaloNeural | Male | es-CO | Microsoft Gonzalo Online (Natural) - Spanish (Colombia) | Yes |
| edge | es-CO-SalomeNeural | Female | es-CO | Microsoft Salome Online (Natural) - Spanish (Colombia) | Yes |
| edge | es-CR-JuanNeural | Male | es-CR | Microsoft Juan Online (Natural) - Spanish (Costa Rica) | Yes |
| edge | es-CR-MariaNeural | Female | es-CR | Microsoft Maria Online (Natural) - Spanish (Costa Rica) | Yes |
| edge | es-CU-BelkysNeural | Female | es-CU | Microsoft Belkys Online (Natural) - Spanish (Cuba) | Yes |
| edge | es-CU-ManuelNeural | Male | es-CU | Microsoft Manuel Online (Natural) - Spanish (Cuba) | Yes |
| edge | es-DO-EmilioNeural | Male | es-DO | Microsoft Emilio Online (Natural) - Spanish (Dominican Republic) | Yes |
| edge | es-DO-RamonaNeural | Female | es-DO | Microsoft Ramona Online (Natural) - Spanish (Dominican Republic) | Yes |
| edge | es-EC-AndreaNeural | Female | es-EC | Microsoft Andrea Online (Natural) - Spanish (Ecuador) | Yes |
| edge | es-EC-LuisNeural | Male | es-EC | Microsoft Luis Online (Natural) - Spanish (Ecuador) | Yes |
| edge | es-ES-AlvaroNeural | Male | es-ES | Microsoft Alvaro Online (Natural) - Spanish (Spain) | Yes |
| edge | es-ES-ElviraNeural | Female | es-ES | Microsoft Elvira Online (Natural) - Spanish (Spain) | Yes |
| edge | es-ES-XimenaNeural | Female | es-ES | Microsoft Ximena Online (Natural) - Spanish (Colombia) | Yes |
| edge | es-GQ-JavierNeural | Male | es-GQ | Microsoft Javier Online (Natural) - Spanish (Equatorial Guinea) | Yes |
| edge | es-GQ-TeresaNeural | Female | es-GQ | Microsoft Teresa Online (Natural) - Spanish (Equatorial Guinea) | Yes |
| edge | es-GT-AndresNeural | Male | es-GT | Microsoft Andres Online (Natural) - Spanish (Guatemala) | Yes |
| edge | es-GT-MartaNeural | Female | es-GT | Microsoft Marta Online (Natural) - Spanish (Guatemala) | Yes |
| edge | es-HN-CarlosNeural | Male | es-HN | Microsoft Carlos Online (Natural) - Spanish (Honduras) | Yes |
| edge | es-HN-KarlaNeural | Female | es-HN | Microsoft Karla Online (Natural) - Spanish (Honduras) | Yes |
| edge | es-MX-DaliaNeural | Female | es-MX | Microsoft Dalia Online (Natural) - Spanish (Mexico) | Yes |
| edge | es-MX-JorgeNeural | Male | es-MX | Microsoft Jorge Online (Natural) - Spanish (Mexico) | Yes |
| edge | es-NI-FedericoNeural | Male | es-NI | Microsoft Federico Online (Natural) - Spanish (Nicaragua) | Yes |
| edge | es-NI-YolandaNeural | Female | es-NI | Microsoft Yolanda Online (Natural) - Spanish (Nicaragua) | Yes |
| edge | es-PA-MargaritaNeural | Female | es-PA | Microsoft Margarita Online (Natural) - Spanish (Panama) | Yes |
| edge | es-PA-RobertoNeural | Male | es-PA | Microsoft Roberto Online (Natural) - Spanish (Panama) | Yes |
| edge | es-PE-AlexNeural | Male | es-PE | Microsoft Alex Online (Natural) - Spanish (Peru) | Yes |
| edge | es-PE-CamilaNeural | Female | es-PE | Microsoft Camila Online (Natural) - Spanish (Peru) | Yes |
| edge | es-PR-KarinaNeural | Female | es-PR | Microsoft Karina Online (Natural) - Spanish (Puerto Rico) | Yes |
| edge | es-PR-VictorNeural | Male | es-PR | Microsoft Victor Online (Natural) - Spanish (Puerto Rico) | Yes |
| edge | es-PY-MarioNeural | Male | es-PY | Microsoft Mario Online (Natural) - Spanish (Paraguay) | Yes |
| edge | es-PY-TaniaNeural | Female | es-PY | Microsoft Tania Online (Natural) - Spanish (Paraguay) | Yes |
| edge | es-SV-LorenaNeural | Female | es-SV | Microsoft Lorena Online (Natural) - Spanish (El Salvador) | Yes |
| edge | es-SV-RodrigoNeural | Male | es-SV | Microsoft Rodrigo Online (Natural) - Spanish (El Salvador) | Yes |
| edge | es-US-AlonsoNeural | Male | es-US | Microsoft Alonso Online (Natural) - Spanish (United States) | Yes |
| edge | es-US-PalomaNeural | Female | es-US | Microsoft Paloma Online (Natural) - Spanish (United States) | Yes |
| edge | es-UY-MateoNeural | Male | es-UY | Microsoft Mateo Online (Natural) - Spanish (Uruguay) | Yes |
| edge | es-UY-ValentinaNeural | Female | es-UY | Microsoft Valentina Online (Natural) - Spanish (Uruguay) | Yes |
| edge | es-VE-PaolaNeural | Female | es-VE | Microsoft Paola Online (Natural) - Spanish (Venezuela) | Yes |
| edge | es-VE-SebastianNeural | Male | es-VE | Microsoft Sebastian Online (Natural) - Spanish (Venezuela) | Yes |
| edge | et-EE-AnuNeural | Female | et-EE | Microsoft Anu Online (Natural) - Estonian (Estonia) | Yes |
| edge | et-EE-KertNeural | Male | et-EE | Microsoft Kert Online (Natural) - Estonian (Estonia) | Yes |
| edge | fa-IR-DilaraNeural | Female | fa-IR | Microsoft Dilara Online (Natural) - Persian (Iran) | Yes |
| edge | fa-IR-FaridNeural | Male | fa-IR | Microsoft Farid Online (Natural) - Persian (Iran) | Yes |
| edge | fi-FI-HarriNeural | Male | fi-FI | Microsoft Harri Online (Natural) - Finnish (Finland) | Yes |
| edge | fi-FI-NooraNeural | Female | fi-FI | Microsoft Noora Online (Natural) - Finnish (Finland) | Yes |
| edge | fil-PH-AngeloNeural | Male | fil-PH | Microsoft Angelo Online (Natural) - Filipino (Philippines) | Yes |
| edge | fil-PH-BlessicaNeural | Female | fil-PH | Microsoft Blessica Online (Natural) - Filipino (Philippines) | Yes |
| edge | fr-BE-CharlineNeural | Female | fr-BE | Microsoft Charline Online (Natural) - French (Belgium) | Yes |
| edge | fr-BE-GerardNeural | Male | fr-BE | Microsoft Gerard Online (Natural) - French (Belgium) | Yes |
| edge | fr-CA-AntoineNeural | Male | fr-CA | Microsoft Antoine Online (Natural) - French (Canada) | Yes |
| edge | fr-CA-JeanNeural | Male | fr-CA | Microsoft Jean Online (Natural) - French (Canada) | Yes |
| edge | fr-CA-SylvieNeural | Female | fr-CA | Microsoft Sylvie Online (Natural) - French (Canada) | Yes |
| edge | fr-CA-ThierryNeural | Male | fr-CA | Microsoft Thierry Online (Natural) - French (Canada) | Yes |
| edge | fr-CH-ArianeNeural | Female | fr-CH | Microsoft Ariane Online (Natural) - French (Switzerland) | Yes |
| edge | fr-CH-FabriceNeural | Male | fr-CH | Microsoft Fabrice Online (Natural) - French (Switzerland) | Yes |
| edge | fr-FR-DeniseNeural | Female | fr-FR | Microsoft Denise Online (Natural) - French (France) | Yes |
| edge | fr-FR-EloiseNeural | Female | fr-FR | Microsoft Eloise Online (Natural) - French (France) | Yes |
| edge | fr-FR-HenriNeural | Male | fr-FR | Microsoft Henri Online (Natural) - French (France) | Yes |
| edge | fr-FR-RemyMultilingualNeural | Male | fr-FR | Microsoft RemyMultilingual Online (Natural) - French (France) | Yes |
| edge | fr-FR-VivienneMultilingualNeural | Female | fr-FR | Microsoft VivienneMultilingual Online (Natural) - French (France) | Yes |
| edge | ga-IE-ColmNeural | Male | ga-IE | Microsoft Colm Online (Natural) - Irish (Ireland) | Yes |
| edge | ga-IE-OrlaNeural | Female | ga-IE | Microsoft Orla Online (Natural) - Irish (Ireland) | Yes |
| edge | gl-ES-RoiNeural | Male | gl-ES | Microsoft Roi Online (Natural) - Galician | Yes |
| edge | gl-ES-SabelaNeural | Female | gl-ES | Microsoft Sabela Online (Natural) - Galician | Yes |
| edge | gu-IN-DhwaniNeural | Female | gu-IN | Microsoft Dhwani Online (Natural) - Gujarati (India) | Yes |
| edge | gu-IN-NiranjanNeural | Male | gu-IN | Microsoft Niranjan Online (Natural) - Gujarati (India) | Yes |
| edge | he-IL-AvriNeural | Male | he-IL | Microsoft Avri Online (Natural) - Hebrew (Israel) | Yes |
| edge | he-IL-HilaNeural | Female | he-IL | Microsoft Hila Online (Natural) - Hebrew (Israel) | Yes |
| edge | hi-IN-MadhurNeural | Male | hi-IN | Microsoft Madhur Online (Natural) - Hindi (India) | Yes |
| edge | hi-IN-SwaraNeural | Female | hi-IN | Microsoft Swara Online (Natural) - Hindi (India) | Yes |
| edge | hr-HR-GabrijelaNeural | Female | hr-HR | Microsoft Gabrijela Online (Natural) - Croatian (Croatia) | Yes |
| edge | hr-HR-SreckoNeural | Male | hr-HR | Microsoft Srecko Online (Natural) - Croatian (Croatia) | Yes |
| edge | hu-HU-NoemiNeural | Female | hu-HU | Microsoft Noemi Online (Natural) - Hungarian (Hungary) | Yes |
| edge | hu-HU-TamasNeural | Male | hu-HU | Microsoft Tamas Online (Natural) - Hungarian (Hungary) | Yes |
| edge | id-ID-ArdiNeural | Male | id-ID | Microsoft Ardi Online (Natural) - Indonesian (Indonesia) | Yes |
| edge | id-ID-GadisNeural | Female | id-ID | Microsoft Gadis Online (Natural) - Indonesian (Indonesia) | Yes |
| edge | is-IS-GudrunNeural | Female | is-IS | Microsoft Gudrun Online (Natural) - Icelandic (Iceland) | Yes |
| edge | is-IS-GunnarNeural | Male | is-IS | Microsoft Gunnar Online (Natural) - Icelandic (Iceland) | Yes |
| edge | it-IT-DiegoNeural | Male | it-IT | Microsoft Diego Online (Natural) - Italian (Italy) | Yes |
| edge | it-IT-ElsaNeural | Female | it-IT | Microsoft Elsa Online (Natural) - Italian (Italy) | Yes |
| edge | it-IT-GiuseppeMultilingualNeural | Male | it-IT | Microsoft GiuseppeMultilingual Online (Natural) - Italian (Italy) | Yes |
| edge | it-IT-IsabellaNeural | Female | it-IT | Microsoft Isabella Online (Natural) - Italian (Italy) | Yes |
| edge | iu-Cans-CA-SiqiniqNeural | Female | iu-Cans-CA | Microsoft Siqiniq Online (Natural) - Inuktitut (Syllabics, Canada) | Yes |
| edge | iu-Cans-CA-TaqqiqNeural | Male | iu-Cans-CA | Microsoft Taqqiq Online (Natural) - Inuktitut (Syllabics, Canada) | Yes |
| edge | iu-Latn-CA-SiqiniqNeural | Female | iu-Latn-CA | Microsoft Siqiniq Online (Natural) - Inuktitut (Latin, Canada) | Yes |
| edge | iu-Latn-CA-TaqqiqNeural | Male | iu-Latn-CA | Microsoft Taqqiq Online (Natural) - Inuktitut (Latin, Canada) | Yes |
| edge | ja-JP-KeitaNeural | Male | ja-JP | Microsoft Keita Online (Natural) - Japanese (Japan) | Yes |
| edge | ja-JP-NanamiNeural | Female | ja-JP | Microsoft Nanami Online (Natural) - Japanese (Japan) | Yes |
| edge | jv-ID-DimasNeural | Male | jv-ID | Microsoft Dimas Online (Natural) - Javanese (Indonesia) | Yes |
| edge | jv-ID-SitiNeural | Female | jv-ID | Microsoft Siti Online (Natural) - Javanese (Indonesia) | Yes |
| edge | ka-GE-EkaNeural | Female | ka-GE | Microsoft Eka Online (Natural) - Georgian (Georgia) | Yes |
| edge | ka-GE-GiorgiNeural | Male | ka-GE | Microsoft Giorgi Online (Natural) - Georgian (Georgia) | Yes |
| edge | kk-KZ-AigulNeural | Female | kk-KZ | Microsoft Aigul Online (Natural) - Kazakh (Kazakhstan) | Yes |
| edge | kk-KZ-DauletNeural | Male | kk-KZ | Microsoft Daulet Online (Natural) - Kazakh (Kazakhstan) | Yes |
| edge | km-KH-PisethNeural | Male | km-KH | Microsoft Piseth Online (Natural) - Khmer (Cambodia) | Yes |
| edge | km-KH-SreymomNeural | Female | km-KH | Microsoft Sreymom Online (Natural) - Khmer (Cambodia) | Yes |
| edge | kn-IN-GaganNeural | Male | kn-IN | Microsoft Gagan Online (Natural) - Kannada (India) | Yes |
| edge | kn-IN-SapnaNeural | Female | kn-IN | Microsoft Sapna Online (Natural) - Kannada (India) | Yes |
| edge | ko-KR-HyunsuMultilingualNeural | Male | ko-KR | Microsoft HyunsuMultilingual Online (Natural) - Korean (Korea) | Yes |
| edge | ko-KR-InJoonNeural | Male | ko-KR | Microsoft InJoon Online (Natural) - Korean (Korea) | Yes |
| edge | ko-KR-SunHiNeural | Female | ko-KR | Microsoft SunHi Online (Natural) - Korean (Korea) | Yes |
| edge | lo-LA-ChanthavongNeural | Male | lo-LA | Microsoft Chanthavong Online (Natural) - Lao (Laos) | Yes |
| edge | lo-LA-KeomanyNeural | Female | lo-LA | Microsoft Keomany Online (Natural) - Lao (Laos) | Yes |
| edge | lt-LT-LeonasNeural | Male | lt-LT | Microsoft Leonas Online (Natural) - Lithuanian (Lithuania) | Yes |
| edge | lt-LT-OnaNeural | Female | lt-LT | Microsoft Ona Online (Natural) - Lithuanian (Lithuania) | Yes |
| edge | lv-LV-EveritaNeural | Female | lv-LV | Microsoft Everita Online (Natural) - Latvian (Latvia) | Yes |
| edge | lv-LV-NilsNeural | Male | lv-LV | Microsoft Nils Online (Natural) - Latvian (Latvia) | Yes |
| edge | mk-MK-AleksandarNeural | Male | mk-MK | Microsoft Aleksandar Online (Natural) - Macedonian (North Macedonia) | Yes |
| edge | mk-MK-MarijaNeural | Female | mk-MK | Microsoft Marija Online (Natural) - Macedonian (North Macedonia) | Yes |
| edge | ml-IN-MidhunNeural | Male | ml-IN | Microsoft Midhun Online (Natural) - Malayalam (India) | Yes |
| edge | ml-IN-SobhanaNeural | Female | ml-IN | Microsoft Sobhana Online (Natural) - Malayalam (India) | Yes |
| edge | mn-MN-BataaNeural | Male | mn-MN | Microsoft Bataa Online (Natural) - Mongolian (Mongolia) | Yes |
| edge | mn-MN-YesuiNeural | Female | mn-MN | Microsoft Yesui Online (Natural) - Mongolian (Mongolia) | Yes |
| edge | mr-IN-AarohiNeural | Female | mr-IN | Microsoft Aarohi Online (Natural) - Marathi (India) | Yes |
| edge | mr-IN-ManoharNeural | Male | mr-IN | Microsoft Manohar Online (Natural) - Marathi (India) | Yes |
| edge | ms-MY-OsmanNeural | Male | ms-MY | Microsoft Osman Online (Natural) - Malay (Malaysia) | Yes |
| edge | ms-MY-YasminNeural | Female | ms-MY | Microsoft Yasmin Online (Natural) - Malay (Malaysia) | Yes |
| edge | mt-MT-GraceNeural | Female | mt-MT | Microsoft Grace Online (Natural) - Maltese (Malta) | Yes |
| edge | mt-MT-JosephNeural | Male | mt-MT | Microsoft Joseph Online (Natural) - Maltese (Malta) | Yes |
| edge | my-MM-NilarNeural | Female | my-MM | Microsoft Nilar Online (Natural) - Burmese (Myanmar) | Yes |
| edge | my-MM-ThihaNeural | Male | my-MM | Microsoft Thiha Online (Natural) - Burmese (Myanmar) | Yes |
| edge | nb-NO-FinnNeural | Male | nb-NO | Microsoft Finn Online (Natural) - Norwegian (Bokmål Norway) | Yes |
| edge | nb-NO-PernilleNeural | Female | nb-NO | Microsoft Pernille Online (Natural) - Norwegian (Bokmål, Norway) | Yes |
| edge | ne-NP-HemkalaNeural | Female | ne-NP | Microsoft Hemkala Online (Natural) - Nepali (Nepal) | Yes |
| edge | ne-NP-SagarNeural | Male | ne-NP | Microsoft Sagar Online (Natural) - Nepali (Nepal) | Yes |
| edge | nl-BE-ArnaudNeural | Male | nl-BE | Microsoft Arnaud Online (Natural) - Dutch (Belgium) | Yes |
| edge | nl-BE-DenaNeural | Female | nl-BE | Microsoft Dena Online (Natural) - Dutch (Belgium) | Yes |
| edge | nl-NL-ColetteNeural | Female | nl-NL | Microsoft Colette Online (Natural) - Dutch (Netherlands) | Yes |
| edge | nl-NL-FennaNeural | Female | nl-NL | Microsoft Fenna Online (Natural) - Dutch (Netherlands) | Yes |
| edge | nl-NL-MaartenNeural | Male | nl-NL | Microsoft Maarten Online (Natural) - Dutch (Netherlands) | Yes |
| edge | pl-PL-MarekNeural | Male | pl-PL | Microsoft Marek Online (Natural) - Polish (Poland) | Yes |
| edge | pl-PL-ZofiaNeural | Female | pl-PL | Microsoft Zofia Online (Natural) - Polish (Poland) | Yes |
| edge | ps-AF-GulNawazNeural | Male | ps-AF | Microsoft GulNawaz Online (Natural) - Pashto (Afghanistan) | Yes |
| edge | ps-AF-LatifaNeural | Female | ps-AF | Microsoft Latifa Online (Natural) - Pashto (Afghanistan) | Yes |
| edge | pt-BR-AntonioNeural | Male | pt-BR | Microsoft Antonio Online (Natural) - Portuguese (Brazil) | Yes |
| edge | pt-BR-FranciscaNeural | Female | pt-BR | Microsoft Francisca Online (Natural) - Portuguese (Brazil) | Yes |
| edge | pt-BR-ThalitaMultilingualNeural | Female | pt-BR | Microsoft ThalitaMultilingual Online (Natural) - Portuguese (Brazil) | Yes |
| edge | pt-PT-DuarteNeural | Male | pt-PT | Microsoft Duarte Online (Natural) - Portuguese (Portugal) | Yes |
| edge | pt-PT-RaquelNeural | Female | pt-PT | Microsoft Raquel Online (Natural) - Portuguese (Portugal) | Yes |
| edge | ro-RO-AlinaNeural | Female | ro-RO | Microsoft Alina Online (Natural) - Romanian (Romania) | Yes |
| edge | ro-RO-EmilNeural | Male | ro-RO | Microsoft Emil Online (Natural) - Romanian (Romania) | Yes |
| edge | ru-RU-DmitryNeural | Male | ru-RU | Microsoft Dmitry Online (Natural) - Russian (Russia) | Yes |
| edge | ru-RU-SvetlanaNeural | Female | ru-RU | Microsoft Svetlana Online (Natural) - Russian (Russia) | Yes |
| edge | si-LK-SameeraNeural | Male | si-LK | Microsoft Sameera Online (Natural) - Sinhala (Sri Lanka) | Yes |
| edge | si-LK-ThiliniNeural | Female | si-LK | Microsoft Thilini Online (Natural) - Sinhala (Sri Lanka) | Yes |
| edge | sk-SK-LukasNeural | Male | sk-SK | Microsoft Lukas Online (Natural) - Slovak (Slovakia) | Yes |
| edge | sk-SK-ViktoriaNeural | Female | sk-SK | Microsoft Viktoria Online (Natural) - Slovak (Slovakia) | Yes |
| edge | sl-SI-PetraNeural | Female | sl-SI | Microsoft Petra Online (Natural) - Slovenian (Slovenia) | Yes |
| edge | sl-SI-RokNeural | Male | sl-SI | Microsoft Rok Online (Natural) - Slovenian (Slovenia) | Yes |
| edge | so-SO-MuuseNeural | Male | so-SO | Microsoft Muuse Online (Natural) - Somali (Somalia) | Yes |
| edge | so-SO-UbaxNeural | Female | so-SO | Microsoft Ubax Online (Natural) - Somali (Somalia) | Yes |
| edge | sq-AL-AnilaNeural | Female | sq-AL | Microsoft Anila Online (Natural) - Albanian (Albania) | Yes |
| edge | sq-AL-IlirNeural | Male | sq-AL | Microsoft Ilir Online (Natural) - Albanian (Albania) | Yes |
| edge | sr-RS-NicholasNeural | Male | sr-RS | Microsoft Nicholas Online (Natural) - Serbian (Serbia) | Yes |
| edge | sr-RS-SophieNeural | Female | sr-RS | Microsoft Sophie Online (Natural) - Serbian (Serbia) | Yes |
| edge | su-ID-JajangNeural | Male | su-ID | Microsoft Jajang Online (Natural) - Sundanese (Indonesia) | Yes |
| edge | su-ID-TutiNeural | Female | su-ID | Microsoft Tuti Online (Natural) - Sundanese (Indonesia) | Yes |
| edge | sv-SE-MattiasNeural | Male | sv-SE | Microsoft Mattias Online (Natural) - Swedish (Sweden) | Yes |
| edge | sv-SE-SofieNeural | Female | sv-SE | Microsoft Sofie Online (Natural) - Swedish (Sweden) | Yes |
| edge | sw-KE-RafikiNeural | Male | sw-KE | Microsoft Rafiki Online (Natural) - Swahili (Kenya) | Yes |
| edge | sw-KE-ZuriNeural | Female | sw-KE | Microsoft Zuri Online (Natural) - Swahili (Kenya) | Yes |
| edge | sw-TZ-DaudiNeural | Male | sw-TZ | Microsoft Daudi Online (Natural) - Swahili (Tanzania) | Yes |
| edge | sw-TZ-RehemaNeural | Female | sw-TZ | Microsoft Rehema Online (Natural) - Swahili (Tanzania) | Yes |
| edge | ta-IN-PallaviNeural | Female | ta-IN | Microsoft Pallavi Online (Natural) - Tamil (India) | Yes |
| edge | ta-IN-ValluvarNeural | Male | ta-IN | Microsoft Valluvar Online (Natural) - Tamil (India) | Yes |
| edge | ta-LK-KumarNeural | Male | ta-LK | Microsoft Kumar Online (Natural) - Tamil (Sri Lanka) | Yes |
| edge | ta-LK-SaranyaNeural | Female | ta-LK | Microsoft Saranya Online (Natural) - Tamil (Sri Lanka) | Yes |
| edge | ta-MY-KaniNeural | Female | ta-MY | Microsoft Kani Online (Natural) - Tamil (Malaysia) | Yes |
| edge | ta-MY-SuryaNeural | Male | ta-MY | Microsoft Surya Online (Natural) - Tamil (Malaysia) | Yes |
| edge | ta-SG-AnbuNeural | Male | ta-SG | Microsoft Anbu Online (Natural) - Tamil (Singapore) | Yes |
| edge | ta-SG-VenbaNeural | Female | ta-SG | Microsoft Venba Online (Natural) - Tamil (Singapore) | Yes |
| edge | te-IN-MohanNeural | Male | te-IN | Microsoft Mohan Online (Natural) - Telugu (India) | Yes |
| edge | te-IN-ShrutiNeural | Female | te-IN | Microsoft Shruti Online (Natural) - Telugu (India) | Yes |
| edge | th-TH-NiwatNeural | Male | th-TH | Microsoft Niwat Online (Natural) - Thai (Thailand) | Yes |
| edge | th-TH-PremwadeeNeural | Female | th-TH | Microsoft Premwadee Online (Natural) - Thai (Thailand) | Yes |
| edge | tr-TR-AhmetNeural | Male | tr-TR | Microsoft Ahmet Online (Natural) - Turkish (Türkiye) | Yes |
| edge | tr-TR-EmelNeural | Female | tr-TR | Microsoft Emel Online (Natural) - Turkish (Turkey) | Yes |
| edge | uk-UA-OstapNeural | Male | uk-UA | Microsoft Ostap Online (Natural) - Ukrainian (Ukraine) | Yes |
| edge | uk-UA-PolinaNeural | Female | uk-UA | Microsoft Polina Online (Natural) - Ukrainian (Ukraine) | Yes |
| edge | ur-IN-GulNeural | Female | ur-IN | Microsoft Gul Online (Natural) - Urdu (India) | Yes |
| edge | ur-IN-SalmanNeural | Male | ur-IN | Microsoft Salman Online (Natural) - Urdu (India) | Yes |
| edge | ur-PK-AsadNeural | Male | ur-PK | Microsoft Asad Online (Natural) - Urdu (Pakistan) | Yes |
| edge | ur-PK-UzmaNeural | Female | ur-PK | Microsoft Uzma Online (Natural) - Urdu (Pakistan) | Yes |
| edge | uz-UZ-MadinaNeural | Female | uz-UZ | Microsoft Madina Online (Natural) - Uzbek (Uzbekistan) | Yes |
| edge | uz-UZ-SardorNeural | Male | uz-UZ | Microsoft Sardor Online (Natural) - Uzbek (Uzbekistan) | Yes |
| edge | vi-VN-HoaiMyNeural | Female | vi-VN | Microsoft HoaiMy Online (Natural) - Vietnamese (Vietnam) | Yes |
| edge | vi-VN-NamMinhNeural | Male | vi-VN | Microsoft NamMinh Online (Natural) - Vietnamese (Vietnam) | Yes |
| edge | zh-CN-XiaoxiaoNeural | Female | zh-CN | Microsoft Xiaoxiao Online (Natural) - Chinese (Mainland) | Yes |
| edge | zh-CN-XiaoyiNeural | Female | zh-CN | Microsoft Xiaoyi Online (Natural) - Chinese (Mainland) | Yes |
| edge | zh-CN-YunjianNeural | Male | zh-CN | Microsoft Yunjian Online (Natural) - Chinese (Mainland) | Yes |
| edge | zh-CN-YunxiNeural | Male | zh-CN | Microsoft Yunxi Online (Natural) - Chinese (Mainland) | Yes |
| edge | zh-CN-YunxiaNeural | Male | zh-CN | Microsoft Yunxia Online (Natural) - Chinese (Mainland) | Yes |
| edge | zh-CN-YunyangNeural | Male | zh-CN | Microsoft Yunyang Online (Natural) - Chinese (Mainland) | Yes |
| edge | zh-CN-liaoning-XiaobeiNeural | Female | zh-CN-liaoning | Microsoft Xiaobei Online (Natural) - Chinese (Northeastern Mandarin) | Yes |
| edge | zh-CN-shaanxi-XiaoniNeural | Female | zh-CN-shaanxi | Microsoft Xiaoni Online (Natural) - Chinese (Zhongyuan Mandarin Shaanxi) | Yes |
| edge | zh-HK-HiuGaaiNeural | Female | zh-HK | Microsoft HiuGaai Online (Natural) - Chinese (Cantonese Traditional) | Yes |
| edge | zh-HK-HiuMaanNeural | Female | zh-HK | Microsoft HiuMaan Online (Natural) - Chinese (Hong Kong SAR) | Yes |
| edge | zh-HK-WanLungNeural | Male | zh-HK | Microsoft WanLung Online (Natural) - Chinese (Hong Kong SAR) | Yes |
| edge | zh-TW-HsiaoChenNeural | Female | zh-TW | Microsoft HsiaoChen Online (Natural) - Chinese (Taiwan) | Yes |
| edge | zh-TW-HsiaoYuNeural | Female | zh-TW | Microsoft HsiaoYu Online (Natural) - Chinese (Taiwanese Mandarin) | Yes |
| edge | zh-TW-YunJheNeural | Male | zh-TW | Microsoft YunJhe Online (Natural) - Chinese (Taiwan) | Yes |
| edge | zu-ZA-ThandoNeural | Female | zu-ZA | Microsoft Thando Online (Natural) - Zulu (South Africa) | Yes |
| edge | zu-ZA-ThembaNeural | Male | zu-ZA | Microsoft Themba Online (Natural) - Zulu (South Africa) | Yes |
| kokoro | zf_xiaobei | Female | cmn-CN | Xiaobei (Mandarin Chinese) | Catalog only |
| kokoro | zf_xiaoni | Female | cmn-CN | Xiaoni (Mandarin Chinese) | Catalog only |
| kokoro | zf_xiaoxiao | Female | cmn-CN | Xiaoxiao (Mandarin Chinese) | Catalog only |
| kokoro | zf_xiaoyi | Female | cmn-CN | Xiaoyi (Mandarin Chinese) | Catalog only |
| kokoro | zm_yunjian | Male | cmn-CN | Yunjian (Mandarin Chinese) | Catalog only |
| kokoro | zm_yunxi | Male | cmn-CN | Yunxi (Mandarin Chinese) | Catalog only |
| kokoro | zm_yunxia | Male | cmn-CN | Yunxia (Mandarin Chinese) | Catalog only |
| kokoro | zm_yunyang | Male | cmn-CN | Yunyang (Mandarin Chinese) | Catalog only |
| kokoro | bf_alice | Female | en-GB | Alice (British English) | Yes |
| kokoro | bf_emma | Female | en-GB | Emma (British English) | Yes |
| kokoro | bf_isabella | Female | en-GB | Isabella (British English) | Yes |
| kokoro | bf_lily | Female | en-GB | Lily (British English) | Yes |
| kokoro | bm_daniel | Male | en-GB | Daniel (British English) | Yes |
| kokoro | bm_fable | Male | en-GB | Fable (British English) | Yes |
| kokoro | bm_george | Male | en-GB | George (British English) | Yes |
| kokoro | bm_lewis | Male | en-GB | Lewis (British English) | Yes |
| kokoro | af_alloy | Female | en-US | Alloy (American English) | Yes |
| kokoro | af_aoede | Female | en-US | Aoede (American English) | Yes |
| kokoro | af_bella | Female | en-US | Bella (American English) | Yes |
| kokoro | af_heart | Female | en-US | Heart (American English) | Yes |
| kokoro | af_jessica | Female | en-US | Jessica (American English) | Yes |
| kokoro | af_kore | Female | en-US | Kore (American English) | Yes |
| kokoro | af_nicole | Female | en-US | Nicole (American English) | Yes |
| kokoro | af_nova | Female | en-US | Nova (American English) | Yes |
| kokoro | af_river | Female | en-US | River (American English) | Yes |
| kokoro | af_sarah | Female | en-US | Sarah (American English) | Yes |
| kokoro | af_sky | Female | en-US | Sky (American English) | Yes |
| kokoro | am_adam | Male | en-US | Adam (American English) | Yes |
| kokoro | am_echo | Male | en-US | Echo (American English) | Yes |
| kokoro | am_eric | Male | en-US | Eric (American English) | Yes |
| kokoro | am_fenrir | Male | en-US | Fenrir (American English) | Yes |
| kokoro | am_liam | Male | en-US | Liam (American English) | Yes |
| kokoro | am_michael | Male | en-US | Michael (American English) | Yes |
| kokoro | am_onyx | Male | en-US | Onyx (American English) | Yes |
| kokoro | am_puck | Male | en-US | Puck (American English) | Yes |
| kokoro | am_santa | Male | en-US | Santa (American English) | Yes |
| kokoro | ef_dora | Female | es-ES | Dora (Spanish) | Catalog only |
| kokoro | em_alex | Male | es-ES | Alex (Spanish) | Catalog only |
| kokoro | em_santa | Male | es-ES | Santa (Spanish) | Catalog only |
| kokoro | ff_siwis | Female | fr-FR | Siwis (French) | Catalog only |
| kokoro | hf_alpha | Female | hi-IN | Alpha (Hindi) | Catalog only |
| kokoro | hf_beta | Female | hi-IN | Beta (Hindi) | Catalog only |
| kokoro | hm_omega | Male | hi-IN | Omega (Hindi) | Catalog only |
| kokoro | hm_psi | Male | hi-IN | Psi (Hindi) | Catalog only |
| kokoro | if_sara | Female | it-IT | Sara (Italian) | Catalog only |
| kokoro | im_nicola | Male | it-IT | Nicola (Italian) | Catalog only |
| kokoro | jf_alpha | Female | ja-JP | Alpha (Japanese) | Catalog only |
| kokoro | jf_gongitsune | Female | ja-JP | Gongitsune (Japanese) | Catalog only |
| kokoro | jf_nezumi | Female | ja-JP | Nezumi (Japanese) | Catalog only |
| kokoro | jf_tebukuro | Female | ja-JP | Tebukuro (Japanese) | Catalog only |
| kokoro | jm_kumo | Male | ja-JP | Kumo (Japanese) | Catalog only |
| kokoro | pf_dora | Female | pt-BR | Dora (Brazilian Portuguese) | Catalog only |
| kokoro | pm_alex | Male | pt-BR | Alex (Brazilian Portuguese) | Catalog only |
| kokoro | pm_santa | Male | pt-BR | Santa (Brazilian Portuguese) | Catalog only |
