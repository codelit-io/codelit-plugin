# Release notes — 1.1.1

September 24, 2026. Initial public source release, based on the supplied private package 1.1.0.

- Hardened the GitHub publication helper: an unsuccessful lookup no longer establishes repository absence; a successful organization inventory is required.
- Matched the directory publisher name to the publisher-selected individual identity.
- Added static checks for qualified skill names, capabilities, and reviewer version consistency.
- Updated release records and version references for public source publication and measured testing.
- Preserved all five workflows, the Codelit display name, codelit-copilot identity, three starter prompts, and original logo bytes.

No account integration, MCP server, independent agent runtime, deployment capability, or license was added. Public source publication and OpenAI review are separate operations. See VALIDATION.md for measured results and outstanding gates.

Validation: 152 static checks and 27 bounded synthetic behavioral cases passed. All five platform skill scans passed. OpenAI submission remains a draft, with submission-type and publisher gates unresolved.
