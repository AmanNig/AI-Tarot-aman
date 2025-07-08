import re
from typing import Tuple, Optional
from deep_translator import GoogleTranslator
import logging
import requests
from os import getenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def groq_invoke(prompt: str, max_tokens: int = 50, temperature: float = 0) -> str:
    """
    Invoke Groq API using the same approach as intent classification and tarot reader.
    
    Args:
        prompt: The prompt to send to the model
        max_tokens: Maximum tokens for response
        temperature: Temperature for response generation
        
    Returns:
        The model's response
    """
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = getenv("GROQ_API_KEY")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return "en"  # Default fallback

def detect_language_with_groq(text: str) -> Tuple[str, float]:
    """
    Detect language using Groq model with confidence scoring.
    
    Args:
        text: Input text to detect language for
        
    Returns:
        Tuple of (language_code, confidence_score)
    """
    if not text or not text.strip():
        return 'en', 0.0
    
    text = text.strip()
    
    # For very short text, use pattern detection first
    if len(text) < 10:
        pattern_result = _detect_by_patterns(text)
        if pattern_result[1] > 0.7:
            return pattern_result
    
    # Use Groq for language detection
    prompt = f"""You are a language detection expert. Your job is to identify the language of the given text and respond with ONLY the ISO 639-1 language code.

Supported languages and their codes:
- English: en
- Hindi: hi
- Romanized Hindi (Hindi written in English letters): hi_rom
- Marathi: mr
- Romanized Marathi (Marathi written in English letters): mr_rom
- Bengali: bn
- Romanized Bengali (Bengali written in English letters): bn_rom
- Telugu: te
- Romanized Telugu (Telugu written in English letters): te_rom
- Tamil: ta
- Romanized Tamil (Tamil written in English letters): ta_rom
- Gujarati: gu
- Romanized Gujarati (Gujarati written in English letters): gu_rom
- Kannada: kn
- Romanized Kannada (Kannada written in English letters): kn_rom
- Malayalam: ml
- Romanized Malayalam (Malayalam written in English letters): ml_rom
- Punjabi: pa
- Romanized Punjabi (Punjabi written in English letters): pa_rom
- Odia: or
- Romanized Odia (Odia written in English letters): or_rom
- Assamese: as
- Romanized Assamese (Assamese written in English letters): as_rom
- Urdu: ur
- Romanized Urdu (Urdu written in English letters): ur_rom
- Nepali: ne
- Romanized Nepali (Nepali written in English letters): ne_rom
- Spanish: es
- French: fr
- German: de
- Italian: it
- Portuguese: pt
- Vietnamese: vi
- Indonesian: id
- Malay: ms
- Filipino: tl
- Thai: th
- Myanmar: my
- Khmer: km
- Lao: lo
- Sinhala: si

Examples:
Text: "Hello, how are you?"
Language: en

Text: "नमस्ते, कैसे हो आप?"
Language: hi

Text: "mai aj kya kru?"
Language: hi_rom

Text: "mi aaj kay karaycha?"
Language: mr_rom

Text: "ami aj ki korbo?"
Language: bn_rom

Text: "naanu ee em chestha?"
Language: te_rom

Text: "naan inru enna seiven?"
Language: ta_rom

Text: "hu aaj shu karish?"
Language: gu_rom

Text: "Hola, ¿cómo estás?"
Language: es

Text: "Bonjour, comment allez-vous?"
Language: fr

Text: "வணக்கம், எப்படி இருக்கிறீர்கள்?"
Language: ta

Text: "নমস্কার, কেমন আছেন?"
Language: bn

Text: "నమస్కారం, ఎలా ఉన్నారు?"
Language: te

Now detect the language of this text:
Text: "{text}"
Language:"""

    try:
        detected_lang = groq_invoke(prompt, max_tokens=10, temperature=0).strip().lower()
        
        # Validate the detected language
        valid_languages = {
            'en', 'hi', 'hi_rom', 'mr', 'mr_rom', 'bn', 'bn_rom', 'te', 'te_rom', 'ta', 'ta_rom', 
            'gu', 'gu_rom', 'kn', 'kn_rom', 'ml', 'ml_rom', 'pa', 'pa_rom', 'or', 'or_rom', 
            'as', 'as_rom', 'ur', 'ur_rom', 'ne', 'ne_rom',
            'es', 'fr', 'de', 'it', 'pt', 'vi', 'id', 'ms', 'tl', 'th', 'my', 'km', 'lo', 'si'
        }
        
        if detected_lang in valid_languages:
            confidence = _calculate_confidence(text, detected_lang)
            return detected_lang, confidence
        else:
            # Fallback to pattern detection
            return _detect_by_patterns(text)
            
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return _detect_by_patterns(text)

