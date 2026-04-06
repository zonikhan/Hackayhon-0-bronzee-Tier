#!/usr/bin/env python3
"""
Testing script to help verify the file processing workflow
"""

import os
import time
from pathlib import Path
import shutil


def create_test_file(filename, content):
    """Create a test file in the Incoming_Files folder"""
    incoming_path = Path("./Incoming_Files")
    incoming_path.mkdir(exist_ok=True)

    file_path = incoming_path / filename
    with open(file_path, 'w') as f:
        f.write(content)

    print(f"Created test file: {file_path}")
    return file_path


def check_folders():
    """Check the contents of all relevant folders"""
    folders = [
        "Incoming_Files",
        "Needs_Action",
        "Approved",
        "Done",
        "Vault/Daily",
        "Vault/Weekly",
        "Vault/Monthly",
        "Logs"
    ]

    print("\nCurrent folder contents:")
    for folder in folders:
        folder_path = Path(folder)
        if folder_path.exists():
            files = list(folder_path.glob("*"))
            print(f"{folder}: {len(files)} files")
            for file in files[:5]:  # Show first 5 files
                print(f"  - {file.name}")
            if len(files) > 5:
                print(f"  ... and {len(files)-5} more files")
        else:
            print(f"{folder}: DOES NOT EXIST")


def main():
    print("File Processing Workflow Test Script")
    print("=" * 40)

    while True:
        print("\nOptions:")
        print("1. Create a test file in Incoming_Files")
        print("2. Check all folder contents")
        print("3. Approve a plan file (manually edit it)")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            filename = input("Enter filename (e.g., test_request.md): ").strip()
            if not filename:
                filename = "test_request.md"

            content = input("Enter content for the file: ").strip()
            if not content:
                content = "# Test Request\n\nThis is a test request for the AI employee.\n\n## Details\n- Test task\n- Sample data"

            create_test_file(filename, content)
            print("Test file created. Wait a moment for the system to process it...")

        elif choice == "2":
            check_folders()

        elif choice == "3":
            print("\nTo approve a plan:")
            print("- Find the plan file in Vault/Daily/")
            print("- Edit it to change '## Approval Status:' from 'PENDING' to 'APPROVED'")
            print("- Save the file")
            print("- The system should detect the change and move the original file to Approved/")

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()