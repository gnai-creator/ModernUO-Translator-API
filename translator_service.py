from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

port = 10100
app = FastAPI()

# Idiomas suportados (ISO 639-1)
LANGS = ["PTB", "ENU", "RUS", "ESN", "FRA"]

# Modelos p/ cada par de tradução (direta)
MODEL_TABLE = {
    ("PTB", "ENU"): "unicamp-dl/translation-pt-en-t5",
    ("ENU", "PTB"): "unicamp-dl/translation-en-pt-t5",
    ("ENU", "ESN"): "Helsinki-NLP/opus-mt-en-es",
    ("ESN", "ENU"): "Helsinki-NLP/opus-mt-es-en",
    ("ENU", "FRA"): "Helsinki-NLP/opus-mt-en-fr",
    ("FRA", "ENU"): "Helsinki-NLP/opus-mt-fr-en",
    ("ENU", "RUS"): "Helsinki-NLP/opus-mt-en-ru",
    ("RUS", "ENU"): "Helsinki-NLP/opus-mt-ru-en",
}

# Prefixos obrigatórios para modelos T5
T5_PREFIXES = {
    "unicamp-dl/translation-en-pt-t5": "translate English to Portuguese: ",
    "unicamp-dl/translation-pt-en-t5": "translate Portuguese to English: ",
}

TRANSLATORS = {}

def get_translator(src, tgt):
    key = (src, tgt)
    if key not in TRANSLATORS:
        model_name = MODEL_TABLE.get(key)
        if not model_name:
            raise ValueError(f"Par de idiomas não suportado: {src}->{tgt}")
        TRANSLATORS[key] = pipeline("translation", model=model_name)
    return TRANSLATORS[key]

class TranslationRequest(BaseModel):
    text: str
    src_lang: str
    tgt_lang: str

def translate_chain(text, src, tgt):
    if src == tgt:
        return text

    key = (src, tgt)
    if key in MODEL_TABLE:
        model_name = MODEL_TABLE[key]
        translator = get_translator(src, tgt)

        # Adiciona prefixo se necessário
        if model_name in T5_PREFIXES:
            text = T5_PREFIXES[model_name] + text

        result = translator(text, max_length=512, max_new_tokens=256)[0]['translation_text']
        return result

    # Tradução indireta via inglês
    if (src, "ENU") in MODEL_TABLE and ("ENU", tgt) in MODEL_TABLE:
        intermediate = translate_chain(text, src, "ENU")
        return translate_chain(intermediate, "ENU", tgt)

    raise ValueError(f"Par de idiomas não suportado: {src}->{tgt}")

@app.post("/translate")
async def translate(req: TranslationRequest):
    src = req.src_lang.lower()
    tgt = req.tgt_lang.lower()
    print(f"Requisição recebida: {req.text} {src}->{tgt}")

    if src not in LANGS or tgt not in LANGS:
        return {"error": "Idioma não suportado."}

    if src == tgt:
        return {
            "original": req.text,
            "translated": req.text,
            "src": src,
            "tgt": tgt,
            "note": "Nenhuma tradução necessária (idiomas iguais)."
        }

    try:
        translated = translate_chain(req.text, src, tgt)
        return {
            "original": req.text,
            "translated": translated,
            "src": src,
            "tgt": tgt
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=port)
