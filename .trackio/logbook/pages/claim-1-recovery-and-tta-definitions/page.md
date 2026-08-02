# Claim 1 — recovery complexity and TTA learnability

**Outcome: toy (finite local operational fixture; not a verification of the general framework).**

The pinned source defines recovery complexity as the smallest time after which the *marginal* excess-risk failure probability remains at most $\delta$ uniformly in later time; it separately defines global $(\epsilon,\rho)$ TTA learnability. We implemented the source Appendix's one-dimensional post-shift fixture locally: $\ell(\theta)=\frac12(\theta-3)^2$, proxy gradient $\alpha\nabla\ell+N(0,3^2/B)$, $\epsilon=1$, 100 seeded runs.

The finite-horizon Monte-Carlo operational proxy gives definition-$\tau$ values 579, 164, 42, and 7 for $\alpha=0.05,0.10,0.20,0.50$ at $B=16$. A negative-alignment control never meets the threshold within horizon 1000. The source-table-style first-crossing statistic has near-constant $\tau\alpha^2$ (0.686–1.053) and $\tau B$ (288–380). Raw data, fixed config, hashes, and the explicit limitations are in `outputs/claim1_attempt1/`.

This finite synthetic calculation operationalizes the local definition and control; it neither proves the framework's definitions in general nor evaluates long-stream $(\epsilon,\rho)$ learnability.
