"""Markdown to PDF converter with style presets."""

import os
from pathlib import Path
from rich.console import Console

console = Console()

STYLE_PRESETS = {
    "default": """
        body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }
        h1 { border-bottom: 2px solid #0366d6; padding-bottom: 8px; }
        h2 { border-bottom: 1px solid #eaecef; padding-bottom: 6px; }
        code { background: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }
        pre { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; }
        pre code { background: none; padding: 0; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #dfe2e5; padding: 8px 12px; text-align: left; }
        th { background: #f6f8fa; }
        blockquote { border-left: 4px solid #0366d6; padding-left: 16px; color: #6a737d; margin: 16px 0; }
    """,
    "minimal": """
        body { font-family: Georgia, serif; max-width: 650px; margin: 60px auto; padding: 20px; line-height: 1.8; color: #222; }
        h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; }
        code { font-size: 0.9em; }
        pre { padding: 12px; background: #f9f9f9; border-left: 3px solid #ccc; }
    """,
    "dark": """
        body { font-family: 'Fira Code', 'Consolas', monospace; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; background: #1e1e1e; color: #d4d4d4; }
        h1, h2, h3 { color: #569cd6; }
        a { color: #4ec9b0; }
        code { background: #2d2d2d; padding: 2px 6px; border-radius: 3px; color: #ce9178; }
        pre { background: #2d2d2d; padding: 16px; border-radius: 6px; }
        pre code { background: none; color: #d4d4d4; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #444; padding: 8px 12px; text-align: left; }
        th { background: #2d2d2d; }
    """,
}


def convert_markdown(input_file: str, output: str = None, style: str = "default"):
    """Convert a Markdown file to styled PDF."""
    try:
        import markdown
        import pdfkit
    except ImportError:
        console.print("[red]Missing dependencies.[/] Install with: pip install devdaily-tools[pdf]")
        return

    input_path = Path(input_file).resolve()
    if not input_path.exists():
        console.print(f"[red]Error:[/] File not found: {input_file}")
        return

    md_content = input_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(md_content, extensions=["extra", "codehilite", "tables", "toc"])

    css = STYLE_PRESETS.get(style, STYLE_PRESETS["default"])
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{css}</style></head>
<body>{html_body}</body>
</html>"""

    output_path = Path(output) if output else input_path.with_suffix(".pdf")
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdfkit.from_string(html, str(output_path))
    console.print(f"[green]✓[/] PDF saved: {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python md_converter.py <markdown_file> [--style default|minimal|dark] [-o output.pdf]")
    else:
        convert_markdown(sys.argv[1])