def _detect_by_patterns(text: str) -> Tuple[str, float]:
    """
    Fallback pattern-based detection for known languages.
    """
    # Indian Languages
    patterns = {
        'hi': (r'[\u0900-\u097F]', 0.9),  # Devanagari script
        'bn': (r'[\u0980-\u09FF]', 0.9),  # Bengali script
        'te': (r'[\u0C00-\u0C7F]', 0.9),  # Telugu script
        'ta': (r'[\u0B80-\u0BFF]', 0.9),  # Tamil script
        'gu': (r'[\u0A80-\u0AFF]', 0.9),  # Gujarati script
        'kn': (r'[\u0C80-\u0CFF]', 0.9),  # Kannada script
        'ml': (r'[\u0D00-\u0D7F]', 0.9),  # Malayalam script
        'pa': (r'[\u0A00-\u0A7F]', 0.9),  # Gurmukhi script
        'or': (r'[\u0B00-\u0B7F]', 0.9),  # Odia script
        'ur': (r'[\u0600-\u06FF]', 0.9),  # Arabic script
        'si': (r'[\u0D80-\u0DFF]', 0.9),  # Sinhala script
        'my': (r'[\u1000-\u109F]', 0.9),  # Myanmar script
        'th': (r'[\u0E00-\u0E7F]', 0.9),  # Thai script
        'km': (r'[\u1780-\u17FF]', 0.9),  # Khmer script
        'lo': (r'[\u0E80-\u0EFF]', 0.9),  # Lao script
    }
    
    for lang, (pattern, confidence) in patterns.items():
        if re.search(pattern, text):
            return lang, confidence
    
    # Romanized Hindi detection
    romanized_hindi_patterns = [
        r'\b(mai|main|mein|me)\b',  # I/me
        r'\b(aj|aaj)\b',  # today
        r'\b(kya|kyaa)\b',  # what
        r'\b(kru|karu|karun)\b',  # should I do
        r'\b(hu|hoon|hun)\b',  # am
        r'\b(tha|thi|the)\b',  # was/were
        r'\b(hoga|hogi|honge)\b',  # will be
        r'\b(kya|kyaa)\b',  # what
        r'\b(kaise|kaisa|kaisi)\b',  # how
        r'\b(kahan|kaha)\b',  # where
        r'\b(kab)\b',  # when
        r'\b(kyun|kyu)\b',  # why
        r'\b(acha|accha)\b',  # good
        r'\b(bura|buri)\b',  # bad
        r'\b(naam|name)\b',  # name
        r'\b(ghar|ghar)\b',  # home
        r'\b(kaam|kam)\b',  # work
        r'\b(dost|friend)\b',  # friend
        r'\b(pyar|prem)\b',  # love
        r'\b(shaadi|shadi)\b',  # marriage
        r'\b(naukri|job)\b',  # job
        r'\b(paise|paisa)\b',  # money
        r'\b(samay|time)\b',  # time
        r'\b(roz|daily)\b',  # daily
        r'\b(kal|tomorrow)\b',  # tomorrow
        r'\b(parso|day after)\b',  # day after tomorrow
        r'\b(kaunsa|kaunsa)\b',  # which
        r'\b(kitna|kitni|kitne)\b',  # how much/many
        r'\b(yahan|yaha)\b',  # here
        r'\b(wahan|waha)\b',  # there
        r'\b(abhi|ab)\b',  # now
        r'\b(phir|fir)\b',  # then/again
        r'\b(bhi)\b',  # also
        r'\b(par|pe)\b',  # on/at
        r'\b(se)\b',  # from/with
        r'\b(ko)\b',  # to
        r'\b(ka|ki|ke)\b',  # of
        r'\b(mein|me)\b',  # in
        r'\b(se|sai)\b',  # from
        r'\b(tak)\b',  # until
        r'\b(sirf|bas)\b',  # only
        r'\b(bahut|zyada)\b',  # very/much
        r'\b(thoda|kam)\b',  # little/less
        r'\b(sab|saare)\b',  # all
        r'\b(kuch|kuchh)\b',  # some
        r'\b(koi|koyi)\b',  # someone
        r'\b(kuch|kuchh)\b',  # something
        r'\b(kahan|kaha)\b',  # where
        r'\b(kabhi|kabhi)\b',  # sometimes
        r'\b(hamesha|hameshaa)\b',  # always
        r'\b(kabhi|kabhi)\b',  # never
        r'\b(acha|accha)\b',  # good
        r'\b(bura|buri)\b',  # bad
        r'\b(sundar|khubsurat)\b',  # beautiful
        r'\b(garam|thanda)\b',  # hot/cold
        r'\b(bada|chota)\b',  # big/small
        r'\b(naya|purana)\b',  # new/old
        r'\b(tez|dheere)\b',  # fast/slow
        r'\b(mushkil|aasan)\b',  # difficult/easy
        r'\b(sahi|galat)\b',  # correct/wrong
        r'\b(upar|neeche)\b',  # up/down
        r'\b(andar|bahar)\b',  # inside/outside
        r'\b(aage|peeche)\b',  # front/back
        r'\b(left|right|daayen|baayen)\b',  # left/right
        r'\b(paas|door)\b',  # near/far
        r'\b(paas|door)\b',  # near/far
        r'\b(andar|bahar)\b',  # inside/outside
        r'\b(aage|peeche)\b',  # front/back
        r'\b(upar|neeche)\b',  # up/down
        r'\b(tez|dheere)\b',  # fast/slow
        r'\b(garam|thanda)\b',  # hot/cold
        r'\b(bada|chota)\b',  # big/small
        r'\b(naya|purana)\b',  # new/old
        r'\b(acha|accha)\b',  # good
        r'\b(bura|buri)\b',  # bad
        r'\b(sundar|khubsurat)\b',  # beautiful
        r'\b(mushkil|aasan)\b',  # difficult/easy
        r'\b(sahi|galat)\b',  # correct/wrong
        r'\b(paas|door)\b',  # near/far
        r'\b(andar|bahar)\b',  # inside/outside
        r'\b(aage|peeche)\b',  # front/back
        r'\b(upar|neeche)\b',  # up/down
        r'\b(tez|dheere)\b',  # fast/slow
        r'\b(garam|thanda)\b',  # hot/cold
        r'\b(bada|chota)\b',  # big/small
        r'\b(naya|purana)\b',  # new/old
        r'\b(acha|accha)\b',  # good
        r'\b(bura|buri)\b',  # bad
        r'\b(sundar|khubsurat)\b',  # beautiful
        r'\b(mushkil|aasan)\b',  # difficult/easy
        r'\b(sahi|galat)\b',  # correct/wrong
    ]
    
    # Romanized Marathi detection
    romanized_marathi_patterns = [
        r'\b(mi|mala|majha)\b',  # I/me/my
        r'\b(aaj|aj)\b',  # today
        r'\b(kay|kay)\b',  # what
        r'\b(karaycha|karayla)\b',  # should do
        r'\b(aahe|ahet)\b',  # is/are
        r'\b(hota|hoti|hote)\b',  # was/were
        r'\b(hoil|hoin)\b',  # will be
        r'\b(kase|kasa|kashi)\b',  # how
        r'\b(kuthe|kuthe)\b',  # where
        r'\b(kevha|kevha)\b',  # when
        r'\b(kashala|kashala)\b',  # why
        r'\b(chan|chhan)\b',  # good
        r'\b(vaat|vaat)\b',  # bad
        r'\b(naav|naav)\b',  # name
        r'\b(ghar|ghar)\b',  # home
        r'\b(kaam|kaam)\b',  # work
        r'\b(mitra|friend)\b',  # friend
        r'\b(prem|love)\b',  # love
        r'\b(lagna|marriage)\b',  # marriage
        r'\b(naukri|job)\b',  # job
        r'\b(paise|money)\b',  # money
        r'\b(vel|time)\b',  # time
        r'\b(rozh|daily)\b',  # daily
        r'\b(udya|tomorrow)\b',  # tomorrow
        r'\b(parva|day after)\b',  # day after tomorrow
        r'\b(konta|konta)\b',  # which
        r'\b(kitka|kitki|kitke)\b',  # how much/many
        r'\b(ikde|ithe)\b',  # here
        r'\b(tikde|tithe)\b',  # there
        r'\b(aata|ata)\b',  # now
        r'\b(mag|mag)\b',  # then/again
        r'\b(pan|pan)\b',  # also
        r'\b(var|var)\b',  # on/at
        r'\b(kadun|kadun)\b',  # from/with
        r'\b(la|la)\b',  # to
        r'\b(cha|chi|che)\b',  # of
        r'\b(madhe|madhe)\b',  # in
        r'\b(kadun|kadun)\b',  # from
        r'\b(poriyant|poriyant)\b',  # until
        r'\b(fakt|bas)\b',  # only
        r'\b(khup|zyada)\b',  # very/much
        r'\b(thoda|kam)\b',  # little/less
        r'\b(sarva|saare)\b',  # all
        r'\b(kuch|kuchh)\b',  # some
        r'\b(koi|koyi)\b',  # someone
        r'\b(kuch|kuchh)\b',  # something
        r'\b(kuthe|kuthe)\b',  # where
        r'\b(kadhi|kadhi)\b',  # sometimes
        r'\b(sada|sadaa)\b',  # always
        r'\b(kadhi|kadhi)\b',  # never
        r'\b(chan|chhan)\b',  # good
        r'\b(vaat|vaat)\b',  # bad
        r'\b(sundar|khubsurat)\b',  # beautiful
        r'\b(garam|thanda)\b',  # hot/cold
        r'\b(motha|lahaan)\b',  # big/small
        r'\b(nava|juna)\b',  # new/old
        r'\b(vega|dheem)\b',  # fast/slow
        r'\b(kathin|saul)\b',  # difficult/easy
        r'\b(bara|chuka)\b',  # correct/wrong
        r'\b(var|khali)\b',  # up/down
        r'\b(aat|baher)\b',  # inside/outside
        r'\b(mage|madhye)\b',  # front/back
        r'\b(davya|uyavya)\b',  # left/right
        r'\b(laagat|door)\b',  # near/far
    ]
    
    # Romanized Bengali detection
    romanized_bengali_patterns = [
        r'\b(ami|amake|amar)\b',  # I/me/my
        r'\b(aj|aaj)\b',  # today
        r'\b(ki|kya)\b',  # what
        r'\b(korbo|korbe)\b',  # will do
        r'\b(achi|ache)\b',  # am/is
        r'\b(chilo|chila)\b',  # was
        r'\b(hobe|hobe)\b',  # will be
        r'\b(kemon|kibhabe)\b',  # how
        r'\b(kothay|kothae)\b',  # where
        r'\b(kokhon|kobe)\b',  # when
        r'\b(keno|karo)\b',  # why
        r'\b(bhalo|valo)\b',  # good
        r'\b(kharap|kharap)\b',  # bad
        r'\b(nam|name)\b',  # name
        r'\b(bari|ghor)\b',  # home
        r'\b(kaaj|kaj)\b',  # work
        r'\b(bondhu|friend)\b',  # friend
        r'\b(bhalobasha|love)\b',  # love
        r'\b(biya|marriage)\b',  # marriage
        r'\b(chakri|job)\b',  # job
        r'\b(taka|money)\b',  # money
        r'\b(somoy|time)\b',  # time
        r'\b(proti|daily)\b',  # daily
        r'\b(agami|tomorrow)\b',  # tomorrow
        r'\b(parsu|day after)\b',  # day after tomorrow
        r'\b(kon|konta)\b',  # which
        r'\b(koto|koyta)\b',  # how much/many
        r'\b(ekhane|eikhane)\b',  # here
        r'\b(okhane|oikhane)\b',  # there
        r'\b(ekhon|akhon)\b',  # now
        r'\b(tarpor|pore)\b',  # then/again
        r'\b(o|o)\b',  # also
        r'\b(upor|upore)\b',  # on/at
        r'\b(theke|theke)\b',  # from/with
        r'\b(ke|ke)\b',  # to
        r'\b(er|or)\b',  # of
        r'\b(majhe|moddhe)\b',  # in
        r'\b(theke|theke)\b',  # from
        r'\b(porjonto|porjonto)\b',  # until
        r'\b(shudhu|bas)\b',  # only
        r'\b(khuba|beshi)\b',  # very/much
        r'\b(ektu|kom)\b',  # little/less
        r'\b(shob|shokol)\b',  # all
        r'\b(kichu|kichu)\b',  # some
        r'\b(keu|karo)\b',  # someone
        r'\b(kichu|kichu)\b',  # something
        r'\b(kothay|kothae)\b',  # where
        r'\b(kokhon|kobe)\b',  # sometimes
        r'\b(shobshomoy|sada)\b',  # always
        r'\b(kokhono|karo)\b',  # never
        r'\b(bhalo|valo)\b',  # good
        r'\b(kharap|kharap)\b',  # bad
        r'\b(sundor|khubsurat)\b',  # beautiful
        r'\b(garam|thanda)\b',  # hot/cold
        r'\b(boro|choto)\b',  # big/small
        r'\b(notun|purono)\b',  # new/old
        r'\b(fast|dhire)\b',  # fast/slow
        r'\b(kothin|shohoj)\b',  # difficult/easy
        r'\b(thik|bhul)\b',  # correct/wrong
        r'\b(upor|niche)\b',  # up/down
        r'\b(bhitore|bahire)\b',  # inside/outside
        r'\b(samne|pichone)\b',  # front/back
        r'\b(bam|dan)\b',  # left/right
        r'\b(kache|dur)\b',  # near/far
    ]
    
    # Romanized Telugu detection
    romanized_telugu_patterns = [
        r'\b(naanu|naku|na)\b',  # I/me/my
        r'\b(ee|e)\b',  # today
        r'\b(em|enti)\b',  # what
        r'\b(chestha|cheyali)\b',  # will do
        r'\b(unnanu|undhi)\b',  # am/is
        r'\b(undedhi|undedi)\b',  # was
        r'\b(avuthadhi|avuthundi)\b',  # will be
        r'\b(elaa|ela)\b',  # how
        r'\b(ekkada|evaru)\b',  # where
        r'\b(eppudu|appudu)\b',  # when
        r'\b(enduku|endhuku)\b',  # why
        r'\b(manchi|baga)\b',  # good
        r'\b(chedda|tappu)\b',  # bad
        r'\b(peru|name)\b',  # name
        r'\b(illu|ghar)\b',  # home
        r'\b(pani|work)\b',  # work
        r'\b(snehitudu|friend)\b',  # friend
        r'\b(prema|love)\b',  # love
        r'\b(pelli|marriage)\b',  # marriage
        r'\b(job|pani)\b',  # job
        r'\b(dabbu|money)\b',  # money
        r'\b(samayam|time)\b',  # time
        r'\b(prati|daily)\b',  # daily
        r'\b(repu|tomorrow)\b',  # tomorrow
        r'\b(marrepu|day after)\b',  # day after tomorrow
        r'\b(edi|evaru)\b',  # which
        r'\b(entha|enni)\b',  # how much/many
        r'\b(ikkada|eekkada)\b',  # here
        r'\b(akkada|aakkada)\b',  # there
        r'\b(ipudu|appudu)\b',  # now
        r'\b(taruvatha|paina)\b',  # then/again
        r'\b(kuda|kooda)\b',  # also
        r'\b(meeda|paina)\b',  # on/at
        r'\b(nundi|nunchi)\b',  # from/with
        r'\b(ki|ku)\b',  # to
        r'\b(di|du)\b',  # of
        r'\b(lo|la)\b',  # in
        r'\b(nundi|nunchi)\b',  # from
        r'\b(varaku|daaka)\b',  # until
        r'\b(matram|okkate)\b',  # only
        r'\b(chaala|baga)\b',  # very/much
        r'\b(koncham|takkuva)\b',  # little/less
        r'\b(andaru|ella)\b',  # all
        r'\b(konni|konni)\b',  # some
        r'\b(evadu|evari)\b',  # someone
        r'\b(edi|enti)\b',  # something
        r'\b(ekkada|evaru)\b',  # where
        r'\b(konni|konni)\b',  # sometimes
        r'\b(epudu|appudu)\b',  # always
        r'\b(evadu|evari)\b',  # never
        r'\b(manchi|baga)\b',  # good
        r'\b(chedda|tappu)\b',  # bad
        r'\b(andam|sundaram)\b',  # beautiful
        r'\b(veyi|chillara)\b',  # hot/cold
        r'\b(pedda|chinna)\b',  # big/small
        r'\b(kotha|puranadi)\b',  # new/old
        r'\b(vega|melliga)\b',  # fast/slow
        r'\b(kastam|sulabham)\b',  # difficult/easy
        r'\b(nijam|tappu)\b',  # correct/wrong
        r'\b(meeda|kinda)\b',  # up/down
        r'\b(lopaliki|bayataki)\b',  # inside/outside
        r'\b(mundu|venuka)\b',  # front/back
        r'\b(edama|kudama)\b',  # left/right
        r'\b(daggara|dooram)\b',  # near/far
    ]
    
    # Romanized Tamil detection
    romanized_tamil_patterns = [
        r'\b(naan|enakku|en)\b',  # I/me/my
        r'\b(inru|indru)\b',  # today
        r'\b(enna|ethu)\b',  # what
        r'\b(seiven|seiyanum)\b',  # will do
        r'\b(irukiren|irukku)\b',  # am/is
        r'\b(irundhen|irundhu)\b',  # was
        r'\b(aagum|aagirum)\b',  # will be
        r'\b(eppadi|eppadi)\b',  # how
        r'\b(enge|engu)\b',  # where
        r'\b(eppo|appo)\b',  # when
        r'\b(enna|endha)\b',  # why
        r'\b(nalla|nalla)\b',  # good
        r'\b(ketta|tappu)\b',  # bad
        r'\b(peru|name)\b',  # name
        r'\b(veedu|illu)\b',  # home
        r'\b(velai|work)\b',  # work
        r'\b(nanban|friend)\b',  # friend
        r'\b(anbu|love)\b',  # love
        r'\b(kalyanam|marriage)\b',  # marriage
        r'\b(job|velai)\b',  # job
        r'\b(panam|money)\b',  # money
        r'\b(neram|time)\b',  # time
        r'\b(thinam|daily)\b',  # daily
        r'\b(naalai|tomorrow)\b',  # tomorrow
        r'\b(marum|day after)\b',  # day after tomorrow
        r'\b(ethu|evaru)\b',  # which
        r'\b(evlo|enna)\b',  # how much/many
        r'\b(inge|inggu)\b',  # here
        r'\b(ange|anggu)\b',  # there
        r'\b(ippo|appo)\b',  # now
        r'\b(piragu|pinnar)\b',  # then/again
        r'\b(um|kooda)\b',  # also
        r'\b(mel|mele)\b',  # on/at
        r'\b(irundhu|nindru)\b',  # from/with
        r'\b(kku|ku)\b',  # to
        r'\b(udaiya|udaiya)\b',  # of
        r'\b(ul|ulla)\b',  # in
        r'\b(irundhu|nindru)\b',  # from
        r'\b(varai|varai)\b',  # until
        r'\b(matram|okkate)\b',  # only
        r'\b(romba|mikka)\b',  # very/much
        r'\b(konjam|kuraivu)\b',  # little/less
        r'\b(ellam|ella)\b',  # all
        r'\b(konjam|konjam)\b',  # some
        r'\b(yaar|evaru)\b',  # someone
        r'\b(ethu|enti)\b',  # something
        r'\b(enge|engu)\b',  # where
        r'\b(konjam|konjam)\b',  # sometimes
        r'\b(epudu|appudu)\b',  # always
        r'\b(yaar|evaru)\b',  # never
        r'\b(nalla|nalla)\b',  # good
        r'\b(ketta|tappu)\b',  # bad
        r'\b(azhagu|sundaram)\b',  # beautiful
        r'\b(veyil|kulir)\b',  # hot/cold
        r'\b(periya|chinna)\b',  # big/small
        r'\b(pudhusu|pazhaya)\b',  # new/old
        r'\b(vega|melliga)\b',  # fast/slow
        r'\b(kastam|sulabham)\b',  # difficult/easy
        r'\b(nijam|tappu)\b',  # correct/wrong
        r'\b(mel|kizh)\b',  # up/down
        r'\b(ul|veli)\b',  # inside/outside
        r'\b(mun|pin)\b',  # front/back
        r'\b(edam|valam)\b',  # left/right
        r'\b(arai|turandu)\b',  # near/far
    ]
    
    # Romanized Gujarati detection
    romanized_gujarati_patterns = [
        r'\b(hu|mari|maru)\b',  # I/me/my
        r'\b(aaj|aj)\b',  # today
        r'\b(shu|su)\b',  # what
        r'\b(karish|karu)\b',  # will do
        r'\b(cho|che)\b',  # am/is
        r'\b(hatu|hati)\b',  # was
        r'\b(thase|thase)\b',  # will be
        r'\b(kem|kaise)\b',  # how
        r'\b(kya|kya)\b',  # where
        r'\b(kya|kya)\b',  # when
        r'\b(kyu|kyu)\b',  # why
        r'\b(saru|bhalo)\b',  # good
        r'\b(kharab|kharab)\b',  # bad
        r'\b(naam|name)\b',  # name
        r'\b(ghar|ghar)\b',  # home
        r'\b(kaam|kam)\b',  # work
        r'\b(mitra|friend)\b',  # friend
        r'\b(prem|love)\b',  # love
        r'\b(lagna|marriage)\b',  # marriage
        r'\b(naukri|job)\b',  # job
        r'\b(paise|money)\b',  # money
        r'\b(samay|time)\b',  # time
        r'\b(roz|daily)\b',  # daily
        r'\b(kal|tomorrow)\b',  # tomorrow
        r'\b(parso|day after)\b',  # day after tomorrow
        r'\b(kon|kona)\b',  # which
        r'\b(ketla|ketli)\b',  # how much/many
        r'\b(aha|eha)\b',  # here
        r'\b(teha|teha)\b',  # there
        r'\b(ha|ha)\b',  # now
        r'\b(pachi|pachi)\b',  # then/again
        r'\b(pan|pan)\b',  # also
        r'\b(par|par)\b',  # on/at
        r'\b(thi|thi)\b',  # from/with
        r'\b(ne|ne)\b',  # to
        r'\b(no|ni)\b',  # of
        r'\b(ma|ma)\b',  # in
        r'\b(thi|thi)\b',  # from
        r'\b(sudhi|sudhi)\b',  # until
        r'\b(j|j)\b',  # only
        r'\b(khuba|beshi)\b',  # very/much
        r'\b(thoda|kam)\b',  # little/less
        r'\b(badhu|badhu)\b',  # all
        r'\b(ketla|ketli)\b',  # some
        r'\b(koy|koy)\b',  # someone
        r'\b(ketla|ketli)\b',  # something
        r'\b(kya|kya)\b',  # where
        r'\b(ketla|ketli)\b',  # sometimes
        r'\b(sada|sada)\b',  # always
        r'\b(ketla|ketli)\b',  # never
        r'\b(saru|bhalo)\b',  # good
        r'\b(kharab|kharab)\b',  # bad
        r'\b(sundar|khubsurat)\b',  # beautiful
        r'\b(garam|thanda)\b',  # hot/cold
        r'\b(mota|nano)\b',  # big/small
        r'\b(nava|purana)\b',  # new/old
        r'\b(vega|dheere)\b',  # fast/slow
        r'\b(kathin|saul)\b',  # difficult/easy
        r'\b(sahi|galat)\b',  # correct/wrong
        r'\b(upar|niche)\b',  # up/down
        r'\b(andar|bahar)\b',  # inside/outside
        r'\b(aage|peeche)\b',  # front/back
        r'\b(davya|uyavya)\b',  # left/right
        r'\b(paas|door)\b',  # near/far
    ]
    
    # Check for all transliterated language patterns
    language_counts = {
        'hi_rom': 0,
        'mr_rom': 0,
        'bn_rom': 0,
        'te_rom': 0,
        'ta_rom': 0,
        'gu_rom': 0,
        'kn_rom': 0,
        'ml_rom': 0,
        'pa_rom': 0,
        'or_rom': 0,
        'as_rom': 0,
        'ur_rom': 0,
        'ne_rom': 0
    }
    
    total_words = len(text.split())
    
    # Count matches for each language
    for pattern in romanized_hindi_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            language_counts['hi_rom'] += 1
    
    for pattern in romanized_marathi_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            language_counts['mr_rom'] += 1
    
    for pattern in romanized_bengali_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            language_counts['bn_rom'] += 1
    
    for pattern in romanized_telugu_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            language_counts['te_rom'] += 1
    
    for pattern in romanized_tamil_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            language_counts['ta_rom'] += 1
    
    for pattern in romanized_gujarati_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            language_counts['gu_rom'] += 1
    
    # Determine which language has the highest ratio
    if total_words > 0:
        best_language = None
        best_ratio = 0
        
        for lang, count in language_counts.items():
            ratio = count / total_words
            if ratio > 0.25 and ratio > best_ratio:  # Minimum 25% threshold
                best_language = lang
                best_ratio = ratio
        
        if best_language:
            confidence = min(0.85, 0.5 + best_ratio * 0.35)
            return best_language, confidence
        
        # If no language meets the 25% threshold, check for mixed patterns
        mixed_languages = [(lang, count/total_words) for lang, count in language_counts.items() if count/total_words > 0.15]
        if len(mixed_languages) > 1:
            # Sort by ratio and return the highest
            mixed_languages.sort(key=lambda x: x[1], reverse=True)
            best_lang, best_ratio = mixed_languages[0]
            confidence = min(0.75, 0.4 + best_ratio * 0.25)
            return best_lang, confidence
    
    # European languages with accented characters
    if re.search(r'[áéíóúñü]', text):
        return 'es', 0.8
    elif re.search(r'[àâäéèêëïîôöùûüÿç]', text):
        return 'fr', 0.8
    elif re.search(r'[äöüß]', text):
        return 'de', 0.8
    
    # Default to English
    return 'en', 0.5

