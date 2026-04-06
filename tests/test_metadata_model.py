#!/usr/bin/env python3
import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import render_workflow_tables as renderer


PLACEHOLDER_RE = re.compile(r"\{([a-z0-9_-]+)\}")
MARKER_RE = re.compile(r"<!-- GENERATED:([^:]+):(start|end) -->")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"OK:   {message}")


def load_json(relative_path: str):
    with (ROOT / relative_path).open() as fh:
        return json.load(fh)


def assert_equal(actual, expected, message: str) -> None:
    if actual != expected:
        fail(f"{message}: expected {expected!r}, got {actual!r}")
    ok(message)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        fail(message)
    ok(message)


def validate_workflows():
    workflows = load_json("core/metadata/workflows.json")["workflows"]
    providers = load_json("core/metadata/providers.json")["providers"]
    provider_ids = tuple(provider["id"] for provider in providers)
    workflow_ids = [workflow["id"] for workflow in workflows]

    assert_equal(len(workflow_ids), len(set(workflow_ids)), "workflow ids are unique")
    assert_true(workflow_ids, "workflow metadata is not empty")

    for workflow in workflows:
        assert_equal(
            tuple(workflow["providers"]),
            provider_ids,
            f"{workflow['id']} provider order matches provider metadata",
        )
        for provider_id, command in workflow["providers"].items():
            assert_true(bool(command.strip()), f"{workflow['id']} has a {provider_id} command")

    for provider_id in provider_ids:
        commands = [workflow["providers"][provider_id] for workflow in workflows]
        assert_equal(
            len(commands),
            len(set(commands)),
            f"{provider_id} commands are unique across workflows",
        )

    return workflows, workflow_ids, provider_ids


def validate_help(workflow_ids):
    help_meta = load_json("core/metadata/help.json")

    assert_true(bool(help_meta["quick_start"].strip()), "help quick start is present")

    command_detail_ids = set(help_meta["command_details"])
    assert_equal(command_detail_ids, set(workflow_ids), "help command details cover every workflow")

    referenced_ids = set()
    for scenario in help_meta["scenario_routes"]:
        assert_true(bool(scenario["goal"].strip()), f"scenario goal is present for {scenario['workflow_ids']}")
        assert_true(bool(scenario["workflow_ids"]), f"{scenario['goal']} includes at least one workflow")
        for workflow_id in scenario["workflow_ids"]:
            if workflow_id not in workflow_ids:
                fail(f"help scenario {scenario['goal']!r} references unknown workflow {workflow_id!r}")
            referenced_ids.add(workflow_id)
    assert_equal(referenced_ids, set(workflow_ids) - {"help"}, "help scenarios cover all non-help workflows")

    for workflow_id, detail in help_meta["command_details"].items():
        for key in ("when_to_use", "inputs", "produces", "next_step_template"):
            assert_true(bool(detail[key].strip()), f"help detail {workflow_id}.{key} is present")
        for placeholder in PLACEHOLDER_RE.findall(detail["next_step_template"]):
            if placeholder not in workflow_ids:
                fail(f"help detail {workflow_id!r} references unknown workflow placeholder {placeholder!r}")
    ok("help next-step placeholders only reference known workflows")


def validate_adapter_docs(workflows):
    adapter_docs = load_json("core/metadata/adapter-docs.json")["workflows"]
    expected_ids = [workflow["id"] for workflow in workflows if workflow["kind"] == "workflow"]

    assert_equal(
        tuple(adapter_docs),
        tuple(expected_ids),
        "adapter doc metadata covers every non-utility workflow in workflow order",
    )
    for workflow_id, entry in adapter_docs.items():
        assert_true(bool(entry["title"].strip()), f"adapter doc title present for {workflow_id}")
        assert_true(
            bool(entry["copilot_description"].strip()),
            f"adapter doc Copilot description present for {workflow_id}",
        )


def validate_routing(workflow_ids):
    routing_meta = load_json("core/metadata/routing.json")
    route_ids = [route["workflow_id"] for route in routing_meta["routes"]]

    assert_equal(route_ids, workflow_ids, "routing order matches workflow order")
    assert_equal(len(route_ids), len(set(route_ids)), "routing workflow ids are unique")

    for route in routing_meta["routes"]:
        for key in ("claude_signal", "copilot_intent", "codex_intent"):
            assert_true(bool(route[key].strip()), f"routing text present for {route['workflow_id']}.{key}")


