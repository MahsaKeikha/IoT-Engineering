# F50 IoT Engineering

**Maturity:** L3 Gold Standard candidate  
**Version:** 1.0.0

A reproducible multi-agent reference architecture for designing, reviewing, and governing connected-device systems across device trust, connectivity, telemetry, security, fleet operations, OTA updates, observability, recovery, and release readiness.

F50 is intended as a practical engineering reference for teams building IoT products in which physical devices, embedded software, networks, cloud services, data pipelines, security controls, and fleet operations must work as one system. The architecture separates specialist responsibilities while preserving shared evidence and a fail-closed release model.

This repository is decision-support and engineering-reference software. It does not autonomously provision production credentials, control physical equipment, deploy firmware to real fleets, authorize safety-critical commands, or approve production releases. Those actions remain under qualified human and organizational authority.

## Why IoT requires a multi-agent engineering model

An IoT product is not only a device and not only a cloud application. A production system can span:

```text
physical environment
       |
       v
 sensors / actuators
       |
       v
 embedded device
       |
       v
 local connectivity
       |
       v
 network / gateway
       |
       v
 ingestion / messaging
       |
       v
 telemetry and command services
       |
       v
 storage / analytics / applications
       |
       v
 fleet operations
```

A weakness at any layer can compromise the whole product. A device may have correct firmware but weak identity. Connectivity may work under ideal conditions but lose telemetry during outages. Cloud services may receive data but lack schema governance. OTA updates may work in a lab but fail at fleet scale. Commands may be authenticated but insufficiently authorized.

F50 therefore divides the engineering problem into five specialist domains.

## Five-agent architecture

```text
IoT product / fleet case
          |
          v
     Device Agent
          |
          v
  Connectivity Agent
          |
          v
      Data Agent
          |
          v
    Security Agent
          |
          v
  Operations Agent
          |
          v
 cross-domain release gates
          |
          v
 explicit human approval
          |
          v
 reviewed fleet release
```

| Agent | Responsibility | Core engineering question |
|---|---|---|
| Device Agent | Device identity, provisioning, hardware trust, firmware and local behavior | Can this device be uniquely trusted and operated within its resource and hardware constraints? |
| Connectivity Agent | Network behavior, reconnect logic, offline operation and transport resilience | Does the product continue to behave predictably when connectivity is intermittent or unavailable? |
| Data Agent | Telemetry schemas, integrity, buffering, data handling and minimization | Is device data well-defined, trustworthy, necessary, and recoverable across the pipeline? |
| Security Agent | Authentication, authorization, least privilege, firmware trust and security controls | Can devices, users, services and commands be trusted without granting unnecessary authority? |
| Operations Agent | Fleet rollout, OTA, observability, rollback, incident recovery and operational readiness | Can the fleet be updated, monitored, recovered and supported safely at scale? |

The agents contribute different evidence to one release decision. A successful network test does not cancel an unsigned firmware blocker, and a successful OTA test does not compensate for missing device identity or command authorization.

## Repository structure

```text
AGENTS/
├── device_agent.py
├── connectivity_agent.py
├── data_agent.py
├── security_agent.py
└── operations_agent.py

SKILLS/
├── device_reasoning.py
├── connectivity_design.py
├── telemetry_design.py
├── security_review.py
└── fleet_operations.py

TOOLS/
├── device_registry.py
├── telemetry_registry.py
├── risk_register.py
├── rollout_plan.py
└── release_gate.py

benchmarks/
├── cases.json
├── heldout_suite.py
└── RESULTS.md

config/
docs/
evals/
examples/
memory/
observability/
schemas/
tests/
.github/workflows/ci.yml
run.py
pyproject.toml
CITATION.cff
LICENSE
README.md
```

The architecture deliberately separates agents, reusable engineering skills, deterministic tools, memory, observability, evaluation, and release governance.

## Device engineering

The Device Agent focuses on the physical endpoint and its trust boundary.

A production device review should consider:

- unique device identity
- manufacturing identity and serial-number strategy
- secure provisioning
- hardware root of trust where required
- secure boot
- firmware authenticity
- key and certificate storage
- key rotation and revocation
- MCU/SoC capabilities
- flash and RAM limits
- power and battery constraints
- sensor and actuator interfaces
- watchdog behavior
- safe local state
- local storage
- diagnostic interfaces
- physical access assumptions
- manufacturing and RMA flows

