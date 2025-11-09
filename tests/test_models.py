
from evolution_client.models import TextMessage, ButtonsMessage, ButtonItem, PollMessage

def test_models_text():
    m = TextMessage(number="324701234567", text="ok")
    assert m.type == "text"

def test_models_buttons():
    m = ButtonsMessage(
        number="324701234567",
        text="ok",
        buttons=[ButtonItem(id="a", label="A")]
    )
    assert m.type == "buttons"

def test_models_poll():
    m = PollMessage(number="324701234567", name="Q", selectableCount=1, values=["A","B"])
    assert m.type == "poll"
