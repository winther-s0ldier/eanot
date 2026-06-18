const fs = require('fs');
const path = require('path');

const file = path.join('z:', 'eanot', 'index.html');
let content = fs.readFileSync(file, 'utf8');

const replacements = {
  'â€¦': '…',
  'â€”': '—',
  'â€“': '–',
  'â€¢': '•',
  'Ã—': '×',
  'â†’': '→',
  'â†”': '↔',
  'â”€': '─'
};

for (const [bad, good] of Object.entries(replacements)) {
  content = content.replaceAll(bad, good);
}

fs.writeFileSync(file, content, 'utf8');
console.log('Fixed encoding issues in index.html');