### Device identity

A fleet should be able to distinguish one legitimate device from another. Shared credentials across an entire fleet create a large blast radius and make revocation difficult.

A production identity record can include:

```text
device_id
hardware_revision
manufacturing_batch
firmware_version
credential_id
provisioning_state
trust_state
last_seen
fleet_group
lifecycle_state
```

`TOOLS/device_registry.py` provides the reference abstraction for maintaining device-level state.

## Secure provisioning

Provisioning is part of product security, not merely manufacturing logistics.

The system should explicitly reason about:

- where device credentials originate
- when they are injected
- whether credentials are unique
- whether private material can be extracted
- how devices prove identity to services
- how credentials are rotated
- how compromised devices are revoked
- what happens during factory reset
- what happens during ownership transfer
- how returned devices are handled

A device with unknown or unverifiable identity should not be treated as release-ready.

## Connectivity engineering

IoT connectivity is inherently imperfect. Networks disappear, gateways restart, mobile devices move, Wi-Fi credentials change, cellular coverage varies, brokers become unavailable, and packets arrive late or out of order.

The Connectivity Agent evaluates resilience rather than assuming continuous connectivity.

Relevant technologies can include:

- Wi-Fi
- Ethernet
- BLE
- cellular
- LTE-M
- NB-IoT
- Thread
- Zigbee
- LoRaWAN
- satellite connectivity
- local gateways
- MQTT
- HTTP
- WebSockets
- CoAP

The repository remains transport-neutral so the control model can be adapted to different IoT stacks.

## Offline-first behavior

A connected device should have an explicit policy for network loss.

Questions include:

- What functions must continue locally?
- What data must be buffered?
- How much local storage is available?
- What happens when the buffer is full?
- Are events timestamped correctly while offline?
- How is ordering reconstructed after reconnection?
- Are duplicate events possible?
- How are retries bounded?
- What backoff strategy is used?
- Can commands expire while the device is disconnected?
- How does the device recover after a gateway or broker outage?

Offline behavior should be tested rather than inferred from the happy path.

## Telemetry architecture

The Data Agent treats telemetry as a versioned interface between devices and downstream systems.

A telemetry event can include:

```text
event_id
device_id
event_type
schema_version
device_timestamp
ingestion_timestamp
sequence_number
payload
firmware_version
quality_flags
```

Depending on the application, the schema may also require units, sensor metadata, calibration state, uncertainty, location context, or provenance.

`TOOLS/telemetry_registry.py` provides the reference layer for telemetry definitions and evidence.

## Schema governance

Telemetry schemas should evolve deliberately.

Production systems should define:

- schema ownership
- schema versioning
- backward and forward compatibility expectations
- required and optional fields
- type validation
- unit conventions
- enum evolution
- timestamp semantics
- deprecation policy
- consumer migration expectations

A device fleet may contain several firmware versions simultaneously, so cloud systems should not assume every endpoint changes at once.

## Telemetry integrity

Data integrity involves more than transport encryption.

The engineering review should consider:

- duplicate messages
- missing sequence numbers
- corrupted payloads
- clock drift
- stale telemetry
- replayed events
- impossible sensor values
- inconsistent units
- firmware-specific schema changes
- buffering and replay after outages

The system must not claim telemetry integrity when no validation evidence exists.

## Data minimization and privacy

Connected products can collect continuous information about people, homes, workplaces, vehicles, health, location, behavior, or the physical environment.

F50 therefore treats data minimization as a release concern.

A review should ask:

- Is every collected field necessary?
- Can processing occur locally instead?
- Is precise location required?
- How long must raw telemetry be retained?
- Can identifiers be pseudonymized?
- Who can access the data?
- Are sensitive fields separated from general telemetry?
- Is consent or notice required?
- What deletion obligations exist?

Privacy requirements vary by product, jurisdiction and data category and require appropriate professional review.

## IoT security model

The Security Agent reviews trust relationships across the device-to-cloud path.