def validate_principles(provider_ids):
    principles_meta = load_json("core/metadata/principles.json")

    assert_true(bool(principles_meta["claude_quick_path"].strip()), "Claude quick path is present")
    for flow_name, flow_text in principles_meta["codex_default_flow"].items():
        assert_true(bool(flow_text.strip()), f"Codex {flow_name} flow is present")

    assert_true(bool(principles_meta["principles"]), "principles list is not empty")
    for index, entry in enumerate(principles_meta["principles"], start=1):
        assert_equal(
            tuple(entry),
            provider_ids,
            f"principle {index} provider order matches provider metadata",
        )
        for provider_id in provider_ids:
            assert_true(bool(entry[provider_id].strip()), f"principle {index} has {provider_id} text")


def validate_status():
    status_meta = load_json("core/metadata/status.json")

    assert_true(bool(status_meta["layers"]), "status layers are present")
    for layer in status_meta["layers"]:
        assert_true(bool(layer["title"].strip()), f"status layer title is present: {layer['title']}")
        assert_true(bool(layer["checks"]), f"status layer has checks: {layer['title']}")
        for check in layer["checks"]:
            for key in ("check", "claude_how", "copilot_how"):
                assert_true(bool(check[key].strip()), f"status check has {key}: {layer['title']}")

    assert_true(bool(status_meta["output_format"]), "status output format is present")
    assert_true(bool(status_meta["closing_note"].strip()), "status closing note is present")


def validate_claude_skill(workflows):
    claude_skill_meta = load_json("core/metadata/claude-skill.json")
    workflow_by_id = {workflow["id"]: workflow for workflow in workflows}
    overview_ids = [item["workflow_id"] for item in claude_skill_meta["workflow_overview"]]
    core_workflow_ids = [workflow["id"] for workflow in workflows if workflow["kind"] == "workflow"]

    assert_equal(overview_ids, core_workflow_ids, "Claude skill overview covers every non-utility workflow")
    assert_equal(len(overview_ids), len(set(overview_ids)), "Claude skill overview ids are unique")

    for item in claude_skill_meta["workflow_overview"]:
        assert_true(bool(item["description"].strip()), f"Claude overview description present for {item['workflow_id']}")

    transitions_text = "\n".join(
        f"{item['just_finished']} {item['suggest_next']}" for item in claude_skill_meta["transitions"]
    )
    assert_true(bool(claude_skill_meta["transitions"]), "Claude transitions are present")
    for workflow_id in core_workflow_ids:
        label = workflow_by_id[workflow_id]["label"]
        assert_true(label in transitions_text, f"Claude transitions mention {label}")


def validate_generated_markers():
    expected_targets = renderer.target_paths()
    assert_true(bool(expected_targets), "renderer target map is not empty")

    for path, expected_markers in expected_targets.items():
        text = path.read_text()
        matches = MARKER_RE.findall(text)
        actual_markers = tuple(marker for marker, kind in matches if kind == "start")
        end_markers = tuple(marker for marker, kind in matches if kind == "end")

        assert_equal(
            set(actual_markers),
            set(expected_markers),
            f"{path.relative_to(ROOT)} has expected generated start markers",
        )
        assert_equal(
            set(end_markers),
            set(expected_markers),
            f"{path.relative_to(ROOT)} has expected generated end markers",
        )
        assert_equal(
            len(actual_markers),
            len(expected_markers),
            f"{path.relative_to(ROOT)} has the expected number of generated start markers",
        )
        assert_equal(
            len(end_markers),
            len(expected_markers),
            f"{path.relative_to(ROOT)} has the expected number of generated end markers",
        )
        for marker in expected_markers:
            assert_equal(
                text.count(f"<!-- GENERATED:{marker}:start -->"),
                1,
                f"{path.relative_to(ROOT)} has one start marker for {marker}",
            )
            assert_equal(
                text.count(f"<!-- GENERATED:{marker}:end -->"),
                1,
                f"{path.relative_to(ROOT)} has one end marker for {marker}",
            )


def main():
    workflows, workflow_ids, provider_ids = validate_workflows()
    validate_adapter_docs(workflows)
    validate_help(workflow_ids)
    validate_routing(workflow_ids)
    validate_principles(provider_ids)
    validate_status()
    validate_claude_skill(workflows)
    validate_generated_markers()


if __name__ == "__main__":
    main()
