# DevDaily Tools

A practical CLI toolkit for developers to streamline daily workflows — file organization, markdown conversion, environment variable management, and log analysis.

> **Why DevDaily?** Modern developers juggle dozens of micro-tasks every day — renaming files in bulk, converting docs, managing .env files across projects, parsing logs. These aren't complex problems, but they eat up time. DevDaily collects these utilities into one lightweight, pip-installable tool so you can stay in the terminal and keep moving.

## Features

| Tool | Command | Description |
|------|---------|-------------|
| File Organizer | `devdaily organize` | Auto-sort files by type/date/size into folders |
| MD Converter | `devdaily md2pdf` | Convert Markdown to PDF with custom styling |
| Env Manager | `devdaily env` | Validate, diff, and sync .env files across projects |
| Log Analyzer | `devdaily log` | Parse and summarize log files with pattern search |

## Installation

```bash
pip install devdaily-tools
```

Or from source:

```bash
git clone https://github.com/Shek-YH/devdaily-tools.git
cd devdaily-tools
pip install -e .
```

## Quick Start

```bash
# Organize a messy downloads folder
devdaily organize ~/Downloads --by type

# Convert a markdown file to PDF
devdaily md2pdf README.md -o README.pdf

# Check .env for missing variables
devdaily env check --required "DB_HOST,DB_PORT,API_KEY"

# Analyze errors in a log file
devdaily log app.log --level ERROR --last 100
```

## Requirements

- Python 3.8+
- wkhtmltopdf (optional, for md2pdf)

## Roadmap

- [ ] Add YAML/JSON config file support for `organize`
- [ ] Watch mode for `log` (tail -f style)
- [ ] `.env` template generation wizard
- [ ] Plugin system for custom commands

## Contributing

PRs and issues welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License — see [LICENSE](LICENSE) for details.
