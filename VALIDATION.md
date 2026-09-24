# Validation record

Release: 1.1.1. Checked September 24, 2026.

## Static validation

The local validator passed 152 checks with no errors. Shell syntax and publication dry run passed. The portable manifest passed the current agent-plugins.org JSON Schema using jsonschema. Pillow decoded the original 600 x 600 RGBA logo; its SHA-256 remains `56df557b948c21b2c582d14aeeb5ef1f2c96a1ead546caf934288b84f9251881`.

Reviewed all 30 supplied source files and the two added sanitized behavioral-result files, including all five skills and their references. A limited pattern scan found no credential/private-key patterns, signed URLs, private account or conversation identifiers, or local filesystem paths. No original Git history, application source, customer data, integrations, hooks, or symlinks are included. This is not an independent security certification.

Direct HTTP retrieval returned 200 for all four canonical workflow links, privacy and terms. Page titles matched the intended destinations. No authenticated website action was tested.

The publication helper now requires a successful organization inventory before treating a repository as absent. Mocked network failure and existing-repository cases both stopped before Git mutation.

## Behavioral validation

Installed through a local Codex marketplace using authenticated ChatGPT access. All 27 cases passed after output review: 18 supplied behavioral cases, eight reviewer cases and one unrelated-request case. Each used an isolated ephemeral context with the installed plugin. P4 initially hit the 150-second limit and passed one retry in 178.2 seconds under a 300-second limit. See release/Behavioral_Results.md and release/behavioral-results.json for observations, durations and output/artifact hashes. Static checks do not establish model behavior. Raw runtime evidence stays outside public source.

## OpenAI status

The public source repository was published and verified at https://github.com/codelit-io/codelit-plugin on main, with matching local/remote commits, an exact intended file inventory, and rendered README/logo.

The OpenAI draft contains listing details, original icons, three prompts, eight reviewer cases and release notes. All five uploaded skills passed the platform safety/security scans. The available draft still requires an MCP server URL and customer support URL, while this package intentionally supplies no MCP server. Country availability and policy attestations remain unconfirmed. No public review submission or approval is claimed. Private draft identifiers and publisher verification records are excluded from this repository.

## Behavioral limits

These tests inspect actual generated outputs and artifacts, not just static strings. They used synthetic input, local file access, and no external writes or production operations. B11 verified an honest unavailable-browsing fallback; live pricing retrieval was not exercised. No live Codelit integration, platform execution isolation, or exhaustive adversarial security test is claimed. All 14 tested skill/reference files match the final release bytes.
