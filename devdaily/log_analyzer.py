"""Log analyzer - Parse, filter, and summarize log files."""

import json
import re
from collections import Counter
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

LOG_LEVEL_PATTERN = re.compile(
    r"\b(ERROR|WARN|WARNING|INFO|DEBUG|TRACE|CRITICAL|FATAL)\b",
    re.IGNORECASE,
)

LEVEL_WEIGHT = {
    "ERROR": 5, "CRITICAL": 5, "FATAL": 5,
    "WARN": 3, "WARNING": 3,
    "INFO": 1,
    "DEBUG": 0, "TRACE": 0,
}


def export_json(result: dict, output_path: str):
    """Export analysis result to a JSON file."""
    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"[green]Report exported to[/] {out}")


def analyze_log(logfile: str, level: str = None, last: int = None, pattern: str = None, json_out: str = None):
    """Parse and summarize a log file."""
    path = Path(logfile).resolve()
    if not path.exists():
        console.print(f"[red]Error:[/] Log file not found: {logfile}")
        return

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    total_lines = len(lines)

    if last:
        lines = lines[-last:]

    # Filter by level
    if level:
        level_filter = re.compile(rf"\b{level}\b", re.IGNORECASE)
        lines = [l for l in lines if level_filter.search(l)]

    # Filter by pattern
    if pattern:
        try:
            pat = re.compile(pattern)
            lines = [l for l in lines if pat.search(l)]
        except re.error as e:
            console.print(f"[red]Invalid regex pattern:[/] {e}")
            return

    if not lines:
        console.print("[yellow]No matching log entries found.[/]")
        return

    # Count levels
    level_counts = Counter()
    for line in lines:
        match = LOG_LEVEL_PATTERN.search(line)
        if match:
            level_counts[match.group(1).upper()] += 1

    # Summary table
    summary = Table(title=f"Log Analysis: {path.name}")
    summary.add_column("Metric", style="cyan")
    summary.add_column("Value", style="bold")

    summary.add_row("Total lines (file)", str(total_lines))
    summary.add_row("Matching lines", str(len(lines)))

    if level_counts:
        summary.add_row("", "")
        for lvl in ["ERROR", "CRITICAL", "FATAL", "WARN", "WARNING", "INFO", "DEBUG", "TRACE"]:
            if lvl in level_counts:
                color = "red" if lvl in ("ERROR", "CRITICAL", "FATAL") else "yellow" if lvl in ("WARN", "WARNING") else "dim"
                summary.add_row(f"[{color}]{lvl}[/]", str(level_counts[lvl]))

    console.print(summary)

    # Show sample: first 5 error/critical lines
    error_lines = [l for l in lines if re.search(r"\b(ERROR|CRITICAL|FATAL)\b", l, re.IGNORECASE)]
    if error_lines:
        console.print("\n[bold red]Sample Errors:[/]")
        for line in error_lines[:5]:
            console.print(f"  [dim]│[/] {line[:120]}")

    # Heat score
    heat = sum(LEVEL_WEIGHT.get(lvl, 0) * cnt for lvl, cnt in level_counts.items())
    if heat >= 50:
        console.print(Panel("[red bold]⚠ High severity — review urgently[/]", title="Assessment"))
    elif heat >= 20:
        console.print(Panel("[yellow bold]Moderate issues detected[/]", title="Assessment"))
    else:
        console.print(Panel("[green]Looks clean[/]", title="Assessment"))

    # Export JSON report if requested
    if json_out:
        export_json({
            "file": str(path),
            "total_lines": total_lines,
            "matching_lines": len(lines),
            "level_counts": dict(level_counts),
            "heat_score": heat,
            "sample_errors": error_lines[:5],
        }, json_out)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <logfile> [--level ERROR] [--last 100] [--pattern 'regex']")
    else:
        analyze_log(sys.argv[1])