def _calculate_confidence(text: str, detected_lang: str) -> float:
    """
    Calculate confidence score for detected language.
    """
    # Base confidence
    confidence = 0.6
    
    # Adjust based on text length
    if len(text) > 50:
        confidence += 0.2
    elif len(text) > 20:
        confidence += 0.1
    
    # Adjust based on character diversity
    unique_chars = len(set(text))
    if unique_chars > 20:
        confidence += 0.1
    
    # Boost confidence for non-Latin scripts (Indian languages)
    if detected_lang in ['hi', 'bn', 'te', 'ta', 'mr', 'gu', 'kn', 'ml', 'pa', 'or', 'as', 'ur', 'ne']:
        confidence += 0.1
    
    return min(confidence, 1.0)

def detect_and_translate(input_text: str, target_language: str = 'en') -> Tuple[str, str, float]:
    """
    Detect language and translate if needed using Groq model.
    
    Args:
        input_text: Text to process
        target_language: Target language for translation
        
    Returns:
        Tuple of (translated_text, detected_language, confidence)
    """
    detected_lang, confidence = detect_language_with_groq(input_text)
    
    # Log detection results
    logger.info(f"Detected language: {detected_lang} (confidence: {confidence:.2f})")
    
    # Translate if needed and confidence is high enough
    if detected_lang != target_language and confidence > 0.3:
        try:
            # Handle transliterated languages by mapping to their native script equivalents
            source_lang = detected_lang
            transliterated_to_native = {
                'hi_rom': 'hi', 'mr_rom': 'mr', 'bn_rom': 'bn', 'te_rom': 'te', 'ta_rom': 'ta',
                'gu_rom': 'gu', 'kn_rom': 'kn', 'ml_rom': 'ml', 'pa_rom': 'pa', 'or_rom': 'or',
                'as_rom': 'as', 'ur_rom': 'ur', 'ne_rom': 'ne'
            }
            if detected_lang in transliterated_to_native:
                source_lang = transliterated_to_native[detected_lang]
            
            translator = GoogleTranslator(source=source_lang, target=target_language)
            translated_text = translator.translate(input_text)
            return translated_text, detected_lang, confidence
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return input_text, detected_lang, confidence
    
    return input_text, detected_lang, confidence

