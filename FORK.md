# About this fork

**This fork is unmaintained.** It is a one-off renamed copy, provided as is,
with no support and no commitment to follow upstream. The original author is
not involved in it and should not be contacted about this version.

This repository is **generated** from Vladimir Iakovlev's MIT-licensed command
corrector by a script. The original project name is deliberately not written
anywhere in this repository, including here. The rest of this file records how
that was done, for anyone who wants to regenerate or adapt it themselves.

## What the fork changes

- **Names.** The package, command, default alias, settings variables, config
  directory and temp files are renamed:

  | Upstream concept | Here |
  |---|---|
  | Command and Python package | `thefix` |
  | Default shell alias | `fix` |
  | Settings variables | `THEFIX_*` |
  | Config directory | `~/.config/thefix/` |
  | Third-party rule packages | `thefix_contrib_*` |

  Existing upstream settings files, environment variables and third-party rule
  packages are therefore not picked up; rename them to match.
- **Removed.** Upstream's CI and issue templates, snap packaging, release
  script, demo recordings and contributing guide.
- **Patched.** A handful of small hand patches, all listed with their reasons
  in `PATCHES` in [tools/sync_upstream.py](tools/sync_upstream.py): wording the
  mechanical rename gets wrong, links that pointed at upstream, packaging that
  relied on removed setuptools internals, package metadata (the original
  author's contact address is removed and the package is marked inactive), a
  `distutils` import (gone in Python
  3.12), a lint setting and a `pytest<8` pin (upstream's own test suite does
  not pass on pytest 8 or later).

## Layout

| Path | Owner |
|---|---|
| `tools/`, `FORK.md`, `.github/workflows/ci.yml` | The fork. Edit these directly. |
| Everything else | Generated. Edits are overwritten by the next sync. |

`UPSTREAM_COMMIT` records the upstream commit the tree was generated from.
`tools/sync-manifest.txt` lists the generated files so a later sync can remove
ones upstream has deleted.

To change generated code, add a patch to `PATCHES` rather than editing the
file. To change the top of the README, edit `tools/readme_head.md`.

## One-time setup after cloning

Enable the hooks that block the original name from files, paths and commit
messages:

```bash
git config core.hooksPath tools/hooks
```

## Pulling in upstream changes

Do this on a machine where having the upstream name on disk and in network
logs is acceptable, not on the machine the fork exists to protect.

1. Clone or update upstream somewhere **outside** this repository.
2. Run the sync against it:

   ```bash
   tools/sync_upstream.py /path/to/upstream/checkout
   ```

   If upstream changed a line that a hand patch targets, the sync stops
   without writing anything and names the patch to revisit.
3. Run the tests (the functional tests need Docker and are skipped here):

   ```bash
   pip install -r requirements.txt
   ```

   ```bash
   pytest --ignore=tests/functional
   ```

4. Commit. Write commit messages without the original name; the `commit-msg`
   hook enforces this.

## The guard

```bash
tools/check_clean.py
```

scans every file's contents and path. With `--history` it also scans every
object and ref in the git repository, which covers commit messages and old
versions of files. It prints locations only, never the matched text.

Never add upstream as a git remote of this repository or merge its history:
upstream's commits contain the original name throughout. The fork's history
should consist only of commits made here.
