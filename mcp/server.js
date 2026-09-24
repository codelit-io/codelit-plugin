import express from 'express';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { z } from 'zod';
import catalog from './catalog.json' with { type: 'json' };

export const version = '1.0.0';
const annotations = { readOnlyHint: true, destructiveHint: false, openWorldHint: false, idempotentHint: true };
const workflow = z.enum(['product-plan', 'architecture', 'agent-team', 'plan-and-ship']);
const summary = z.object({ id: workflow, title: z.string(), url: z.string().url() });
const boundary = 'Public, bundled planning templates only. No account access, saved drafts, agent execution, deployment, or live website lookup. Returned links navigate to template collections; they do not import or save content.';
export function createServer() {
  const server = new McpServer({ name: 'codelit-public-templates', version }, { instructions: boundary });
  server.registerTool('list_codelit_workflows', {
    title: 'List Codelit planning workflows',
    description: 'List four public Codelit planning workflows and their canonical template collection URLs. Use to choose the appropriate planning template. Returns a bundled catalog, not live account data.',
    inputSchema: z.object({}).strict(),
    outputSchema: { workflows: z.array(summary), boundaries: z.string() }, annotations
  }, async () => {
    const result = { workflows: Object.values(catalog).map(({ id, title, url }) => ({ id, title, url })), boundaries: boundary };
    return { content: [{ type: 'text', text: JSON.stringify(result) }], structuredContent: result };
  });
  server.registerTool('get_codelit_planning_template', {
    title: 'Get a Codelit planning template',
    description: 'Retrieve a complete bundled Markdown template for a product plan, proposed architecture, supervised agent-team design, or connected implementation handoff. Supply only a workflow ID; never send private draft content. Does not create, save, run, or deploy anything.',
    inputSchema: z.object({ workflow }).strict(),
    outputSchema: { id: workflow, title: z.string(), url: z.string().url(), template: z.string(), boundaries: z.string() }, annotations
  }, async ({ workflow }) => {
    const result = { ...catalog[workflow], boundaries: boundary };
    return { content: [{ type: 'text', text: JSON.stringify(result) }], structuredContent: result };
  });
  return server;
}
const app = express();
app.disable('x-powered-by');
app.use((req, res, next) => {
  res.set('X-Content-Type-Options', 'nosniff');
  res.set('Cache-Control', 'no-store');
  const origin = req.get('origin');
  if (origin && !['https://chatgpt.com', 'https://platform.openai.com', 'https://codelit.io'].includes(origin)) return res.status(403).json({ error: 'Origin not allowed' });
  next();
});
app.use(express.json({ limit: '16kb' }));
app.get('/', (_req, res) => res.json({ name: 'Codelit Public Templates MCP', version, endpoint: '/mcp', support: 'https://codelit.io/about', privacy: 'https://codelit.io/privacy', boundaries: boundary }));
app.get('/health', (_req, res) => res.json({ status: 'ok', version }));
app.get('/.well-known/openai-apps-challenge', (_req, res) => {
  const token = process.env.OPENAI_APPS_CHALLENGE;
  if (!token) return res.status(404).end();
  return res.type('text/plain').send(token);
});
app.post('/mcp', async (req, res) => {
  const server = createServer();
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
  res.on('close', () => { transport.close(); server.close(); });
  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch {
    if (!res.headersSent) res.status(500).json({ jsonrpc: '2.0', id: null, error: { code: -32603, message: 'Internal server error' } });
  }
});
app.all('/mcp', (_req, res) => res.status(405).set('Allow', 'POST').json({ jsonrpc: '2.0', id: null, error: { code: -32000, message: 'Method not allowed' } }));
app.use((err, _req, res, _next) => res.status(err.type === 'entity.too.large' ? 413 : 400).json({ error: 'Invalid request body' }));
export default app;
