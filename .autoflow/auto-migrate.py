#!/usr/bin/env python3
"""
Automated Archon → AutoFlow Migration
Reads Archon data directly and creates GitHub Issues
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

# Archon projects data (from mcp__archon__find_projects)
ARCHON_DATA = {"success": True, "projects": [{"id": "3a4c3aa3-fdc2-4de7-9f42-96bdf13ce519", "title": "AutoFlow - Complete Git-Native AI Workflow System", "description": "Complete git-native workflow system combining CCPM, BMAD-METHOD, Backlog.md, Context Forge, Claude Hooks, Design Review, and AppSec Guardian. Features: GitHub Issues integration, git worktrees for parallel execution, context firewalls, MCP resource pattern, PreCompact hook, human-in-the-loop checkpoints, design system integration for UI prevention, scale-adaptive intelligence (Quick/Standard/Enterprise), and real agent orchestration.", "github_repo": "https://github.com/your-username/autoflow", "created_at": "2025-11-10T06:46:10.059487+00:00", "updated_at": "2025-11-10T06:46:10.0595+00:00", "docs": [], "features": {}, "data": {}, "technical_sources": [], "business_sources": [], "pinned": False}, {"id": "6093d8de-43be-40a9-ba7d-6a632c8d9f50", "title": "ProductionForge - AI Agent Workflow System", "description": "ProductionForge - COMPLETE! A lean, git-native workflow system that solves UI hallucination through design system integration, visual validation, and Claude SDK agent orchestration.", "github_repo": "https://github.com/your-username/productionforge", "created_at": "2025-11-10T04:52:10.468788+00:00", "updated_at": "2025-11-10T06:38:05.188415+00:00", "docs": [], "features": {}, "data": {}, "technical_sources": [], "business_sources": [], "pinned": False}]}


def map_status(archon_status):
    """Map Archon status to AutoFlow status"""
    mapping = {
        "todo": "todo",
        "doing": "in_progress",
        "in_progress": "in_progress",
        "review": "review",
        "done": "completed"
    }
    return mapping.get(str(archon_status).lower(), "todo")


def create_migration_issue(project):
    """Create GitHub Issue to track migration for a project"""

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
        result = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/samiullah/AutoFlow")
        if result.returncode == 0:
            issue_url = result.stdout.strip()
            print(f"✅ Migration tracking issue: {issue_url}")
            return issue_url
        else:
            print(f"⚠️  Failed to create migration issue: {result.stderr}")
            return None
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return None


def save_migration_record(project, issue_url):
    """Save migration record"""

    migrations_dir = Path("/Users/samiullah/AutoFlow/.autoflow/migrations")
    migrations_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "migrated_at": datetime.now().isoformat(),
        "source": "archon",
        "archon_project_id": project['id'],
        "project": project,
        "github_issue": issue_url,
        "status": "migrated"
    }

    record_file = migrations_dir / f"archon-{project['id']}.json"
    with open(record_file, 'w') as f:
        json.dump(record, f, indent=2)

    print(f"📄 Migration record saved: {record_file}")
    return record_file


def migrate_all_projects():
    """Migrate all Archon projects"""

    print("="*60)
    print("🔄 Archon → AutoFlow Migration")
    print("="*60)
    print("")

    projects = ARCHON_DATA.get("projects", [])
    print(f"Found {len(projects)} Archon projects to migrate\n")

    # Check if GitHub CLI is authenticated
    try:
        result = subprocess.run(['/opt/homebrew/bin/gh', 'auth', 'status'],
                              capture_output=True, text=True)
        gh_authenticated = result.returncode == 0
    except Exception:
        gh_authenticated = False

    if not gh_authenticated:
        print("⚠️  GitHub CLI not authenticated")
        print("   Saving migration data only (no GitHub Issues will be created)")
        print("")

    migrated = []
    for project in projects:
        print(f"\n{'='*60}")
        print(f"📦 Migrating: {project['title']}")
        print(f"{'='*60}\n")

        # Save migration record first
        record_file = save_migration_record(project, None)

        migration_entry = {
            "project_id": project['id'],
            "project_title": project['title'],
            "record_file": str(record_file),
            "github_issue": None
        }

        # Try to create migration tracking issue if authenticated
        if gh_authenticated:
            issue_url = create_migration_issue(project)
            if issue_url:
                migration_entry["github_issue"] = issue_url
                # Update record with issue URL
                with open(record_file, 'r') as f:
                    record = json.load(f)
                record["github_issue"] = issue_url
                with open(record_file, 'w') as f:
                    json.dump(record, f, indent=2)

        migrated.append(migration_entry)

    # Create summary
    summary_dir = Path("/Users/samiullah/AutoFlow/.autoflow/migrations")
    summary_dir.mkdir(parents=True, exist_ok=True)
    summary_file = summary_dir / f"migration-summary-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

    summary = {
        "migrated_at": datetime.now().isoformat(),
        "total_projects": len(projects),
        "successfully_migrated": len(migrated),
        "github_issues_created": len([m for m in migrated if m["github_issue"]]),
        "migrations": migrated
    }

    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print("✅ MIGRATION COMPLETE")
    print(f"{'='*60}\n")
    print(f"📊 Summary:")
    print(f"   Total projects: {summary['total_projects']}")
    print(f"   Migration records saved: {summary['successfully_migrated']}")
    print(f"   GitHub Issues created: {summary['github_issues_created']}")
    print(f"   Summary file: {summary_file}\n")

    if not gh_authenticated:
        print("📋 To Create GitHub Issues:")
        print("   1. Authenticate: /opt/homebrew/bin/gh auth login")
        print("   2. Run: python3 .autoflow/create-issues-from-migrations.py")
        print("")
    else:
        print("📋 Next Steps:")
        print("   1. Review migration issues: gh issue list --label 'migration'")
        print("   2. Check migration records: ls -la .autoflow/migrations/")
        print("   3. Start using AutoFlow: ./autoflow 'your task'")
        print("")

    print("⚠️  IMPORTANT: Archon is UNTOUCHED and still working!")
    print("   You can use both systems in parallel.")
    print("")


if __name__ == '__main__':
    migrate_all_projects()
