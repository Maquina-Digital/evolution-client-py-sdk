# Evolution API Python SDK — Usage Guide

Complete reference for the `evolution-client-sdk` Python package.

---

## ⚙️ Baileys vs Cloud API Compatibility

Evolution API supports two connection engines. **Most SDK methods work with both**, but a few are **engine-specific**:

| Feature | Baileys (Unofficial) | Cloud API (Meta Official) |
|---------|:-------------------:|:------------------------:|
| Send Text, Media, Audio, Sticker, Location | ✅ | ✅ |
| Send Contact, List, Buttons, Poll | ✅ | ✅ |
| Send Reaction | ✅ | ✅ |
| Send Status / Story | ✅ | ✅ |
| Send PTV (push-to-video) | ✅ | ❌ |
| Reply to Message | ✅ | ✅ |
| Instance Create / Connect / Restart / Delete | ✅ | ✅ |
| Set / Get Settings, Proxy | ✅ | ✅ |
| Check WhatsApp Number | ✅ | ✅ |
| Mark Read / Unread, Archive | ✅ | ✅ |
| Block / Unblock Contact | ✅ | ✅ |
| Update / Edit Message | ✅ | ✅ |
| Fetch Profile Picture URL | ✅ | ✅ |
| Get Media as Base64 | ✅ | ❌ |
| **Delete Message for Everyone** | ✅ | ❌ |
| **Find Status Messages** | ✅ | ❌ |
| Find Contacts / Messages / Chats | ✅ | ✅ |
| Fake Call | ✅ | ❌ |
| Group Create / Update / Leave | ✅ | ✅ |
| **Find Group by Invite Code** | ✅ | ❌ |
| Group Ephemeral Toggle | ✅ | ❌ |
| Profile Update (Name, Status, Picture) | ✅ | ✅ |
| Privacy Settings (Fetch / Update) | ✅ | ✅ |
| **Remove Profile Picture** | ✅ | ✅ |
| Labels | ✅ | ✅ |
| Webhooks, WebSocket, RabbitMQ, SQS, NATS, Pusher | ✅ | ✅ |
| Chatwoot, Typebot, OpenAI, Dify, Flowise, N8N | ✅ | ✅ |
| S3 Storage | ✅ | ✅ |

> **Key takeaway:** Cloud API cannot do `send_ptv`, `send_fake_call`, `delete_message_for_everyone`, `find_status_message`, `get_base64_media`, `group_find_by_invite_code`, or `group_toggle_ephemeral`. These are Baileys-only because they rely on the WhatsApp Web protocol.

---

## Installation

```bash
pip install evolution-client
```

## Initialization

### Sync Client

```python
from evolution_client import EvolutionApiClient

client = EvolutionApiClient(
    base_url="https://your-evolution-api.com",
    instance="my-instance",
    api_key="YOUR_API_KEY",
    timeout=15,
    verify_ssl=True,
)
```

### Async Client

```python
from evolution_client import AsyncEvolutionClient

async with AsyncEvolutionClient(
    base_url="https://your-evolution-api.com",
    instance="my-instance",
    api_key="YOUR_API_KEY",
) as client:
    resp = await client.send_text(number="5511999999999", text="Hello!")
```

### Accessing Properties

All constructor params are exposed as instance attributes for downstream use:

```python
print(client.base_url)    # "https://your-evolution-api.com"
print(client.api_key)     # "YOUR_API_KEY"
print(client.instance)    # "my-instance"
print(client.timeout)     # 15
print(client.verify_ssl)  # True
```

---

## Sending Messages

### Text

```python
client.send_text(number="5511999999999", text="Hello!", delay=0)
```

### Media (Image / Video / Document)

```python
client.send_media(
    number="5511999999999",
    url_media="https://example.com/photo.jpg",
    caption="Check this out!",
)
```

### Audio

```python
client.send_audio(number="5511999999999", audio="https://example.com/voice.ogg")
```

### Sticker

