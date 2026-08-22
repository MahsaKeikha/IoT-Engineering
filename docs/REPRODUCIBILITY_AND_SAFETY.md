# Reproducibility and Safety

Use Python 3.10, 3.11, or 3.12. From a clean checkout run `python -m pip install -e '.[dev]'`, `ruff check .`, `pytest -q`, `python benchmarks/heldout_suite.py`, `python examples/minimal.py`, `python examples/complete.py`, and `python run.py`.

The held-out suite writes deterministic JSON results to `benchmarks/heldout_results.json`. CI repeats the process on all supported Python versions and uploads the Python 3.12 result as `f50-heldout-results`.

F50 is advisory and fail-closed. Real device enrollment, credential issuance, remote commands, firmware deployment, production fleet changes, and safety-critical actions remain human-controlled and must follow organizational security, privacy, and change-management procedures.
