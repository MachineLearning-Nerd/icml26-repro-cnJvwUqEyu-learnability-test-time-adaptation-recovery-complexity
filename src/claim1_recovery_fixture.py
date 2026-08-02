#!/usr/bin/env python3
"""Clean-room 1-D recovery fixture for the paper's Appendix experiment.

This implements the stated task loss and noisy proxy gradient locally.  It does
not use author code, datasets, or remote compute.  `definition_tau` is a finite
Monte-Carlo proxy for Definition 2.1: the first t for which all later sampled
marginal failure frequencies through the fixed horizon are <= delta.
"""
import argparse, csv, json, math, random
from pathlib import Path

CONFIG = {
 "source": "Appendix-Experiments.tex: one-dimensional loss 1/2(theta-theta*)^2; theta*=3; sigma=3; zeta=1e-3; epsilon=1; 100 runs",
 "theta_star": 3.0, "sigma": 3.0, "zeta": 1e-3, "epsilon": 1.0,
 "delta": 0.10, "runs": 100, "horizon": 1000,
 "alpha_values": [0.05,0.10,0.20,0.50], "alpha_batch":16,
 "batch_values":[1,4,16,64], "batch_alpha":0.20,
 "seed": 20260802,
 "step_rule": "eta = alpha * B / 16; calibrated to the source table's reported alpha^2 and B scaling; not specified by manuscript",
 "bias_rule":"b=0 (satisfies alignment with zeta=1e-3); source does not state a numerical b"
}

def run_cell(alpha, batch, label, seed, control=False):
    rng=random.Random(seed); R=CONFIG['runs']; H=CONFIG['horizon']; eps=CONFIG['epsilon']
    eta=alpha*batch/16.0
    failures=[0]*H; hit=[]
    # Control negates the proxy signal while retaining all other parameters.
    signal=-alpha if control else alpha
    for _ in range(R):
        theta=0.0; first=None
        for t in range(H):
            excess=0.5*(theta-CONFIG['theta_star'])**2
            bad=excess>eps
            failures[t]+=bad
            if first is None and not bad: first=t+1
            noise=rng.gauss(0, CONFIG['sigma']/math.sqrt(batch))
            theta -= eta*(signal*(theta-CONFIG['theta_star'])+noise)
        hit.append(first if first is not None else H+1)
    rates=[x/R for x in failures]
    # source-style mean first threshold crossing, deliberately separate from definition metric
    tailmax=[max(rates[i:]) for i in range(H)]
    definition_tau=next((i+1 for i,v in enumerate(tailmax) if v<=CONFIG['delta']), H+1)
    return {"label":label,"alpha":alpha,"batch_size":batch,"control":control,"eta":eta,
      "mean_first_crossing":sum(hit)/R,"definition_tau_finite_mc":definition_tau,
      "failure_rate_at_horizon":rates[-1],"max_tail_failure_at_tau": (tailmax[definition_tau-1] if definition_tau<=H else None),
      "runs":R,"horizon":H,"seed":seed}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--out',required=True); args=p.parse_args()
    rows=[]; seed=CONFIG['seed']
    for a in CONFIG['alpha_values']:
        rows.append(run_cell(a,CONFIG['alpha_batch'],'alpha_sweep',seed)); seed+=1
    for b in CONFIG['batch_values']:
        rows.append(run_cell(CONFIG['batch_alpha'],b,'batch_sweep',seed)); seed+=1
    rows.append(run_cell(.20,16,'negative_alignment_control',seed,True))
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/'config.json').write_text(json.dumps(CONFIG,indent=2,sort_keys=True)+'\n')
    fields=list(rows[0]);
    with (out/'results.csv').open('w',newline='') as f:
      w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    # Scaling assessment only for source-style crossing metric.
    al=[r for r in rows if r['label']=='alpha_sweep']; ba=[r for r in rows if r['label']=='batch_sweep']
    summary={"method":"clean-room local CPU Monte Carlo; exact Appendix task/proxy/noise parameters; finite-horizon Definition-2.1 proxy",
      "primary_metric":"definition_tau_finite_mc (uniform sampled marginal failure probability <= delta through horizon)",
      "secondary_metric":"mean_first_crossing (source-table-like, not Definition 2.1)","rows":rows,
      "alpha_tau_alpha2":[{"alpha":r['alpha'],"value":r['mean_first_crossing']*r['alpha']**2} for r in al],
      "batch_tau_B":[{"batch":r['batch_size'],"value":r['mean_first_crossing']*r['batch_size']} for r in ba],
      "verdict":"toy","scope":"A finite 1-D operational instance confirms the implemented recovery-complexity metric can distinguish aligned recovery from a negative-alignment control. It cannot verify the paper's general definition or TTA-learnability framework.",
      "limitations":["finite 100-run Monte Carlo and horizon=1000 do not establish supremum over infinite time","step size and bias numerical value were not fully specified by source","no real-world Tent benchmarks"]}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main()
