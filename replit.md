# Podcast Transcript Processing Tool

## Overview

This is a Python-based data processing tool for managing podcast episode metadata. The project transforms podcast episode data from a wide-format CSV export (from Google Sheets) into normalized database-ready tables. It processes episode metadata and extracts domain categorizations into a separate long-format table for relational database storage.

The tool reads a single input CSV file containing episode metadata with domain columns (prefixed with `domain_`), and outputs two CSV files:
- `episodes.csv` - Core episode metadata
- `episode_domains.csv` - Long-format domain associations

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Data Processing Pipeline

**Problem**: Podcast episode metadata is stored in a denormalized "wide" format from Google Sheets, with boolean domain flags as separate columns. This format is not ideal for database storage or querying.

**Solution**: A Python script (`main.py`) that:
1. Reads the wide-format CSV input
2. Normalizes boolean values (handles various truthy/falsy string representations)
3. Splits domain columns into a separate relational table
4. Outputs two normalized CSV files ready for database import

**Design Decisions**:
- Uses Python's built-in `csv` module rather than pandas for simplicity and minimal dependencies
- Domain columns are identified by a configurable prefix (`domain_`)
- Boolean normalization handles common spreadsheet variations (true/false, yes/no, 1/0, t/f, y/n)
- UTF-8 with BOM handling for Google Sheets compatibility

### Frontend (Domain Constellation Viewer)

A browser-based interactive force graph visualization showing domain co-occurrences across podcast episodes. Built with the ForceGraph library, served via a simple Python HTTP server (`server.py`) on port 5000.

### File Structure

```
├── server.py                            # HTTP server serving frontend on port 5000
├── main.py                              # Data processing script
├── Wide_EPISODES METADATA_Anthropic.csv # Input file (Google Sheets export)
├── episodes.csv                         # Output: episode metadata
├── episode_domains.csv                  # Output: domain associations
├── frontend/                            # Web frontend
│   ├── index.html                       # Main HTML page
│   ├── app.js                           # Force graph visualization logic
│   ├── style.css                        # Styling
│   └── data/                            # JSON datasets for the graph
│       ├── domain_constellation.json
│       ├── domain_constellation_pre_ai.json
│       ├── domain_constellation_transition.json
│       └── domain_constellation_post_ai.json
└── transcripts/                         # Raw podcast transcript files (50 episodes)
    └── aPM-*.txt                        # Individual episode transcripts
```

### Data Model

**Episodes Table**: Contains core metadata fields (extracted from non-domain columns)

**Episode Domains Table**: Long-format table linking episodes to their domain categorizations
- Each row represents one episode-domain relationship
- Domain values are converted to 0/1 integers

## External Dependencies

**Runtime Dependencies**:
- Python 3.x standard library only (`csv`, `pathlib`)
- No external packages required

**Input Requirements**:
- Google Sheets CSV export named `Wide_EPISODES METADATA_Anthropic.csv`
- Expected encoding: UTF-8 with BOM

**Output Format**:
- Standard CSV files suitable for database import or further processing