```python
client.send_sticker(number="5511999999999", sticker="https://example.com/sticker.webp")
```

### Location

```python
client.send_location(
    number="5511999999999",
    latitude=-23.55,
    longitude=-46.63,
    name="São Paulo",
    address="SP, Brazil",
)
```

### Contact Card

```python
client.send_contact(
    number="5511999999999",
    contact_name="Alice",
    contact_number="5511888888888",
    organization="Acme Corp",
)
```

### Reaction

```python
client.send_reaction(key={"remoteJid": "5511@s.whatsapp.net", "id": "MSG_ID"}, reaction="👍")
```

### Poll

```python
client.send_poll(
    number="5511999999999",
    name="Favorite color?",
    selectableCount=1,
    values=["Red", "Blue", "Green"],
)
```

### List

```python
client.send_list(
    number="5511999999999",
    title="Menu",
    button_text="Open Menu",
    sections=[{
        "title": "Main",
        "rows": [
            {"title": "Option A", "description": "Desc A", "rowId": "a"},
            {"title": "Option B", "description": "Desc B", "rowId": "b"},
        ]
    }],
)
```

### Buttons

```python
client.send_buttons(
    number="5511999999999",
    text="Choose one:",
    buttons=[{"id": "1", "label": "Yes"}, {"id": "2", "label": "No"}],
)
```

### PTV (Push-to-Video) — *Baileys only*

```python
client.send_ptv(number="5511999999999", ptv="https://example.com/video.mp4")
```

### Status / Story

```python
client.send_status(type="text", content="Hello world!", all_contacts=True)
```

### Reply to Message

```python
client.reply_message(number="5511999999999", message_id="MSG_ID", text="Replying!")
```

### Fake Call — *Baileys only*

```python
client.send_fake_call(number="5511999999999", is_video=False, call_duration=5)
```

---

## Instance Management

```python
# Create
client.create_instance(instance_name="new-inst", qrcode=True)

# Connect (QR code)
client.connect_instance(instance_name="new-inst")

# Status
client.get_instance_status()

# Set presence
client.set_presence(presence="available")

# Restart (uses PUT)
client.restart_instance()

# List all
client.fetch_instances()

# Logout
client.logout_instance()

# Delete
client.delete_instance()
```

---

## Chat Management

```python
# Check WhatsApp numbers
client.check_wa_number(numbers=["5511999999999", "5511888888888"])

# Read / Unread
client.chat_mark_read(number="5511999999999", read=True)

# Archive
client.chat_archive(number="5511999999999", archive=True)

# Delete chat
client.delete_chat(number="5511999999999")

# Delete message for everyone — Baileys only
client.delete_message_for_everyone(message_id="MSG_ID", remote_jid="5511@s.whatsapp.net")

# Fetch profile picture URL
client.fetch_profile_picture_url(number="5511999999999")

# Get media as base64 — Baileys only
client.get_base64_media(message_id="MSG_ID")

# Edit a sent message
client.update_message(number="5511999999999", message_id="MSG_ID", text="Edited!")

# Show typing / recording indicator
client.set_chat_presence(number="5511999999999", presence="composing")

# Block / Unblock
client.block_contact(number="5511999999999", status="block")

# Find contacts
client.find_contacts(where={"id": "5511@s.whatsapp.net"})

# Find messages
client.find_messages(where={"key": {"remoteJid": "5511@s.whatsapp.net"}}, limit=50)

# Find status/story messages — Baileys only
client.find_status_message()

# Find all chats
client.find_chats()
```

---

## Group Management

