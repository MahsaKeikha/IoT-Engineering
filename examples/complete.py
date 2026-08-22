import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from orchestration.orchestrator import run  # noqa: E402

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
result = run(case)
assert result["status"] == "approved_for_fleet_release"
print(result["status"], result["analyses"].keys())
