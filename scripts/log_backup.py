#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

REPORT_DIR = BASE_DIR / "reports"
BACKUP_DIR = BASE_DIR / "backups"

REPORT_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)


def get_timestamp():

    result = subprocess.run(
        ["date", "+%Y%m%d_%H%M%S"],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip()


def analyze_logs(log_file):

    if not log_file.exists():
        print("Log file not found!")
        return

    errors = []
    warnings = []
    info = []

    with log_file.open("r", encoding="utf-8", errors="replace") as file:

        for line in file:

            upper_line = line.upper()

            if "ERROR" in upper_line:
                errors.append(line.strip())

            elif "WARNING" in upper_line:
                warnings.append(line.strip())

            elif "INFO" in upper_line:
                info.append(line.strip())

    report_file = REPORT_DIR / f"log_report_{get_timestamp()}.txt"

    with report_file.open("w", encoding="utf-8") as report:

        report.write("LINUX LOG ANALYSIS REPORT\n")
        report.write("=" * 40 + "\n\n")

        report.write(f"Log file: {os.path.basename(log_file)}\n\n")

        report.write(f"ERROR COUNT: {len(errors)}\n")
        report.write(f"WARNING COUNT: {len(warnings)}\n")
        report.write(f"INFO COUNT: {len(info)}\n\n")

        report.write("ERROR DETAILS\n")

        for error in errors:
            report.write(error + "\n")

        report.write("\nWARNING DETAILS\n")

        for warning in warnings:
            report.write(warning + "\n")

    print("\nLOG ANALYSIS COMPLETED")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Info: {len(info)}")
    print(f"Report: {report_file}")


def create_backup(source):

    if not source.exists() or not source.is_dir():
        print("Invalid source directory!")
        return

    backup_path = BACKUP_DIR / f"backup_{get_timestamp()}"

    try:

        shutil.copytree(source, backup_path)

        print("\nBACKUP COMPLETED")
        print(f"Backup location: {backup_path}")

    except OSError as error:
        print(f"Backup failed: {error}")


def verify_backup(source, backup):

    if not source.is_dir() or not backup.is_dir():
        print("Source or backup directory not found!")
        return

    result = subprocess.run(
        ["diff", "-qr", str(source), str(backup)],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        print("\nBACKUP VERIFICATION SUCCESSFUL")
        print("Source and backup are identical.")

    elif result.returncode == 1:

        print("\nBACKUP VERIFICATION FAILED")
        print(result.stdout)

    else:

        print("Verification error:")
        print(result.stderr)


def restore_backup(backup, destination):

    if not backup.is_dir():
        print("Backup directory not found!")
        return

    if destination.exists():
        print("Destination already exists!")
        return

    try:

        shutil.copytree(backup, destination)

        print("\nRESTORE COMPLETED")
        print(f"Restored location: {destination}")

    except OSError as error:
        print(f"Restore failed: {error}")


def main():

    while True:

        print("\n===== LINUX LOG & BACKUP SYSTEM =====")
        print("1. Analyze Logs")
        print("2. Create Backup")
        print("3. Verify Backup")
        print("4. Restore Backup")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            log_file = Path(input("Enter log file path: "))
            analyze_logs(log_file)

        elif choice == "2":

            source = Path(input("Enter source directory: "))
            create_backup(source)

        elif choice == "3":

            source = Path(input("Enter original directory: "))
            backup = Path(input("Enter backup directory: "))
            verify_backup(source, backup)

        elif choice == "4":

            backup = Path(input("Enter backup directory: "))
            destination = Path(input("Enter restore destination: "))
            restore_backup(backup, destination)

        elif choice == "5":

            print("Exiting program...")
            break

        else:

            print("Invalid choice!")


if __name__ == "__main__":
    main()
