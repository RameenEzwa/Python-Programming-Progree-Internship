"""
Task 3: Automated File Operating & Text-Parsing Script
Progree Internship

The utility:
1. Scans a local directory.
2. Creates extension-based subdirectories.
3. Moves files into their matching folders.
4. Reads text/log files.
5. Extracts email addresses and transaction IDs with regex.
6. Writes all extracted records to a clean master CSV.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

TRANSACTION_PATTERN = re.compile(
    r"\bTXN-\d{8}-\d{3}\b"
)

TEXT_EXTENSIONS = {".txt", ".log", ".md"}


def normalize_extension(extension: str) -> str:
    """Return a safe folder name for a file extension."""
    extension = extension.lower().strip()
    return extension[1:] if extension.startswith(".") else extension


def organize_files(source_dir: Path) -> dict[str, int]:
    """
    Sort files in source_dir into extension-based subdirectories.

    Returns a count of moved files by extension.
    Existing destination folders are skipped during the scan.
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")

    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_dir}")

    moved_counts: dict[str, int] = {}

    for item in source_dir.iterdir():
        if not item.is_file():
            continue

        folder_name = normalize_extension(item.suffix) or "no_extension"
        destination_dir = source_dir / folder_name
        destination_dir.mkdir(exist_ok=True)

        destination = destination_dir / item.name

        # Avoid overwriting an existing file.
        if destination.exists():
            stem = destination.stem
            suffix = destination.suffix
            counter = 1
            while destination.exists():
                destination = destination_dir / f"{stem}_{counter}{suffix}"
                counter += 1

        shutil.move(str(item), str(destination))
        moved_counts[folder_name] = moved_counts.get(folder_name, 0) + 1

    return moved_counts


def format_text_content(text: str) -> str:
    """
    Normalize text for reliable parsing without modifying the original file.
    It standardizes line endings and removes trailing whitespace.
    """
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in normalized.split("\n"))


def parse_text_file(file_path: Path) -> list[dict[str, str]]:
    """
    Extract valid email addresses and transaction IDs from a text file.

    A record is created for each transaction ID found. If a valid email
    occurs on the same line, it is associated with that transaction.
    Lines containing only an email are also recorded with a blank ID.
    """
    records: list[dict[str, str]] = []

    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as error:
        print(f"Warning: could not read {file_path}: {error}")
        return records

    text = format_text_content(text)

    for line_number, line in enumerate(text.splitlines(), start=1):
        emails = EMAIL_PATTERN.findall(line)
        transactions = TRANSACTION_PATTERN.findall(line)

        if transactions:
            for transaction_id in transactions:
                records.append({
                    "source_file": file_path.name,
                    "line_number": str(line_number),
                    "email": emails[0] if emails else "",
                    "transaction_id": transaction_id,
                })
        elif emails:
            for email in emails:
                records.append({
                    "source_file": file_path.name,
                    "line_number": str(line_number),
                    "email": email,
                    "transaction_id": "",
                })

    return records


def collect_records(source_dir: Path) -> list[dict[str, str]]:
    """Parse text/log files after organization."""
    records = []

    for file_path in sorted(source_dir.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() in TEXT_EXTENSIONS:
            records.extend(parse_text_file(file_path))

    return records


def write_master_csv(records: list[dict[str, str]], output_path: Path) -> None:
    """Write extracted records to a clean master CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["source_file", "line_number", "email", "transaction_id"]

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def run_automation(source_dir: Path, output_csv: Path) -> dict:
    """Run the complete file organization and parsing workflow."""
    if output_csv.resolve().parent == source_dir.resolve():
        # Keep generated CSV outside the scan's top level when possible.
        raise ValueError(
            "Place the master CSV outside the source directory to avoid "
            "processing the generated output on future runs."
        )

    moved_counts = organize_files(source_dir)
    records = collect_records(source_dir)
    write_master_csv(records, output_csv)

    return {
        "moved_counts": moved_counts,
        "records": records,
        "output_csv": output_csv,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize files, parse text/log data, and create a master CSV."
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Directory containing the unorganized files",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("master_records.csv"),
        help="Path for the generated master CSV",
    )
    args = parser.parse_args()

    try:
        result = run_automation(args.source, args.output)
    except (FileNotFoundError, NotADirectoryError, ValueError) as error:
        parser.error(str(error))

    print("=" * 60)
    print("TASK 3 - FILE AUTOMATION & TEXT PARSING")
    print("=" * 60)
    print("\nFiles organized:")
    for extension, count in sorted(result["moved_counts"].items()):
        print(f"  {extension}/ -> {count} file(s)")

    print(f"\nParsed records: {len(result['records'])}")
    print(f"Master CSV: {result['output_csv'].resolve()}")
    print("\nExtracted records:")
    for record in result["records"]:
        print(
            f"  {record['source_file']} | line {record['line_number']} | "
            f"{record['email'] or '(no email)'} | "
            f"{record['transaction_id'] or '(no transaction ID)'}"
        )


if __name__ == "__main__":
    main()
