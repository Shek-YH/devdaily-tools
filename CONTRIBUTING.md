# Contributing to DevDaily Tools

Thanks for your interest in contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/devdaily-tools.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Install in dev mode: `pip install -e .`

## Development Setup

```bash
pip install -e ".[pdf]"
```

Run tests:

```bash
python -m pytest tests/
```

## Code Style

- Follow PEP 8
- Use type hints where practical
- Keep functions focused and single-purpose
- Add docstrings for public functions

## Pull Request Process

1. Update the README if your change adds a new feature
2. Add yourself to contributors if you wish
3. PRs require one approving review before merge

## Adding a New Tool

1. Create a new module in `devdaily/`
2. Add the CLI command in `devdaily/cli.py`
3. Update README table with the new command
