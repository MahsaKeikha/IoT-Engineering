from orchestration.orchestrator import run


def healthy(**updates):
    case = {
        "device_identity_verified": True,
        "secure_provisioning": True,
        "hardware_root_of_trust": True,
        "telemetry_schema_validated": True,
        "telemetry_integrity_protected": True,
        "offline_buffering_tested": True,
        "command_authentication": True,
        "command_authorization": True,
        "least_privilege_verified": True,
        "firmware_signed": True,
        "ota_update_tested": True,
        "rollback_tested": True,
        "connectivity_recovery_tested": True,
        "privacy_review_complete": True,
        "data_minimization_verified": True,
        "observability_ready": True,
        "fleet_canary_tested": True,
        "incident_recovery_tested": True,
        "unresolved_conflicts": [],
        "unresolved_questions": [],
        "open_risks": [],
        "human_approval": True,
    }
    case.update(updates)
    return case


def test_healthy_fleet_release():
    result = run(healthy())
    assert result["status"] == "approved_for_fleet_release"
    assert result["blockers"] == []


def test_human_approval_required():
    assert run(healthy(human_approval=False))["status"] == "awaiting_human_approval"


def test_security_gap_blocks_release():
    result = run(healthy(command_authorization=False))
    assert "command_authorization_missing" in result["blockers"]
    assert result["status"] == "review_required"


def test_operational_gap_blocks_release():
    result = run(healthy(rollback_tested=False, fleet_canary_tested=False))
    assert "rollback_untested" in result["blockers"]
    assert "fleet_canary_untested" in result["blockers"]


def test_unresolved_governance_fails_closed():
    result = run(healthy(unresolved_questions=["Who owns recovery?"], open_risks=["battery drain"]))
    assert "unresolved_question" in result["blockers"]
    assert "open_risk" in result["blockers"]
