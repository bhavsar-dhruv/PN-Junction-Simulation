const fs = require('fs');
const https = require('https');

https.get('https://raw.githubusercontent.com/bhavsar-dhruv/Nano-hub-PN-Junction/main/src/pnjunctionapp.ipynb', (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  res.on('end', () => {
    fs.writeFileSync('notebook.json', data);
    console.log('Downloaded');
  });
});
