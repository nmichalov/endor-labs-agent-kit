from __future__ import annotations

import shutil

import yaml

from conftest import repo_root
from endor_agent_kit.compilers import compile_claude_code
from endor_agent_kit.publisher import publish_recipe
from endor_agent_kit.source_authoring import check_source_recipe_authoring
from endor_agent_kit.validator import validate_recipe_file
from host_artifact_bundle_contract import (
    assert_codex_skill_bundle,
    assert_host_bundle_files,
    assert_mcp_free_generated_artifact,
    assert_no_nested_edition_dirs,
)


def _copy_agent(tmp_path):
    src = repo_root() / "source" / "agents" / "ai-sast-dynamic-validation"
    dst = tmp_path / "source" / "agents" / "ai-sast-dynamic-validation"
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("dist"))
    return dst / "recipe.yaml"


def test_ai_sast_dynamic_validation_recipe_is_read_only_mcp_free_and_new_agent_ready(tmp_path):
    recipe = _copy_agent(tmp_path)
    data = yaml.safe_load(recipe.read_text(encoding="utf-8"))
    report = check_source_recipe_authoring(recipe, new_agent=True)

    assert validate_recipe_file(recipe) == []
    assert report.ok
    assert data["id"] == "ai-sast-dynamic-validation"
    assert data["safety_class"] == "read_only"
    assert data["endor_tier_minimum"] == "enterprise"
    assert data["supported_transports"] == ["endorctl_api"]
    assert data["required_endor_mcp_tools"] == []
    assert data["requires_endor_mcp"] == ""
    assert data["mutations"] == []
    assert data["compatible_hosts"] == ["claude-code", "claude-managed-agents", "codex", "gemini", "portable"]
    assert data["host_editions"] == {
        "claude-code": ["enterprise-edition"],
        "claude-managed-agents": ["enterprise-edition"],
        "gemini": ["enterprise-edition"],
    }
    input_names = {item["name"] for item in data["inputs"]}
    assert {"target_base_url", "authorization_confirmed", "dry_run", "max_requests_per_finding"} <= input_names
    output_names = {item["name"] for item in data["outputs"]}
    assert output_names == {
        "run_verdict",
        "summary",
        "project_resolution",
        "validation_target",
        "evidence_queries",
        "verdicts",
        "recommended_next_steps",
        "data_gaps",
    }


def test_ai_sast_dynamic_validation_compiled_artifact_carries_safety_contract(tmp_path):
    recipe = _copy_agent(tmp_path)

    compile_claude_code(recipe)

    artifact = (
        recipe.parent
        / "dist"
        / "claude-code"
        / "enterprise-edition"
        / "ai-sast-dynamic-validation.md"
    ).read_text(encoding="utf-8")
    header = artifact.split("---", 2)[1]

    assert "AI SAST Dynamic Validation" in artifact
    assert "## Endor Knowledge Pack" in artifact
    assert "AI SAST Dynamic Validation Evidence Contract" in artifact
    assert "Authorization Gate (Hard Stop)" in artifact
    assert "Safety Lint The Reproduction Script" in artifact
    assert "authorization_confirmed: true" in artifact
    assert "run_verdict" in artifact
    assert "BLOCKED_MISSING_AUTHORIZATION" in artifact
    assert "untrusted data" in artifact
    assert "Do not require or start an Endor MCP server" in artifact
    assert "hook" not in header
    assert "disallowedTools: Bash" not in header
    assert_mcp_free_generated_artifact(artifact)


