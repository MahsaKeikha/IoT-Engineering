import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from orchestration.orchestrator import run

result = run({})
assert result["status"] == "review_required"
print(result["status"], result["blockers"][:3])
