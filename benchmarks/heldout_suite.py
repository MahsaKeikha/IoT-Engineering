import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from orchestration.orchestrator import run


def healthy(**updates):
    case = {
        "device_identity_verified": True, "secure_provisioning": True,
        "hardware_root_of_trust": True, "telemetry_schema_validated": True,
        "telemetry_integrity_protected": True, "offline_buffering_tested": True,
        "command_authentication": True, "command_authorization": True,
        "least_privilege_verified": True, "firmware_signed": True,
        "ota_update_tested": True, "rollback_tested": True,
        "connectivity_recovery_tested": True, "privacy_review_complete": True,
        "data_minimization_verified": True, "observability_ready": True,
        "fleet_canary_tested": True, "incident_recovery_tested": True,
        "unresolved_conflicts": [], "unresolved_questions": [], "open_risks": [],
        "human_approval": True,
    }
    case.update(updates)
    return case


SCENARIOS = [
    ("healthy_fleet", healthy(), "approved_for_fleet_release"),
    ("awaiting_approval", healthy(human_approval=False), "awaiting_human_approval"),
    ("identity_gap", healthy(device_identity_verified=False), "review_required"),
    ("telemetry_gap", healthy(telemetry_integrity_protected=False), "review_required"),
    ("command_authz_gap", healthy(command_authorization=False), "review_required"),
    ("ota_rollback_gap", healthy(ota_update_tested=False, rollback_tested=False), "review_required"),
    ("privacy_gap", healthy(privacy_review_complete=False), "review_required"),
    ("fleet_recovery_gap", healthy(fleet_canary_tested=False, incident_recovery_tested=False), "review_required"),
]


def main():
    rows = []
    for name, payload, expected in SCENARIOS:
        actual = run(payload)["status"]
        rows.append({"scenario": name, "expected": expected, "actual": actual, "passed": actual == expected})
    passed = sum(row["passed"] for row in rows)
    result = {"system_id": "F50", "version": "1.0.0", "scenario_count": len(rows), "passed": passed, "pass_rate": passed / len(rows), "scenarios": rows}
    Path("benchmarks/heldout_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["pass_rate"] != 1.0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
