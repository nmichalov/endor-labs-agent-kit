# AI SAST Dynamic Validation Gemini CLI Bundle

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

This is the Gemini CLI generated skill and subagent bundle for `ai-sast-dynamic-validation`.

| Reader | First move |
| --- | --- |
| Human operator | Prefer the generated Gemini extension under `plugins/gemini/endor-labs-agent-kit`, then restart Gemini CLI. Then use the example prompt below: Use @ai-sast-dynamic-validation to help with this Endor Labs workflow. |
| Agent installer | Copy the generated files exactly, including the generated prompt or skill file, `endorctl-setup.md`, `architecture.svg`. Do not summarize or rewrite the generated prompt. |
| Maintainer | Change `source/agents/ai-sast-dynamic-validation/recipe.yaml`, `instructions.md`, evals, action contracts, or `architecture.svg`, then regenerate the catalog. Do not hand-edit generated copies. |

## Install Through The Generated Extension

Prefer the generated extension package under `plugins/gemini/endor-labs-agent-kit`.

```bash
gemini extensions install /path/to/endor-labs-agent-kit/plugins/gemini/endor-labs-agent-kit
```

Restart Gemini CLI after installing or updating the extension.

## Manual Fallback

Copy this bundle into a custom Gemini extension or install the skill and
subagent manually under your Gemini configuration.

## Requirements

- Gemini CLI with access to the current workspace.
- The Endor access path declared by the recipe.
- No mutating repository, source-provider, or Endor writes for this workflow.

## Example

```text
Use @ai-sast-dynamic-validation to help with this Endor Labs workflow.
```

## Architecture

![AI SAST Dynamic Validation architecture](architecture.svg)

This diagram shows the generated agent contract, host responsibilities, and external systems required at runtime.

## Notes

- `SKILL.md` and the subagent markdown are generated from the source recipe and should not be hand-edited in installed copies.
- The plugin package installs the skill under `skills/<agent>/` and the subagent under `agents/<agent>.md`.
- Keep host-specific approval gates intact: local edits, branch pushes, PR/MR creation, PR/MR comments, and Endor policy writes are separate decisions.
- This read-only workflow must report unavailable signals in `data_gaps`.
