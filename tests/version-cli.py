#!/usr/bin/env python3
"""Check version reporting and installed compatibility command aliases."""
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
subprocess.run(["cargo", "build", "--workspace", "--bins"], cwd=ROOT, check=True)
expected = re.compile(r"^drops(?:ctl|d) \S+(?: \(.+\))?$")
for binary in ("dropsctl", "dropsd"):
    result = subprocess.run([str(ROOT / "target" / "debug" / binary), "--version"], cwd=ROOT, check=True, capture_output=True, text=True)
    assert expected.fullmatch(result.stdout.strip()), result.stdout

launcher = subprocess.run([str(ROOT / "scripts" / "drops"), "--version"], cwd=ROOT, check=True, capture_output=True, text=True)
assert launcher.stdout.startswith("Drops 0.1.0"), launcher.stdout

with tempfile.TemporaryDirectory(prefix="drops-version-aliases-") as directory:
    prefix = pathlib.Path(directory)
    (prefix / "buddyctl").symlink_to(ROOT / "target" / "debug" / "dropsctl")
    (prefix / "buddyd").symlink_to(ROOT / "target" / "debug" / "dropsd")
    for alias in ("buddyctl", "buddyd"):
        result = subprocess.run([str(prefix / alias), "--version"], cwd=ROOT, check=True, capture_output=True, text=True)
        assert expected.fullmatch(result.stdout.strip()), result.stdout

print("PASS: drops, dropsctl, dropsd and legacy binaries report the build version")
