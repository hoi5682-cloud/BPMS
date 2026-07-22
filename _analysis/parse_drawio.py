import xml.etree.ElementTree as ET
import re, html, json, sys

path = "/Users/kwan/workspace/workspace/10-projects/12-bpms/제목 없는 다이어그램.drawio"
tree = ET.parse(path)
root = tree.getroot()

def strip_html(s):
    if s is None:
        return ""
    s = html.unescape(s)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</p>|</div>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\n\s*\n+', '\n', s)
    s = s.strip()
    s = re.sub(r'[ \t]+', ' ', s)
    return s

cells = {}
for cell in root.iter('mxCell'):
    cid = cell.get('id')
    if cid is None:
        continue
    geom = cell.find('mxGeometry')
    entry = {
        'id': cid,
        'parent': cell.get('parent'),
        'source': cell.get('source'),
        'target': cell.get('target'),
        'value': strip_html(cell.get('value')),
        'style': cell.get('style') or '',
        'vertex': cell.get('vertex') == '1',
        'edge': cell.get('edge') == '1',
    }
    if geom is not None:
        entry['x'] = float(geom.get('x', 0))
        entry['y'] = float(geom.get('y', 0))
        entry['w'] = float(geom.get('width', 0))
        entry['h'] = float(geom.get('height', 0))
    cells[cid] = entry

def classify(style):
    if 'rhombus' in style:
        return 'decision'
    if 'shape=parallelogram' in style:
        return 'data'
    if 'shape=mxgraph.basic.document' in style or 'shape=mxgraph.flowchart.document2' in style:
        return 'document'
    if 'swimlane' in style:
        return 'lane'
    if 'ellipse' in style:
        return 'event'
    if 'text;' in style and 'fillColor=none' in style:
        return 'text'
    if 'fillColor=#FF3333' in style or 'sketch=1' in style:
        return 'exception'
    if 'fillColor=#CCE5FF' in style:
        return 'system-task'
    if style.strip() == '' or 'rounded=0;whiteSpace=wrap;html=1' in style or 'rounded=0;whiteSpace=wrap;html=1;shadow=0' == style.strip(';').strip()+';' :
        return 'task'
    return 'other'

vertices = [c for c in cells.values() if c['vertex']]
edges = [c for c in cells.values() if c['edge']]

print(f"TOTAL vertices={len(vertices)} edges={len(edges)}", file=sys.stderr)

# classify counts
from collections import Counter
cnt = Counter(classify(v['style']) for v in vertices)
print("CLASS COUNTS:", dict(cnt), file=sys.stderr)

out = {'vertices': [], 'edges': []}
for v in vertices:
    out['vertices'].append({
        'id': v['id'], 'parent': v['parent'], 'value': v['value'],
        'class': classify(v['style']),
        'x': v.get('x'), 'y': v.get('y'), 'w': v.get('w'), 'h': v.get('h'),
    })
for e in edges:
    out['edges'].append({
        'id': e['id'], 'source': e['source'], 'target': e['target'], 'value': e['value'],
    })

with open('/private/tmp/claude-501/-Users-kwan-workspace-workspace/04c4ef4d-435a-499b-a0ac-5b7bb5148f6b/scratchpad/drawio_parsed.json', 'w') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("done", file=sys.stderr)
