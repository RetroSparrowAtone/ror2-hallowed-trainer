# Contributing to ror2-hallowed-trainer

Thanks for your interest in the Hallowed Concepts Trainer for Risk of Rain 2.

## Development setup

1. Install Python 3.11+ (64-bit).
2. `pip install -r requirements.txt`
3. Copy `config/default.yaml` to `config/local.yaml` and point `game.exe_path` at your Risk of Rain 2 install.
4. Run `python -m src.bootstrap` as administrator.

## Plugin development

The trainer is a plugin host. New features live under `src/plugins/` and implement
the `TrainerPlugin` contract from `src/core/contracts.py`. Register your plugin
in `src/plugins/registry.py` so the loader picks it up.

Plugins should:

- Declare a `NAME`, `VERSION`, and `REQUIRES` (list of other plugin names).
- Implement `enable(ctx)` / `disable(ctx)` and clean up any hooks.
- Never hardcode offsets — read them from `src/offsets/resolver.py`.

## Pull requests

- Keep PRs scoped to one plugin or one core module.
- Include a test under `tests/` when touching offset resolution or memory IO.
- Run `pytest -q` before submitting.

## Responsible use

This project is for single-player / private-lobby experimentation and modding
research only. Do not use it in public lobbies — you will get banned and it
ruins the game for others.