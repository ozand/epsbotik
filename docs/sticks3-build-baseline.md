# StickS3 own-firmware build baseline

This page records the tested StickS3 build procedure and its limits. It is a software-build baseline, not a claim about installed firmware or physical-device behavior.

## Evidence and exact provenance

The sanitized machine-readable inventory is [sticks3-baseline.json](build-evidence/sticks3-baseline.json). It records the 57 metadata fixture files by filename, length, and SHA-256; the 39 managed-component checksum-file hashes; effective sdkconfig and run lock hashes; selected artifact hashes; and hashes of the four patched SDK files. It deliberately contains no sdkconfig contents, private paths, credentials, or images. The fixture's records were served by the public registry URL pattern `https://components-file.espressif.com/components/{namespace}/{name}.json`; the file hashes identify exact downloaded JSON bytes. The tested server served only fixture JSON, rejected non-allowlisted paths, and did not serve archives. There were 86 allowlisted requests in each run (not 86 combined).

| Input | Measured value |
|---|---|
| Candidate source | `ce90852b919f4ed86312493f03ca3e00f69c201f` |
| ESP-IDF | v5.5.4, commit `735507283d5b2f9fb363a1901172dbd9e847945d` |
| Target / board | `esp32s3` / `m5stack_sticks3` |
| Board configuration | 8 MB flash, `partitions_8MB.csv`, Octal PSRAM |
| Python / Component Manager / Board Manager | 3.12.14 / 2.5.2 / 0.6.2 |
| Compiler / CMake / Ninja | GCC 14.2.0 / 3.30.2 / 1.12.1 |
| Effective sdkconfig SHA-256 | `9c0d8e48c1e8239c9f42c2c8515fcc3ea2e587d25e11d15031008759b516c626` |

The SDK gitlinks are enumerated in the manifest from recursive `git ls-tree` at the recorded SDK commit. All 23 referenced commit objects were present in initialized local submodule object stores when checked, including `components/mbedtls/mbedtls` at `ffb280bb63c78bfec1e1ab55040671768c85c923`. Four post-patch file hashes identify patched SDK content. This confirms expected submodule objects are available now; the original run did not retain an independently signed per-submodule export receipt.

The current local historical reference lock at upstream revision `345073de68179542c307e303df81e38baadf77f0` hashes to `b8f3e1d062337b87e26f6cdadcac1bb7c5a586d5b1a801a5e182e33e43ab7952`; its dependency entries are summarized in the manifest with name, version, registry component hash, and source kind, without machine paths. The run lock hashes differ because Component Manager updated the copied lock. The original copied lock bytes were not separately retained, so the current reference hash establishes the extant historical input, not independently the exact bytes at run time.

The manifest also gives canonical content digests for current reference managed-component trees and individual `CHECKSUMS.json` digests. These are current snapshots, not a contemporaneous per-run inventory. Run managed checksum-file hashes match reference snapshot values; the cache entry present in both run directories is identified by its checksum-file hash. Do not infer that this inventories all cache content or proves the cache unchanged before/after each build. The sdkconfig remains identified by hash only; its private contents are not published.

This is a **measured two-run baseline, not a zero-input clean-checkout package**. Exact metadata fixture bytes are enumerated; the required historical config, lock, source cache, managed sources, SDK, and host tool/runtime remain external inputs. Current snapshots improve provenance but cannot prove every input was byte-identical at run time. Do not publish private config, use `/sources/` as an editable tree, or claim universal bootstrap reproducibility.

## Reproduction with explicitly supplied local inputs

This recipe describes the tested workflow, not an installer or a new project build contract. It only applies where the operator already has compatible local source repositories and tool/input trees. Do not install or download tools/components. If a required input is absent or fails its manifest hash, stop. The historical lock is available in the local reference tree at `application/edge_agent/dependencies.lock` in revision `345073de68179542c307e303df81e38baadf77f0`; its current SHA-256 and canonical dependency table are in the manifest. `CONFIG_INPUT` must be supplied from the same authorized local reference input set and must hash to the documented sdkconfig digest after BMGR; its contents are intentionally not published. `MANAGED_INPUT` and `CACHE_INPUT` likewise must be supplied from existing local source/cache snapshots and validated against recorded checksums. The metadata fixture is enumerated by hashes but its JSON files are external. Thus a maintainer with only this repository cannot reproduce; the recipe is for explicitly supplied matching inputs. Use two separate disposable output roots; never point output variables at a source checkout, installed SDK, or original cache.

Set these absolute path variables to pre-existing local inputs (none has a machine-specific default):