```text
Device
  |
  | authenticated channel
  v
Gateway / broker / API
  |
  | authorized service identity
  v
Cloud services
  |
  | scoped application access
  v
Operators / applications
```

Important controls include:

- device authentication
- user authentication
- service authentication
- authorization
- least privilege
- certificate validation
- encryption in transit
- encryption at rest where required
- secure boot
- signed firmware
- anti-rollback policy where appropriate
- credential rotation
- secrets management
- audit logging
- vulnerability response
- dependency and supply-chain review

## Authentication versus authorization

Authentication answers who or what is making a request. Authorization answers whether that identity is allowed to perform the requested action.

This distinction is especially important for IoT commands.

A valid device, user or service identity should not automatically receive permission to:

- unlock equipment
- change safety limits
- alter device configuration
- disable monitoring
- rotate fleet credentials
- trigger firmware installation
- issue commands to unrelated devices

Command authorization should be explicit and scoped.

## Command safety

Remote commands can affect the physical world. Production designs should define:

- command identity
- target device or group
- requesting principal
- authorization decision
- issuance timestamp
- expiration
- replay protection
- acknowledgement
- execution result
- audit record

Safety-critical commands may require additional local interlocks, physical confirmation, multi-party authorization, or complete exclusion from autonomous remote control.

## Firmware trust

Firmware is part of the device trust chain.

A release review should verify, as applicable:

- build provenance
- firmware version
- signing
- signature verification on-device
- secure boot compatibility
- dependency review
- hardware compatibility
- configuration compatibility
- downgrade policy
- recovery image availability

Unsigned or unverifiable firmware should fail closed where firmware authenticity is a release requirement.

## OTA update lifecycle

OTA is one of the most consequential IoT operational workflows.

A robust lifecycle is:

```text
build firmware
      |
      v
sign artifact
      |
      v
validate hardware compatibility
      |
      v
lab testing
      |
      v
pilot devices
      |
      v
fleet canary
      |
      v
observe health
      |
      +--> rollback / stop
      |
      v
staged expansion
      |
      v
full approved rollout
```

`TOOLS/rollout_plan.py` provides the reference rollout-planning layer.

Production rollout plans should define fleet cohorts, rollout percentages, observation windows, stop thresholds, health signals, rollback criteria and accountable owners.

## Rollback and recovery

Rollback must be designed before deployment.

Questions include:

- Can the bootloader recover from an interrupted update?
- Is an A/B image strategy available?
- Can the device revert automatically?
- Can an operator stop the rollout?
- Are incompatible data migrations reversible?
- Can a device become permanently unreachable after a bad update?
- How is recovery handled when connectivity is also degraded?

A release should not depend on an untested recovery assumption.

## Fleet operations

The Operations Agent focuses on operating thousands or millions of heterogeneous endpoints over time.

Fleet state can include:

- hardware revision
- firmware version
- connectivity type
- geography
- tenant or customer
- health state
- credential state
- last communication
- rollout cohort
- update status
- incident state

Fleet segmentation makes targeted rollout, diagnosis and recovery possible.

## Observability

IoT observability must connect device behavior to network, cloud and fleet behavior.

Useful signals include:

### Device

- boot count
- reset reason
- watchdog resets
- battery state
- memory pressure
- storage pressure
- sensor health
- firmware version

### Connectivity

- connection success rate
- reconnect count
- signal quality
- broker failures
- latency
- packet or message loss

### Telemetry

- ingestion rate
- schema failures
- duplicates
- stale events
- buffer depth
- replay volume

### Fleet operations

- OTA success rate
- rollback rate
- unhealthy device percentage
- version distribution
- offline device percentage
- incident count

Metrics should be generated by deterministic telemetry systems, not inferred from narrative agent output.

## Risk register

`TOOLS/risk_register.py` provides a structured place for cross-domain IoT risks.

Useful fields include:

```text
risk_id
domain
description
likelihood
impact
severity
owner
mitigation
verification
status
```

Examples include compromised device credentials, firmware rollback failure, telemetry loss during outages, insecure debug interfaces, privacy overcollection, cloud dependency failure, and unsupported hardware revisions.

## Shared memory and evidence

