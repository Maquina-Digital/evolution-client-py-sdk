# 📨 Evolution Client SDK (Python)

Typed and reusable **Python SDK for the [Evolution API](https://doc.evolution-api.com)** — a WhatsApp automation API.

This package offers a clean, type-safe client for sending **messages, polls, buttons, and media**, and for handling **webhooks** easily.

✅ Compatible with **Django**, **FastAPI**, **Flask**, or any Python project.  
✅ Designed for both **local development** and **production (via GitHub Packages / private repos)**.

---

## 🚀 Features

- Typed message models (`TextMessage`, `ButtonsMessage`, `PollMessage`, `MediaMessage`)
- High-level `MessagingService` abstraction
- Automatic retries, structured logging via `Loguru`
- Easy to extend for custom message types
- Webhook helpers (signature verification, normalization)
- Fully typed using `Pydantic v2`

---

## 🧩 Project structure

```
evolution-client-sdk/
│
├── evolution_client/
│   ├── client.py          # Base HTTP client
│   ├── service.py         # MessagingService abstraction
│   ├── models/            # Typed message models
│   ├── webhook.py         # Webhook helpers
│   ├── utils.py
│   ├── exceptions.py
│   └── __init__.py
├── pyproject.toml
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Local development (editable mode)

If you’re actively developing or testing the SDK locally:

```bash
cd ./evolution-client-sdk
pip install -e .
```

Any changes you make to the SDK source code will reflect instantly.

---

### 2️⃣ Install in another project (Poetry)

If your app uses Poetry:

#### Option A — Local path (for development)
```bash
poetry add ../evolution-client-sdk
```

Or manually add to your `pyproject.toml`:

```toml
[tool.poetry.dependencies]
evolution-client = { path = "../evolution-client-sdk", develop = true }
```

#### Option B — From a private Git repository
Once you’ve pushed this SDK to your private GitHub repo:

```bash
poetry add git+ssh://git@github.com/Maquina-Digital/evolution-client-py-sdk.git@v1.0.0
```

or in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
evolution-client = { git = "ssh://git@github.com/Maquina-Digital/evolution-client-py-sdk.git", rev = "v1.0.0" }
```

Then install:

```bash
poetry install
```

---

## 💡 Usage example

```python
from evolution_client import (
    EvolutionApiClient, MessagingService,
    TextMessage, ButtonsMessage, ButtonItem,
    PollMessage, MediaMessage
)

# Initialize the client
client = EvolutionApiClient(
    base_url="https://your-evolution-api-url",
    instance="Your Instance Name",
    api_key="YOUR_API_KEY"
)
service = MessagingService(client)
number = "+32489098226"

# 🗨️ Send text
service.send(TextMessage(number=number, text="Hello from Evolution SDK!"))

# 🔘 Send buttons
service.send(ButtonsMessage(
    number=number,
    text="Do you approve?",
    buttons=[
        ButtonItem(id="accept", label="✅ Approve"),
        ButtonItem(id="reject", label="❌ Reject")
    ]
))

# 📊 Send poll
service.send(PollMessage(
    number=number,
    name="Your decision?",
    selectableCount=1,
    values=["✅ Approve", "❌ Reject"]
))

# 🖼️ Send media
service.send(MediaMessage(
    number=number,
    url="https://example.com/sample-image.png",
    caption="🖼️ Example media from Evolution API",
    mime_type="image"
))
```

---

## 🧰 Webhook Example

```python
from evolution_client.webhook import verify_signature, normalize_event_type, extract_from_number

def handle_webhook(request):
    raw_body = request.body
    signature = request.headers.get("X-Signature")
    secret = "YOUR_WEBHOOK_SECRET"

    if not verify_signature(raw_body, signature, secret):
        return {"status": 403, "message": "Invalid signature"}

    event_data = json.loads(raw_body)
    event_type = normalize_event_type(event_data.get("event"), event_data.get("data", {}))
    sender = extract_from_number(event_data.get("data", {}))

    print(f"Webhook event {event_type} received from {sender}")
```

---

## 🧪 Testing the SDK in a Django project

Example test case:

```python
from evolution_client import (
    EvolutionApiClient, MessagingService,
    TextMessage, ButtonsMessage, ButtonItem,
    PollMessage, MediaMessage
)

client = EvolutionApiClient(
    base_url="https://api.evolution.example.com",
    instance="Test Instance",
    api_key="TEST_API_KEY"
)
service = MessagingService(client)
number = "+32489098226"

def test_send_all_messages():
    service.send(TextMessage(number=number, text="Test message"))
    service.send(ButtonsMessage(
        number=number,
        text="Approve?",
        buttons=[
            ButtonItem(id="yes", label="✅ Yes"),
            ButtonItem(id="no", label="❌ No")
        ]
    ))
    service.send(PollMessage(
        number=number,
        name="Decision?",
        selectableCount=1,
        values=["✅ Accept", "❌ Reject"]
    ))
    service.send(MediaMessage(
        number=number,
        url="https://example.com/media.png",
        caption="Example media",
        mime_type="image"
    ))
```
Run:
```bash
poetry run pytest
```

---

## 🧩 Troubleshooting

| Problem | Likely cause | Solution |
|----------|---------------|-----------|
| `ImportError: cannot import name 'TextMessage'` | wrong import path | ensure your project’s dependency points to the right package |
| `Required property 'mediatype'` | missing mime type for media | use `mime_type="image"` or similar |
| `Required environment variable not set` | `.env` not loaded | check `load_dotenv()` in your settings |
| `401 Unauthorized` | invalid or expired Evolution API key | verify `api_key` in client initialization |

---

## 🏗️ Roadmap

- [ ] Async support (`httpx.AsyncClient`)
- [ ] Built-in message queue retry decorators
- [ ] Event models for webhook handling
- [ ] MIME type auto-detection for media uploads

---

## 📦 Versioning

Each release is tagged in Git (`vX.Y.Z`)  
and can be referenced in Poetry via:
```toml
rev = "v1.0.0"
```

---

## 📜 License

MIT License © 2025 Jonas Da Silva

---

## 💬 Support & Contributions

For bug reports or improvements, open an issue in the private GitHub repo:  
👉 [Maquina-Digital/evolution-client-py-sdk](https://github.com/Maquina-Digital/evolution-client-py-sdk)

For questions or collaboration, contact **leao.jonas@gmail.com**.
