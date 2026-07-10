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

This is the Claude Managed Agents generated agent for `ai-sast-dynamic-validation`.

| Reader | First move |
| --- | --- |
| Human operator | Update generated YAML placeholders, then create the managed agent and environment. Then use the example prompt below: Help me use this Endor Labs agent. |
| Agent installer | Copy the generated files exactly, including the generated prompt or skill file, `endorctl-setup.md`, `architecture.svg`. Do not summarize or rewrite the generated prompt. |
| Maintainer | Change `source/agents/ai-sast-dynamic-validation/recipe.yaml`, `instructions.md`, evals, action contracts, or `architecture.svg`, then regenerate the catalog. Do not hand-edit generated copies. |

## Install

Update placeholders in `agent.yaml`, `environment.yaml`, and
`session-template.yaml`, then create the agent and environment in
Claude Managed Agents.

```bash
ant beta:agents create < agent.yaml
ant beta:environments create < environment.yaml
```

Use `session-template.yaml` as the starting point for session creation after
you have the created agent ID, environment ID, and any required vault IDs.

## Requirements

- Anthropic Console or `ant` CLI access to Claude Managed Agents.
- An environment that can install and authenticate endorctl for the read-only API lookups documented in endorctl-setup.md.

## Example User Message

```text
Help me use this Endor Labs agent.
```

## Architecture

![AI SAST Dynamic Validation architecture](architecture.svg)

This diagram shows the generated agent contract, host responsibilities, and external systems required at runtime.

## Notes

- This agent uses read-only endorctl api lookups and does not require Endor MCP.
- The generated `agent.yaml` enables only the Managed Agents Bash tool from the pre-built toolset, with confirmation required.
- Bash use remains limited by prompt to the documented Endor lookup commands.