The `memory/` layer preserves engineering evidence across specialist reviews.

Useful evidence includes:

- device trust state
- provisioning evidence
- hardware revision
- firmware identity
- connectivity test results
- offline-buffer test results
- telemetry schema results
- security findings
- privacy findings
- rollout results
- rollback tests
- operational incidents
- unresolved questions

Evidence should be scoped by product, hardware revision, firmware version, environment, fleet cohort and release candidate.

## Fail-closed release governance

`TOOLS/release_gate.py` represents the release-control layer.

F50 is designed to block release when material evidence is missing or failed, including conditions such as:

- device identity missing
- secure provisioning incomplete
- hardware trust requirement unmet
- telemetry integrity unverified
- schema validation incomplete
- offline buffering untested
- connectivity recovery untested
- command authentication incomplete
- command authorization incomplete
- least privilege unverified
- firmware unsigned when signing is required
- OTA testing incomplete
- rollback testing incomplete
- privacy or data-minimization review missing
- observability not ready
- fleet canary testing absent
- incident recovery untested
- unresolved conflicts
- unresolved questions
- unresolved critical risks

Human approval is required after automated gates pass. Human approval does not convert an active blocker into a passing condition.

## Human authority boundaries

F50 must not autonomously:

- provision real production credentials
- rotate production fleet keys
- send commands to physical devices
- change safety limits
- deploy firmware to production fleets
- disable security controls
- bypass device authorization
- approve privacy compliance
- approve safety-critical operation
- suppress critical incidents
- authorize full-fleet rollout

Those actions should remain behind authenticated operational systems, least-privilege permissions, change management, and accountable human approval.

## End-to-end reference workflow

A typical F50 review follows this sequence:

1. Define the IoT product, device classes and intended operating environment.
2. Identify hardware revisions, firmware versions and device trust requirements.
3. Review identity and secure provisioning.
4. Review connectivity architecture and failure behavior.
5. Test offline buffering, reconnection and recovery.
6. Define and validate telemetry schemas.
7. Review data integrity, retention and minimization.
8. Review authentication, authorization, firmware trust and least privilege.
9. Review OTA, staged rollout and rollback behavior.
10. Confirm device, connectivity, telemetry and fleet observability.
11. Review incident and recovery readiness.
12. Consolidate open risks and cross-agent conflicts.
13. Apply the fail-closed release gate.
14. Require explicit human approval for a real fleet release.

## Reproduce the reference implementation

Install development dependencies:

```bash
python -m pip install -e '.[dev]'
```

Run static checks and tests:

```bash
ruff check .
pytest -q
```

Run the held-out benchmark suite:

```bash
python benchmarks/heldout_suite.py
```

Run the examples:

```bash
python examples/minimal.py
python examples/complete.py
```

Run the main entry point:

```bash
python run.py
```

CI validates Python 3.10, 3.11, and 3.12 and publishes held-out results from Python 3.12.

## Benchmarks and evaluation

The repository includes:

```text
benchmarks/cases.json
benchmarks/heldout_suite.py
benchmarks/RESULTS.md
evals/evaluate.py
```

Evaluation should test engineering behavior rather than only the quality of generated prose.

Useful dimensions include:

- missing-identity detection
- provisioning-gap detection
- connectivity-recovery analysis
- offline-buffering detection
- telemetry-schema validation
- command-authentication detection
- authorization-gap detection
- least-privilege review
- unsigned-firmware detection
- OTA-readiness analysis
- rollback-readiness analysis
- privacy-gap detection
- observability-gap detection
- fleet-canary enforcement
- incident-recovery detection
- unresolved-risk propagation
- human-gate enforcement

Strong benchmark cases should contain deliberately incomplete or contradictory IoT release evidence.

## Failure states

Useful explicit states include:

