from pathlib import Path
p = Path(r'Z:\eanot\index.html')
s = p.read_text(encoding='utf-8')

fixes = [
    ("priColors=['#657487','#7f8ea1','#9bb0c7','#c2cfde']",
     "priColors=['#cc7066','#d6a85a','#638ecc','#6fc0a0']"),
    ("var gColors={A:'#c2cfde',B:'#9bb0c7',C:'#7f8ea1',D:'#657487','?':'#8b95ad'}",
     "var gColors={A:'#6fc0a0',B:'#638ecc',C:'#d6a85a',D:'#cc7066','?':'#8b95ad'}"),
    ("backgroundColor:['#c2cfde','#9bb0c7','#b6c4d5','#7f8ea1','#72829a','#657487']",
     "backgroundColor:['#6fc0a0','#638ecc','#7facd6','#d6a85a','#d4828a','#cc7066']"),
    ("backgroundColor:['#657487','#7f8ea1','#9bb0c7','#c2cfde']",
     "backgroundColor:['#cc7066','#d6a85a','#638ecc','#6fc0a0']"),
    ("backgroundColor:['#c2cfde','#9bb0c7','#7f8ea1','#657487','#8b95ad']",
     "backgroundColor:['#6fc0a0','#638ecc','#d6a85a','#cc7066','#8b95ad']"),
    ("backgroundColor:['#657487','#7f8ea1','#c2cfde']",
     "backgroundColor:['#cc7066','#d6a85a','#6fc0a0']"),
    ("fPalette=['#9bb0c7','#b2c0d1','#7b8da3','#6b7c93','#8fa0b6','#aebccd']",
     "fPalette=['#638ecc','#6fc0a0','#d6a85a','#cc7066','#7facd6','#b47ad9']"),
]

for old, new in fixes:
    count = s.count(old)
    if count:
        s = s.replace(old, new)
    else:
        print(f'NOT FOUND: {old[:80]}')

# Restore ch-tat-monthly line chart
s = s.replace("borderColor:'#9bb0c7',backgroundColor:'rgba(155,176,199,0.10)'",
              "borderColor:'#638ecc',backgroundColor:'rgba(99,142,204,0.10)'")
s = s.replace("borderColor:'#7f8ea1',backgroundColor:'transparent'",
              "borderColor:'#d6a85a',backgroundColor:'transparent'")

# Restore ch-tat-brand bar (median blue, mean amber)
s = s.replace("backgroundColor:'#9bb0c7'},{label:'Mean (h)',data:bSum.map(function(x){return+x.mn.toFixed(1)}),backgroundColor:'#7f8ea1'",
              "backgroundColor:'#638ecc'},{label:'Mean (h)',data:bSum.map(function(x){return+x.mn.toFixed(1)}),backgroundColor:'#d6a85a'")

# Restore ch-tat-pri bar
s = s.replace("backgroundColor:'#9bb0c7'},{label:'Mean (h)',data:pMeds,backgroundColor:'#7f8ea1'",
              "backgroundColor:'#638ecc'},{label:'Mean (h)',data:pMeds,backgroundColor:'#d6a85a'")

# Restore single bar fills
s = s.replace("ch-regions',{type:'bar',data:{labels:rt.map(function(e){return e[0]}),datasets:[{data:rt.map(function(e){return e[1]}),backgroundColor:'#9bb0c7'}",
              "ch-regions',{type:'bar',data:{labels:rt.map(function(e){return e[0]}),datasets:[{data:rt.map(function(e){return e[1]}),backgroundColor:'#638ecc'}")

s = s.replace("ch-monthly-spend',{type:'bar',data:{labels:mKeys,datasets:[{data:mKeys.map(function(m){return ms[m]}),backgroundColor:'#9bb0c7'}",
              "ch-monthly-spend',{type:'bar',data:{labels:mKeys,datasets:[{data:mKeys.map(function(m){return ms[m]}),backgroundColor:'#638ecc'}")

# Restore am-trend and am-types
s = s.replace("backgroundColor:'#9bb0c7'", "backgroundColor:'#638ecc'", 1)  # am-trend first
s = s.replace("backgroundColor:'#c2cfde'", "backgroundColor:'#6fc0a0'", 1)  # am-types first

# Restore ai-features
s = s.replace("backgroundColor:'rgba(255,111,139,0.72)'", "backgroundColor:'rgba(212,130,138,0.72)'")

p.write_text(s, encoding='utf-8')
print('All chart colors restored')
