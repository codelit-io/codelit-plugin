# Public-submission checklist

Prepared September 23, 2026. Package: Codelit 1.1.1 (`codelit-copilot`).

## Prepared in this release

- Updated display name, concise listing copy, three starter prompts, and original square PNG logo/icon.
- Five existing workflow skills, with scoped template navigation and explicit no-live-connection boundaries.
- HTTPS website, privacy, and terms links from Codelit's public pages.
- Five positive and three negative reviewer cases with fixtures and expected results.
- Release notes and a reproducible local static package validator.

## Still required or unverified

- Completed: 27 isolated synthetic behavioral/reviewer cases passed; see Behavioral_Results.md for scope and evidence hashes.
- Completed: publisher-selected individual identity applied in the portal; private verification details are not stored here.
- Draft edits were saved in the publisher-confirmed existing draft.
- Review the linked website privacy/terms for coverage of this skills-only plugin and decide whether a dedicated HTTPS support page is needed. No legal attestation has been completed here.
- Choose supported countries or regions; do not assume worldwide availability.
- Resolve portal submission type: only With MCP is currently offered. The existing authorized draft has listing, icons, prompts, reviewer cases and all five skills, but requires an MCP URL. Do not add a server to this skills-only release.
- Completed: all five platform skill safety/security scans passed. These are separate from local validation.
- Complete policy attestations only after the publisher verifies their accuracy, then submit for review.
- After approval, choose when to publish. Submission does not immediately publish the plugin.

## Documented limits used for local checks

Display name and short description: at most 30 characters each. Starter prompts: at most three, at most 128 characters each. Logo/icon: supported square image, at least 48 × 48 and no more than 4096 × 4096 for raster images, no more than 5 MiB. No listing screenshots for this skills-only build.

The general submission guide asks for listing URLs and five positive/three negative cases; the specific error reference distinguishes some requirements by submission type. This release prepares reviewer cases anyway and does not misstate omitted optional fields as validated account settings. Recheck the current portal before submitting.

## Scope of this update

Plugin Creator updates preserve the existing audience. This package contains no request to change sharing, select an organization, accept terms, complete identity verification, or attest legal rights. Those decisions require the publisher's own confirmed information. No public submission or approval is implied.

## Official references

https://developers.openai.com/plugins/deploy/submission
https://developers.openai.com/plugins/deploy/submission-errors
https://developers.openai.com/plugins/build/plugins