def translate_back(result_text: str, target_language: str) -> str:
    """
    Translate result back to target language.
    
    Args:
        result_text: Text to translate
        target_language: Target language
        
    Returns:
        Translated text
    """
    if target_language == 'en':
        return result_text
    
    try:
        # Handle transliterated languages - translate to native script first
        transliterated_to_native = {
            'hi_rom': 'hi', 'mr_rom': 'mr', 'bn_rom': 'bn', 'te_rom': 'te', 'ta_rom': 'ta',
            'gu_rom': 'gu', 'kn_rom': 'kn', 'ml_rom': 'ml', 'pa_rom': 'pa', 'or_rom': 'or',
            'as_rom': 'as', 'ur_rom': 'ur', 'ne_rom': 'ne'
        }
        if target_language in transliterated_to_native:
            # For transliterated languages, we need to translate to native script first
            # then convert to transliterated format
            native_lang = transliterated_to_native[target_language]
            translator = GoogleTranslator(source='en', target=native_lang)
            native_text = translator.translate(result_text)
            
            # Convert native script to transliterated format
            transliterated_text = convert_to_transliterated(native_text, target_language)
            return transliterated_text
        else:
         translator = GoogleTranslator(source='en', target=target_language)
        return translator.translate(result_text)
    except Exception as e:
        logger.error(f"Back translation failed: {e}")
        return result_text

