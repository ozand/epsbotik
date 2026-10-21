#!/usr/bin/env python3
"""Offline downstream repository invariants; no device or network access."""

from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


class ProjectContract(unittest.TestCase):
    # @lat: [[verification#Verification#Upstream ancestry]]
    def test_upstream_ancestry(self):
        base = (ROOT / "docs/upstream-base.txt").read_text().strip()
        self.assertRegex(base, r"^[0-9a-f]{40}$")
        subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", base, "HEAD"],
            check=True,
        )

    # @lat: [[verification#Verification#Public boundary]]
    def test_public_boundary(self):
        prefixes = ("sources/", ".pi/", "--session/", ".local-context/", "blueprint/")
        for prefix in prefixes:
            subprocess.run(
                ["git", "-C", str(ROOT), "check-ignore", "-q", "--", prefix + "probe"],
                check=True,
            )
        paths = git("ls-files", "-z").split("\0")
        self.assertFalse([p for p in paths if p.startswith(prefixes)])
        self.assertFalse([p for p in paths if Path(p).name == ".env"])

    # @lat: [[verification#Verification#ADR index]]
    def test_adr_index(self):
        directory = ROOT / "docs/adr"
        index = (directory / "INDEX.md").read_text()
        files = {p.name for p in directory.glob("ADR-*.md")}
        references = set(re.findall(r"\(\./(ADR-\d{3}-[a-z0-9-]+\.md)\)", index))
        self.assertEqual(files, references)
        for name in sorted(files):
            content = (directory / name).read_text()
            for heading in ("## Context", "## Decision", "## Consequences"):
                self.assertIn(heading, content, name)
            status = re.search(r"\*\*Status\*\*: (.+)", content)
            self.assertIsNotNone(status, name)
            row = next(line for line in index.splitlines() if f"(./{name})" in line)
            self.assertIn(status.group(1), row)

    # @lat: [[verification#Verification#Knowledge entrypoints]]
    def test_knowledge_entrypoints(self):
        for name in ("README.md", "AGENTS.md", "lat.md/lat.md", "docs/epsbotik-workflow.md"):
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertIn("0.13.3", (ROOT / "README.md").read_text())
        self.assertIn("lat check", (ROOT / "AGENTS.md").read_text())
        self.assertIn("epsbotik", (ROOT / "README.md").read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