```python
# Create group
client.group_create(subject="My Group", participants=["5511999999999"])

# Get group info by JID
client.group_find_infos(group_jid="123456789@g.us")

# Find group by invite code — Baileys only
client.group_find_by_invite_code(invite_code="ABCDEF")

# List all groups
client.group_fetch_all()

# Get participants
client.group_get_participants(group_jid="123456789@g.us")

# Update subject / description / picture
client.group_update_subject(group_jid="123456789@g.us", subject="New Name")
client.group_update_description(group_jid="123456789@g.us", description="New Desc")
client.group_update_picture(group_jid="123456789@g.us", image_url="https://img.jpg")

# Manage participants (add, remove, promote, demote)
client.group_participants_update(group_jid="123456789@g.us", action="add", participants=["5511888888888"])

# Invite link
client.group_get_invite_code(group_jid="123456789@g.us")
client.group_revoke_invite(group_jid="123456789@g.us")
client.group_send_invite(group_jid="123456789@g.us", numbers=["5511888888888"])

# Settings (announcement, locked, etc.)
client.group_update_settings(group_jid="123456789@g.us", action="announcement")

# Ephemeral messages — Baileys only
client.group_toggle_ephemeral(group_jid="123456789@g.us", expiration=86400)

# Leave group
client.group_leave(group_jid="123456789@g.us")
```

---

## Labels

```python
client.label_find()
client.label_handle(number="5511999999999", label_id="1", action="add")
```

---

## Profile

```python
client.profile_fetch(number="5511999999999")
client.profile_fetch_business(number="5511999999999")
client.profile_update_name("My Name")
client.profile_update_status("Available")
client.profile_update_picture(picture="https://img.jpg")
client.profile_remove_picture()
client.profile_fetch_privacy()
client.profile_update_privacy(settings={"readreceipts": "all", "profile": "contacts"})
```

---

## Proxy & Settings

```python
# Proxy
client.set_proxy(proxy_url="http://proxy:8080", enabled=True)
client.find_proxy()

# Settings
client.set_settings(settings={"rejectCall": True, "msgCall": "Can't talk now"})
client.find_settings()
```

---

## Integrations

### Webhooks & Event Transports

```python
# Webhook
client.set_webhook(url="https://your-app.com/webhook", events=["messages.upsert"])
client.find_webhook()

# WebSocket
client.set_websocket(enabled=True, events=["messages.upsert"])
client.find_websocket()

# RabbitMQ
client.set_rabbitmq(enabled=True, events=["messages.upsert"])
client.find_rabbitmq()

# SQS, NATS, Pusher — same pattern
client.set_sqs(enabled=True)
client.set_nats(enabled=True)
client.set_pusher(enabled=True)
```

### Chatbot Integrations

All chatbot integrations follow the same `set/find` pattern, accepting a `settings` dict:

```python
client.set_chatwoot(settings={"enabled": True, "accountId": "123", "token": "..."})
client.find_chatwoot()

# Same pattern for: typebot, openai, dify, flowise, n8n
client.set_typebot(settings={...})
client.set_openai(settings={...})
client.set_dify(settings={...})
client.set_flowise(settings={...})
client.set_n8n(settings={...})
```

### Channels

```python
client.set_evolution_channel(settings={"enabled": True})
client.find_evolution_channel()

client.set_cloud_api(settings={"token": "..."})
client.find_cloud_api()
```

---

## Storage (S3)

Credentials are passed through from your application — the SDK never stores them.

```python
client.set_s3(settings={
    "bucket": "my-bucket",
    "accessKey": "AK...",
    "secretKey": "SK...",
    "endpoint": "https://s3.amazonaws.com",
    "region": "us-east-1",
})
client.find_s3()
```

---

## High-Level MessagingService

For typed message routing using Pydantic models:

```python
from evolution_client import MessagingService, TextMessage, ContactMessage

service = MessagingService(client)
status, body = service.send(TextMessage(number="5511999999999", text="Hi!"))
status, body = service.send(ContactMessage(
    number="5511999999999",
    contact_name="Alice",
    contact_number="5511888888888",
))
```

---

## Webhook Handler

```python
from evolution_client import WebhookHandler

handler = WebhookHandler()

@handler.on("messages.upsert")
def on_message(event):
    print(f"Message from {event.data}")

# In your web framework, forward the webhook body:
handler.handle(request_body)
```
