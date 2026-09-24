#!/usr/bin/env python3
"""Validate this local skills package without network requests or side effects."""
from __future__ import annotations
import json
import re
import sys
import hashlib
import struct
import unicodedata
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
checks: list[str] = []

def require(condition: bool, message: str) -> None:
    (checks if condition else errors).append(message)

def read_json(path: Path) -> dict:
    try:
        obj = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(obj, dict):
            raise ValueError('Expected an object')
        return obj
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f'{path.relative_to(ROOT)}: {exc}')
        return {}

portable = read_json(ROOT / 'plugin.json')
compat = read_json(ROOT / '.codex-plugin/plugin.json')
require(portable.get('name') == compat.get('name') == 'codelit-copilot', 'One consistent plugin identity')
version = portable.get('version', '')
require(version == compat.get('version') and bool(re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?', version)), 'Consistent semantic release version')
require(portable.get('$schema') == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'Portable schema declaration')
require(compat.get('skills') in ('./skills', './skills/'), 'Compatibility skills path')
require(portable.get('extensions', {}).get('com.openai', {}).get('interface') == compat.get('interface'), 'Consistent display metadata')
require(bool(portable.get('description')), 'Nonempty plugin description')
require(bool(compat.get('interface', {}).get('defaultPrompt')), 'Starter prompts present')
require(len(list(ROOT.rglob('plugin.json'))) == 2, 'Only the root manifest and same-plugin compatibility overlay')

skills = sorted((ROOT / 'skills').glob('*/SKILL.md'))
require(len(skills) == 5, 'Exactly five skill entry points')
seen: set[str] = set()
for path in skills:
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n', text)
    require(bool(match), f'Valid skill frontmatter: {path.parent.name}')
    if match:
        name, encoded_description = match.groups()
        try:
            description = json.loads(encoded_description)
            require(isinstance(description, str) and 1 <= len(description) <= 1024, f'Valid description: {name}')
        except ValueError:
            require(False, f'Invalid quoted description: {name}')
        require(name == path.parent.name and name not in seen and len(name) <= 64, f'Unique matching skill name: {name}')
        require(len('codelit-copilot:' + name) <= 64, f'Qualified skill identity within limit: {name}')
        seen.add(name)
    require('## Evidence, permissions, and execution boundaries' in text, f'Action/evidence rules present: {path.parent.name}')
    require('Proposed design' in text and 'Unknown' in text, f'Uncertainty categories: {path.parent.name}')
    require('timeout is an unknown outcome' in text, f'Unknown-write-outcome guard: {path.parent.name}')

# Relative markdown links must stay inside the package and resolve to files.
for path in ROOT.rglob('*.md'):
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        if target.startswith(('https://', 'http://', 'mailto:', '#')):
            continue
        clean = target.split('#', 1)[0]
        resolved = (path.parent / clean).resolve()
        try:
            resolved.relative_to(ROOT)
            inside = True
        except ValueError:
            inside = False
        require(inside and resolved.is_file(), f'Resolvable internal link: {path.relative_to(ROOT)} -> {target}')

for forbidden in ('.mcp.json', 'mcp.json', '.app.json', 'hooks/hooks.json', '.env'):
    require(not (ROOT / forbidden).exists(), f'No unconfigured integration, hook, or secret file: {forbidden}')
require(not any(p.is_symlink() for p in ROOT.rglob('*')), 'No symlinks')
require(not any(k in compat for k in ('mcpServers', 'apps', 'hooks')), 'No declared compatibility connections or hooks')
require(not any(k in portable.get('extensions', {}).get('com.openai', {}) for k in ('apps', 'hooks')), 'No declared portable connections or hooks')

fixture = read_json(ROOT / 'tests/traceability-fixture.json')
ids = {name: {item['id'] for item in fixture.get(name, [])} for name in ('requirements', 'components', 'agents', 'tasks', 'tests')}
covered: set[str] = set()
for link in fixture.get('links', []):
    require(link.get('requirement') in ids['requirements'], 'Fixture requirement link resolves')
    covered.add(link.get('requirement', ''))
    require(all(c in ids['components'] for c in link.get('components', [])), 'Fixture component links resolve')
    require(link.get('owner') in ids['agents'], 'Fixture agent owner resolves')
    require(link.get('task') in ids['tasks'], 'Fixture task link resolves')
    require(bool(link.get('tests')) and all(t in ids['tests'] for t in link['tests']), 'Fixture acceptance tests resolve')
require(covered == ids['requirements'], 'All fixture requirements have traceability')
require(fixture.get('execution') == {'run_id': None, 'provider_receipt': None, 'state': 'not_executed'}, 'No fabricated execution evidence in fixture')
require(all(t.get('status') == 'not_run' for t in fixture.get('tests', [])), 'Behavioral test statuses remain not run')


# Directory-facing metadata checks: local validation, not a portal scan.
interface = portable.get('extensions', {}).get('com.openai', {}).get('interface', {})
require(interface.get('displayName') == 'Codelit', 'Public display name updated; internal identity preserved')
for key, limit in [('displayName',30),('shortDescription',30),('developerName',80),('longDescription',4000)]:
    value=interface.get(key)
    require(isinstance(value,str) and 0<len(value.strip())<=limit, f'Directory limit: {key}')
    if key!='longDescription':
        require(isinstance(value,str) and not any(ch in value for ch in '\r\n'), f'Single-line field: {key}')
capabilities = interface.get('capabilities', [])
require(isinstance(capabilities, list) and len(capabilities) <= 20 and all(isinstance(c, str) and 0 < len(c.strip()) <= 120 and '\n' not in c and '\r' not in c for c in capabilities), 'Capabilities within final directory limits')
prompts=interface.get('defaultPrompt',[])
require(isinstance(prompts,list) and len(prompts)==3, 'Exactly three starter prompts')
normalized=set()
for prompt in prompts:
    require(isinstance(prompt,str) and 0<len(prompt)<=128 and '\n' not in prompt and '\r' not in prompt and '@' not in prompt, 'Valid final-directory starter prompt')
    normalized.add(' '.join(unicodedata.normalize('NFKC',prompt).split()))
require(len(normalized)==len(prompts), 'Unique normalized starter prompts')
require(interface.get('category') in {'Productivity','Creativity','Developer Tools','Business & Operations','Data & Analytics','Communication','Education & Research','Security','Finance','Healthcare','Travel','Entertainment','Other'}, 'Supported category')
require('screenshots' not in interface, 'No unsupported skills-only listing screenshots')
for key in ('websiteURL','privacyPolicyURL','termsOfServiceURL'):
    value=interface.get(key,''); u=urlparse(value)
    require(u.scheme=='https' and u.hostname=='codelit.io' and not u.username and not u.password and len(value)<=1024, f'Valid Codelit URL: {key}')

provenance=read_json(ROOT/'release/Brand_Provenance.json')
for key in ('logo','composerIcon'):
    rel=interface.get(key,'')
    p=(ROOT/rel).resolve()
    valid=rel.startswith('./assets/') and p.is_relative_to(ROOT) and p.is_file()
    require(valid, f'Packaged {key} path resolves inside assets')
    if valid:
        data=p.read_bytes()
        png=data[:8]==b'\x89PNG\r\n\x1a\n' and data[12:16]==b'IHDR'
        require(png, f'{key}: valid PNG signature and IHDR')
        if png:
            width,height=struct.unpack('>II',data[16:24])
            require(width==height and 48<=width<=4096, f'{key}: square raster within directory dimensions')
        require(len(data)<=5*1024*1024, f'{key}: within image byte limit')
        require(hashlib.sha256(data).hexdigest()==provenance.get('sha256'), f'{key}: original supplied bytes preserved')

def luminance(hex_color):
    vals=[int(hex_color[i:i+2],16)/255 for i in (1,3,5)]
    linear=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in vals]
    return sum(a*b for a,b in zip(linear,(0.2126,0.7152,0.0722)))
for key,bg in [('brandColor','#FFFFFF'),('brandColorDark','#212121')]:
    color=interface.get(key,'')
    valid=bool(re.fullmatch(r'#[0-9A-Fa-f]{6}',color))
    require(valid, f'{key}: six-digit hex')
    if valid:
        ls=sorted((luminance(color),luminance(bg)))
        require((ls[1]+0.05)/(ls[0]+0.05)>=2, f'{key}: at least 2:1 contrast')
registry=read_json(ROOT/'skills/codelit-guide/references/codelit-links.json')
expected={
    'product-plan': 'https://codelit.io/specs',
    'architecture': 'https://codelit.io/templates',
    'agent-team': 'https://codelit.io/agent-templates',
    'plan-and-ship': 'https://codelit.io/plan-and-ship'
}
actual={r.get('asset_type'):r.get('url') for r in registry.get('routes',[])}
require(actual==expected, 'All four output types map to the verified collection or overview')
for asset,url in actual.items():
    u=urlparse(url)
    require(u.scheme=='https' and u.hostname=='codelit.io' and not any((u.query,u.fragment,u.username,u.password)),f'Clean navigation URL without user data: {asset}')
for skill in skills:
    text=skill.read_text()
    require('template-links.md' in text, f'Link guidance referenced: {skill.parent.name}')
for folder,filename,kind in [
    ('codelit-product-plan','product-plan-template.md','product-plan'),
    ('codelit-architecture','architecture-template.md','architecture'),
    ('codelit-agent-team','agent-team-template.md','agent-team'),
    ('codelit-plan-and-ship','handoff-template.md','plan-and-ship')
]:
    text=(ROOT/'skills'/folder/'references'/filename).read_text()
    require(expected[kind] in text and 'does not save or transfer this draft' in text, f'Standalone template carries honest navigation: {kind}')
review=read_json(ROOT/'release/reviewer-cases.json')
require(review.get('plugin_version') == version, 'Reviewer fixture version matches manifest')
cases=review.get('cases',[])
require(sum(c.get('type')=='positive' for c in cases)==5, 'Five positive reviewer cases prepared')
require(sum(c.get('type')=='negative' for c in cases)==3, 'Three negative reviewer cases prepared')
require(all(c.get('actual_status')=='not_run' and c.get('evidence') is None for c in cases), 'Reviewer cases not mislabeled as executed')
for forbidden in ('mcp.json','.mcp.json','.app.json','hooks/hooks.json','.env'):
    require(not any(p.name==Path(forbidden).name for p in ROOT.rglob('*') if p.is_file()),f'No unrequested live runtime or secrets file: {forbidden}')
require(not any(re.search(r'(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)',p.read_text(errors='replace')) for p in ROOT.rglob('*') if p.is_file() and p.suffix in {'.md','.json','.txt','.yaml','.yml','.py'}), 'No common credential/private-key patterns detected (limited scan)')

result = {'status': 'PASS' if not errors else 'FAIL', 'passed_checks': len(checks), 'errors': errors, 'behavioral_tests': 'NOT EVALUATED by this static validator; see VALIDATION.md', 'live_integration_tests': 'NOT RUN: no connection configured'}
print(json.dumps(result, indent=2))
if errors:
    sys.exit(1)
