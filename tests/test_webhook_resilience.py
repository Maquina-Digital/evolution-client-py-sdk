"""
Comprehensive tests for webhook parsing resilience.

These tests verify the SDK's core guarantee:
- SDK NEVER raises ValidationError to consumers
- SDK NEVER returns None from handle()
- On parse failure, SDK returns RawWebhookPayload with preserved data

Test categories:
1. Regression tests - valid payloads still parse correctly
2. Missing field tests - no crashes on incomplete data
3. Malformed payload tests - graceful degradation
4. Contract tests - handler guarantees never violated
"""
import json
import pytest
from pathlib import Path
from pydantic import ValidationError
from evolution_client import (
    WebhookHandler,
    MessageUpsertEvent,
    MessageUpdateEvent,
    ConnectionUpdateEvent,
    QrCodeEvent,
    RawWebhookPayload,
    WebhookBase,
)


# =============================================================================
# FIXTURES LOADING
# =============================================================================

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    """Load a JSON fixture by name."""
    with open(FIXTURES_DIR / name, "r") as f:
        return json.load(f)


@pytest.fixture
def valid_message_upsert():
    return load_fixture("valid_message_upsert.json")


@pytest.fixture
def missing_from_field():
    return load_fixture("missing_from_field.json")


@pytest.fixture
def incomplete_message_data():
    return load_fixture("incomplete_message_data.json")


@pytest.fixture
def unknown_event():
    return load_fixture("unknown_event.json")


@pytest.fixture
def malformed_random():
    return load_fixture("malformed_random.json")


@pytest.fixture
def empty_payload():
    return load_fixture("empty_payload.json")


@pytest.fixture
def null_required_fields():
    return load_fixture("null_required_fields.json")


@pytest.fixture
def handler():
    return WebhookHandler()


# =============================================================================
# 1. REGRESSION TESTS - Valid payloads still parse correctly
# =============================================================================

class TestValidPayloadParsing:
    """Regression tests ensuring backward compatibility with valid payloads."""

    def test_valid_payload_still_parses(self, handler, valid_message_upsert):
        """
        Test: Valid messages.upsert payload parses into MessageUpsertEvent.
        Verifies backward compatibility for existing valid payloads.
        """
        result = handler.handle(valid_message_upsert)
        
        # Must return the strict MessageUpsertEvent type
        assert isinstance(result, MessageUpsertEvent), \
            f"Expected MessageUpsertEvent, got {type(result).__name__}"
        
        # Verify important fields match expected values
        assert result.event == "messages.upsert"
        assert result.instance == "production-instance"
        assert result.data.pushName == "João Silva"
        assert result.data.messageType == "conversation"
        assert result.data.key["remoteJid"] == "5531999887766@s.whatsapp.net"

    def test_message_upsert_with_minimal_valid_data(self, handler, missing_from_field):
        """
        Test: Payload without 'from' field but with all required model fields.
        The 'from' field isn't part of the Pydantic model, so this should parse.
        """
        result = handler.handle(missing_from_field)
        
        # This payload has all required MessageData fields, just missing 'from'
        assert isinstance(result, MessageUpsertEvent), \
            f"Expected MessageUpsertEvent for valid structure, got {type(result).__name__}"

    def test_unknown_event_returns_base(self, handler, unknown_event):
        """
        Test: Unknown event types fall back to WebhookBase.
        """
        result = handler.handle(unknown_event)
        
        # Unknown but valid structure → WebhookBase
        assert isinstance(result, WebhookBase), \
            f"Expected WebhookBase for unknown event, got {type(result).__name__}"
        assert result.event == "some.future.event"
        assert result.instance == "test-instance"
        assert result.data["custom"] == "data"


# =============================================================================
# 2. MISSING REQUIRED FIELD TESTS - Returns RawWebhookPayload
# =============================================================================

