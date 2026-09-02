# AI SAST Dynamic Validation

Use this agent when the user wants to confirm whether Endor AI SAST findings
are actually exploitable by safely replaying each finding's non-destructive
Exploit Reproduction proof-of-concept against a running instance of the
target web app. The agent parses Endor's AI SAST case file, statically lints
the embedded proof-of-concept for destructive patterns, retargets it to a
user-authorized base URL only, executes bounded read-only probes, and
classifies each finding as dynamically confirmed, not reproducible, blocked
by a control, or inconclusive. It never mutates the repository, the Endor
tenant, or the target application, and it never sends a single request
without explicit current-turn authorization.

## Start Here

This is the Claude Code generated agent for `ai-sast-dynamic-validation`.

| Reader | First move |
| --- | --- |
| Human operator | Copy the generated subagent into `.claude/agents/` and restart Claude Code if needed. Then use the example prompt below: @agent-ai-sast-dynamic-validation help |
| Agent installer | Copy the generated files exactly, including the generated prompt or skill file, `endorctl-setup.md`, `architecture.svg`. Do not summarize or rewrite the generated prompt. |
| Maintainer | Change `source/agents/ai-sast-dynamic-validation/recipe.yaml`, `instructions.md`, evals, action contracts, or `architecture.svg`, then regenerate the catalog. Do not hand-edit generated copies. |

## Recommended Model

This is a release-QA target, not a requirement or model allowlist.
Agent Kit does not block compatible customer-selected host models.

- Recommended model: `sonnet`.
- Selection mode: `pinned`.
- Recommended reasoning/effort: `host default pending tier validation`.
- Generated behavior: agent frontmatter defaults to sonnet.
- Override behavior: Claude environment or per-invocation subagent override wins.
- Provider guidance: <https://code.claude.com/docs/en/sub-agents>.

## Install

Copy `ai-sast-dynamic-validation.md` into your target repository's `.claude/agents/` directory,
then restart Claude Code if needed.

## Requirements

- Claude Code with the generated subagent file installed.
- Authenticated endorctl for the read-only API lookups documented in endorctl-setup.md.

## Example

```text
@agent-ai-sast-dynamic-validation help
```

## Architecture

![AI SAST Dynamic Validation architecture](architecture.svg)

This diagram shows the generated agent contract, host responsibilities, and external systems required at runtime.

## Notes

- This agent uses read-only `endorctl agent api --agent-id ai-sast-dynamic-validation` lookups and does not require Endor MCP.
- Bash use is limited by prompt to the documented Endor lookup commands.
