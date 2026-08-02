import json
from pathlib import Path
ROOT=Path(__file__).parents[1]
def test_anchored_contract_is_five_claims():
    claims=json.loads((ROOT/'contract/live_claims.json').read_text())
    manifest=json.loads((ROOT/'contract/contract_manifest.json').read_text())
    assert len(claims)==5
    assert manifest['claim_count']==5 and manifest['max_points']==10
def test_source_manifest_names_pins():
    text=(ROOT/'evidence/source/SHA256SUMS').read_text()
    assert 'arxiv_source.tar.gz' in text and 'paper.pdf' in text
