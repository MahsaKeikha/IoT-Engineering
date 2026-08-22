# F50 Held-Out Reproducibility Results

Gold Standard validation was executed from a clean GitHub Actions checkout on the `l3-gold-standard` branch.

- Evidence source run: `32548147168`
- Head: `df5e8ca83586a99939b0860ce47532c76f157236`
- Python 3.10: PASS
- Python 3.11: PASS
- Python 3.12: PASS
- Held-out IoT scenarios: 8/8 expected behaviors passed
- Pass rate: 1.0
- Artifact: `f50-heldout-results`
- Artifact digest: `sha256:264bd82181b20abd5f6fb6b0ee2de347526d1ad243c083325f8674ad69b061b9`

The suite validates healthy fleet release, withheld human approval, device-identity failure, telemetry-integrity failure, command-authorization failure, OTA/rollback failure, privacy-review failure, and fleet/recovery readiness failure.

The benchmark validates deterministic reference behavior and does not authorize autonomous real-world fleet changes.
