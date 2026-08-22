from __future__ import annotations

from copy import deepcopy
from typing import Any

AGENT_ORDER = ("device", "connectivity", "data", "security", "operations")


def _normalize(ctx: dict[str, Any]) -> dict[str, Any]:
    state = deepcopy(ctx)
    defaults = {
        "device_identity_verified": False,
        "secure_provisioning": False,
        "hardware_root_of_trust": False,
        "telemetry_schema_validated": False,
        "telemetry_integrity_protected": False,
        "offline_buffering_tested": False,
        "command_authentication": False,
        "command_authorization": False,
        "least_privilege_verified": False,
        "firmware_signed": False,
        "ota_update_tested": False,
        "rollback_tested": False,
        "connectivity_recovery_tested": False,
        "privacy_review_complete": False,
        "data_minimization_verified": False,
        "observability_ready": False,
        "fleet_canary_tested": False,
        "incident_recovery_tested": False,
        "unresolved_conflicts": [],
        "unresolved_questions": [],
        "open_risks": [],
        "human_approval": False,
    }
    for key, value in defaults.items():
        state.setdefault(key, value)
    return state


def _analyses(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "device": {
            "identity_ready": state["device_identity_verified"] and state["secure_provisioning"],
            "hardware_trust": state["hardware_root_of_trust"],
        },
        "connectivity": {
            "recovery_ready": state["connectivity_recovery_tested"],
            "offline_ready": state["offline_buffering_tested"],
        },
        "data": {
            "telemetry_ready": state["telemetry_schema_validated"] and state["telemetry_integrity_protected"],
            "privacy_ready": state["privacy_review_complete"] and state["data_minimization_verified"],
        },
        "security": {
            "commands_safe": state["command_authentication"] and state["command_authorization"] and state["least_privilege_verified"],
            "firmware_trusted": state["firmware_signed"],
        },
        "operations": {
            "update_ready": state["ota_update_tested"] and state["rollback_tested"],
            "fleet_ready": state["observability_ready"] and state["fleet_canary_tested"] and state["incident_recovery_tested"],
        },
    }


def _blockers(state: dict[str, Any]) -> list[str]:
    checks = {
        "device_identity_unverified": state["device_identity_verified"],
        "secure_provisioning_missing": state["secure_provisioning"],
        "hardware_trust_missing": state["hardware_root_of_trust"],
        "telemetry_schema_unvalidated": state["telemetry_schema_validated"],
        "telemetry_integrity_missing": state["telemetry_integrity_protected"],
        "offline_buffering_untested": state["offline_buffering_tested"],
        "command_authentication_missing": state["command_authentication"],
        "command_authorization_missing": state["command_authorization"],
        "least_privilege_unverified": state["least_privilege_verified"],
        "firmware_unsigned": state["firmware_signed"],
        "ota_update_untested": state["ota_update_tested"],
        "rollback_untested": state["rollback_tested"],
        "connectivity_recovery_untested": state["connectivity_recovery_tested"],
        "privacy_review_incomplete": state["privacy_review_complete"],
        "data_minimization_unverified": state["data_minimization_verified"],
        "observability_not_ready": state["observability_ready"],
        "fleet_canary_untested": state["fleet_canary_tested"],
        "incident_recovery_untested": state["incident_recovery_tested"],
    }
    blockers = [name for name, passed in checks.items() if not passed]
    if state["unresolved_conflicts"]:
        blockers.append("unresolved_conflict")
    if state["unresolved_questions"]:
        blockers.append("unresolved_question")
    if state["open_risks"]:
        blockers.append("open_risk")
    return blockers


def run(ctx: dict[str, Any]) -> dict[str, Any]:
    state = _normalize(ctx)
    analyses = _analyses(state)
    blockers = _blockers(state)
    if blockers:
        status = "review_required"
    elif not state["human_approval"]:
        status = "awaiting_human_approval"
    else:
        status = "approved_for_fleet_release"
    trace = [{"step": i + 1, "actor": name, "event": "completed"} for i, name in enumerate(AGENT_ORDER)]
    trace.append({"step": len(trace) + 1, "actor": "iot_release_gate", "event": status, "blockers": blockers})
    return {
        "system_id": "F50",
        "system_name": "IoT Engineering",
        "version": "1.0.0",
        "maturity": "L3 Gold Standard",
        "state": state,
        "analyses": analyses,
        "blockers": blockers,
        "ready_for_approval": not blockers,
        "status": status,
        "trace": trace,
        "human_authority": "Qualified humans retain fleet release authority.",
    }
