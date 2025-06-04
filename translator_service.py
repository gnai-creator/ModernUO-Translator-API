from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

port = 10100
app = FastAPI()

# Idiomas suportados (ISO 639-1)
LANGS = ["pt", "en", "ru", "es", "fr"]

# Modelos públicos e confiáveis para cada par (nem todos estão disponíveis!)
MODEL_TABLE = {
    ("pt", "en"): "unicamp-dl/translation-pt-en-t5",
    ("en", "pt"): "unicamp-dl/translation-en-pt-t5",
    ("en", "es"): "Helsinki-NLP/opus-mt-en-es",
    ("es", "en"): "Helsinki-NLP/opus-mt-es-en",
    ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
    ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
    ("en", "ru"): "Helsinki-NLP/opus-mt-en-ru",
    ("ru", "en"): "Helsinki-NLP/opus-mt-ru-en",
    # Se precisar adicionar outros pares diretos, coloque aqui
}
T5_PREFIXES = {
    "unicamp-dl/translation-en-pt-t5": "translate English to Portuguese: ",
    "unicamp-dl/translation-pt-en-t5": "translate Portuguese to English: ",
    # Adicione outros se for usar
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
        # Prefixo para modelos T5
        if model_name.startswith("unicamp-dl/translation-"):
            if src == "en" and tgt == "pt":
                text = f"translate English to Portuguese: {text}"
            elif src == "pt" and tgt == "en":
                text = f"translate Portuguese to English: {text}"
        result = translator(text, max_new_tokens=256)[0]['translation_text']
        return result

@app.post("/translate")
async def translate(req: TranslationRequest):
    src = req.src_lang.lower()
    tgt = req.tgt_lang.lower()
    print(f"Requisição recebida: {req.text} {req.src_lang}->{req.tgt_lang}")

    if src not in LANGS or tgt not in LANGS:
        return {"error": "Idioma não suportado."}
    try:
        translated = translate_chain(req.text, src, tgt)
        return {"original": req.text, "translated": translated, "src": src, "tgt": tgt}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=port)