class TestMissingRequiredFields:
    """Tests for payloads missing required fields in strict models."""

    def test_missing_required_field_returns_fallback(self, handler, incomplete_message_data):
        """
        Test: Payload missing required MessageData fields returns RawWebhookPayload.
        This is the "from" field crash case scenario.
        """
        result = handler.handle(incomplete_message_data)
        
        # Must NOT raise exception
        # Must return RawWebhookPayload since MessageData validation fails
        assert isinstance(result, RawWebhookPayload), \
            f"Expected RawWebhookPayload for incomplete data, got {type(result).__name__}"
        
        # Verify raw_payload is preserved
        assert result.raw_payload == incomplete_message_data
        
        # Verify event_type is preserved
        assert result.event_type == "messages.upsert"
        
        # Verify parse_error is populated
        assert result.parse_error is not None
        assert len(result.parse_error) > 0

    def test_null_required_fields_returns_fallback(self, handler, null_required_fields):
        """
        Test: Payload with null values for required fields returns RawWebhookPayload.
        """
        result = handler.handle(null_required_fields)
        
        assert isinstance(result, RawWebhookPayload), \
            f"Expected RawWebhookPayload for null fields, got {type(result).__name__}"
        assert result.raw_payload == null_required_fields
        assert result.event_type == "messages.upsert"


# =============================================================================
# 3. MALFORMED PAYLOAD TESTS - Graceful degradation
# =============================================================================

class TestMalformedPayloads:
    """Tests for completely malformed or unexpected payloads."""

    def test_empty_payload_returns_fallback(self, handler, empty_payload):
        """
        Test: Empty payload returns RawWebhookPayload.
        """
        result = handler.handle(empty_payload)
        
        # Empty payload has no 'event' field, should fall back
        assert isinstance(result, RawWebhookPayload), \
            f"Expected RawWebhookPayload for empty payload, got {type(result).__name__}"
        assert result.raw_payload == {}
        assert result.event_type is None

    def test_malformed_random_returns_fallback(self, handler, malformed_random):
        """
        Test: Random garbage payload returns RawWebhookPayload.
        """
        result = handler.handle(malformed_random)
        
        assert isinstance(result, RawWebhookPayload), \
            f"Expected RawWebhookPayload for garbage payload, got {type(result).__name__}"
        assert result.raw_payload == malformed_random
        assert result.event_type is None  # No 'event' field in fixture

    def test_wrong_types_returns_fallback(self, handler):
        """
        Test: Payload with wrong types for fields returns RawWebhookPayload.
        """
        payload = {
            "event": "messages.upsert",
            "instance": 12345,  # Should be string
            "data": "not a dict"  # Should be dict
        }
        
        result = handler.handle(payload)
        
        assert isinstance(result, RawWebhookPayload)
        assert result.raw_payload == payload
        assert result.event_type == "messages.upsert"


# =============================================================================
# 4. HANDLER CONTRACT TESTS - Never raises, never returns None
# =============================================================================

class TestHandlerContract:
    """Tests proving the handler guarantees are never violated."""

    @pytest.mark.parametrize("fixture_name", [
        "valid_message_upsert.json",
        "missing_from_field.json",
        "incomplete_message_data.json",
        "unknown_event.json",
        "malformed_random.json",
        "empty_payload.json",
        "null_required_fields.json",
    ])
    def test_handler_never_raises(self, handler, fixture_name):
        """
        Test: handle() NEVER raises for any fixture.
        Parametrized across all fixtures.
        """
        payload = load_fixture(fixture_name)
        
        # Must NOT raise any exception
        try:
            result = handler.handle(payload)
        except Exception as e:
            pytest.fail(f"handle() raised {type(e).__name__}: {e}")

    @pytest.mark.parametrize("fixture_name", [
        "valid_message_upsert.json",
        "missing_from_field.json",
        "incomplete_message_data.json",
        "unknown_event.json",
        "malformed_random.json",
        "empty_payload.json",
        "null_required_fields.json",
    ])
    def test_handler_never_returns_none(self, handler, fixture_name):
        """
        Test: handle() NEVER returns None for any fixture.
        Parametrized across all fixtures.
        """
        payload = load_fixture(fixture_name)
        
        result = handler.handle(payload)
        
        assert result is not None, \
            f"handle() returned None for {fixture_name}"

    def test_handler_with_completely_random_dict(self, handler):
        """
        Test: Even completely random dict doesn't break the handler.
        """
        random_payloads = [
            {},
            {"x": None},
            {"a": {"b": {"c": [1, 2, 3]}}},
            {"event": None, "data": []},
            {"event": 123, "instance": [], "data": "string"},
        ]
        
        for payload in random_payloads:
            result = handler.handle(payload)
            assert result is not None, f"Returned None for {payload}"


