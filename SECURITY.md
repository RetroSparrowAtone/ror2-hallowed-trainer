# Security Policy

## Scope

This repository is a hobbyist trainer for Risk of Rain 2. It performs
read/write memory operations against a locally running `Risk of Rain 2.exe`
process. It does not phone home, does not contain a remote loader, and does
not ship any obfuscated binaries.

## Reporting

If you find a vulnerability — e.g. an unsafe pointer dereference that can
crash the host, an arbitrary file write in the config loader, or a plugin
loader path traversal — please open a private security advisory on GitHub
rather than a public issue.

## Out of scope

- Anti-cheat bypasses for online play (not supported, not shipped).
- Requests to add remote code execution features (spoofer, loader, dumper
  over network) — these are rejected.

## Supported versions

Only the latest `main` branch is supported.