"""Main CLI entry point for DevDaily Tools."""

import click
from devdaily.file_organizer import organize_files
from devdaily.md_converter import convert_markdown
from devdaily.env_manager import manage_env
from devdaily.log_analyzer import analyze_log


@click.group()
@click.version_option(version="0.3.1", prog_name="devdaily")
def main():
    """DevDaily Tools - Streamline your daily development workflows."""
    pass


@main.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--by", "sort_by", type=click.Choice(["type", "date", "size"]), default="type",
              help="Sort files by type, date modified, or size.")
@click.option("--dry-run", is_flag=True, help="Preview changes without moving files.")
def organize(directory, sort_by, dry_run):
    """Organize files in DIRECTORY by type, date, or size."""
    organize_files(directory, sort_by, dry_run)


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", default=None, help="Output PDF file path.")
@click.option("--style", default="default", help="CSS style preset: default, minimal, dark.")
def md2pdf(input_file, output, style):
    """Convert a Markdown file to PDF."""
    convert_markdown(input_file, output, style)


@main.command()
@click.argument("action", type=click.Choice(["check", "diff", "sync"]))
@click.option("--required", default="", help="Comma-separated list of required env vars.")
@click.option("--file", "-f", default=".env", help="Path to .env file.")
@click.option("--other", default=None, help="Second .env file for diff/sync.")
def env(action, required, file, other):
    """Manage environment variables: check, diff, or sync .env files."""
    manage_env(action, required, file, other)


@main.command()
@click.argument("logfile", type=click.Path(exists=True))
@click.option("--level", "-l", default=None, help="Filter by log level (ERROR, WARN, INFO, DEBUG).")
@click.option("--last", "-n", default=None, type=int, help="Show only last N lines.")
@click.option("--pattern", "-p", default=None, help="Search for a regex pattern.")
@click.option("--json-out", "-j", default=None, help="Export analysis report to a JSON file.")
def log(logfile, level, last, pattern, json_out):
    """Analyze and summarize a log file."""
    analyze_log(logfile, level, last, pattern, json_out)


if __name__ == "__main__":
    main()
