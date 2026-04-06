#!/usr/bin/env python3
"""
Utility to approve a plan file by updating its status
"""

import sys
from pathlib import Path


def approve_plan(plan_file_path):
    """Approve a plan by updating its Approval Status to APPROVED"""
    plan_path = Path(plan_file_path)

    if not plan_path.exists():
        print(f"Error: Plan file does not exist: {plan_file_path}")
        return False

    # Read the current content
    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update the approval status
    updated_content = content.replace("## Approval Status:\nPENDING", "## Approval Status:\nAPPROVED")

    # If it was already approved, we still want to make sure the status is correct
    if "## Approval Status:\nAPPROVED" not in updated_content:
        # If the status wasn't pending, add or update it
        if "## Approval Status:" in updated_content:
            updated_content = updated_content.replace(
                "## Approval Status:\n",
                "## Approval Status:\nAPPROVED\n"
            )
        else:
            # If there's no approval status section, add it
            updated_content += "\n## Approval Status:\nAPPROVED\n"

    # Write the updated content back
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Plan approved: {plan_file_path}")
    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python approve_plan.py <plan_file_path>")
        sys.exit(1)

    plan_file_path = sys.argv[1]
    success = approve_plan(plan_file_path)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()