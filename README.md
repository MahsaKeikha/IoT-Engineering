# F50 IoT Engineering

**Maturity:** L3 Gold Standard candidate  
**Version:** 1.0.0

A reproducible multi-agent reference system for IoT engineering and fleet-release governance. Five specialist domains cover device trust, connectivity resilience, telemetry/data handling, security controls, and fleet operations.

## Release model

The system fails closed when device identity or secure provisioning is missing, hardware trust is absent, telemetry integrity or schema validation is incomplete, offline buffering or connectivity recovery is untested, command authentication/authorization is incomplete, least privilege is unverified, firmware is unsigned, OTA or rollback testing is incomplete, privacy/data-minimization review is missing, observability is not ready, fleet canary testing is absent, incident recovery is untested, or unresolved conflicts/questions/risks remain.

Human approval is required after all automated gates pass and cannot override an active blocker.

## Reproduce

```bash
python -m pip install -e '.[dev]'
ruff check .
pytest -q
python benchmarks/heldout_suite.py
python examples/minimal.py
python examples/complete.py
python run.py
```

CI validates Python 3.10, 3.11, and 3.12 and publishes held-out results from Python 3.12.

## Scope

This repository is an engineering reference and decision-support system. It does not autonomously authorize real fleet releases, credential provisioning, firmware deployment, or safety-critical actions. Those remain under qualified human and organizational authority.
