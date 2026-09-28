#!/usr/bin/env python3
"""Personal asset catalog and project skill selection. Python 3.10+, stdlib only."""
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
STATES = {"available", "adopted", "deferred", "retired"}
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


def enable(root, project, harness, selected, apply=False):
    check(root)
    data, assets = catalog(root)
    project = Path(project).resolve()
    if not project.is_dir() or project == root.resolve():
        fail("Choose an existing target project outside the asset library")
    chosen = closure(assets, selected)
    if not chosen:
        fail("No assets selected")
    if any(a["kind"] != "skill" or a.get("dependency_review") != "reviewed" for a in chosen):
        fail("Enable accepts reviewed skills only")
    if any(a["state"] == "retired" for a in chosen):
        fail("Retired skills cannot be enabled")
    names = [a["name"] for a in chosen]
    if len(names) != len(set(names)):
        fail("Two selected sources use the same skill name; enable them separately")
    mapping = {a["name"]: slug(a["id"].replace("/", "-")) for a in chosen}
    if len(set(mapping.values())) != len(mapping):
        fail("Selected assets produce the same project skill name")
    sources = {s["id"]: s for s in data["sources"]}
    prepared, rows = [], []
    for asset in chosen:
        source = within(root, asset["path"])
        files, changes = transform(tree_files(source), mapping)
        metadata = files.get("agents/openai.yaml")
        if metadata is not None:
            metadata_text = metadata.decode("utf-8")
            label = re.search(r'(?m)^(\s*display_name:\s*")([^"]+)(")', metadata_text)
            prefix = asset["source"].title() + " "
            if label and not label.group(2).startswith(prefix):
                updated = metadata_text[:label.start(2)] + prefix + label.group(2) + metadata_text[label.end(2):]
                files["agents/openai.yaml"] = updated.encode("utf-8")
                changes.append({"path": "agents/openai.yaml", "display_name_prefix": prefix.strip()})
        relative = INSTALL_ROOTS[harness] + "/" + mapping[asset["name"]]
        dest = within(project, relative)
        if dest.exists():
            if not dest.is_dir() or tree_files(dest) != files:
                fail("Existing skill differs; inspect it before replacing: " + str(dest))
            state = "already-enabled"
        else:
            state = "would-enable"
        prepared.append((source, dest, files, state))
        rows.append({"asset": asset["id"], "name": mapping[asset["name"]],
                     "path": str(dest), "source_revision": sources[asset["source"]].get("revision", "workspace"),
                     "state": state, "transformations": changes})
    notices = []
    for source_id in sorted({a["source"] for a in chosen}):
        for filename in ("LICENSE", "NOTICE", "THIRD-PARTY-NOTICES.md"):
            notice = within(root, str(Path(sources[source_id]["path"]) / filename))
            if not notice.is_file():
                continue
            dest = within(project, INSTALL_ROOTS[harness] + "/" + source_id.upper() + "-" + filename)
            content = notice.read_bytes()
            if dest.exists() and (not dest.is_file() or dest.read_bytes() != content):
                fail("Existing source notice differs; inspect it before replacing: " + str(dest))
            notices.append((dest, content))
    if apply:
        written = []
        try:
            for source, dest, files, state in prepared:
                if state == "already-enabled":
                    continue
                dest.mkdir(parents=True)
                written.append((dest, files))
                for name, content in files.items():
                    target = within(dest, name)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with target.open("xb") as stream:
                        stream.write(content)
                    target.chmod((source / name).stat().st_mode & 0o777)
            for dest, content in notices:
                if not dest.exists():
                    with dest.open("xb") as stream:
                        stream.write(content)
                    written.append((dest, content))
        except Exception:
            for dest, files in reversed(written):
                if isinstance(files, bytes) and dest.is_file() and dest.read_bytes() == files:
                    dest.unlink()
                elif isinstance(files, dict) and dest.is_dir():
                    actual = tree_files(dest)
                    if all(name in files and data == files[name] for name, data in actual.items()):
                        shutil.rmtree(dest)
            raise
        for row in rows:
            if row["state"] == "would-enable":
                row["state"] = "enabled"
    return {"project": str(project), "harness": harness,
            "state": "enabled" if apply else "preview", "skills": rows,
            "notices": [str(dest) for dest, _ in notices]}


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
                          "state": "available", "source": source_id, "path": "staging/" + source_id + "/upstream/skills/" + name,
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
        "- Review explicit dependencies and adjacent-skill recommendations before enabling in a project.\n", encoding="utf-8")
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
    p = sub.add_parser("enable")
    p.add_argument("--project", required=True); p.add_argument("--harness", choices=INSTALL_ROOTS, required=True)
    p.add_argument("--asset", action="append", default=[]); p.add_argument("--profile")
    p.add_argument("--apply", action="store_true")
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
    elif args.command == "enable":
        selected = list(args.asset)
        if args.profile:
            selected += read_json(within(root, "profiles/" + slug(args.profile) + ".json"))["assets"]
        result = enable(root, args.project, args.harness, selected, args.apply)
    else:
        result = decide(root, args.decision_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssetError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print("asset-manager: " + str(error), file=sys.stderr)
        sys.exit(1)
