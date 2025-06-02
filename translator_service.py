from fastapi import FastAPI
from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer, pipeline

app = FastAPI()

# Idiomas suportados (ISO 639-1)
LANGS = ["pt", "en", "ru", "es", "fr"]

# Tabela de modelo MarianMT para cada par de idiomas (apenas direcional)
MODEL_TABLE = {
    ("pt", "en"): "Helsinki-NLP/opus-mt-pt-en",
    ("en", "pt"): "Helsinki-NLP/opus-mt-en-pt",
    ("pt", "es"): "Helsinki-NLP/opus-mt-pt-es",
    ("es", "pt"): "Helsinki-NLP/opus-mt-es-pt",
    ("pt", "ru"): "Helsinki-NLP/opus-mt-pt-ru",
    ("ru", "pt"): "Helsinki-NLP/opus-mt-ru-pt",
    ("pt", "fr"): "Helsinki-NLP/opus-mt-pt-fr",
    ("fr", "pt"): "Helsinki-NLP/opus-mt-fr-pt",
    ("en", "es"): "Helsinki-NLP/opus-mt-en-es",
    ("es", "en"): "Helsinki-NLP/opus-mt-es-en",
    ("en", "ru"): "Helsinki-NLP/opus-mt-en-ru",
    ("ru", "en"): "Helsinki-NLP/opus-mt-ru-en",
    ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
    ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
    ("es", "ru"): "Helsinki-NLP/opus-mt-es-ru",
    ("ru", "es"): "Helsinki-NLP/opus-mt-ru-es",
    ("es", "fr"): "Helsinki-NLP/opus-mt-es-fr",
    ("fr", "es"): "Helsinki-NLP/opus-mt-fr-es",
    ("ru", "fr"): "Helsinki-NLP/opus-mt-ru-fr",
    ("fr", "ru"): "Helsinki-NLP/opus-mt-fr-ru",
}

# Carregue todos os pipelines necessários na inicialização (pode demorar alguns segundos)
TRANSLATORS = {}

def get_translator(src, tgt):
    key = (src, tgt)
    if key not in TRANSLATORS:
        model_name = MODEL_TABLE.get(key)
        if not model_name:
            raise ValueError(f"Par de idiomas não suportado: {src}->{tgt}")
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        TRANSLATORS[key] = pipeline("translation", model=model, tokenizer=tokenizer)
    return TRANSLATORS[key]

class TranslationRequest(BaseModel):
    text: str
    src_lang: str
    tgt_lang: str

@app.post("/translate")
async def translate(req: TranslationRequest):
    src = req.src_lang.lower()
    tgt = req.tgt_lang.lower()
    if src == tgt:
        return {"original": req.text, "translated": req.text}
    if src not in LANGS or tgt not in LANGS:
        return {"error": "Idioma não suportado."}
    try:
        translator = get_translator(src, tgt)
        result = translator(req.text, max_length=512)
        translated = result[0]['translation_text']
    except Exception as e:
        return {"error": str(e)}
    return {"original": req.text, "translated": translated, "src": src, "tgt": tgt}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