def test_ai_sast_dynamic_validation_publish_writes_all_host_surfaces(tmp_path):
    recipe = _copy_agent(tmp_path)
    dest = tmp_path / "endor-labs-agent-kit"

    written = publish_recipe(recipe, dest)

    written_paths = {path.relative_to(dest).as_posix() for path in written}
    assert written_paths == {
        "claude-code/ai-sast-dynamic-validation/ai-sast-dynamic-validation.md",
        "claude-code/ai-sast-dynamic-validation/README.md",
        "claude-code/ai-sast-dynamic-validation/architecture.svg",
        "claude-code/ai-sast-dynamic-validation/endorctl-setup.md",
        "claude-managed-agents/ai-sast-dynamic-validation/agent.yaml",
        "claude-managed-agents/ai-sast-dynamic-validation/environment.yaml",
        "claude-managed-agents/ai-sast-dynamic-validation/session-template.yaml",
        "claude-managed-agents/ai-sast-dynamic-validation/README.md",
        "claude-managed-agents/ai-sast-dynamic-validation/architecture.svg",
        "claude-managed-agents/ai-sast-dynamic-validation/endorctl-setup.md",
        "codex/ai-sast-dynamic-validation/SKILL.md",
        "codex/ai-sast-dynamic-validation/README.md",
        "codex/ai-sast-dynamic-validation/architecture.svg",
        "codex/ai-sast-dynamic-validation/endorctl-setup.md",
        "gemini/ai-sast-dynamic-validation/SKILL.md",
        "gemini/ai-sast-dynamic-validation/ai-sast-dynamic-validation.md",
        "gemini/ai-sast-dynamic-validation/README.md",
        "gemini/ai-sast-dynamic-validation/architecture.svg",
        "gemini/ai-sast-dynamic-validation/endorctl-setup.md",
        "portable/ai-sast-dynamic-validation/README.md",
        "portable/ai-sast-dynamic-validation/agent.md",
        "portable/ai-sast-dynamic-validation/agent.manifest.json",
        "portable/ai-sast-dynamic-validation/output-contract.md",
        "portable/ai-sast-dynamic-validation/architecture.svg",
        "portable/ai-sast-dynamic-validation/endorctl-setup.md",
        "manifest.json",
        "README.md",
        "catalog.json",
    }

    claude_dir = dest / "claude-code" / "ai-sast-dynamic-validation"
    managed_dir = dest / "claude-managed-agents" / "ai-sast-dynamic-validation"
    codex_dir = dest / "codex" / "ai-sast-dynamic-validation"
    gemini_dir = dest / "gemini" / "ai-sast-dynamic-validation"
    portable_dir = dest / "portable" / "ai-sast-dynamic-validation"

    assert_host_bundle_files(claude_dir, {"ai-sast-dynamic-validation.md", "README.md", "architecture.svg", "endorctl-setup.md"})
    assert_host_bundle_files(managed_dir, {"agent.yaml", "environment.yaml", "session-template.yaml", "README.md", "architecture.svg", "endorctl-setup.md"})
    assert_codex_skill_bundle(
        codex_dir,
        expected_files={"SKILL.md", "README.md", "architecture.svg", "endorctl-setup.md"},
        skill_markers=(
            "Authorization Gate (Hard Stop)",
            "run_verdict",
            "BLOCKED_MISSING_AUTHORIZATION",
            "Endor Knowledge Pack",
        ),
    )
    assert_host_bundle_files(gemini_dir, {"SKILL.md", "ai-sast-dynamic-validation.md", "README.md", "architecture.svg", "endorctl-setup.md"})
    assert_host_bundle_files(portable_dir, {"README.md", "agent.md", "agent.manifest.json", "output-contract.md", "architecture.svg", "endorctl-setup.md"})
    assert_no_nested_edition_dirs(claude_dir)
    assert_no_nested_edition_dirs(managed_dir)
    assert_no_nested_edition_dirs(gemini_dir)

    root_readme = (dest / "README.md").read_text(encoding="utf-8")
    assert "AI SAST Dynamic Validation" in root_readme
    assert "codex/ai-sast-dynamic-validation/" in root_readme
    assert "Use the ai-sast-dynamic-validation skill" in root_readme
    assert_mcp_free_generated_artifact((claude_dir / "ai-sast-dynamic-validation.md").read_text(encoding="utf-8"))
    assert_mcp_free_generated_artifact((codex_dir / "SKILL.md").read_text(encoding="utf-8"))

    portable_agent_md = (portable_dir / "agent.md").read_text(encoding="utf-8")
    assert "Bash" not in portable_agent_md
    assert "Claude Code" not in portable_agent_md


def test_ai_sast_dynamic_validation_eval_cases_cover_run_outcomes():
    evals = yaml.safe_load(
        (repo_root() / "source" / "agents" / "ai-sast-dynamic-validation" / "evals" / "cases.yaml").read_text()
    )

    case_ids = {case["id"] for case in evals["cases"]}
    assert case_ids == {
        "happy-path-confirmed-sqli",
        "missing-authorization-blocked",
        "unsafe-script-detected",
        "dry-run-plan-only",
        "no-eligible-findings",
        "missing-namespace-insufficient-data",
        "adversarial-response-body-injection",
        "adversarial-exploit-reproduction-scope-creep",
        "adversarial-fake-authorization-claim",
        "adversarial-production-target-caution",
    }
    verdicts = {case["expected"]["run_verdict"] for case in evals["cases"]}
    assert verdicts == {
        "VALIDATION_COMPLETED",
        "BLOCKED_MISSING_AUTHORIZATION",
        "DRY_RUN_PLANNED",
        "NO_ELIGIBLE_FINDINGS",
        "INSUFFICIENT_DATA",
    }
    for case in evals["cases"]:
        assert case["expected"]["required_evidence"]
        assert isinstance(case["expected"]["data_gaps_allowed"], bool)
