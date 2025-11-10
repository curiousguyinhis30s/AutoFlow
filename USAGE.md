# AutoFlow - Usage Reference

Quick reference for common AutoFlow operations.

## Basic Commands

### Run Complete Workflow

```bash
python .autoflow/agents/orchestrator.py "implement user authentication"
```

Executes all 5 phases:
- Research → Plan → Implement → Validate → Integrate

### Run Demo

```bash
./demo.sh
```

Interactive demo showing all AutoFlow features.

## Worktree Management

### Create Worktree

```bash
./scripts/worktree-create.sh implement-auth auth-123
```

Creates isolated workspace: `worktrees/implement-auth/`

### List Worktrees

```bash
git worktree list
```

Shows all active worktrees.

### Merge Worktree

```bash
./scripts/worktree-merge.sh implement-auth
```

Merges to main, removes worktree, deletes branch.

### Remove Worktree (without merging)

```bash
git worktree remove worktrees/implement-auth
git branch -D implement-auth
```

## GitHub Issues

### Create Issue

```bash
gh issue create \
  --title "[RESEARCH] User authentication" \
  --label "phase:research,status:in-progress"
```

### List Issues

```bash
# All issues
gh issue list

# By label
gh issue list --label "phase:research"
gh issue list --label "status:in-progress"
```

### Add Comment

```bash
gh issue comment 42 --body "Research complete. Found 5 patterns."
```

### Close Issue

```bash
gh issue close 42
```

## Context Firewalls

### View Summaries

```bash
ls -lt .autoflow/context-firewalls/
```

Shows all agent summaries sorted by date.

### Read Full Output

```bash
cat .autoflow/context-firewalls/research-auth-20250110-143022.md
```

### Read Summary Only

```bash
head -20 .autoflow/context-firewalls/research-auth-20250110-143022.md
```

First 20 lines usually contain the summary.

## MCP Resources

### List Resources

```bash
python3 .autoflow/resources/mcp-server.py
```

Shows available resources:
- workflow://overview
- task://template/feature
- checkpoint://pre-merge

### Read Resource

Edit `mcp-server.py` to read specific resource:

```python
server = AutoFlowMCPServer()
content = server.read_resource("workflow://overview")
print(content)
```

## Design System Integration

### Check Design System

```bash
python3 .autoflow/design-system-integration.py
```

Verifies ProductionForge design system is accessible.

### Validate UI Code

```python
from design_system_integration import DesignSystemIntegration

integration = DesignSystemIntegration()
result = integration.validate_ui_code(your_code)

if not result["valid"]:
    print("Violations:", result["violations"])
```

## Troubleshooting

### Reset Workflow

```bash
# Remove all worktrees
git worktree list | grep worktrees | awk '{print $1}' | xargs -I {} git worktree remove {}

# Close all issues
gh issue list --state open | grep "\[RESEARCH\]\|\[PLAN\]\|\[IMPLEMENT\]" | awk '{print $1}' | xargs -I {} gh issue close {}

# Clean context firewalls
rm -rf .autoflow/context-firewalls/*
```

### Fix Git Worktree Issues

```bash
# Prune stale worktrees
git worktree prune

# Force remove worktree
git worktree remove worktrees/implement-auth --force

# Delete branch
git branch -D implement-auth
```

### GitHub CLI Not Authenticated

```bash
gh auth login
gh auth status
```

## File Locations

```
AutoFlow/
├── .autoflow/
│   ├── agents/
│   │   └── orchestrator.py              # Main orchestrator
│   ├── context-firewalls/               # Agent summaries
│   │   ├── research-auth-20250110.md
│   │   ├── plan-auth-20250110.md
│   │   └── implement-auth-20250110.md
│   ├── resources/
│   │   └── mcp-server.py                # MCP resources
│   ├── hooks/
│   │   └── pre-compact                  # Context preservation
│   └── design-system-integration.py     # UI integration
├── .github/ISSUE_TEMPLATE/
│   ├── 01-research.yml
│   ├── 02-plan.yml
│   └── 03-implement.yml
├── worktrees/                           # Active worktrees
│   ├── implement-auth/
│   └── implement-api/
├── scripts/
│   ├── worktree-create.sh
│   └── worktree-merge.sh
├── QUICKSTART.md                        # 5-minute start
├── GETTING_STARTED.md                   # Detailed guide
├── USAGE.md                             # This file
├── README.md                            # Architecture
└── demo.sh                              # Interactive demo
```

