# ModernUO Translator Service API

## Visão Geral

O **ModernUO Translator Service** é um microserviço multilíngue de tradução automática para integração com servidores de Ultima Online ou qualquer sistema de jogos/roleplay.

Com suporte a português, inglês, russo, espanhol e francês, ele permite que jogadores de diferentes nacionalidades se comuniquem perfeitamente, exibindo falas tanto no idioma original quanto traduzido.

O serviço pode ser usado junto ao sistema de NPCs inteligentes, permitindo que tanto jogadores quanto personagens IA interajam de forma natural e compreensível em vários idiomas.

---

## Como Funciona

* API REST (FastAPI) exposta no endpoint `/translate`.
* Utiliza modelos MarianMT da Helsinki-NLP (Hugging Face) para cada par de línguas.
* Cada requisição especifica o idioma de origem (`src_lang`) e destino (`tgt_lang`).
* O serviço retorna o texto traduzido, mantendo o original.

---

## Exemplo de Uso

### Payload JSON

```json
{
  "text": "Olá, tudo bem?",
  "src_lang": "pt",
  "tgt_lang": "en"
}
```

### Resposta JSON

```json
{
  "original": "Olá, tudo bem?",
  "translated": "Hello, how are you?",
  "src": "pt",
  "tgt": "en"
}
```

---

## Dinâmica Recomendada

* **Jogador russo** fala: "Привет! Как дела?"

  * API traduz para português: "Olá! Como vai?"
  * Mensagem exibida: "Привет! Как дела? (Olá! Como vai?)"
* **NPC responde em português**

  * API traduz para russo antes de exibir para o jogador russo.
* **Funciona também para inglês, espanhol, francês e outras combinações suportadas.**

---

## Integração com ModernUO ou outros sistemas

* Envie toda mensagem entre jogadores/NPCs para o `/translate` se o idioma do destinatário for diferente do remetente.
* Pode ser chamado via HTTP de qualquer linguagem (Python, C#, etc).

---

## Rodando o serviço

* Com Python e dependências instaladas:

```bash
uvicorn translator_service:app --host 0.0.0.0 --port 8100
```

* Ou via Docker/DevContainer (ver instruções do projeto).

---

## Idiomas Suportados

* **Português** (`pt`)
* **Inglês** (`en`)
* **Russo** (`ru`)
* **Espanhol** (`es`)
* **Francês** (`fr`)

## Pontos Fortes

* Tradução rápida, local e privada (não depende de nuvem externa)
* Pode ser expandido para outros idiomas ou modelos universais (NLLB)
* Integração fácil com outros microserviços de IA
* Escalável para múltiplos jogadores/conexões

---

## Extensões Possíveis

* Cache de traduções para reduzir latência
* Suporte a mais idiomas
* Detecção automática de idioma
* Logs e métricas de uso

---

**Pronto para quebrar a barreira do idioma no seu servidor Ultima Online!**
