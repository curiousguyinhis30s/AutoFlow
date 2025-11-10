#!/usr/bin/env python3
"""
Migrate from Archon to AutoFlow

Reads Archon projects and migrates them to AutoFlow format.
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ArchonToAutoFlowMigration:
    """Migrate projects from Archon MCP to AutoFlow"""

    def __init__(self):
        self.autoflow_dir = Path.cwd() / ".autoflow"
        self.migrations_dir = self.autoflow_dir / "migrations"
        self.migrations_dir.mkdir(parents=True, exist_ok=True)

    def get_archon_projects(self) -> List[Dict]:
        """Get all projects from Archon MCP"""
        try:
            # Call Archon MCP to list projects
            import anthropic

            client = anthropic.Anthropic()

            # Use MCP tool to get projects
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                tools=[
                    {
                        "name": "mcp__archon__find_projects",
                        "description": "List projects from Archon",
                        "input_schema": {
                            "type": "object",
                            "properties": {},
                        }
                    }
                ],
                messages=[{
                    "role": "user",
                    "content": "List all Archon projects"
                }]
            )

            # Extract projects from response
            if response.content:
                for block in response.content:
                    if hasattr(block, 'type') and block.type == 'tool_use':
                        return block.input

            return []

        except Exception as e:
            print(f"⚠️  Could not fetch Archon projects: {e}")
            return []

    def migrate_project(self, archon_project: Dict) -> Dict:
        """Migrate a single Archon project to AutoFlow"""

        print(f"\n🔄 Migrating project: {archon_project.get('title', 'Unnamed')}")

        # Create AutoFlow project structure
        project_name = archon_project.get('title', 'Migrated Project')
        project_id = archon_project.get('id', 'unknown')

        migration_data = {
            "source": "archon",
            "archon_project_id": project_id,
            "migrated_at": datetime.now().isoformat(),
            "project": {
                "name": project_name,
                "description": archon_project.get('description', ''),
                "github_repo": archon_project.get('github_repo', ''),
            },
            "tasks": [],
            "documents": []
        }

        # Migrate tasks
        if 'tasks' in archon_project:
            for task in archon_project['tasks']:
                migration_data['tasks'].append({
                    "title": task.get('title', ''),
                    "description": task.get('description', ''),
                    "status": self._map_archon_status(task.get('status', 'todo')),
                    "assignee": task.get('assignee', 'User'),
                    "archon_task_id": task.get('id', '')
                })

        # Migrate documents
        if 'documents' in archon_project:
            for doc in archon_project['documents']:
                migration_data['documents'].append({
                    "title": doc.get('title', ''),
                    "type": doc.get('document_type', 'note'),
                    "content": doc.get('content', ''),
                    "archon_doc_id": doc.get('id', '')
                })

        # Save migration data
        migration_file = self.migrations_dir / f"archon-{project_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(migration_file, 'w') as f:
            json.dump(migration_data, f, indent=2)

        print(f"✅ Migration data saved: {migration_file}")

        return migration_data

    def _map_archon_status(self, archon_status: str) -> str:
        """Map Archon task status to AutoFlow status"""
        mapping = {
            "todo": "todo",
            "doing": "in_progress",
            "in_progress": "in_progress",
            "review": "review",
            "done": "completed"
        }
        return mapping.get(archon_status.lower(), "todo")

    def create_github_issues_from_migration(self, migration_data: Dict):
        """Create GitHub Issues from migrated Archon tasks"""

        print(f"\n📋 Creating GitHub Issues for: {migration_data['project']['name']}")

        for task in migration_data['tasks']:
            title = f"[MIGRATED] {task['title']}"
            body = f"""Migrated from Archon

**Original Description:**
{task['description']}

**Original Status:** {task['status']}
**Original Assignee:** {task['assignee']}

**Archon Task ID:** {task['archon_task_id']}
"""

            labels = ["migrated-from-archon", f"status:{task['status']}"]

            # Create GitHub Issue
            cmd = [
                'gh', 'issue', 'create',
                '--title', title,
                '--body', body,
                '--label', ','.join(labels)
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    issue_url = result.stdout.strip()
                    print(f"✅ Created: {issue_url}")
                    task['github_issue'] = issue_url
                else:
                    print(f"⚠️  Failed to create issue: {task['title']}")
            except Exception as e:
                print(f"⚠️  Error creating issue: {e}")

    def migrate_all_projects(self):
        """Migrate all Archon projects to AutoFlow"""

        print("="*60)
        print("🚀 Archon → AutoFlow Migration")
        print("="*60)
        print("")

        # Get all Archon projects
        print("📊 Fetching Archon projects...")
        archon_projects = self.get_archon_projects()

        if not archon_projects:
            print("❌ No Archon projects found")
            print("   Make sure Archon MCP is running and accessible")
            return

        print(f"✅ Found {len(archon_projects)} Archon projects")
        print("")

        # Migrate each project
        migrated = []
        for project in archon_projects:
            try:
                migration_data = self.migrate_project(project)

                # Ask user if they want to create GitHub Issues
                print("")
                response = input("Create GitHub Issues for this project? [yes/no]: ")
                if response.lower() in ['yes', 'y']:
                    self.create_github_issues_from_migration(migration_data)

                migrated.append(migration_data)

            except Exception as e:
                print(f"❌ Failed to migrate project: {e}")

        # Create migration summary
        summary = {
            "migrated_at": datetime.now().isoformat(),
            "total_projects": len(archon_projects),
            "successfully_migrated": len(migrated),
            "projects": migrated
        }

        summary_file = self.migrations_dir / f"migration-summary-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print("")
        print("="*60)
        print("✅ Migration Complete!")
        print("="*60)
        print("")
        print(f"📊 Summary:")
        print(f"   Total projects: {summary['total_projects']}")
        print(f"   Successfully migrated: {summary['successfully_migrated']}")
        print(f"   Migration data: {self.migrations_dir}")
        print(f"   Summary: {summary_file}")
        print("")


def main():
    """Main entry point"""
    migrator = ArchonToAutoFlowMigration()
    migrator.migrate_all_projects()


if __name__ == '__main__':
    main()
