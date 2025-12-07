# 📨 Evolution Client SDK (Python)

Typed and reusable **Python SDK for the [Evolution API](https://doc.evolution-api.com)** — a WhatsApp automation API.

This package offers a clean, type-safe client for sending **messages, polls, buttons, and media**, and for handling **webhooks** easily.

✅ Compatible with **Django**, **FastAPI**, **Flask**, or any Python project.  
✅ Designed for both **local development** and **production (via GitHub Packages / private repos)**.

---

## 🌟 Why use this SDK?

Here is a simple breakdown of what the **Evolution Client SDK** can do:

### 1. 📤 Send Anything on WhatsApp
Send all important message types with just one line of code:
*   **Text Messages**: Simple chat messages.
*   **Buttons**: Interactive messages with "Yes/No" or "Buy Now" buttons.
*   **Polls**: Create polls for users to vote on.
*   **Media**: Send images, videos, or documents easily.

### 2. 📥 Receive & Handle Messages (Webhooks)
It makes "listening" to WhatsApp easy. Instead of dealing with messy raw data, you get clean, organized events when:
*   A new message arrives.
*   A message is delivered or read (blue ticks).
*   The phone connection status changes.

### 3. ⚡ High Performance (Async)
It supports **Async** (asynchronous) programming. This means your app can handle thousands of messages at the same time without freezing or slowing down—perfect for high-traffic chatbots.

### 4. 🛡️ Bulletproof Reliability
*   **Auto-Retry**: If the Evolution API blips or the network fails, the SDK automatically tries sending the message again, so you don't lose data.
*   **Type Safe**: It uses strict data models. Your code editor (VS Code, PyCharm) will autocomplete fields for you and warn you if you make a mistake *before* you run the code.

### 5. 🔌 Easy Integration
It works with any Python framework:
*   **Django**, **Flask**, **FastAPI**, or simple scripts.
*   Designed to be installed and used in minutes.

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
    PollMessage, MediaMessage, AudioMessage,
    StickerMessage, LocationMessage, ListMessage,
    ListSection, ListRow, ReactionMessage
)

# Initialize the client
client = EvolutionApiClient(
    base_url="https://your-evolution-api-url",
    instance="Your Instance Name",
    api_key="YOUR_API_KEY"
)
service = MessagingService(client)
number = "+001234567890"

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

# 🎤 Send audio
service.send(AudioMessage(
    number=number,
    url="https://example.com/audio.mp3"
))

# 📍 Send location
service.send(LocationMessage(
    number=number,
    latitude=40.7128,
    longitude=-74.0060,
    name="New York City",
    address="NY, USA"
))

# 📋 Send list (Menu)
service.send(ListMessage(
    number=number,
    title="Main Menu",
    buttonText="Open Menu",
    description="Select an option",
    sections=[
        ListSection(
            title="Support",
            rows=[
                ListRow(title="Talk to Agent", rowId="agent"),
                ListRow(title="FAQ", rowId="faq")
            ]
        )
    ]
))

# ❤️ Send reaction
service.send(ReactionMessage(
    number=number,
    key={"id": "MESSAGE_ID_TO_REACT", "fromMe": True},
    reaction="🔥"
))
```

---

## ⚡ Async Support

For high-performance applications (FastAPI, Django Async), use `AsyncEvolutionClient` and `AsyncMessagingService`.

```python
import asyncio
from evolution_client import AsyncEvolutionClient, AsyncMessagingService, TextMessage

async def main():
    async with AsyncEvolutionClient(
        base_url="https://api.evolution.com",
        instance="MyInstance",
        api_key="MY_KEY"
    ) as client:
        service = AsyncMessagingService(client)
        
        # Send a message
        await service.send(TextMessage(
            number="+1234567890", 
            text="Hello from Async World! 🚀"
        ))

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🛠️ Instance Management

You can create, connect, and manage instances directly from the SDK.

```python
# Create a new instance
client.create_instance(
    instance_name="my_new_instance",
    token="optional_secret_token",
    qrcode=True
)

# Get QR Code (base64) to scan
response = client.connect_instance("my_new_instance")
print(response.json())

# List all instances
instances = client.fetch_instances()
print(instances.json())

# Logout
client.logout_instance("my_new_instance")

# Delete
client.delete_instance("my_new_instance")
```

---

## 👥 Group & Chat Management

Manage groups and chats programmatically.

```python
# Create a group
client.group_create(
    subject="My Community",
    participants=["1234567890", "0987654321"],
    description="Welcome to our group!"
)

# Update group picture
client.group_update_picture(
    group_jid="1234567890-123456@g.us",
    image_url="https://example.com/group-icon.png"
)

# Manage participants
client.group_participants_update(
    group_jid="1234567890-123456@g.us",
    action="add", # add, remove, promote, demote
    participants=["1122334455"]
)

# Archive a chat
client.chat_archive(number="1234567890", archive=True)

# Mark as read
client.chat_mark_read(number="1234567890", read=True)
```

---

## 👤 Profile Management

```python
# Update Name
client.profile_update_name("My Business Name")

# Update Status (About)
client.profile_update_status("Available for new orders! 🚀")
```

---

## 🧰 Webhook Handling

To receive messages, you must configure your Evolution API instance to send events to your application.

### 1. Configure Evolution API
You need to tell Evolution API where your Python app is running.
- Go to your Evolution API Manager (or use the API).
- Find your **Instance Settings**.
- Set **Webhook URL** to your server's endpoint (e.g., `https://your-server.com/webhook`).
- Enable the events you want to receive (e.g., `MESSAGES_UPSERT`, `MESSAGES_UPDATE`).

### 2. Handle Events in Python
The SDK provides a `WebhookHandler` to process these incoming requests easily.

```python
from evolution_client import WebhookHandler, MessageUpsertEvent, MessageUpdateEvent

# Initialize handler (optional: pass secret for signature verification)
handler = WebhookHandler(secret="YOUR_WEBHOOK_SECRET")

@handler.on("messages.upsert")
def on_new_message(event: MessageUpsertEvent):
    print(f"📩 New message from {event.data.pushName}: {event.data.message}")

@handler.on("messages.update")
def on_message_update(event: MessageUpdateEvent):
    print(f"🔄 Message status updated: {event.data}")

# Example integration with Flask/FastAPI
# payload = request.json()
# handler.handle(payload)
```

---

## 🧪 Testing the SDK in a Django project

Example test case:

```python
from evolution_client import (
    EvolutionApiClient, MessagingService,
    TextMessage, ButtonsMessage, ButtonItem,
    PollMessage, MediaMessage, AudioMessage,
    StickerMessage, LocationMessage, ListMessage,
    ListSection, ListRow, ReactionMessage
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

- [x] Async support (`httpx.AsyncClient`)
- [x] Event models for webhook handling
- [x] Typed API responses
- [ ] Built-in message queue retry decorators
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