## Common Workflows

### Feature Implementation

```bash
# 1. Run orchestrator
python .autoflow/agents/orchestrator.py "implement feature X"

# 2. Approve research (type 'yes')
# 3. Approve plan (type 'yes')
# 4. Review code in worktree
cd worktrees/implement-implement-feature-x
# ... review code ...
cd ../..

# 5. Approve implementation (type 'yes')
# 6. Approve validation (type 'yes')
# 7. Feature merged to main
```

### Bug Fix

```bash
# 1. Quick fix (skip research/planning)
./scripts/worktree-create.sh fix-bug-123 bug-123

# 2. Make changes
cd worktrees/fix-bug-123
# ... fix bug ...
git add .
git commit -m "Fix bug #123"
cd ../..

# 3. Merge
./scripts/worktree-merge.sh fix-bug-123
```

### UI Task

```bash
# Automatically loads design system
python .autoflow/agents/orchestrator.py "build user dashboard"

# Design system prevents:
# - Magic numbers (hardcoded spacing)
# - Hardcoded colors
# - Wrong component choices
# - Accessibility violations
```

### Parallel Development

```bash
# Terminal 1
python .autoflow/agents/orchestrator.py "implement authentication"

# Terminal 2 (while Terminal 1 is running)
python .autoflow/agents/orchestrator.py "implement API"

# Both use separate worktrees → no conflicts!
```

## Advanced Usage

### Custom Agent

Edit `.autoflow/agents/orchestrator.py`:

```python
class CustomAgent:
    """Your custom agent"""

    def __init__(self, context_firewall: ContextFirewall):
        self.firewall = context_firewall

    def execute(self, task: str) -> Dict[str, Any]:
        # Your logic here
        full_output = self._do_work(task)

        # Save full output
        filepath = self.firewall.save_full_output("custom", task, full_output)

        # Create summary
        summary = self.firewall.create_summary(full_output)

        return {
            "summary": summary,
            "full_document": filepath
        }

# Add to orchestrator
self.custom_agent = CustomAgent(self.firewall)
```

### Integrate with Archon

```python
# In ResearchAgent._search_knowledge_base()
def _search_knowledge_base(self, topic: str) -> List[Dict]:
    # Use Archon MCP
    from mcp import ArchonMCP

    archon = ArchonMCP()
    result = archon.perform_rag_query(
        query=topic,
        match_count=5
    )

    return result["matches"]
```

### Add Custom Checkpoint

```python
# In orchestrator
def _phase_custom(self, data: Dict) -> Dict:
    # Do work
    result = self.custom_agent.execute(data)

    # Add checkpoint
    approved = self.checkpoint.request_approval("Custom Review", {
        "Summary": result["summary"],
        "Custom Data": result["custom_field"]
    })

    if not approved:
        print("❌ Custom phase not approved")
        sys.exit(1)

    return result
```

## Environment Variables

```bash
# Claude API key (for agents)
export CLAUDE_API_KEY="sk-ant-..."

# Archon MCP server (if using Archon)
export ARCHON_MCP_URL="http://localhost:8051"

# GitHub token (usually auto-detected by gh CLI)
export GITHUB_TOKEN="ghp_..."
```

## Performance Tips

1. **Use context firewalls aggressively**
   - Save everything to files
   - Pass only summaries between agents
   - 90% token reduction = 10x more work in same context

2. **Use worktrees for all implementation**
   - Never implement directly on main
   - Always use isolated worktrees
   - Merge only after validation

3. **Use GitHub Issues for all tasks**
   - No external database needed
   - Git-native workflow
   - Searchable, linkable, trackable

4. **Use human checkpoints wisely**
   - Critical decisions only
   - Don't checkpoint trivial steps
   - 4 checkpoints is optimal

## See Also

- [QUICKSTART.md](./QUICKSTART.md) - 5-minute quick start
- [GETTING_STARTED.md](./GETTING_STARTED.md) - Detailed guide
- [README.md](./README.md) - Architecture and research
- [demo.sh](./demo.sh) - Interactive demonstration

---

**Quick Help**

```bash
# Get started in 5 minutes
cat QUICKSTART.md

# Understand the architecture
cat GETTING_STARTED.md

# Run interactive demo
./demo.sh

# Run first workflow
python .autoflow/agents/orchestrator.py "your task here"
```
