import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import app from './server.js';
test('MCP handshake, catalog, all templates, invalid inputs and HTTP boundaries', async () => {
 const http = app.listen(0, '127.0.0.1');
 await new Promise(r => http.once('listening', r));
 const base = process.env.TEST_MCP_BASE || `http://127.0.0.1:${http.address().port}`;
 const client = new Client({name:'codelit-verification',version:'1.0.0'});
 try {
  await client.connect(new StreamableHTTPClientTransport(new URL(base+'/mcp')));
  const {tools} = await client.listTools();
  assert.equal(tools.length,2);
  for (const t of tools) { assert.equal(t.annotations.readOnlyHint,true); assert.equal(t.annotations.destructiveHint,false); assert.equal(t.annotations.openWorldHint,false); }
  const list=await client.callTool({name:'list_codelit_workflows',arguments:{}});
  assert.equal(list.structuredContent.workflows.length,4);
  for (const item of list.structuredContent.workflows) {
   const result=await client.callTool({name:'get_codelit_planning_template',arguments:{workflow:item.id}});
   assert.equal(result.isError,undefined);
   assert.ok(result.structuredContent.template.length>200);
   assert.equal(result.structuredContent.url,item.url);
   assert.match(result.structuredContent.url,/^https:\/\/codelit.io\//);
  }
  for (const args of [{workflow:'../../etc/passwd'},{workflow:'architecture',privateDraft:'not accepted'}]) {
   const result=await client.callTool({name:'get_codelit_planning_template',arguments:args}); assert.equal(result.isError,true);
  }
  assert.equal((await fetch(base+'/mcp',{method:'GET'})).status,405);
  assert.equal((await fetch(base+'/mcp',{method:'POST',headers:{Origin:'https://evil.example','Content-Type':'application/json'},body:'{}'})).status,403);
  assert.equal((await fetch(base+'/mcp',{method:'POST',headers:{'Content-Type':'application/json'},body:'{'})).status,400);
  assert.equal((await fetch(base+'/mcp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({x:'x'.repeat(20000)})})).status,413);
 } finally { await client.close(); await new Promise(r=>http.close(r)); }
});