def convert_to_transliterated(text: str, target_language: str) -> str:
    """
    Convert native script text to transliterated format.
    
    Args:
        text: Text in native script
        target_language: Target transliterated language code
        
    Returns:
        Text in transliterated format
    """
    try:
        # Use Groq to convert native script to transliterated format
        prompt = f"""Convert the following text from native script to transliterated format (Roman script).

Target language: {target_language}

Text to convert: "{text}"

Convert this to transliterated format using English letters while maintaining the same meaning and natural flow.

Transliterated text:"""
        
        transliterated = groq_invoke(prompt, max_tokens=200, temperature=0.3)
        return transliterated.strip()
        
    except Exception as e:
        logger.error(f"Transliteration failed: {e}")
        return text  # Return original text if transliteration fails

def get_supported_languages() -> list:
    """
    Get list of supported languages.
    """
    return [
        'en', 'hi', 'hi_rom', 'mr', 'mr_rom', 'bn', 'bn_rom', 'te', 'te_rom', 'ta', 'ta_rom', 
        'gu', 'gu_rom', 'kn', 'kn_rom', 'ml', 'ml_rom', 'pa', 'pa_rom', 'or', 'or_rom', 
        'as', 'as_rom', 'ur', 'ur_rom', 'ne', 'ne_rom',
        'es', 'fr', 'de', 'it', 'pt', 'vi', 'id', 'ms', 'tl', 'th', 'my', 'km', 'lo', 'si'
    ]

