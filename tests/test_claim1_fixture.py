import csv, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).parents[1]
def test_fixture_and_control(tmp_path):
    out=tmp_path/'out'
    subprocess.run([sys.executable,'src/claim1_recovery_fixture.py','--out',str(out)],cwd=ROOT,check=True)
    s=json.loads((out/'summary.json').read_text()); rows=list(csv.DictReader((out/'results.csv').open()))
    assert len(rows)==9 and s['verdict']=='toy'
    control=[r for r in rows if r['label']=='negative_alignment_control'][0]
    aligned=[r for r in rows if r['label']=='batch_sweep' and r['batch_size']=='16'][0]
    assert float(control['mean_first_crossing']) > float(aligned['mean_first_crossing'])
def test_source_parameters_are_pregistered(tmp_path):
    out=tmp_path/'out'; subprocess.run([sys.executable,'src/claim1_recovery_fixture.py','--out',str(out)],cwd=ROOT,check=True)
    c=json.loads((out/'config.json').read_text())
    assert (c['theta_star'],c['sigma'],c['epsilon'],c['runs']) == (3.0,3.0,1.0,100)
