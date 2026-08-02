OpenReview ID: cnJvwUqEyu
Submission number: 9856
Live claim count / maximum points: 5 / 10
Selection timestamp: 2026-08-02T12:30:41Z
Contract manifest SHA-256: d775d40bf270bc8fcee89c2fc271dcebf96ddd7eee8d45705d62baa586e4ff87
Source paper/version: arXiv:2605.28057 source archive and PDF pinned
Official code/data/model pins: no author executable confirmed in initial source audit
Compute policy: local CPU/local GPU only; no HF cpu-upgrade, Jobs, paid, or remote compute
GitHub repository: https://github.com/MachineLearning-Nerd/icml26-repro-cnJvwUqEyu-learnability-test-time-adaptation-recovery-complexity
Current phase: claim_1_protocol_pending_direct_local_recovery_experiment
Per-claim state: C1 pending; C2-C5 not started
Publication status: not published
Selection rationale: anchored five-claim contract; the source specifies a controlled one-dimensional recovery experiment and theorem scaling claims that admit clean-room local CPU tests. CIFAR/ImageNet benchmark work remains separately resource-audited and is not assumed reproducible.

## Claim 1 attempt 1 — finite local recovery fixture (completed)
- **Verdict:** toy. A clean-room local CPU implementation of the pinned Appendix's 1-D quadratic post-shift setting operationalized finite-horizon recovery complexity. It is not a verification of the general definitions or of global $(\epsilon,\rho)$ learnability.
- **Method/metric/control:** source task loss/proxy/noise/shift (`theta*=3`, `sigma=3`, `epsilon=1`, 100 seeded trajectories); primary finite Monte-Carlo uniform-tail failure metric (`delta=.1`, horizon 1000); source-table-style first crossing reported only secondarily; negative-alignment control.
- **Results:** finite definition-tau is 579, 164, 42, 7 across alpha .05/.10/.20/.50 at B=16; the negative-alignment control never recovers by horizon 1000. The first-crossing scaling products are retained without generalization.
- **Evidence:** `src/claim1_recovery_fixture.py`, `outputs/claim1_attempt1/{config.json,results.csv,summary.json,SHA256SUMS}`, `evidence/claim1_attempt1/README.md`; `sha256sum -c` and pytest pass.
- **Next:** independent review of the toy against literal Claim 1 before any logbook escalation; then source audit Claim 2.
