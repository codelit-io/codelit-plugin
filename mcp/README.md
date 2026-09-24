# Codelit Public Templates MCP

Read-only companion service for Codelit's five planning skills. Server version 1.0.0 is independent of the downloadable skills-only plugin version 1.1.1.

Endpoint: **https://codelit-public-mcp.vercel.app/mcp**

Transport: stateless Streamable HTTP. Authentication: none; all returned content is public and bundled with this service.

## Tools

- `list_codelit_workflows`: returns four planning workflows and canonical Codelit collection links.
- `get_codelit_planning_template`: accepts exactly one `workflow` enum (`product-plan`, `architecture`, `agent-team`, `plan-and-ship`) and returns the bundled Markdown template and collection link.

Both tools declare read-only, non-destructive, idempotent, closed-world behavior. There are no account connections, write operations, arbitrary URL fetches, user-content fields, or live website queries. Results are templates, not executed plans or saved assets.

`catalog.json` contains verbatim template snapshots from the existing plugin references. Updating those references does not automatically update the service snapshot.

## Operation

Use Node.js 24 and `npm ci`. Run `npm test` for the MCP client integration tests. `npm start` serves only on 127.0.0.1:8787 for local development.

The Express app is deployed from this directory as a separate Vercel project. `GET /health` reports service version; `POST /mcp` serves MCP. GET/DELETE on `/mcp` return 405 because persistent sessions and SSE subscriptions are not provided.

The optional `OPENAI_APPS_CHALLENGE` environment variable serves the exact OpenAI domain-verification token at `/.well-known/openai-apps-challenge`. Keep its value out of source control. No token means a 404 response.

Request bodies are limited to 16 KiB. Unknown tool input fields and workflow IDs are rejected. Browser origins are restricted to ChatGPT, OpenAI Platform, and Codelit; server-to-server requests without Origin are supported. The application does not log request bodies or persist data. Hosting infrastructure may retain standard request metadata under its platform settings; do not send private drafts or credentials.

## Verification

The same real MCP client test passed locally and against the unauthenticated production endpoint: initialization, tool listing and annotations, all four template calls, invalid/path-traversal IDs, extra fields, unsupported methods, invalid origins, malformed JSON, and oversized bodies. `npm audit --omit=dev` reported zero vulnerabilities on 2026-09-24.

The prior 27 skill behavior cases are evidence for the unchanged 1.1.1 skill package, not for this new server. Server verification is recorded separately here. OpenAI review remains a separate process.

Support: https://codelit.io/about