```text
DEVICE IDENTITY MISSING
PROVISIONING INCOMPLETE
DEVICE TRUST UNVERIFIED
CONNECTIVITY RECOVERY UNTESTED
OFFLINE BUFFERING UNTESTED
TELEMETRY SCHEMA INVALID
TELEMETRY INTEGRITY UNVERIFIED
COMMAND AUTHENTICATION INCOMPLETE
COMMAND AUTHORIZATION INCOMPLETE
LEAST PRIVILEGE UNVERIFIED
FIRMWARE TRUST FAILED
OTA TEST REQUIRED
ROLLBACK TEST REQUIRED
PRIVACY REVIEW REQUIRED
OBSERVABILITY INCOMPLETE
FLEET CANARY REQUIRED
INCIDENT RECOVERY UNTESTED
CRITICAL RISK OPEN
HUMAN APPROVAL REQUIRED
```

The system should never fabricate a successful device test, telemetry result, security control, OTA result, rollback result, incident recovery result, or approval to make a release appear ready.

## CI and reproducibility

The GitHub Actions workflow under `.github/workflows/ci.yml` validates the reference implementation across supported Python versions.

For production IoT programs, CI and release automation should additionally cover:

- firmware unit and integration tests
- hardware-in-loop tests
- protocol compatibility tests
- schema compatibility tests
- dependency scanning
- secrets scanning
- firmware signing verification
- SBOM generation where appropriate
- static analysis
- device-security tests
- cloud integration tests
- OTA simulation
- interrupted-update recovery
- rollback testing
- fleet-cohort simulation

Version hardware, firmware, schemas, configuration, cloud APIs, policies and benchmark cases so release evidence can be reproduced.

## L3 Gold Standard candidate

The repository includes `docs/L3_AUDIT.md` and is labeled an **L3 Gold Standard candidate** based on its reproducible multi-agent structure, explicit release gates, held-out benchmark path, CI, safety boundaries and engineering evidence model.

This maturity label describes the reference implementation. It does not certify a real IoT product, guarantee security, establish regulatory compliance, or authorize autonomous control of connected devices.

## Extending F50

Common extensions include:

- MQTT broker integration
- cloud IoT platform adapters
- device certificate authorities
- PKI lifecycle management
- secure-element integration
- manufacturing provisioning workflows
- digital twins
- device-shadow synchronization
- gateway management
- edge computing
- local inference
- BLE provisioning
- cellular fleet management
- LoRaWAN device management
- schema registries
- time-series databases
- stream processing
- anomaly detection
- fleet health dashboards
- SBOM and vulnerability tracking
- firmware-signing services
- OTA campaign managers
- privacy-policy enforcement
- device lifecycle and decommissioning workflows

New integrations should preserve the separation between reasoning, deterministic validation, operational execution and human authority.

## Example applications

F50 can serve as an architectural reference for:

- connected home devices
- industrial sensors
- environmental monitoring
- smart-building systems
- asset tracking
- fleet telemetry
- connected appliances
- agricultural IoT
- energy monitoring
- wearable and wellness devices
- research instrumentation
- edge AI systems

Medical, automotive, aviation, industrial-safety, critical-infrastructure and other regulated deployments require additional domain-specific engineering, verification, cybersecurity, quality-system and regulatory controls.

## Design principles

1. Treat every device as an independently identifiable trust boundary.
2. Design for intermittent connectivity rather than assuming a permanent network.
3. Version telemetry as an interface contract.
4. Minimize collected data and make retention intentional.
5. Separate authentication from authorization.
6. Treat firmware provenance and OTA recovery as release requirements.
7. Roll out to fleets progressively with measurable stop conditions.
8. Make observability span device, network, data and fleet layers.
9. Fail closed when critical evidence is missing.
10. Keep consequential physical and fleet authority with authenticated humans and controlled operational systems.

## Documentation

Additional repository documentation is available in:

- `docs/ARCHITECTURE.md`
- `docs/L3_AUDIT.md`
- `docs/REPRODUCIBILITY_AND_SAFETY.md`

## Citation and reuse

The repository includes `CITATION.cff` for academic and technical citation and is distributed under the MIT license. It can be studied, referenced, adapted and extended subject to the license terms.

## Responsible use

Use F50 as an IoT engineering and multi-agent architecture reference. Validate device identity, firmware, hardware compatibility, network behavior, telemetry, cloud dependencies, security controls, privacy requirements, OTA recovery, observability and fleet operations against representative real systems before production deployment. Final fleet-release and physical-control authority remains with qualified, authenticated and accountable humans.