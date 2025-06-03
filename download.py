# download_translators.py

from transformers import pipeline

# Pares de tradução e modelos públicos
PAIRS = {
    ("en", "pt"): "unicamp-dl/translation-en-pt-t5",
    ("pt", "en"): "unicamp-dl/translation-pt-en-t5",
    ("en", "es"): "Helsinki-NLP/opus-mt-en-es",
    ("es", "en"): "Helsinki-NLP/opus-mt-es-en",
    ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
    ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
    ("en", "ru"): "Helsinki-NLP/opus-mt-en-ru",
    ("ru", "en"): "Helsinki-NLP/opus-mt-ru-en",
    # outros pares direto, se quiser adicionar...
}

if __name__ == "__main__":
    for pair, model in PAIRS.items():
        print(f"Baixando modelo {pair}: {model}")
        try:
            pipe = pipeline("translation", model=model)
            print(f"OK: {model}")
        except Exception as e:
            print(f"ERRO ({model}): {e}")