```bash
set -euo pipefail
: "${SOURCE_REPO:?committed epsbotik Git repository containing the source commit}"
: "${SDK_REPO:?ESP-IDF Git repository containing the SDK commit and submodule objects}"
: "${TOOL_ROOT:?already installed Espressif tools, Python env, runtime profile, bwrap, tar, git}"
: "${PY_ENV:?already installed ESP-IDF Python 3.12 environment}"
: "${PY_RUNTIME:?compatible host runtime/profile required by that Python environment}"
: "${PROFILE:?host runtime profile path, if required by PY_ENV}"
: "${CACHE_INPUT:?existing Component Manager source cache}"
: "${CONFIG_INPUT:?authorized local historical sdkconfig; content is not published}"
: "${LOCK_INPUT:?authorized historical dependencies.lock from the stated upstream revision}"
: "${MANAGED_INPUT:?matching historical managed_components directory}"
: "${METADATA_DIR:?directory containing exactly the 57 JSON fixture files identified in the manifest}"
: "${OUTPUT_BASE:?new, empty, disposable output directory outside all input trees}"
```

A source `git archive` preserves repository nesting without changing the checkout. For SDK export, verify top-level commit and all 23 path/gitlink pairs against the manifest, then recursively export each recorded commit from its existing local Git object store. Confirm each submodule worktree contains the expected commit object; do not assume current submodule HEAD equals the recorded commit. A `git archive` of a superproject alone omits submodule contents.

Example preparation and two-run execution skeleton (all commands use existing local objects and do not fetch):

```bash
SOURCE_REV=ce90852b919f4ed86312493f03ca3e00f69c201f
SDK_REV=735507283d5b2f9fb363a1901172dbd9e847945d
for run in A B; do
  OUT="$OUTPUT_BASE/$run"
  mkdir -p "$OUT"
  test -z "$(find "$OUT" -mindepth 1 -print -quit)"
  mkdir -p "$OUT/source" "$OUT/sdk"
  git -C "$SOURCE_REPO" archive "$SOURCE_REV" | tar -x -C "$OUT/source"
  test "$(git -C "$SDK_REPO" rev-parse "$SDK_REV^{commit}")" = "$SDK_REV"
  git -C "$SDK_REPO" archive "$SDK_REV" | tar -x -C "$OUT/sdk"
  # Extract each submodule tree from its initialized local git object database
  # at exactly the gitlink in the manifest; fail if any object is unavailable.
  python3 - "$SDK_REPO" "$OUT/sdk" <<'PY'
import json, subprocess, sys
from pathlib import Path
repo, dest = map(Path, sys.argv[1:])
manifest = json.loads(Path("docs/build-evidence/sticks3-baseline.json").read_text())
for item in manifest["sdk"]["submodules"]["entries"]:
    source, target, commit = repo / item["path"], dest / item["path"], item["gitlink"]
    subprocess.run(["git", "-C", str(source), "cat-file", "-e", commit + "^{commit}"], check=True)
    target.mkdir(parents=True, exist_ok=True)
    archive = subprocess.Popen(["git", "-C", str(source), "archive", commit], stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", str(target)], stdin=archive.stdout, check=True)
    if archive.wait() != 0: raise SystemExit(f"archive failed: {item['path']}")
PY
  cp -a "$CACHE_INPUT" "$OUT/cache"
  APP="$OUT/source/application/edge_agent"
  cp -a "$MANAGED_INPUT" "$APP/managed_components"
  cp "$LOCK_INPUT" "$APP/dependencies.lock"
  cp -a "$METADATA_DIR" "$OUT/metadata"
  # A pre-existing local Python 3.12 environment is selected explicitly below.
  PY="$PY_ENV/bin/python"
  PATH="$PY_ENV/bin:$TOOL_ROOT/bin:$SDK_REPO/tools:$PATH"
  export PATH IDF_PATH="$OUT/sdk" IDF_PYTHON_ENV_PATH="$PY_ENV"
  export IDF_TOOLS_PATH="$OUT/tools" IDF_TARGET=esp32s3
  export IDF_COMPONENT_CACHE_PATH="$OUT/cache"
  # Run BMGR first; it writes generated board files only in this disposable app.
  (cd "$APP" && "$PY" "$IDF_PATH/tools/idf.py" bmgr -c ./boards -b m5stack_sticks3)
  cp "$CONFIG_INPUT" "$APP/sdkconfig"
  echo '9c0d8e48c1e8239c9f42c2c8515fcc3ea2e587d25e11d15031008759b516c626  '"$APP/sdkconfig" | sha256sum -c -
  # Confirm selected Python, idf.py, compilers, CMake, and Ninja are on PATH.
  # Start the Python fixture server in the sandbox with "$OUT/metadata".
  # Run idf.py build and idf.py size there; preserve logs and exit status.
done
```

The above is not sufficient isolation by itself. The successful runs used Bubblewrap with private user/network namespaces, cleared environment, private `/dev` and `/proc`, temporary HOME, read-only runtime/tool mounts, and writable mounts only for disposable run output and copied cache. No `/` or device nodes were exposed. The existing SDK source had to be writable in the disposable export because project CMake applies four SDK patches (their resulting file hashes are in the manifest). Do not bind the original SDK/cache writable. Bubblewrap must be positively verified on the host before invoking any resolver/build command; if its network namespace cannot be created, stop.

