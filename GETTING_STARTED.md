# AutoFlow - Getting Started Guide

A comprehensive guide to understanding and using AutoFlow's git-native workflow system.

## Table of Contents

1. [What is AutoFlow?](#what-is-autoflow)
2. [Why AutoFlow?](#why-autoflow)
3. [Architecture Overview](#architecture-overview)
4. [Installation](#installation)
5. [Core Concepts](#core-concepts)
6. [Complete Workflow Example](#complete-workflow-example)
7. [Advanced Usage](#advanced-usage)
8. [Integration Guide](#integration-guide)
9. [Troubleshooting](#troubleshooting)

## What is AutoFlow?

AutoFlow is a **git-native AI agent workflow system** that implements the CCPM (Critical Chain Project Management) 5-phase workflow:

```
Research → Plan → Implement → Validate → Integrate
   ↓        ↓        ↓          ↓           ↓
GitHub   GitHub   Git      Worktree     Main
Issue    Issue    Worktree  Testing     Branch
```

**Key Innovation**: Everything lives in Git. No external databases, no complex setup.

## Why AutoFlow?

### Problem: Traditional Multi-Agent Systems

Traditional systems suffer from:
- **Token explosion**: Full agent outputs consume 20,000+ tokens
- **Context loss**: Agents lose track of previous work
- **State management**: Complex databases for task tracking
- **Merge conflicts**: Agents stepping on each other's work
- **UI hallucination**: Inconsistent designs, endless rework

### Solution: AutoFlow

AutoFlow solves these with:
- **Context firewalls**: 90% token reduction (summaries not full output)
- **Git worktrees**: Parallel execution without conflicts
- **GitHub Issues**: Git-native task management
- **Human checkpoints**: Control at critical decision points
- **Design system**: Prevents UI hallucination
- **PreCompact hook**: Preserves context across sessions

## Architecture Overview

### Directory Structure

```
your-project/
├── .autoflow/                    # AutoFlow system
│   ├── agents/
│   │   └── orchestrator.py       # Main orchestrator (800+ lines)
│   ├── context-firewalls/        # Agent summaries (90% reduction)
│   │   ├── research-auth-20250110.md
│   │   ├── plan-auth-20250110.md
│   │   └── implement-auth-20250110.md
│   ├── resources/
│   │   └── mcp-server.py         # MCP resource server
│   ├── hooks/
│   │   └── pre-compact           # Context preservation
│   └── design-system-integration.py
├── .github/
│   └── ISSUE_TEMPLATE/           # GitHub Issue templates
│       ├── 01-research.yml
│       ├── 02-plan.yml
│       └── 03-implement.yml
├── worktrees/                    # Git worktrees (parallel execution)
│   ├── implement-auth/           # Agent 1 working here
│   └── implement-api/            # Agent 2 working here
└── scripts/
    ├── worktree-create.sh
    └── worktree-merge.sh
```

### Component Overview

#### 1. Orchestrator (`orchestrator.py`)
- **GitHubIssues**: Creates/manages issues for task tracking
- **ContextFirewall**: Saves full output, creates summaries
- **WorktreeManager**: Creates/merges git worktrees
- **HumanCheckpoint**: Requests approval at critical points
- **Agents**: Research, Plan, Implement, Validate

#### 2. Context Firewalls
Saves full agent output (20,000 tokens), passes summary (2,000 tokens):
```
Agent 1 (Research)
  ↓ [Full output saved]
  ↓ [Summary generated: 2,000 tokens]
Agent 2 (Plan) receives summary
  ↓ [Full output saved]
  ↓ [Summary generated: 2,000 tokens]
Agent 3 (Implement) receives summary
```

**Token savings**: 90% reduction

#### 3. Git Worktrees
Parallel execution without conflicts:
```bash
# Main branch (protected)
main/

# Agent 1 (implement authentication)
worktrees/implement-auth/

# Agent 2 (implement API)
worktrees/implement-api/
```

Both agents work simultaneously without stepping on each other.

#### 4. GitHub Issues
Tasks are GitHub Issues with labels:
- `phase:research` - Research phase
- `phase:plan` - Planning phase
- `phase:implement` - Implementation phase
- `status:todo` - Not started
- `status:in-progress` - Currently working
- `status:done` - Completed

## Installation

### Prerequisites

```bash
# Check prerequisites
python --version    # Need 3.8+
git --version       # Need 2.25+ (worktree support)
gh --version        # GitHub CLI

# Install if missing
brew install python git gh  # macOS
```

### Authenticate GitHub CLI

```bash
gh auth login
# Follow prompts to authenticate
```

### Install AutoFlow

```bash
# Option 1: Copy from AutoFlow project
cd /path/to/your/project
cp -r /Users/samiullah/AutoFlow/.autoflow .
cp -r /Users/samiullah/AutoFlow/.github/ISSUE_TEMPLATE .github/
cp -r /Users/samiullah/AutoFlow/scripts .
chmod +x scripts/*.sh .autoflow/hooks/*

# Option 2: Initialize manually
mkdir -p .autoflow/agents .autoflow/context-firewalls .autoflow/resources .autoflow/hooks
mkdir -p .github/ISSUE_TEMPLATE worktrees scripts
# Then copy individual files
```

## Core Concepts

### Concept 1: Context Firewalls

**Problem**: Agent outputs 20,000 tokens → next agent receives 20,000 tokens → token explosion

**Solution**: Context Firewall

```python
# Agent generates output
full_output = agent.execute()  # 20,000 tokens

# Save full output to file
filepath = firewall.save_full_output("research", full_output)
# Saved to: .autoflow/context-firewalls/research-20250110.md

# Generate summary
summary = firewall.create_summary(full_output)  # 2,000 tokens

# Pass ONLY summary to next agent
next_agent.execute(summary)  # 90% token reduction!
```

**Benefits**:
- 90% token reduction
- Full output preserved for human review
- Next agent gets only relevant info

### Concept 2: Git Worktrees

**Problem**: Agents on same branch → merge conflicts

**Solution**: Git Worktrees

```bash
# Create isolated worktree for Agent 1
git worktree add worktrees/implement-auth -b implement-auth

# Agent 1 works in worktrees/implement-auth/
cd worktrees/implement-auth
git add src/auth.py
git commit -m "Add authentication"

# Meanwhile, Agent 2 works in parallel
git worktree add worktrees/implement-api -b implement-api
cd worktrees/implement-api
git add src/api.py
git commit -m "Add API"

# No conflicts! Each has isolated directory
```

**Benefits**:
- Parallel execution
- No merge conflicts during development
- Merge only after human approval

### Concept 3: GitHub Issues as Database

**Problem**: External task database (PostgreSQL, MongoDB) → complexity

**Solution**: GitHub Issues

```bash
# Create research issue
gh issue create \
  --title "[RESEARCH] User authentication" \
  --label "phase:research,status:in-progress"

# Add comment with summary
gh issue comment 42 --body "Research complete. Found 5 patterns."

# Close issue
gh issue close 42

# List all research issues
gh issue list --label "phase:research"
```

**Benefits**:
- No external database needed
- Works with existing GitHub workflow
- Searchable, linkable, trackable

### Concept 4: Human Checkpoints

**Problem**: Agents make wrong decisions → wasted work

**Solution**: Human-in-the-loop checkpoints

```python
# After research
approved = checkpoint.request_approval("Research Complete", {
    "Summary": result["summary"],
    "Findings": "5 patterns found",
    "Recommendation": "Proceed with JWT approach"
})

if not approved:
    print("❌ Research not approved. Stopping.")
    sys.exit(1)
# Human types 'yes' → continue
# Human types 'no' → stop
```

**Checkpoints**:
1. After research → Approve direction
2. After planning → Approve plan
3. After implementation → Code review
4. After validation → Approve deployment

### Concept 5: MCP Resource Pattern

**Problem**: Agents need instructions, not just data

**Solution**: MCP resources provide workflows, templates, checklists

```python
# List available resources
resources = mcp_server.list_resources()
# Returns:
# - workflow://overview → Complete workflow guide
# - task://template/feature → Feature implementation template
# - checkpoint://pre-merge → Pre-merge checklist

# Read resource
content = mcp_server.read_resource("workflow://overview")
# Returns: Complete markdown guide with instructions
```

**Benefits**:
- Agents get reusable templates
- Consistent workflows across projects
- Easy to update/customize

## Complete Workflow Example

Let's implement "user authentication" step-by-step.

### Step 1: Run Orchestrator

```bash
python .autoflow/agents/orchestrator.py "implement user authentication"
```

### Step 2: Phase 1 - Research

```
🔍 Research Agent: implement user authentication
============================================================

📚 Searching knowledge base...
```

**What happens**:
1. Creates GitHub Issue: `[RESEARCH] implement user authentication`
2. Agent searches Archon knowledge base (via MCP)
3. Agent searches code examples
4. Agent reviews documentation
5. Creates full research document (20,000 tokens)
6. Saves to: `.autoflow/context-firewalls/research-implement-user-authentication-20250110.md`
7. Generates summary (2,000 tokens)

**Human checkpoint**:
```
🚦 HUMAN CHECKPOINT: Research Complete

Summary:
  - Found 5 authentication patterns
  - JWT + Passport.js recommended
  - Security: token rotation + HTTPS required
  - Estimated: 4 hours implementation

Full Document: .autoflow/context-firewalls/research-implement-user-authentication-20250110.md

❓ Approve? [yes/no/modify]:
```

**Action**: Type `yes`

### Step 3: Phase 2 - Plan

```
📋 Plan Agent: implement user authentication
============================================================

🔨 Breaking down into tasks...
   6 tasks identified
```

**What happens**:
1. Creates GitHub Issue: `[PLAN] implement user authentication`
2. Agent receives research summary (2,000 tokens, not 20,000!)
3. Agent breaks down into 6 tasks:
   - Set up project structure (1h)
   - Implement core functionality (4h)
   - Add error handling (2h)
   - Write unit tests (3h)
   - Write integration tests (2h)
   - Update documentation (1h)
4. Agent identifies dependencies
5. Agent estimates complexity: 13 hours (medium)
6. Creates full plan document (15,000 tokens)
7. Saves to: `.autoflow/context-firewalls/plan-implement-user-authentication-20250110.md`
8. Generates summary (1,500 tokens)

**Human checkpoint**:
```
🚦 HUMAN CHECKPOINT: Plan Review

Summary:
  - 6 tasks identified
  - 13 hours estimated
  - Medium complexity
  - Recommend standard track

Tasks:
  1. Set up project structure (1h)
  2. Implement core functionality (4h)
  3. Add error handling (2h)
  4. Write unit tests (3h)
  5. Write integration tests (2h)
  6. Update documentation (1h)

Full Document: .autoflow/context-firewalls/plan-implement-user-authentication-20250110.md

❓ Approve? [yes/no/modify]:
```

**Action**: Type `yes`

### Step 4: Phase 3 - Implement

```
💻 Implement Agent: implement user authentication
============================================================

✅ Created worktree: worktrees/implement-implement-user-authentication
```

**What happens**:
1. Creates git worktree: `worktrees/implement-implement-user-authentication/`
2. Agent changes to worktree directory
3. Agent receives plan summary (1,500 tokens)
4. Agent implements features:
   - Creates `src/auth/passport.js`
   - Creates `src/auth/jwt.js`
   - Creates `src/middleware/authenticate.js`
   - Creates `tests/auth.test.js`
5. Agent commits incrementally:
   - Commit 1: "Add Passport.js setup"
   - Commit 2: "Add JWT token generation"
   - Commit 3: "Add authentication middleware"
   - Commit 4: "Add auth tests"
6. Creates implementation report
7. Saves to: `.autoflow/context-firewalls/implement-implement-user-authentication-20250110.md`

**Human checkpoint**:
```
🚦 HUMAN CHECKPOINT: Code Review

Summary:
  - 4 files created
  - 4 commits made
  - Authentication implemented with JWT
  - Tests added

Files Created:
  - src/auth/passport.js
  - src/auth/jwt.js
  - src/middleware/authenticate.js
  - tests/auth.test.js

Commits:
  1. Add Passport.js setup
  2. Add JWT token generation
  3. Add authentication middleware
  4. Add auth tests

Full Document: .autoflow/context-firewalls/implement-implement-user-authentication-20250110.md

❓ Approve? [yes/no/modify]:
```

**Action**: Type `yes` (or review code first)

### Step 5: Phase 4 - Validate

```
✅ Validate Agent: implement user authentication
============================================================

🧪 Running unit tests...
   ✅ 15/15 passed (85% coverage)
```

**What happens**:
1. Agent runs in worktree: `worktrees/implement-implement-user-authentication/`
2. Runs unit tests: `npm test`
3. Runs integration tests: `npm run test:integration`
4. Checks code quality: `eslint src/`
5. Runs security scan: `npm audit`
6. Creates validation report
7. Saves to: `.autoflow/context-firewalls/validate-implement-user-authentication-20250110.md`

**Human checkpoint**:
```
🚦 HUMAN CHECKPOINT: Validation Review

Summary:
  ✅ All tests passed
  ✅ Code quality: 0 issues
  ✅ Security: 0 vulnerabilities

Unit Tests:
  - 15/15 passed
  - 85% coverage

Integration Tests:
  - 8/8 passed

Security:
  - 0 vulnerabilities
  - No hardcoded secrets

Full Document: .autoflow/context-firewalls/validate-implement-user-authentication-20250110.md

❓ Approve? [yes/no/modify]:
```

**Action**: Type `yes`

### Step 6: Phase 5 - Integrate

```
🔀 Integrate: Merging to main
============================================================

🔀 Merging implement-implement-user-authentication into main...
   Merge complete

🗑️  Removing worktree...
   Worktree removed

✅ Integration complete!
```

**What happens**:
1. Switches to main branch
2. Merges worktree branch: `git merge --no-ff implement-implement-user-authentication`
3. Removes worktree: `git worktree remove worktrees/implement-implement-user-authentication`
4. Deletes branch: `git branch -d implement-implement-user-authentication`
5. Closes all related GitHub Issues

**Result**: Feature implemented, tested, merged to main!

## Advanced Usage

### Parallel Workflows

Run multiple workflows simultaneously:

```bash
# Terminal 1: Implement authentication
python .autoflow/agents/orchestrator.py "implement authentication"

# Terminal 2: Implement API (while Terminal 1 is running)
python .autoflow/agents/orchestrator.py "implement REST API"
```

Both use separate worktrees → no conflicts!

### Custom Agents

Edit `.autoflow/agents/orchestrator.py` to add custom agent logic:

```python
class CustomAgent:
    """Your custom agent"""

    def execute(self, task: str) -> Dict:
        # Your custom logic here
        pass

# Add to orchestrator
self.custom_agent = CustomAgent(self.firewall)
```

### Integration with Archon MCP

Connect to Archon for real knowledge base:

```python
# In ResearchAgent._search_knowledge_base()
def _search_knowledge_base(self, topic: str) -> List[Dict]:
    # Call Archon MCP
    result = archon_mcp.perform_rag_query(
        query=topic,
        match_count=5
    )
    return result["matches"]
```

## Integration Guide

### With Existing Projects

```bash
# 1. Initialize AutoFlow in existing project
cd /path/to/existing/project
mkdir -p .autoflow/agents .autoflow/context-firewalls
cp /Users/samiullah/AutoFlow/.autoflow/agents/orchestrator.py .autoflow/agents/

# 2. Test with small feature
python .autoflow/agents/orchestrator.py "add logging"

# 3. Gradually adopt for larger features
```

### With CI/CD

```yaml
# .github/workflows/autoflow.yml
name: AutoFlow Validation

on:
  push:
    branches: ['implement-*']  # Only worktree branches

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          python .autoflow/agents/orchestrator.py validate
```

### With ProductionForge Design System

For UI tasks, AutoFlow automatically loads design system:

```python
# Automatic for UI tasks
python .autoflow/agents/orchestrator.py "build user dashboard"

# Design system loaded:
# - design-tokens.ts (spacing, colors, typography)
# - components-guide.md (decision tree)
# - responsive-rules.md (mobile-first)
# - accessibility.md (WCAG 2.1 AA)
# - anti-patterns.md (what NOT to do)
```

Result: Perfect UI on first try, no hallucination!

## Troubleshooting

### GitHub CLI not authenticated

```bash
gh auth login
# Follow prompts
```

### Git worktree fails

```bash
# Check for stale worktrees
git worktree list

# Remove stale worktrees
git worktree prune

# Force remove specific worktree
git worktree remove worktrees/implement-auth --force
```

### Context firewall directory not found

```bash
mkdir -p .autoflow/context-firewalls
```

### Agent produces hallucinated output

Add to context firewall:
```python
# In agent.execute()
system_prompt = f"""
{base_prompt}

# CRITICAL: Use only these patterns:
{load_patterns_from_knowledge_base()}
"""
```

## Next Steps

- Read [QUICKSTART.md](./QUICKSTART.md) for 5-minute start
- Read [DOCUMENTATION.md](./DOCUMENTATION.md) for architecture deep-dive
- Read [README.md](./README.md) for research background
- Try example workflows in `/examples/`

---

**You now understand AutoFlow's complete architecture!**

- ✅ Context firewalls → 90% token reduction
- ✅ Git worktrees → Parallel execution
- ✅ GitHub Issues → Git-native tasks
- ✅ Human checkpoints → Control at critical points
- ✅ MCP resources → Reusable templates
- ✅ Design system → No UI hallucination
