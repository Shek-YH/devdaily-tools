# Changelog

All notable changes to DevDaily Tools will be documented in this file.

## [Unreleased]

### Added
- JSON report export option for log analyzer (`--json-out` / `-j`)
- `.env.example` template generator (`devdaily env example`)
- Automatic filename conflict resolution in file organizer (avoids overwrites)

### Fixed
- File organizer now handles name collisions by appending numeric suffixes

## [0.3.1] - 2026-05-31

### Added
- Initial public release with four CLI tools
- `devdaily organize` — sort files by type, date, or size
- `devdaily md2pdf` — convert Markdown to PDF
- `devdaily env` — check, diff, and sync environment variables
- `devdaily log` — parse and summarize log files
- MIT license, README with roadmap, and contributing guidelines
