#!/usr/bin/env python3
"""
Create GitHub Issues from saved migration records
Run this after authenticating with GitHub CLI
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime


def create_migration_issue(project):
    """Create GitHub Issue from migration record"""

    title = f"[MIGRATION] {project['title']}"
    body = f"""# Migrated from Archon

**Project ID**: `{project['id']}`
**Created**: {project['created_at']}
**Updated**: {project['updated_at']}

## Description
{project['description']}

## GitHub Repo
{project.get('github_repo', 'Not set')}

## Migration Status
- [ ] Project structure created in AutoFlow
- [ ] Tasks migrated to GitHub Issues
- [ ] Documents migrated to `.autoflow/` directory
- [ ] Context firewalls set up
- [ ] Git worktrees configured

## Original Archon Data
Saved to: `.autoflow/migrations/archon-{project['id']}.json`

---
*Auto-migrated from Archon to AutoFlow*
"""

    labels = ["migration", "from-archon", "project-setup"]

    cmd = [
        '/opt/homebrew/bin/gh', 'issue', 'create',
        '--title', title,
        '--body', body,
        '--label', ','.join(labels)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                              cwd="/Users/samiullah/AutoFlow")
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


def main():
    """Create GitHub Issues from all migration records"""

    print("="*60)
    print("🔄 Creating GitHub Issues from Migration Records")
    print("="*60)
    print("")

    # Check GitHub CLI authentication
    try:
        result = subprocess.run(['/opt/homebrew/bin/gh', 'auth', 'status'],
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ GitHub CLI not authenticated")
            print("   Run: /opt/homebrew/bin/gh auth login")
            return
    except Exception as e:
        print(f"❌ Error checking GitHub auth: {e}")
        return

    print("✅ GitHub CLI authenticated\n")

    # Find migration records
    migrations_dir = Path("/Users/samiullah/AutoFlow/.autoflow/migrations")
    if not migrations_dir.exists():
        print("❌ No migrations directory found")
        return

    migration_files = list(migrations_dir.glob("archon-*.json"))
    if not migration_files:
        print("❌ No migration records found")
        return

    print(f"Found {len(migration_files)} migration records\n")

    # Create issues for each migration
    created = 0
    for migration_file in migration_files:
        with open(migration_file, 'r') as f:
            record = json.load(f)

        # Skip if issue already created
        if record.get("github_issue"):
            print(f"⏭️  Skipping {record['project']['title']} (already has issue)")
            continue

        print(f"\n{'='*60}")
        print(f"📦 Creating issue for: {record['project']['title']}")
        print(f"{'='*60}\n")

        issue_url = create_migration_issue(record['project'])

        if issue_url:
            # Update migration record with issue URL
            record["github_issue"] = issue_url
            record["issue_created_at"] = datetime.now().isoformat()

            with open(migration_file, 'w') as f:
                json.dump(record, f, indent=2)

            created += 1

    print(f"\n{'='*60}")
    print("✅ COMPLETE")
    print(f"{'='*60}\n")
    print(f"📊 Created {created} GitHub Issues")
    print(f"   View: /opt/homebrew/bin/gh issue list --label 'migration'")
    print("")


if __name__ == '__main__':
    main()
