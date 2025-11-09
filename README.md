
# evolution-client
# 📨 Evolution Client SDK (Python)

Typed and reusable **Python SDK for the [Evolution API](https://doc.evolution-api.com)** — a WhatsApp automation API.  
This library provides a clean client and service layer to send messages, polls, buttons, and media, and handle webhooks easily.  

Compatible with **Django**, **Flask**, **FastAPI**, or any Python app.

---

## 🚀 Features

- ✅ Typed models (Pydantic v2)
- ✅ High-level `MessagingService` abstraction
- ✅ Automatic retries and logging with Loguru
- ✅ Flat or nested message payload support
- ✅ Webhook utilities for validation & deduplication
- ✅ Ready to integrate with Celery or Django apps

---

## 🧩 Project structure

```
evolution-client-sdk/
│
├── evolution_client/
│   ├── client.py          # HTTP wrapper for Evolution API
│   ├── service.py         # MessagingService (routes typed messages)
│   ├── models/            # Message models (Text, Buttons, Poll, Media)
│   ├── webhook.py         # Webhook helpers (signature, normalization)
│   ├── exceptions.py
│   ├── utils.py
│   └── __init__.py
├── pyproject.toml
└── README.md
```

---

## ⚙️ Installation

### **1️⃣ Local (Editable Mode)**

If you are developing or testing locally:

```bash
cd ./evolution-client-sdk
pip install -e .
```

This installs the SDK in *editable mode* (any change you make to the source reflects instantly).

---

### **2️⃣ Add to another project (Poetry-managed project)**

Inside your Django or FastAPI app directory:

```bash
poetry add ../evolution-client-sdk
```

If Poetry doesn’t detect changes, edit your `pyproject.toml` manually:

```toml
[tool.poetry.dependencies]
evolution-client = { path = "../evolution-client-sdk", develop = true }
```

Then reinstall:

```bash
poetry install
```

✅ This makes your SDK available to import:

```python
from evolution_client import EvolutionApiClient, MessagingService
```

---

## 💡 Quick usage example

```python
from evolution_client import (
    EvolutionApiClient, MessagingService,
    TextMessage, ButtonsMessage, ButtonItem, PollMessage, MediaMessage
)

client = EvolutionApiClient(
    base_url="https://evo1.redemulticom.com.br",
    instance="Jonas Br",
    api_key="YOUR_API_KEY"
)
service = MessagingService(client)
number = "+32489098226"

# 🗨️ Send text
service.send(TextMessage(number=number, text="Hello from Evolution SDK!"))

# 🔘 Send buttons
service.send(ButtonsMessage(
    number=number,
    text="Aprovar proposta?",
    buttons=[
        ButtonItem(id="accept", label="✅ Aprovar"),
        ButtonItem(id="reject", label="❌ Rejeitar"),
    ]
))

# 📊 Send poll
service.send(PollMessage(
    number=number,
    name="Qual é a sua decisão?",
    selectableCount=1,
    values=["✅ Aprovar", "❌ Rejeitar"]
))

# 🖼️ Send media
service.send(MediaMessage(
    number=number,
    url="https://storage.googleapis.com/storage.phished.be/Academy/Silver_Level/TS6/illustrator/S-TS6_15_DND_PC%20paper%20bin.svg",
    caption="🖼️ Exemplo de imagem enviada via Evolution API",
    mime_type="image"
))
```

---

## 🧰 Webhook usage example

```python
from evolution_client.webhook import verify_signature, normalize_event_type, extract_from_number

def handle_webhook(request):
    raw = request.body
    signature = request.headers.get("X-Signature")
    secret = "YOUR_WEBHOOK_SECRET"

    if not verify_signature(raw, signature, secret):
        return {"status": 403, "message": "Invalid signature"}

    data = json.loads(raw)
    event = normalize_event_type(data.get("event"), data.get("data", {}))
    sender = extract_from_number(data.get("data", {}))

    print(f"Webhook received: {event} from {sender}")
```

---

## 🧪 Integration Test Example

Inside your Django project (e.g. `/django_app/sebrae/tests/test_whatsapp_integration_pkg.py`):

```python
from evolution_client import (
    EvolutionApiClient, MessagingService,
    TextMessage, ButtonsMessage, ButtonItem, PollMessage, MediaMessage
)

client = EvolutionApiClient(
    base_url='URL_OF_YOUR_EVOLUTION_API_INSTANCE',
    instance='YOUR_INSTANCE_NAME',
    api_key='YOUR_API_KEY',
)
service = MessagingService(client)
number = "PHONE_NUMBER_TO_TEST"

def test_send_all():
    service.send(TextMessage(number=number, text="Hello from SDK"))
    service.send(ButtonsMessage(
        number=number,
        text="Approve?",
        buttons=[
            ButtonItem(id="yes", label="✅ Yes"),
            ButtonItem(id="no", label="❌ No"),
        ],
    ))
    service.send(PollMessage(
        number=number,
        name="Decision?",
        selectableCount=1,
        values=["✅ Accept", "❌ Reject"],
    ))
    service.send(MediaMessage(
        number=number,
        url="https://example.com/image.png",
        caption="🖼️ Example media",
        mime_type="image"
    ))
```

Run it:

```bash
poetry run python ./django_app/sebrae/tests/test_whatsapp_integration_pkg.py
```

---

## 🧩 Troubleshooting

| Problem | Possible Cause | Solution |
|----------|----------------|-----------|
| `ImportError: cannot import name 'TextMessage'` | Wrong folder structure or missing `__init__.py` | Keep `models/messages.py` flat and ensure `__init__.py` imports it |
| `Required environment variable not set` | `.env` not loaded early | Verify `load_dotenv()` path in Django `common.py` |
| `400 instance requires property "mediatype"` | API schema change | Pass `mime_type="image"` or update client method (v1.0.1+) |

---

## 🏗️ Roadmap

- [ ] Automatic MIME type detection for media
- [ ] Async support with `httpx.AsyncClient`
- [ ] Webhook event model mapping
- [ ] Built-in Celery retry decorators

---

## 📜 License

MIT License © 2025 **Jonas Da Silva**

---

## 💬 Support

For internal questions or contributions, contact:  
**leao.jonas@gmail.com**
