import importlib.util
from pathlib import Path
import tempfile
import subprocess
import unittest

SPEC = importlib.util.spec_from_file_location("assets", Path(__file__).resolve().parents[1] / "scripts" / "assets.py")
a = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(a)


class TrialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "library"
        self.project = self.base / "project"
        self.root.mkdir(); self.project.mkdir()
        self.catalog = {"schema_version": 1, "sources": [{"id": "vendor", "revision": "abc123"}], "assets": []}
        self.add_skill("helper")
        self.add_skill("main", ["vendor/helper"])
        a.write_json(self.root / "catalog.json", self.catalog)

    def add_skill(self, name, dependencies=None):
        path = self.root / "source" / name
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text("---\nname: " + name + "\ndescription: Test a skill.\ndisable-model-invocation: true\n---\nUse `helper` and $helper. Read [helper](../helper/SKILL.md).\nSource: https://example.com/skills/helper/SKILL.md\n", encoding="utf-8")
        (path / "references").mkdir()
        (path / "references" / "data.bin").write_bytes(b"\x00\xff\x01")
        (path / "agents").mkdir()
        (path / "agents" / "openai.yaml").write_text('policy:\n  allow_implicit_invocation: false\ninterface:\n  default_prompt: "$helper"\n')
        self.catalog["assets"].append({"id": "vendor/" + name, "name": name, "source": "vendor", "kind": "skill",
             "state": "staged", "domains": ["general"], "path": "source/" + name, "entrypoint": "SKILL.md",
             "dependencies": dependencies or [], "dependency_review": "reviewed"})

    def prepare(self, harness="codex", run="one", apply=True):
        return a.prepare(self.root, self.project, harness, ["vendor/main"], "Inspect a task", apply, run)

    def test_preview_has_no_side_effects(self):
        before = a.tree_files(self.root)
        plan = self.prepare(apply=False)
        self.assertEqual(plan["state"], "preview")
        self.assertEqual(a.tree_files(self.root), before)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_dependency_namespace_resources_policy_and_cleanup(self):
        original = a.tree_files(self.root / "source")
        user_skill = self.project / ".agents/skills/helper/SKILL.md"
        user_skill.parent.mkdir(parents=True)
        user_skill.write_text("personal version")
        baseline = a.tree_files(self.project)
        self.prepare()
        _, m = a.load_trial(self.root, "one")
        self.assertEqual(len(m["bundles"]), 2)
        for b in m["bundles"]:
            folder = self.project / b["install_relative"]
            self.assertEqual(a.skill_name(folder / "SKILL.md"), b["alias"])
            body = (folder / "SKILL.md").read_text()
            self.assertIn("$" + m["name_mapping"]["helper"], body)
            self.assertIn("https://example.com/skills/helper/SKILL.md", body)
            self.assertIn("disable-model-invocation: true", body)
            self.assertIn("allow_implicit_invocation: false", (folder / "agents/openai.yaml").read_text())
            self.assertEqual((folder / "references/data.bin").read_bytes(), b"\x00\xff\x01")
        self.assertTrue(all(b["files_match"] for b in a.verify(self.root, "one")["bundles"]))
        self.assertEqual(a.cleanup(self.root, "one")["state"], "cleaned")
        self.assertEqual(a.tree_files(self.project), baseline)
        self.assertEqual(a.tree_files(self.root / "source"), original)
        self.assertEqual(a.cleanup(self.root, "one")["state"], "cleaned")

    def test_dsh_target_and_empty_parent_cleanup(self):
        self.prepare(harness="dsh")
        self.assertTrue((self.project / ".dsh/skills").is_dir())
        a.cleanup(self.root, "one")
        self.assertEqual(list(self.project.iterdir()), [])

    def test_cleanup_protects_user_changes_and_additions(self):
        self.prepare()
        _, m = a.load_trial(self.root, "one")
        b = m["bundles"][0]
        folder = self.project / b["install_relative"]
        original = (folder / "SKILL.md").read_bytes()
        (folder / "SKILL.md").write_text("user edit")
        extra = folder / "user-note.txt"
        extra.write_text("keep me")
        result = a.cleanup(self.root, "one")
        self.assertEqual(result["state"], "cleanup-needs-review")
        self.assertEqual(extra.read_text(), "keep me")
        self.assertEqual((folder / "SKILL.md").read_text(), "user edit")
        extra.unlink(); (folder / "SKILL.md").write_bytes(original)
        self.assertEqual(a.cleanup(self.root, "one")["state"], "cleaned")

    def test_existing_run_or_target_is_never_overwritten(self):
        self.prepare()
        before = a.tree_files(self.project)
        with self.assertRaises(a.AssetError): self.prepare()
        self.assertEqual(a.tree_files(self.project), before)
        plan = self.prepare(run="two", apply=False)
        dest = self.project / plan["bundles"][0]["install_relative"]
        dest.mkdir(); (dest / "keep.txt").write_text("existing")
        with self.assertRaises(a.AssetError): self.prepare(run="two")
        self.assertEqual((dest / "keep.txt").read_text(), "existing")

    def test_source_and_target_symlinks_rejected(self):
        outside = self.base / "outside"; outside.mkdir()
        (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(a.AssetError): self.prepare()
        self.assertEqual(list(outside.iterdir()), [])
        (self.project / ".agents").unlink()
        (self.root / "source/main/link").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(a.AssetError): self.prepare()

    def test_dependency_cycle_and_missing_dependency_fail_before_writes(self):
        self.catalog["assets"][0]["dependencies"] = ["vendor/main"]
        a.write_json(self.root / "catalog.json", self.catalog)
        with self.assertRaises(a.AssetError): self.prepare()
        self.catalog["assets"][0]["dependencies"] = ["vendor/missing"]
        a.write_json(self.root / "catalog.json", self.catalog)
        with self.assertRaises(a.AssetError): self.prepare()
        self.assertEqual(list(self.project.iterdir()), [])

    def test_pending_dependency_review_blocks_install(self):
        self.catalog["assets"][0]["dependency_review"] = "pending"
        a.write_json(self.root / "catalog.json", self.catalog)
        with self.assertRaises(a.AssetError): self.prepare()

    def test_manifest_cannot_redirect_cleanup(self):
        self.prepare()
        folder, m = a.load_trial(self.root, "one")
        victim = self.project / "important"; victim.mkdir()
        (victim / "keep.txt").write_text("keep")
        m["bundles"][0]["install_relative"] = "important"
        a.write_json(folder / "manifest.json", m)
        with self.assertRaises(a.AssetError): a.cleanup(self.root, "one")
        self.assertEqual((victim / "keep.txt").read_text(), "keep")

    def test_pinned_source_drift_is_detected(self):
        self.catalog["sources"][0].update(path="source", checksums="checksum.json")
        a.write_json(self.root / "checksum.json", a.hashes(a.tree_files(self.root / "source")))
        a.write_json(self.root / "catalog.json", self.catalog)
        self.assertTrue(a.check(self.root)["valid"])
        (self.root / "source/main/SKILL.md").write_text("changed")
        with self.assertRaises(a.AssetError): self.prepare()

    def test_record_distinguishes_preparation_from_invocation_and_no_auto_adoption(self):
        self.prepare()
        with self.assertRaises(a.AssetError):
            a.record(self.root, "one", ["vendor/main"], "useful", "copied", [], "unverified", "unverified")
        (self.root / "evidence.md").write_text("A bounded actual run, with result evidence.")
        result = a.record(self.root, "one", ["vendor/main"], "useful", "observed", ["evidence.md"], "verified", "verified")
        self.assertEqual(result["adoption"], "not_decided")
        _, assets = a.catalog(self.root)
        self.assertEqual(assets["vendor/main"]["state"], "testing")
        self.assertEqual(assets["vendor/helper"]["state"], "staged")
        with self.assertRaises(a.AssetError):
            a.record(self.root, "one", ["vendor/main"], "useful", "overwrite", ["evidence.md"], "verified", "verified")

    def test_adoption_requires_a_user_decision_record(self):
        a.write_json(self.root / "decision.json", {"assets": ["vendor/main"], "state": "adopted"})
        with self.assertRaises(a.AssetError): a.decide(self.root, "decision.json")
        a.write_json(self.root / "decision.json", {"assets": ["vendor/main"], "state": "adopted", "decided_by": "user",
             "user_statement": "Adopt this asset", "conversation_reference": "test-fixture-only", "reason": "observed useful"})
        a.decide(self.root, "decision.json")
        self.assertTrue(a.check(self.root)["valid"])
        self.assertEqual(a.catalog(self.root)[1]["vendor/main"]["state"], "adopted")


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "library"
        self.checkout = self.base / "checkout"
        self.root.mkdir(); self.checkout.mkdir()
        a.write_json(self.root / "catalog.json", {"schema_version": 1, "sources": [], "assets": []})
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Test fixture")
        self.git("remote", "add", "origin", "https://example.invalid/skills.git")
        (self.checkout / "LICENSE").write_text("Test fixture license")
        for name in ("first", "second"):
            folder = self.checkout / "skills" / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Test fixture.\n---\nFixture only.\n")
            (folder / "resource.bin").write_bytes(b"\x00\xff")
        self.git("add", ".")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "fixture")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.checkout), *args], text=True)

    def test_extend_same_snapshot_preserves_existing_files_and_license(self):
        a.intake(self.root, self.checkout, "external", ["first"], ["research"])
        first = a.tree_files(self.root / "staging/external/upstream/skills/first")
        result = a.intake(self.root, self.checkout, "external", ["first", "second"], ["research"])
        self.assertEqual(result["assets"], ["external/second"])
        self.assertEqual(a.tree_files(self.root / "staging/external/upstream/skills/first"), first)
        data, assets = a.catalog(self.root)
        self.assertEqual(len(data["sources"]), 1)
        self.assertEqual(len(assets), 2)
        self.assertEqual(assets["external/second"]["dependency_review"], "pending")
        self.assertTrue(a.check(self.root)["valid"])
        self.assertEqual((self.root / "staging/external/upstream/LICENSE").read_bytes(), (self.checkout / "LICENSE").read_bytes())

    def test_dirty_checkout_or_changed_revision_cannot_extend_source(self):
        a.intake(self.root, self.checkout, "external", ["first"])
        baseline = a.tree_files(self.root)
        (self.checkout / "LICENSE").write_text("Modified fixture license")
        with self.assertRaises(a.AssetError):
            a.intake(self.root, self.checkout, "external", ["second"])
        self.assertEqual(a.tree_files(self.root), baseline)
        self.git("add", ".")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "changed fixture")
        with self.assertRaises(a.AssetError):
            a.intake(self.root, self.checkout, "external", ["second"])
        self.assertEqual(a.tree_files(self.root), baseline)


if __name__ == "__main__":
    unittest.main()
