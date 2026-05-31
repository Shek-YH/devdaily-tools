"""Environment variable manager - validate, diff, and sync .env files."""

import os
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

ENV_LINE_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")


def parse_env_file(filepath: str) -> dict:
    """Parse a .env file into a dict, skipping comments and blanks."""
    path = Path(filepath)
    if not path.exists():
        return {}
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = ENV_LINE_RE.match(line)
        if match:
            result[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return result


def manage_env(action: str, required: str, file: str, other: str = None):
    """Dispatch env management actions."""
    if action == "check":
        check_env(required, file)
    elif action == "diff":
        diff_env(file, other)
    elif action == "sync":
        sync_env(file, other)


def check_env(required: str, file: str):
    """Check if required environment variables are present."""
    if not required:
        console.print("[yellow]Use --required to specify required variables (comma-separated).[/]")
        return

    required_vars = [v.strip() for v in required.split(",") if v.strip()]
    env_vars = parse_env_file(file)

    table = Table(title=f"Environment Check: {file}")
    table.add_column("Variable", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Value Preview")

    all_ok = True
    for var in required_vars:
        if var in env_vars:
            val = env_vars[var]
            preview = val[:30] + "..." if len(val) > 30 else val
            table.add_row(var, "[green]✓ Present[/]", preview)
        else:
            table.add_row(var, "[red]✗ Missing[/]", "—")
            all_ok = False

    console.print(table)

    if all_ok:
        console.print("\n[green]All required variables present.[/]")
    else:
        console.print("\n[red]Some required variables are missing.[/]")


def diff_env(file: str, other: str):
    """Show differences between two .env files."""
    if not other:
        console.print("[red]Use --other to specify the second .env file.[/]")
        return

    env1 = parse_env_file(file)
    env2 = parse_env_file(other)

    only_in_1 = set(env1) - set(env2)
    only_in_2 = set(env2) - set(env1)
    common = set(env1) & set(env2)

    console.print(f"\n[bold]Comparing {file} ↔ {other}[/]\n")

    if only_in_1:
        console.print(f"[yellow]Only in {file}:[/] {', '.join(sorted(only_in_1))}")
    if only_in_2:
        console.print(f"[yellow]Only in {other}:[/] {', '.join(sorted(only_in_2))}")

    diff_values = []
    for key in sorted(common):
        if env1[key] != env2[key]:
            diff_values.append((key, env1[key], env2[key]))

    if diff_values:
        table = Table(title="Value Differences")
        table.add_column("Variable", style="cyan")
        table.add_column(file, style="yellow")
        table.add_column(other, style="green")
        for key, v1, v2 in diff_values:
            table.add_row(key, v1[:50], v2[:50])
        console.print(table)

    if not only_in_1 and not only_in_2 and not diff_values:
        console.print("[green]Files are identical.[/]")


def sync_env(source: str, target: str):
    """Sync missing keys from source .env to target .env."""
    if not target:
        console.print("[red]Use --other to specify the target .env file.[/]")
        return

    src_env = parse_env_file(source)
    tgt_env = parse_env_file(target)

    missing = {k: v for k, v in src_env.items() if k not in tgt_env}
    if not missing:
        console.print("[green]Target already has all keys from source. Nothing to sync.[/]")
        return

    target_path = Path(target)
    with open(target_path, "a", encoding="utf-8") as f:
        f.write(f"\n# Synced from {source}\n")
        for k, v in missing.items():
            f.write(f'{k}="{v}"\n')

    console.print(f"[green]✓[/] Synced {len(missing)} variables to {target}:")
    for k in sorted(missing):
        console.print(f"  + {k}")
