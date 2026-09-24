# Optional live Codelit integration: future design

Status: **proposed, not configured, not deployed, not tested**. This release intentionally bundles no MCP server, registered app mapping, credentials, scheduled tasks, or lifecycle hooks.

## Evidence available

The public API reference at https://codelit.io/docs/api describes architecture generation, repository analysis, and signed workflow triggers. It does not establish a complete authenticated project-management API or MCP service for the plugin. Some model-key instructions conflict. Confirm the actual production contract before writing an adapter.

## Proposed connection sequence

1. Inspect the authorized Codelit backend/API contract and authentication model. Do not fabricate a production endpoint or use an example URL as a real service.
2. Define the intended user/tenant identity and narrow resource scope. Use a properly authenticated integration; keep tokens and signing secrets outside prompts, artifacts, and logs.
3. Start with a bounded read-only operation. Verify tenant isolation, pagination, redaction, and permission errors before any write capability.
4. Add draft-saving operations only after the target project, exact payload, version, and authorization are known. Handle concurrency and idempotency using the provider's actual contract.
5. Add live-team execution only with scoped deployment identity, authorized runtime/spend limits, approval handling, signature verification where required, replay defenses, and observable confirmation.
6. Register the real MCP service through the supported connection flow and add its exact returned registration ID or verified server configuration. Do not invent an app ID, MCP hostname, or OAuth grant.
7. Test staging or a bounded test project before exposing production writes. Treat a timeout after a write as unknown; reconcile before retrying.

## Possible future tools

These names are design proposals, NOT current Codelit endpoints or installed tools:

- Read project/artifact metadata within one tenant.
- Save a versioned draft plan to an authorized project.
- Read a team specification and run status.
- Request a scoped live run after the required approval.
- Fetch redacted evidence for a confirmed run.

Required tests: cross-tenant denial; revoked credentials; altered approved payload; changed target; expired approval; duplicate event; failed signature; delayed completion; cancellation; budget exhaustion; secret redaction; and unknown external outcome.

Creating or installing a skills plugin alone does not implement any of these operations.
