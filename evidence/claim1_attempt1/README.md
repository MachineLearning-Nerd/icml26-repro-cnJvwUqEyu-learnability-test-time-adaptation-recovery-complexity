# Claim 1 attempt 1 artifacts

Run locally with:

```bash
.venv/bin/python src/claim1_recovery_fixture.py --out outputs/claim1_attempt1
(cd outputs/claim1_attempt1 && sha256sum -c SHA256SUMS)
```

The task, proxy, shift, sigma, epsilon, and 100-run setup follow `proof/Appendix-Experiments.tex` in the pinned archive. Numerical step-size and bias choices are declared in `config.json` because the source does not specify them. `definition_tau_finite_mc` estimates the definition's uniform-after-$t$ condition only across the finite horizon and 100 Monte-Carlo trajectories.