Inside that sandbox, start a loopback-only metadata responder over the verified fixture, then run BMGR/build. A minimal fixture server must enforce the exact filename allowlist, validate JSON package identity, reject encoded/traversal/backslash paths and every unknown route, and serve bytes only from the fixture directory. The following is the tested server algorithm in executable Python form; save as a disposable file outside source trees, pass the metadata directory as its sole argument, and run it only inside the isolated namespace:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json, sys
root = Path(sys.argv[1]).resolve()
allowed = {p.stem.replace("__", "/"): p for p in root.glob("*.json")}
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        raw = self.path.split("?", 1)[0]
        if "%" in raw or "\\" in raw or ".." in raw or not raw.startswith("/components/") or not raw.endswith(".json"):
            self.send_error(404); return
        name = raw[len("/components/"):-5]
        file = allowed.get(name)
        if file is None or file.resolve().parent != root:
            self.send_error(404); return
        data = file.read_bytes()
        try:
            obj = json.loads(data)
            if obj.get("namespace", "").lower() + "/" + obj.get("name", "").lower() != name:
                raise ValueError("identity mismatch")
        except Exception:
            self.send_error(404); return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)
    def log_message(self, fmt, *args): print("fixture", fmt % args, flush=True)
HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
```

Before use, verify every fixture file against `metadata_fixture.files` in the JSON manifest. The tested sandbox set `IDF_COMPONENT_LOCAL_STORAGE_URL=http://127.0.0.1:8765`; `IDF_COMPONENT_CACHE_PATH` pointed only to the disposable copied source cache. Permit loopback only inside the namespace and deny external network; confirm resolver logs contain no archive requests. The public registry metadata was previously fetched under issue-specific read-only metadata authorization. That historical authorization is not a standing permission to fetch anything. If an operator separately has authorization to retrieve missing metadata, retrieve only the named public `.json` records, enforce a bounded response size and no redirects, verify hashes, and never request archives; otherwise stop when the fixture is incomplete.

Within the sandbox, explicitly set `HOME` to a private temporary directory and `PATH` to the already installed Python 3.12 environment, ESP-IDF tools, Xtensa/RISC-V GCC, CMake, Ninja, and required host runtime binaries. Invoke the selected Python executable directly (do not rely on shell `python` selection). The host used a Nix-provided runtime/profile; this is a host-specific prerequisite, not a generic Linux claim. A generic command outline after provisioning and verified isolation is:

```sh
"$PY" "$IDF_PATH/tools/idf.py" build
"$PY" "$IDF_PATH/tools/idf.py" size
stat -c '%n %s bytes' build/edge_agent.bin build/system.bin build/storage.bin \
  build/bootloader/bootloader.bin build/partition_table/partition-table.bin \
  build/ota_data_initial.bin
```

Capture separate exit codes/logs for both runs. Verify both effective sdkconfig hashes, metadata fixture hashes, 86 metadata requests per run, managed component checksum files, and normalized lock dependency selections; normalize only temporary source-root path fields. Keep output directories independent and compare artifact sizes and SHA-256 values. The manifest includes the current historical lock hash and sanitized canonical dependency table as well as both final run-lock hashes. It cannot establish that the current reference file is byte-identical to the copied pre-resolution lock at run time; that exact snapshot was not separately retained. The recipe is therefore useful with explicitly supplied local inputs and still has bounded provenance limits.

## Measured results

Both disposable builds completed all 2782 steps and matched these sizes and static reports:

| Artifact / report | Run A | Run B |
|---|---:|---:|
| `edge_agent.bin` | 3,531,792 B | 3,531,792 B |
| `system.bin` | 2,662,400 B | 2,662,400 B |
| `storage.bin` | 1,703,936 B | 1,703,936 B |
| Bootloader | 22,272 B | 22,272 B |
| Partition table | 3,072 B | 3,072 B |
| OTA data | 8,192 B | 8,192 B |
| Smallest app partition | 0x3b6000 B | 0x3b6000 B |
| App image used / remaining | 0x35e410 / 0x57bf0 B (9% remaining) | 0x35e410 / 0x57bf0 B (9% remaining) |
| Flash Code / Flash Data | 2,553,670 / 861,968 B | 2,553,670 / 861,968 B |
| DIRAM | 157,919 / 341,760 B | 157,919 / 341,760 B |
| IRAM | 16,384 / 16,384 B | 16,384 / 16,384 B |
| RTC SLOW | 32 / 8,192 B | 32 / 8,192 B |
| RTC FAST | 24 / 8,192 B | 24 / 8,192 B |

Artifact hashes differ despite equal sizes and static budgets: this is two successful builds with matching reported sizes, not bit-identical output. Static linker budgets do not establish runtime heap/stack. Device installation, physical UI/peripherals, and installed firmware version were not tested. No firmware image is published.

For the ordinary repository workflow and checks, see the [development workflow](epsbotik-workflow.md). This documentation describes measured existing build behavior; it creates no lockfile, vendored dependency policy, or deployment contract.
