# The Fix

*The Fix* corrects errors in your previous console command. Type a command,
get an error, type `fix`, and it proposes the command you meant.

> **Status: unmaintained.** This is a one-off renamed copy, provided as is.
> There is no support, and issues and pull requests are not monitored.
> Please do not contact the original author, who is not involved in this
> version, about it.

This is a renamed fork of Vladimir Iakovlev's MIT-licensed command corrector
with a name that is comfortable to type, share and see in logs. The program
behaves the same as upstream; only the names differ. See [FORK.md](FORK.md)
for how the fork was produced and what differs.

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ fix
sudo apt-get install vim [enter/↑/↓/ctrl+c]
Reading package lists... Done
...
```

```bash
➜ git brnch
git: 'brnch' is not a git command. See 'git --help'.

Did you mean this?
    branch

➜ fix
git branch [enter/↑/↓/ctrl+c]
* master
```

## Requirements

- Python 3.5 or later
- pip

## Installation

Install from this repository, by path or by repository URL. Do not install by
bare name from a package index: a different package could be registered there
under the same name.

```bash
pip install --user /path/to/this/checkout
```

```bash
pip install --user git+https://github.com/alewan/thefix.git
```

## Shell setup

Add this to your `.bashrc`, `.zshrc` or other startup script:

```bash
eval "$(thefix --alias)"
```

The alias is called `fix` by default. To use another name, pass it:

```bash
eval "$(thefix --alias oops)"
```

Changes apply to new shell sessions. To apply them immediately, run
`source ~/.bashrc` (or your shell's startup file).

To run the corrected command without confirmation, use `fix --yeah` (or
`fix -y`). To keep correcting until a command succeeds, use `fix -r`.

## Uninstall

Remove the `thefix --alias` line from your shell startup file, then:

```bash
pip uninstall thefix
```
