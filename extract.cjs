const fs = require('fs');
const nb = JSON.parse(fs.readFileSync('notebook.json', 'utf8'));
let code = '';
nb.cells.forEach(cell => {
  if (cell.cell_type === 'code') {
    code += cell.source.join('') + '\n\n';
  }
});
fs.writeFileSync('extracted_code.py', code);
console.log('Extracted code to extracted_code.py');
