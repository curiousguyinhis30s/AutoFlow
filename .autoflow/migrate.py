#!/usr/bin/env python3
"""
Simple Archon → AutoFlow Migration

Uses direct MCP calls to fetch Archon data and create AutoFlow structure.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def get_archon_projects():
    """Get projects via archon MCP - to be called by Claude Code"""
    print("📊 To migrate from Archon, I need you to run:")
    print("")
    print("In Claude Code, use the Archon MCP tool:")
    print("  mcp__archon__find_projects()")
    print("")
    print("This will list all your Archon projects.")
    print("Then copy the output here.")
    print("")
    return None


def map_status(archon_status):
    """Map Archon status to AutoFlow"""
    mapping = {
        "todo": "todo",
        "doing": "in_progress",
        "in_progress": "in_progress",
        "review": "review",
        "done": "completed"
    }
    return mapping.get(archon_status.lower(), "todo")


def create_github_issue(title, description, status, assignee):
    """Create GitHub Issue from task"""

    issue_title = f"[MIGRATED] {title}"
    issue_body = f"""Migrated from Archon

{description}

**Status:** {status}
**Assignee:** {assignee}
"""

    labels = ["migrated-from-archon", f"status:{status}"]

    cmd = [
        '/opt/homebrew/bin/gh', 'issue', 'create',
        '--title', issue_title,
        '--body', issue_body,
        '--label', ','.join(labels)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            issue_url = result.stdout.strip()
            print(f"✅ Created: {issue_url}")
            return issue_url
        else:
            print(f"⚠️  Failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return None


def migrate_project_interactive():
    """Interactive migration"""

    print("="*60)
    print("🔄 Archon → AutoFlow Migration (Interactive)")
    print("="*60)
    print("")

    print("Step 1: Get your Archon project data")
    print("")
    print("In Claude Code, run these MCP tools:")
    print("")
    print("  1. mcp__archon__find_projects()")
    print("     (Lists all projects)")
    print("")
    print("  2. mcp__archon__find_tasks(project_id='your-project-id')")
    print("     (Gets all tasks for a project)")
    print("")
    print("  3. mcp__archon__find_documents(project_id='your-project-id')")
    print("     (Gets all documents)")
    print("")

    print("Step 2: Paste the JSON data when prompted")
    print("")

    # Get project data
    print("Paste your Archon project JSON (or 'skip' to skip):")
    print("")

    try:
        lines = []
        while True:
            line = input()
            if line.strip().lower() == 'skip':
                print("Skipping interactive mode.")
                return
            if line.strip() == '':
                break
            lines.append(line)

        if not lines:
            print("No data entered.")
            return

        project_json = '\n'.join(lines)
        project_data = json.loads(project_json)

        # Extract project info
        project_name = project_data.get('title', 'Migrated Project')
        print(f"\n📋 Migrating: {project_name}")
        print("")

        # Get tasks
        if 'tasks' in project_data:
            tasks = project_data['tasks']
            print(f"Found {len(tasks)} tasks")
            print("")

            response = input("Create GitHub Issues for these tasks? [yes/no]: ")
            if response.lower() in ['yes', 'y']:
                for task in tasks:
                    title = task.get('title', 'Untitled')
                    description = task.get('description', '')
                    status = map_status(task.get('status', 'todo'))
                    assignee = task.get('assignee', 'User')

                    create_github_issue(title, description, status, assignee)

        # Save migration record
        migrations_dir = Path.cwd() / ".autoflow" / "migrations"
        migrations_dir.mkdir(parents=True, exist_ok=True)

        migration_record = {
            "migrated_at": datetime.now().isoformat(),
            "source": "archon",
            "project": project_data
        }

        migration_file = migrations_dir / f"archon-migration-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(migration_file, 'w') as f:
            json.dump(migration_record, f, indent=2)

        print("")
        print(f"✅ Migration complete!")
        print(f"   Record saved: {migration_file}")
        print("")

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main entry point"""

    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
Archon → AutoFlow Migration Tool

Usage:
  python3 .autoflow/migrate.py              # Interactive mode

Interactive Mode:
  1. Run mcp__archon__find_projects() in Claude Code
  2. Copy the project JSON
  3. Run this script
  4. Paste the JSON when prompted
  5. Script creates GitHub Issues for all tasks

The script will:
  - Parse Archon project data
  - Map task statuses (todo/doing/review/done)
  - Create GitHub Issues with proper labels
  - Save migration record in .autoflow/migrations/

Archon stays untouched. This only reads data and creates
new GitHub Issues in your AutoFlow project.
""")
        return

    migrate_project_interactive()


if __name__ == '__main__':
    main()
