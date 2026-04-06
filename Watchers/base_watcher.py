#!/usr/bin/env python3
"""
Personal AI Employee - Base Watcher Class

Base class for all watchers that monitor external systems
and generate structured .md files in the /Needs_Action folder.
"""

import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class BaseWatcher(ABC):
    """Abstract base class for all watchers"""

    def __init__(self, name, needs_action_path):
        self.name = name
        self.needs_action_path = Path(needs_action_path)
        self.running = False

    @abstractmethod
    def check_for_events(self):
        """Check for new events in the monitored system"""
        pass

    @abstractmethod
    def generate_markdown_content(self, event_data):
        """Generate structured markdown content from event data"""
        pass

    def create_action_file(self, content, filename_suffix=""):
        """Create a markdown file in the Needs_Action folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if filename_suffix:
            filename = f"{self.name}_{filename_suffix}_{timestamp}.md"
        else:
            filename = f"{self.name}_action_{timestamp}.md"

        filepath = self.needs_action_path / filename

        with open(filepath, 'w') as f:
            f.write(content)

        print(f"Created action file: {filepath}")
        return filepath

    def start_monitoring(self):
        """Start the monitoring loop"""
        self.running = True
        print(f"Starting {self.name} watcher...")

        while self.running:
            try:
                events = self.check_for_events()
                if events:
                    for event in events:
                        content = self.generate_markdown_content(event)
                        self.create_action_file(content)

                time.sleep(self.get_check_interval())

            except KeyboardInterrupt:
                print(f"\nStopping {self.name} watcher...")
                self.running = False
            except Exception as e:
                print(f"Error in {self.name} watcher: {str(e)}")
                time.sleep(self.get_error_retry_interval())

    def get_check_interval(self):
        """Return the interval between checks (default 60 seconds)"""
        return 60

    def get_error_retry_interval(self):
        """Return the retry interval after an error (default 60 seconds)"""
        return 60


class FileDropWatcher(BaseWatcher):
    """Watcher for file drop events"""

    def __init__(self, needs_action_path, watch_folder):
        super().__init__("FileDrop", needs_action_path)
        self.watch_folder = Path(watch_folder)
        self.processed_files = {}  # Track processed files to prevent duplicates

    def check_for_events(self):
        """Check for new files in the watched folder"""
        if not self.watch_folder.exists():
            return []

        events = []
        current_time = time.time()

        for file_path in self.watch_folder.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                # Get file stats
                stat_info = file_path.stat()
                file_modified = stat_info.st_mtime

                # Check if this file was recently modified (last 5 minutes)
                if (current_time - file_modified) < 300:
                    # Check if we've already processed this file based on its modification time
                    file_key = f"{file_path.name}_{int(file_modified)}"

                    # If we've seen this file with this modification time recently, skip it
                    if file_key in self.processed_files:
                        # Check if the cached info is still recent (less than 10 seconds old)
                        if (current_time - self.processed_files[file_key]) < 10:
                            continue

                    # Cache this file with current timestamp
                    self.processed_files[file_key] = current_time

                    # Clean up old entries (older than 1 minute)
                    keys_to_remove = []
                    for key, timestamp in self.processed_files.items():
                        if (current_time - timestamp) > 60:
                            keys_to_remove.append(key)
                    for key in keys_to_remove:
                        del self.processed_files[key]

                    events.append({
                        'type': 'file_drop',
                        'file_path': str(file_path),
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_modified).isoformat()
                    })

        return events

    def generate_markdown_content(self, event_data):
        """Generate markdown content for a file drop event"""
        return f"""# New File Dropped

## Event Details
- Type: {event_data['type']}
- File: {event_data['file_path']}
- Size: {event_data['size']} bytes
- Modified: {event_data['modified']}

## Action Required
Please review the dropped file and determine appropriate next steps.

## Context
This file was dropped into the monitored folder and requires attention.
"""


class EmailWatcher(BaseWatcher):
    """Watcher for email events (placeholder implementation)"""

    def __init__(self, needs_action_path, email_config):
        super().__init__("Email", needs_action_path)
        self.email_config = email_config

    def check_for_events(self):
        """Check for new emails (placeholder)"""
        # This would connect to email server and check for new messages
        # For now, return empty list
        return []

    def generate_markdown_content(self, event_data):
        """Generate markdown content for an email event"""
        return f"""# New Email Received

## Email Details
- From: {event_data.get('from', 'Unknown')}
- Subject: {event_data.get('subject', 'No Subject')}
- Date: {event_data.get('date', 'Unknown')}

## Message Preview
{event_data.get('preview', 'No preview available')}

## Action Required
Review the email and determine if any action is needed.
"""


def main():
    """Example usage of watchers"""
    base_path = Path(__file__).parent
    needs_action_path = base_path / "Needs_Action"

    # Create a file drop watcher
    watch_folder = base_path / "Incoming_Files"  # Create this folder separately
    if not watch_folder.exists():
        watch_folder.mkdir(parents=True, exist_ok=True)

    file_watcher = FileDropWatcher(needs_action_path, watch_folder)

    # Start monitoring
    file_watcher.start_monitoring()


if __name__ == "__main__":
    main()