// Development convenience only. The application also opens directly from index.html.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const files = new Set(['index.html', 'styles.css', 'core.js', 'app.js']);
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript' };
const server = http.createServer((req, res) => {
  const name = req.url === '/' ? 'index.html' : req.url.split('?')[0].slice(1);
  if (!files.has(name)) {
    res.writeHead(404);
    res.end('Not found');
    return;
  }
  res.setHeader('Content-Type', types[path.extname(name)] + '; charset=utf-8');
  fs.createReadStream(path.join(root, name)).pipe(res);
});
server.listen(Number(process.env.PORT || 4173), '127.0.0.1', () => {
  console.log(`Creative Landscaping is running at http://127.0.0.1:${server.address().port}`);
});
