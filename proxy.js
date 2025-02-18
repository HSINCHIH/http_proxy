const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

const targetUrl = 'http://example.com';

app.use(
  '/',
  createProxyMiddleware({
    target: targetUrl,
    changeOrigin: true,
    ws: true,
    secure: false,
    onProxyReq: (proxyReq, req, res) => {
      console.log(`[Proxy] Forwarding request: ${req.method} ${req.url}`);
    },
    onProxyRes: (proxyRes, req, res) => {
      console.log(`[Proxy] Received response with status: ${proxyRes.statusCode}`);
    },
    onError: (err, req, res) => {
      console.error(`[Proxy] Error: ${err.message}`);
      res.status(500).send('Proxy Error');
    },
  })
);

const PORT = 8080;
app.listen(PORT, () => {
  console.log(`Proxy server running at http://localhost:${PORT}`);
});
