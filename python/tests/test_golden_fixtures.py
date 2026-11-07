import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from mt5_assistant.protocol import validate_envelope

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "protocol" / "fixtures"
SCHEMAS = ROOT / "protocol" / "schema"


@pytest.mark.parametrize(
    ("fixture_name", "schema_name"),
    [
        ("request-account-snapshot.json", "request.schema.json"),
        ("ready.json", "ready.schema.json"),
        ("response-success.json", "response.schema.json"),
        ("response-error.json", "response.schema.json"),
        ("event-sync-progress.json", "event.schema.json"),
    ],
)
def test_shared_golden_protocol_fixtures_validate_in_python(fixture_name, schema_name):
    instance = json.loads((FIXTURES / fixture_name).read_text(encoding="utf-8"))
    schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator(
        schema, format_checker=FormatChecker()
    ).validate(instance)
    assert validate_envelope(instance) == instance


def test_mt5_fixture_covers_required_account_and_history_edge_cases():
    dataset = json.loads(
        (FIXTURES / "mt5" / "account-history-cases.json").read_text(encoding="utf-8")
    )
    assert dataset["synthetic"] is True
    assert {account["mode"] for account in dataset["accounts"]} == {"NETTING", "HEDGING"}
    assert len({p["positionId"] for account in dataset["accounts"] for p in account["positions"]}) == 3
    assert {deal["case"] for deal in dataset["deals"]} >= {
        "partial-close-open", "partial-close", "final-close",
        "cash-flow-deposit", "cash-flow-withdrawal"
    }
    assert set(dataset["expectedCoverageCases"]) >= {
        "netting", "hedging", "partial-close", "commission", "swap",
        "deposit", "withdrawal", "broker-symbol-suffix",
        "separate-position-identifiers"
    }
    for account in dataset["accounts"]:
        assert isinstance(account["balance"], str)
        assert isinstance(account["equity"], str)
        for position in account["positions"]:
            assert isinstance(position["volume"], str)
            assert isinstance(position["floatingProfit"], str)


def test_operation_registry_is_allow_listed_and_has_no_trade_entry_operation():
    registry = json.loads((ROOT / "protocol" / "operations.json").read_text(encoding="utf-8"))
    operation_ids = {operation["id"] for operation in registry["operations"]}
    assert len(operation_ids) == len(registry["operations"])
    assert registry["managementActions"] == [
        "MODIFY_POSITION",
        "PARTIAL_CLOSE_POSITION",
        "CLOSE_POSITION",
        "CLOSE_ALL_POSITIONS",
        "MODIFY_PENDING_ORDER",
        "CANCEL_PENDING_ORDER",
    ]
    assert not any("open" in operation_id.lower() or "placeorder" in operation_id.lower()
                   for operation_id in operation_ids)
    assert registry["prohibitedOperations"] == [
        "trade.openPosition", "trade.openPendingOrder", "trade.placeOrder"
    ]
    capability_ids = {
        capability["id"] for capability in
        json.loads((ROOT / "protocol" / "capabilities.json").read_text(encoding="utf-8"))["capabilities"]
    }
    assert all(operation["capability"] in capability_ids for operation in registry["operations"])


def test_error_catalogue_has_stable_codes_and_safe_recovery_metadata():
    catalogue = json.loads((ROOT / "protocol" / "error-codes.json").read_text(encoding="utf-8"))
    required_codes = {
        "TERMINAL_NOT_FOUND", "TERMINAL_INITIALIZATION_FAILED", "TERMINAL_DISCONNECTED",
        "ACCOUNT_UNAUTHORISED", "ACCOUNT_MISMATCH", "HISTORY_UNAVAILABLE",
        "SYMBOL_UNAVAILABLE", "MARKET_CLOSED", "BROKER_CONSTRAINT_VIOLATION",
        "UNSUPPORTED_OPERATION", "REQUEST_REJECTED", "REQUEST_TIMEOUT_UNKNOWN",
        "PROTOCOL_VERSION_UNSUPPORTED", "PROTOCOL_INVALID_MESSAGE", "SERVICE_START_FAILED",
        "SERVICE_CRASHED", "DATA_STALE", "DATA_INCOMPLETE", "RISK_LIMIT_REACHED",
        "APP_LOCKED", "EXPORT_FAILED", "OPERATION_RECONCILIATION_REQUIRED"
    }
    assert required_codes <= set(catalogue["errors"])
    for definition in catalogue["errors"].values():
        assert isinstance(definition["retryable"], bool)
        assert definition["message"].strip()
        assert definition["recovery"].strip()
