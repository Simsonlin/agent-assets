#!/usr/bin/env python3
"""Personal asset catalog and reversible skill trials. Python 3.10+, stdlib only."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
STATES = {"staged", "testing", "adopted", "deferred", "retired"}
KINDS = {"skill", "standard", "workflow", "template", "tool"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
INSTALL_ROOTS = {"codex": ".agents/skills", "dsh": ".dsh/skills"}


class AssetError(Exception):
    pass


def fail(message):
    raise AssetError(message)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex[:8])
    try:
        temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def slug(value):
    if not SLUG.fullmatch(value) or len(value) > 80:
        fail("Invalid identifier: " + value)
    return value


def within(root, relative):
    root = Path(root).resolve()
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts or not rel.parts:
        fail("Expected a relative path inside " + str(root))
    target = root / rel
    for part in [target, *target.parents]:
        if part == root:
            break
        if part.is_symlink():
            fail("Symlink requires manual review: " + str(part))
    if not target.resolve().is_relative_to(root):
        fail("Path escapes root: " + str(target))
    return target


def tree_files(root):
    root = Path(root)
    if root.is_symlink():
        fail("Symlink source is unsupported: " + str(root))
    result = {}
    for item in sorted(root.rglob("*")):
        if item.is_symlink():
            fail("Symlink resource is unsupported: " + str(item))
        if item.is_file():
            result[item.relative_to(root).as_posix()] = item.read_bytes()
        elif not item.is_dir():
            fail("Unsupported resource: " + str(item))
    return result


def hashes(files):
    return {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}


def skill_name(path):
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---" not in text[4:]:
        fail("Missing frontmatter: " + str(path))
    front = text.split("---", 2)[1]
    match = re.search(r"^name:\s*[\"']?([a-z0-9-]+)[\"']?\s*$", front, re.M)
    if not match or not re.search(r"^description:\s*\S", front, re.M):
        fail("Missing name/description: " + str(path))
    return slug(match.group(1))


def catalog(root):
    data = read_json(root / "catalog.json")
    if data.get("schema_version") != 1:
        fail("Unsupported catalog schema")
    ids = [a["id"] for a in data["assets"]]
    if len(ids) != len(set(ids)):
        fail("Duplicate asset IDs")
    return data, {a["id"]: a for a in data["assets"]}


def closure(assets, selected):
    ordered, visiting, seen = [], set(), set()
    def visit(key):
        if key in visiting:
            fail("Dependency cycle at " + key)
        if key in seen:
            return
        if key not in assets:
            fail("Unknown asset/dependency: " + key)
        visiting.add(key)
        for dep in assets[key].get("dependencies", []):
            visit(dep)
        visiting.remove(key)
        seen.add(key)
        ordered.append(assets[key])
    for key in selected:
        visit(key)
    return ordered


def check(root):
    data, assets = catalog(root)
    source_ids = [s["id"] for s in data["sources"]]
    if len(source_ids) != len(set(source_ids)):
        fail("Duplicate source IDs")
    for a in assets.values():
        if a["state"] not in STATES or a["kind"] not in KINDS:
            fail("Invalid state/kind: " + a["id"])
        if a["source"] not in source_ids:
            fail("Unknown source: " + a["id"])
        path = within(root, a["path"])
        if not path.is_dir():
            fail("Missing asset directory: " + str(path))
        if a["kind"] == "skill" and skill_name(path / "SKILL.md") != a["name"]:
            fail("Name differs from registered source: " + a["id"])
        if not within(path, a["entrypoint"]).is_file():
            fail("Missing entrypoint: " + a["id"])
        closure(assets, [a["id"]])
        if a["state"] in {"adopted", "deferred", "retired"}:
            if not a.get("decision") or not within(root, a["decision"]).is_file():
                fail("State requires a decision record: " + a["id"])
    for source in data["sources"]:
        if source.get("checksums"):
            base = within(root, source["path"])
            manifest = read_json(within(root, source["checksums"]))
            actual = hashes(tree_files(base))
            if actual != manifest:
                fail("Source differs from fixed snapshot: " + source["id"])
    profile_count = 0
    for path in (root / "profiles").glob("*.json"):
        profile = read_json(path)
        if profile["id"] != path.stem:
            fail("Profile ID differs from filename: " + str(path))
        if not profile.get("assets"):
            fail("Empty profile: " + str(path))
        closure(assets, profile["assets"])
        profile_count += 1
    return {"valid": True, "assets": len(assets), "profiles": profile_count, "sources": len(source_ids)}


def alias_name(asset, run_id):
    prefix = "trial-" + asset["id"].replace("/", "-")
    return prefix[:55].rstrip("-") + "-" + hashlib.sha256(run_id.encode()).hexdigest()[:6]


def transform(files, mapping):
    """Rename selected skill identifiers, leaving URLs and behavior intact."""
    pattern = re.compile(r"(?<![\w-])(" + "|".join(re.escape(n) for n in sorted(mapping, key=len, reverse=True)) + r")(?![\w-])")
    output, changes = {}, []
    for name, content in files.items():
        count = 0
        if Path(name).suffix in {".md", ".yaml", ".yml", ".json"}:
            text = content.decode("utf-8")
            chunks = re.split(r"(https?://[^\s<>\"\)]+)", text)
            for i in range(0, len(chunks), 2):
                chunks[i], n = pattern.subn(lambda m: mapping[m.group(1)], chunks[i])
                count += n
            content = "".join(chunks).encode("utf-8")
        output[name] = content
        if count:
            changes.append({"path": name, "identifier_replacements": count})
    return output, changes


def trial_dir(root, run_id):
    return root / ".local" / "trials" / slug(run_id)


def load_trial(root, run_id):
    folder = trial_dir(root, run_id)
    manifest = read_json(folder / "manifest.json")
    if manifest.get("id") != run_id or manifest.get("schema_version") != 1:
        fail("Invalid trial manifest")
    for bundle in manifest["bundles"]:
        expected = INSTALL_ROOTS[manifest["harness"]] + "/" + slug(bundle["alias"])
        if bundle["install_relative"] != expected or not bundle["alias"].startswith("trial-"):
            fail("Unexpected managed installation path")
    return folder, manifest


def prepare(root, project, harness, selected, task, apply=False, run_id=None):
    check(root)
    data, assets = catalog(root)
    project = Path(project).resolve()
    if not project.is_dir():
        fail("Project must already exist: " + str(project))
    if project == root.resolve():
        fail("Choose a target project or disposable fixture, not the asset library")
    run_id = slug(run_id or (dt.datetime.now().strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:10]))
    folder = trial_dir(root, run_id)
    if folder.exists():
        fail("Run already exists; inspect or clean it first: " + run_id)
    chosen = closure(assets, selected)
    if not chosen:
        fail("No assets selected")
    if any(a.get("dependency_review") != "reviewed" for a in chosen):
        fail("Review the selected assets dependencies before preparing")
    if any(a["kind"] != "skill" for a in chosen):
        fail("prepare installs skills only; follow the registered adoption guide for standards and other assets")
    if any(a["state"] in {"retired", "deferred"} for a in chosen):
        fail("Deferred/retired assets need an explicit lifecycle decision before another trial")
    names = [a["name"] for a in chosen]
    if len(names) != len(set(names)):
        fail("Two selected sources use the same skill name; split them into separate trials")
    mapping = {a["name"]: alias_name(a, run_id) for a in chosen}
    manifest = {"schema_version": 1, "id": run_id, "created_at": now(), "project": str(project),
                "harness": harness, "task": task, "state": "preview", "requested_assets": selected,
                "name_mapping": mapping, "bundles": [], "created_parents": []}
    prepared = []
    source_versions = {s["id"]: s.get("revision", "workspace") for s in data["sources"]}
    for a in chosen:
        original = tree_files(within(root, a["path"]))
        files, changes = transform(original, mapping)
        relative = INSTALL_ROOTS[harness] + "/" + mapping[a["name"]]
        dest = within(project, relative)
        if dest.exists():
            fail("Destination already exists: " + str(dest))
        bundle = {"asset": a["id"], "source_path": a["path"], "source_revision": source_versions[a["source"]],
                  "alias": mapping[a["name"]], "install_relative": relative,
                  "source_hashes": hashes(original), "installed_hashes": hashes(files), "transformations": changes,
                  "written": False}
        manifest["bundles"].append(bundle)
        prepared.append((dest, files))
    if not apply:
        return manifest
    folder.mkdir(parents=True, exist_ok=False)
    manifest["state"] = "preparing"
    write_json(folder / "manifest.json", manifest)
    try:
        for bundle, (dest, files) in zip(manifest["bundles"], prepared):
            current = project
            for part in Path(bundle["install_relative"]).parts[:-1]:
                current = current / part
                if not current.exists():
                    current.mkdir()
                    manifest["created_parents"].append(current.relative_to(project).as_posix())
                    write_json(folder / "manifest.json", manifest)
                if current.is_symlink() or not current.is_dir():
                    fail("Unsafe installation parent: " + str(current))
            dest.mkdir(exist_ok=False)
            bundle["written"] = True
            write_json(folder / "manifest.json", manifest)
            for name, content in files.items():
                target = within(dest, name)
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as stream:
                    stream.write(content)
                source = within(root, bundle["source_path"]) / name
                target.chmod(source.stat().st_mode & 0o777)
        manifest["state"] = "prepared"
        write_json(folder / "manifest.json", manifest)
        lines = ["# Prepared skill trial", "", "Task: " + task, "", "Harness: " + harness,
                 "", "Use the following exact trial copies; source files and user-level skills are unchanged."]
        for b in manifest["bundles"]:
            gesture = ("$" if harness == "codex" else "/") + b["alias"]
            lines += ["", "- " + b["asset"] + ": " + gesture,
                      "  - Entry: " + str(project / b["install_relative"] / "SKILL.md")]
        lines += ["", "Verify the exact loaded path and observable result. Preserve the skill invocation policy.",
                  "If the current session cannot discover it, start a fresh target-project session and use this prompt.",
                  "Do not count copying or reading source as proof of native invocation.",
                  "Record which assets were actually used, the evidence, and environment limits before cleanup."]
        (folder / "PROMPT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    except Exception:
        manifest["state"] = "prepare-failed"
        write_json(folder / "manifest.json", manifest)
        raise
    return {"id": run_id, "state": manifest["state"], "prompt": str(folder / "PROMPT.md"),
            "manifest": str(folder / "manifest.json"), "assets": mapping}


def verify(root, run_id):
    _, m = load_trial(root, run_id)
    rows = []
    for b in m["bundles"]:
        dest = within(Path(m["project"]), b["install_relative"])
        actual = hashes(tree_files(dest)) if dest.exists() else None
        rows.append({"asset": b["asset"], "alias": b["alias"], "path": str(dest / "SKILL.md"),
                     "files_match": actual == b["installed_hashes"]})
    return {"id": run_id, "bundles": rows, "native_discovery": "not_proved_by_file_check",
            "native_invocation": "not_proved_by_file_check"}


def cleanup(root, run_id):
    folder, m = load_trial(root, run_id)
    project, removed, protected = Path(m["project"]), [], []
    for b in m["bundles"]:
        if not b["written"]:
            continue
        try:
            dest = within(project, b["install_relative"])
            if not dest.exists():
                continue
            actual = hashes(tree_files(dest))
            if actual != b["installed_hashes"]:
                protected.append({"asset": b["asset"], "path": str(dest), "reason": "Files were changed, added, removed, or incompletely installed; inspect manually"})
                continue
            shutil.rmtree(dest)
            removed.append(b["asset"])
        except AssetError as error:
            protected.append({"asset": b["asset"], "reason": str(error)})
    for relative in sorted(set(m["created_parents"]), key=lambda x: len(Path(x).parts), reverse=True):
        if relative not in {".agents", ".agents/skills", ".dsh", ".dsh/skills"}:
            fail("Unexpected managed parent")
        try:
            within(project, relative).rmdir()
        except (OSError, AssetError):
            pass
    m["state"] = "cleanup-needs-review" if protected else "cleaned"
    m["cleanup"] = {"at": now(), "removed": removed, "protected": protected}
    write_json(folder / "manifest.json", m)
    return {"id": run_id, "state": m["state"], **m["cleanup"]}


def record(root, run_id, used, outcome, note, evidence, discovery, invocation):
    _, m = load_trial(root, run_id)
    bundles = {b["asset"]: b for b in m["bundles"]}
    if not used or any(a not in bundles for a in used):
        fail("Specify the installed assets actually used or attempted")
    for ref in evidence:
        if not within(root, ref).is_file():
            fail("Evidence must be an existing file in the asset repository: " + ref)
    if outcome == "useful" and (not evidence or invocation != "verified"):
        fail("A useful native trial needs invocation evidence; use inconclusive for preparation-only checks")
    path = root / "trials" / run_id / "record.json"
    if path.exists():
        fail("Record exists; preserve the original and add a follow-up note instead")
    result = {"schema_version": 1, "id": run_id, "recorded_at": now(), "task": m["task"],
              "harness": m["harness"], "project_name": Path(m["project"]).name,
              "outcome": outcome, "note": note, "evidence": evidence,
              "native_discovery": discovery, "native_invocation": invocation,
              "assets": [{k: bundles[a][k] for k in ("asset", "source_revision", "source_hashes", "alias", "transformations")} for a in used],
              "adoption": "not_decided"}
    write_json(path, result)
    data, assets = catalog(root)
    for key in used:
        if assets[key]["state"] == "staged":
            assets[key]["state"] = "testing"
    write_json(root / "catalog.json", data)
    return {"record": str(path), "outcome": outcome, "adoption": "not_decided"}


def decide(root, decision_file):
    decision = read_json(within(root, decision_file))
    if decision.get("decided_by") != "user" or not decision.get("user_statement") or not decision.get("conversation_reference"):
        fail("Decision requires the user's actual statement and conversation reference")
    if decision.get("state") not in STATES or not decision.get("assets") or not decision.get("reason"):
        fail("Incomplete decision")
    data, assets = catalog(root)
    for key in decision["assets"]:
        if key not in assets:
            fail("Unknown asset: " + key)
    for key in decision["assets"]:
        assets[key]["state"] = decision["state"]
        assets[key]["decision"] = decision_file
    write_json(root / "catalog.json", data)
    return {"assets": decision["assets"], "state": decision["state"], "decision": decision_file}


def intake(root, checkout, source_id, selected, domains=None):
    slug(source_id)
    checkout = Path(checkout).resolve()
    def git(*args):
        return subprocess.check_output(["git", "-C", str(checkout), *args], text=True).strip()
    if git("status", "--porcelain"):
        fail("Intake requires an unchanged source checkout")
    revision, url = git("rev-parse", "HEAD"), git("remote", "get-url", "origin")
    if "@" in url and url.startswith("https://"):
        fail("Remove credentials from the source URL before intake")
    data, assets = catalog(root)
    existing = next((s for s in data["sources"] if s["id"] == source_id), None)
    if existing and (existing.get("revision") != revision or existing.get("url") != url):
        fail("Use a new source ID for a different version or origin")
    if existing:
        check(root)
    target = within(root, "staging/" + source_id)
    if target.exists() and not existing:
        fail("Staging destination exists without registration")
    license_files = [name for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "THIRD-PARTY-NOTICES.md") if (checkout / name).is_file()]
    if not any(name != "THIRD-PARTY-NOTICES.md" for name in license_files):
        fail("No license file found; review this source before importing")
    additions, copies = [], {}
    for name in selected:
        slug(name)
        if source_id + "/" + name in assets:
            continue
        folder = within(checkout, "skills/" + name)
        registered_name = skill_name(folder / "SKILL.md")
        if registered_name != name:
            fail("Skill folder/name mismatch: " + name)
        files = tree_files(folder)
        copies.update({"skills/" + name + "/" + p: value for p, value in files.items()})
        additions.append({"id": source_id + "/" + name, "name": name, "kind": "skill", "domains": domains or ["general"],
                          "state": "staged", "source": source_id, "path": "staging/" + source_id + "/upstream/skills/" + name,
                          "entrypoint": "SKILL.md", "dependencies": [], "dependency_review": "pending"})
    if len(selected) != len(set(selected)):
        fail("Duplicate selection")
    for name in license_files:
        copies[name] = (checkout / name).read_bytes()
    target.mkdir(parents=True, exist_ok=bool(existing))
    for name, content in copies.items():
        dest = within(target / "upstream", name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            if dest.read_bytes() != content:
                fail("Existing source file differs: " + str(dest))
        else:
            with dest.open("xb") as stream:
                stream.write(content)
            dest.chmod((checkout / name).stat().st_mode & 0o777)
    write_json(target / "SHA256SUMS.json", hashes(tree_files(target / "upstream")))
    source = {"id": source_id, "type": "external", "url": url, "revision": revision,
              "path": "staging/" + source_id + "/upstream", "checksums": "staging/" + source_id + "/SHA256SUMS.json"}
    if not existing:
        data["sources"].append(source)
    data["assets"].extend(additions)
    write_json(root / "catalog.json", data)
    (target / "SOURCE.md").write_text("# Source snapshot\n\n- URL: " + url + "\n- Commit: " + revision +
        "\n- Retrieved: " + now() + "\n- Selected complete skills: " + ", ".join(a["name"] for a in data["assets"] if a["source"] == source_id) +
        "\n- Source files are unchanged. Licenses and notices are retained.\n"
        "- Review explicit dependencies and adjacent-skill recommendations before preparing a trial.\n", encoding="utf-8")
    return {"source": source, "assets": [a["id"] for a in additions], "next": "Review dependencies and update dependency_review to reviewed"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("list")
    p.add_argument("--state", choices=sorted(STATES))
    p.add_argument("--domain")
    p = sub.add_parser("show"); p.add_argument("asset")
    sub.add_parser("check")
    p = sub.add_parser("intake")
    p.add_argument("--checkout", required=True); p.add_argument("--source", required=True)
    p.add_argument("--skill", action="append", required=True)
    p.add_argument("--domain", action="append")
    p = sub.add_parser("prepare")
    p.add_argument("--project", required=True); p.add_argument("--harness", choices=INSTALL_ROOTS, required=True)
    p.add_argument("--asset", action="append", default=[]); p.add_argument("--profile")
    p.add_argument("--task", required=True); p.add_argument("--run"); p.add_argument("--apply", action="store_true")
    for name in ("verify", "cleanup"):
        p = sub.add_parser(name); p.add_argument("run")
    p = sub.add_parser("record")
    p.add_argument("run"); p.add_argument("--used", action="append", required=True)
    p.add_argument("--outcome", choices=["useful", "limited", "inconclusive", "blocked"], required=True)
    p.add_argument("--note", required=True); p.add_argument("--evidence", action="append", default=[])
    p.add_argument("--discovery", choices=["verified", "unverified"], default="unverified")
    p.add_argument("--invocation", choices=["verified", "unverified"], default="unverified")
    p = sub.add_parser("decide"); p.add_argument("decision_file")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command == "check":
        result = check(root)
    elif args.command in {"list", "show"}:
        _, assets = catalog(root)
        if args.command == "show":
            if args.asset not in assets: fail("Unknown asset: " + args.asset)
            result = assets[args.asset]
        else:
            result = [a for a in assets.values() if (not args.state or a["state"] == args.state) and
                      (not args.domain or args.domain in a["domains"])]
    elif args.command == "intake":
        result = intake(root, args.checkout, args.source, args.skill, args.domain)
    elif args.command == "prepare":
        selected = list(args.asset)
        if args.profile:
            selected += read_json(within(root, "profiles/" + slug(args.profile) + ".json"))["assets"]
        _, assets = catalog(root)
        for a in closure(assets, selected):
            if a.get("dependency_review") != "reviewed":
                fail("Review dependencies before preparing: " + a["id"])
        result = prepare(root, args.project, args.harness, selected, args.task, args.apply, args.run)
    elif args.command == "verify":
        result = verify(root, args.run)
    elif args.command == "cleanup":
        result = cleanup(root, args.run)
    elif args.command == "record":
        result = record(root, args.run, args.used, args.outcome, args.note, args.evidence, args.discovery, args.invocation)
    else:
        result = decide(root, args.decision_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.command == "cleanup" and result["state"] != "cleaned":
        return 2
    if args.command == "verify" and not all(b["files_match"] for b in result["bundles"]):
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssetError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print("asset-manager: " + str(error), file=sys.stderr)
        sys.exit(1)