# =============================================================================
# 5. NO VALIDATIONERROR LEAKS TESTS
# =============================================================================

class TestNoValidationErrorLeaks:
    """Explicit tests that ValidationError never escapes SDK."""

    def test_no_validationerror_from_handle(self, handler):
        """
        Test: ValidationError is NEVER raised by handle(), even with invalid data.
        """
        invalid_payloads = [
            {"event": "messages.upsert", "instance": None, "data": None},
            {"event": "messages.upsert"},
            {"event": "connection.update"},
            {"event": "qrcode.updated", "invalid": True},
        ]
        
        for payload in invalid_payloads:
            try:
                handler.handle(payload)
            except ValidationError as e:
                pytest.fail(
                    f"ValidationError leaked from SDK!\n"
                    f"Payload: {payload}\n"
                    f"Error: {e}"
                )

    def test_validationerror_caught_internally(self, handler):
        """
        Test: Confirm that invalid MessageData triggers RawWebhookPayload,
        not ValidationError.
        """
        # This will fail MessageData validation
        payload = {
            "event": "messages.upsert",
            "instance": "test",
            "data": {
                "key": {"id": "123"}
                # Missing: message, messageType, messageTimestamp
            }
        }
        
        # Direct model instantiation WOULD raise
        with pytest.raises(ValidationError):
            MessageUpsertEvent(**payload)
        
        # But handler.handle() MUST NOT raise
        result = handler.handle(payload)
        assert isinstance(result, RawWebhookPayload)


# =============================================================================
# 6. RAW WEBHOOK PAYLOAD STRUCTURE TESTS
# =============================================================================

class TestRawWebhookPayloadStructure:
    """Tests for RawWebhookPayload model correctness."""

    def test_raw_payload_preserves_all_data(self, handler, incomplete_message_data):
        """
        Test: RawWebhookPayload.raw_payload contains exact original data.
        """
        result = handler.handle(incomplete_message_data)
        
        assert isinstance(result, RawWebhookPayload)
        assert result.raw_payload == incomplete_message_data

    def test_raw_payload_has_event_type(self, handler, incomplete_message_data):
        """
        Test: RawWebhookPayload.event_type is extracted if present.
        """
        result = handler.handle(incomplete_message_data)
        
        assert result.event_type == "messages.upsert"

    def test_raw_payload_has_parse_error(self, handler, incomplete_message_data):
        """
        Test: RawWebhookPayload.parse_error describes the validation failure.
        """
        result = handler.handle(incomplete_message_data)
        
        assert result.parse_error is not None
        # Error should mention the missing fields
        assert "message" in result.parse_error.lower() or "field" in result.parse_error.lower()


# =============================================================================
# 7. HANDLER CALLBACK BEHAVIOR TESTS
# =============================================================================

class TestHandlerCallbacks:
    """Tests for handler callback behavior with fallback payloads."""

    def test_callback_receives_parsed_event(self, handler, valid_message_upsert):
        """
        Test: Registered callbacks receive parsed event for valid payloads.
        """
        received = []
        
        @handler.on("messages.upsert")
        def on_message(event):
            received.append(event)
        
        handler.handle(valid_message_upsert)
        
        assert len(received) == 1
        assert isinstance(received[0], MessageUpsertEvent)

    def test_callback_not_called_for_raw_fallback(self, handler, incomplete_message_data):
        """
        Test: Callbacks for specific event types are still called even with fallback.
        (The handler dispatches based on event type in payload, not parsed type)
        """
        received = []
        
        @handler.on("messages.upsert")
        def on_message(event):
            received.append(event)
        
        result = handler.handle(incomplete_message_data)
        
        # Handler still dispatches based on 'event' field
        assert len(received) == 1
        assert isinstance(received[0], RawWebhookPayload)

    def test_callback_error_does_not_propagate(self, handler, valid_message_upsert):
        """
        Test: Errors in user callbacks are caught and logged, not propagated.
        """
        @handler.on("messages.upsert")
        def bad_handler(event):
            raise RuntimeError("User callback exploded!")
        
        # Should NOT raise
        result = handler.handle(valid_message_upsert)
        assert result is not None
