const http = require('http');

const port = 3000;

const server = http.createServer((req, res) => {
  res.end('Hello Node!\n');
});

server.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
