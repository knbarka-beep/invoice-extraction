"""Method 3: expensive LLM (Claude Opus via the Claude Code CLI, on the Pro subscription).

Run from the repo root: py -m methods.method3_claude
"""
import json
import shutil
import subprocess
import tempfile

from methods.llm_common import run

# Flags checked against `claude --help` (2.1.289). Beyond -p/--model/--output-format,
# the rest make it a plain model call: no CLAUDE.md, plugins, hooks, MCP servers or
# tools, a neutral system prompt instead of the coding-agent one, nothing saved.
CMD = [
    shutil.which("claude") or "claude", "-p", "--model", "opus", "--output-format", "json",
    "--safe-mode", "--strict-mcp-config", "--tools", "", "--no-session-persistence",
    "--system-prompt", "You are a data extraction assistant.",
]


def call(prompt):
    proc = subprocess.run(CMD, input=prompt, capture_output=True, encoding="utf-8",
                          timeout=300, cwd=tempfile.gettempdir())  # cwd outside the repo
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(f"claude exited {proc.returncode}: {proc.stderr.strip()}")
    out = json.loads(proc.stdout)
    u = out.get("usage", {})
    usage = {
        "model": ", ".join(out.get("modelUsage", {})) or "opus",
        # the CLI caches the prompt, so most input is reported as cache tokens
        "input_tokens": sum(u.get(k, 0) for k in
                            ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")),
        "output_tokens": u.get("output_tokens", 0),
        "cost_usd": out.get("total_cost_usd"),  # API-equivalent list price, not money paid
    }
    if out.get("is_error"):
        raise RuntimeError(str(out.get("result"))[:300])
    return out["result"], usage


if __name__ == "__main__":
    run("method3_claude", call)
