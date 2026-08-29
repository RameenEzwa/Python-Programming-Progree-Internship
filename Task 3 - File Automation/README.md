# Task 3 - Automated File Operating & Text-Parsing Script

## Internship
Progree Internship

## Objective
Build a background-style automation utility that manages a local directory,
formats/sorts files, extracts useful text with regular expressions, and
writes the extracted information to a clean master CSV.

## Requirements Covered
- Standard Python libraries: `pathlib`, `shutil`, `re`, and `csv`
- Scans an unorganized local data folder
- Sorts files into subdirectories based on extension
- Uses regular expressions to extract:
  - email addresses
  - transaction IDs in the `TXN-YYYYMMDD-NNN` format
- Normalizes text content (line endings/trailing whitespace) before parsing
- Creates a clean master CSV
- Handles invalid paths and file-reading problems

## Run the Project

From this directory:

```bash
python task3_file_automation.py sample_data -o master_records.csv
```

The source directory is organized in place. A generated `master_records.csv`
is created outside the source directory.

## Expected Folder Organization

Before:

```text
sample_data/
├── archive.zip
├── image1.jpg
├── notes.md
├── report1.txt
├── server.log
└── transactions.log
```

After:

```text
sample_data/
├── jpg/
├── log/
├── md/
├── txt/
└── zip/
```

## CSV Columns

- `source_file`
- `line_number`
- `email`
- `transaction_id`

## Regex Patterns

Email:

```text
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b
```

Transaction ID:

```text
\bTXN-\d{8}-\d{3}\b
```

The transaction pattern deliberately rejects malformed IDs such as
`BAD-003`.
