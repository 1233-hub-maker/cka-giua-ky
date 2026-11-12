const http = require('http');
const os = require('os');
const VERSION = process.env.APP_VERSION || 'dev';
let hits = 0;
http.createServer((req, res) => {
  if (req.url === '/healthz') { res.writeHead(200); return res.end('ok'); }
  if (req.url.startsWith('/api/info')) {
    hits++;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ version: VERSION, pod: os.hostname(), hits }));
  }
  res.writeHead(404); res.end('not found');
}).listen(3000, () => console.log('backend', VERSION, 'listening on 3000'));