def get_indian_languages() -> dict:
    """
    Get dictionary of supported Indian languages.
    
    Returns:
        Dictionary mapping language codes to names
    """
    return {
        'hi': 'Hindi',
        'hi_rom': 'Romanized Hindi',
        'mr': 'Marathi',
        'mr_rom': 'Romanized Marathi',
        'bn': 'Bengali',
        'bn_rom': 'Romanized Bengali',
        'te': 'Telugu',
        'te_rom': 'Romanized Telugu',
        'ta': 'Tamil',
        'ta_rom': 'Romanized Tamil',
        'gu': 'Gujarati',
        'gu_rom': 'Romanized Gujarati',
        'kn': 'Kannada',
        'kn_rom': 'Romanized Kannada',
        'ml': 'Malayalam',
        'ml_rom': 'Romanized Malayalam',
        'pa': 'Punjabi',
        'pa_rom': 'Romanized Punjabi',
        'or': 'Odia',
        'or_rom': 'Romanized Odia',
        'as': 'Assamese',
        'as_rom': 'Romanized Assamese',
        'ur': 'Urdu',
        'ur_rom': 'Romanized Urdu',
        'ne': 'Nepali',
        'ne_rom': 'Romanized Nepali'
    }

# Global instance for backward compatibility
class LanguageDetector:
    def __init__(self):
        pass
    
    def detect_language_enhanced(self, text: str) -> Tuple[str, float]:
        return detect_language_with_groq(text)
    
    def detect_and_translate(self, input_text: str, target_language: str = 'en') -> Tuple[str, str, float]:
        return detect_and_translate(input_text, target_language)
    
    def translate_back(self, result_text: str, target_language: str) -> str:
        return translate_back(result_text, target_language)
    
    def get_supported_languages(self) -> list:
        return get_supported_languages()

# Global instance
language_detector = LanguageDetector() 