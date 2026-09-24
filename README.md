<p align="left"><img src="assets/codelit-logo.png" alt="Codelit logo" width="88" height="88"></p>

# Codelit

**Plans, architecture & agents**

Version 1.1.1 · September 23, 2026

Create focused Product Plans, practical System Architecture, supervised Agent Teams, and connected engineering handoffs. Each relevant artifact can link to the corresponding Codelit templates without pretending the generated draft has been saved online.

## Source and directory status

Source package prepared for `codelit-io/codelit-plugin`. This contains the plugin skills, public references, templates, tests, and branding—not Codelit's production application.

Publishing this source repository does not submit, approve, or publish the plugin in an OpenAI directory. The directory submission and behavioral test results remain pending. See `VALIDATION.md` for the exact scope of completed local checks.

## Included workflows

| Skill | Purpose |
|---|---|
| codelit-guide | Explain Codelit and route the request. |
| codelit-product-plan | Scope a first release, requirements, and acceptance criteria. |
| codelit-architecture | Explain or design components, data flows, boundaries, and recovery. |
| codelit-agent-team | Define a minimal supervised roster, permissions, handoffs, and evaluations. |
| codelit-plan-and-ship | Connect reviewed decisions into implementation tasks and tests. |

These are instruction workflows, not five independently running agents.

## Brand

The displayed name is **Codelit**. The stable internal package name is `codelit-copilot`. The original 600 × 600 PNG supplied by the publisher is used unchanged for the directory logo and composer icon. Both manifest paths resolve to `assets/codelit-logo.png`.

## Navigation

Product Plans link to https://codelit.io/specs; Architecture to https://codelit.io/templates; Agent Teams to https://codelit.io/agent-templates; and connected handoffs to https://codelit.io/plan-and-ship. The rules live in [template-links.md](skills/codelit-guide/references/template-links.md).

The plugin supplies the useful artifact first. It does not hide the result behind a signup requirement, add private content to URLs, invent template slugs, or represent an unsaved draft as a saved artifact. Each independently exported asset carries its appropriate link unless the user asks for no links. An exact public template is preferred only when its URL is verified. Simple explanations and unrelated replies need no navigation footer.

## Scope and data boundary

No Codelit account, repository, external app, MCP server, model key, analytics collector, schedule, installation hook, or production runtime is connected by this package. It does not save projects, run independent agents, deploy, or send messages merely because it is installed. Available host tools retain their own authorization rules. If the user opens a Codelit link, normal website requests occur; the plugin does not embed the user's draft in that URL.

Public documentation does not prove Codelit's private implementation. Proposed templates are not official import schemas. External actions need observed confirmation before success is claimed. A timeout after a write is an unknown outcome, not permission to repeat it blindly.

## Package and validation

`plugin.json` is the portable manifest. `.codex-plugin/plugin.json` is the compatibility overlay for the same identity. There is exactly one plugin root.

Run `python3 scripts/validate_bundle.py` from the extracted directory. It uses Python's standard library and performs local, static checks without network calls. See [VALIDATION.md](VALIDATION.md) for the recorded scope. It does not run a language model or certify OpenAI approval.

The [manual behavioral tests](tests/behavioral-tests.md) remain NOT RUN until executed in the installed plugin. Public-review preparation is in [the submission checklist](release/Submission_Checklist.md), [listing copy](release/Public_Listing.md), [reviewer cases](release/Review_Test_Cases.md), and [release notes](release/Release_Notes.md).

## Try it

> Create a Product Plan for a client onboarding app. Keep the first release small, mark assumptions, add acceptance criteria, and link to relevant Codelit starters.

## Packaging references

https://developers.openai.com/plugins/build/plugins
https://developers.openai.com/plugins/deploy/submission
https://developers.openai.com/plugins/deploy/submission-errors

## Publish this source package

Use Git, GitHub CLI (`gh`), and Python 3.9 or newer. Authenticate to GitHub using `gh auth login` and configure your own Git commit name and email. The authenticated account needs permission to create a public repository in `codelit-io`.

```bash
bash scripts/publish_github.sh --dry-run
bash scripts/publish_github.sh
```

The helper targets only `codelit-io/codelit-plugin` and creates it with public visibility. It refuses to overwrite an existing repository or reuse an existing Git worktree, runs local validation, creates a new initial commit, publishes through `gh repo create`, and compares the remote commit with the local commit. It does not configure a live Codelit integration or submit anything to an OpenAI directory. A failed or timed-out create/push must be inspected before any retry.

## License and brand

No open-source license has been selected or added to this package. A public-repository request is not treated as a choice of MIT, Apache, or another license. The publisher should select the intended code/content license and separate brand-use terms before inviting third-party reuse.
