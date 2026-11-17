# Security rules for AI coding agents

## Secrets and credentials
- Never hardcode passwords, API keys, access tokens, private keys, connection strings, or other credentials in source code, documentation, examples, tests, logs, or commit messages.
- Never print, copy, summarize, or expose secret values. Refer to the file or variable name only.
- Do not read `.env`, credential stores, private keys, or files under `secrets/` unless the task explicitly requires it and the user authorizes it.
- Never place credentials in agent settings, MCP configuration, prompts, generated reports, or tracked files.
- Use placeholders such as `YOUR_API_KEY` in examples and provide a safe `.env.example` containing names only.
- Prefer short-lived, least-privilege credentials and isolated test accounts. Never use production credentials for development.

## Git and publication
- Treat `.claude/settings.local.json`, local agent settings, environment files, private keys, and credential stores as sensitive.
- Never force-add ignored files containing credentials.
- Inspect the staged diff before every commit; verify no secret or local configuration is included.
- Never bypass secret scanning, push protection, or CI security checks.
- Do not assume `.gitignore` protects files already tracked or removes secrets from Git history.

## Incident handling
- If a possible credential is found, do not reveal its value or propagate it. Stop, identify only the file and credential type, and notify the operator.
- Treat any credential committed to a public repository as compromised: revoke it, rotate it, inspect access logs, and assess history/artifact exposure.
- Do not rewrite public Git history or revoke/rotate credentials autonomously; obtain operator approval.

## Final verification
- Run the repository's secret scanner when available.
- Verify the staged diff and generated artifacts contain no credentials.
- Report security checks that could not be performed; never claim a clean scan without running one.
