# AutoFlow - Quick Start Guide

Get started with AutoFlow in 5 minutes.

## Prerequisites

- Python 3.8+
- Git 2.25+ (with worktree support)
- GitHub CLI (`gh`) installed and authenticated
- Claude API key (for agents)

## Installation

```bash
# 1. Clone AutoFlow
cd /path/to/your/project

# 2. Initialize AutoFlow
mkdir -p .autoflow/agents .autoflow/context-firewalls .autoflow/resources .autoflow/hooks
mkdir -p .github/ISSUE_TEMPLATE worktrees scripts

# 3. Copy AutoFlow files
cp /Users/samiullah/AutoFlow/.autoflow/agents/orchestrator.py .autoflow/agents/
cp /Users/samiullah/AutoFlow/.autoflow/resources/mcp-server.py .autoflow/resources/
cp /Users/samiullah/AutoFlow/.autoflow/hooks/pre-compact .autoflow/hooks/
chmod +x .autoflow/hooks/pre-compact

# 4. Copy scripts
cp /Users/samiullah/AutoFlow/scripts/*.sh scripts/
chmod +x scripts/*.sh

# 5. Copy GitHub Issue templates
cp /Users/samiullah/AutoFlow/.github/ISSUE_TEMPLATE/*.yml .github/ISSUE_TEMPLATE/
```

## Your First Workflow

Run a complete 5-phase workflow:

```bash
python .autoflow/agents/orchestrator.py "implement user authentication"
```

This will:
1. **Research** → Search knowledge base, create GitHub Issue, save summary
2. **Plan** → Create implementation plan, create GitHub Issue, human approval
3. **Implement** → Create git worktree, write code, commit incrementally
4. **Validate** → Run tests, security scan, human approval
5. **Integrate** → Merge to main, cleanup worktree

## Understanding the Output

### Phase 1: Research
```
🔍 Research Agent: implement user authentication
============================================================

📚 Searching knowledge base...
   Found 3 patterns

💻 Searching code examples...
   Found 2 examples

📖 Reviewing documentation...
   Found 1 docs

✅ Created issue #42
📄 Saved full research: .autoflow/context-firewalls/research-implement-user-authentication-20250110-143022.md

🚦 HUMAN CHECKPOINT: Research Complete
   Summary: [2000 token summary]
   Findings: 5 patterns/examples found
   Full Document: .autoflow/context-firewalls/...

❓ Approve? [yes/no/modify]:
```

**Type 'yes' to continue.**

### Phase 2: Plan
```
📋 Plan Agent: implement user authentication
============================================================

🔨 Breaking down into tasks...
   6 tasks identified

🔗 Identifying dependencies...
   3 dependencies mapped

⏱️  Estimating complexity...
   13 hours total (medium complexity)

✅ Created issue #43

🚦 HUMAN CHECKPOINT: Plan Review
   Tasks: 6 tasks identified
   Estimated Time: 13 hours

❓ Approve? [yes/no/modify]:
```

**Type 'yes' to continue.**

### Phase 3: Implement
```
💻 Implement Agent: implement user authentication
============================================================

✅ Created worktree: worktrees/implement-implement-user-authentication

🔧 Setting up environment...
   Environment ready

✍️  Implementing features...
   Created: src/main.py
   Created: src/utils.py
   Created: tests/test_main.py

📝 Committing changes...
   Commit 1/3: Add src/main.py
   Commit 2/3: Add src/utils.py
   Commit 3/3: Add tests/test_main.py

🚦 HUMAN CHECKPOINT: Code Review
   Files Created: 3
   Commits: 3

❓ Approve? [yes/no/modify]:
```

**Type 'yes' to continue.**

### Phase 4: Validate
```
✅ Validate Agent: implement user authentication
============================================================

🧪 Running unit tests...
   ✅ 15/15 passed (85% coverage)

🔗 Running integration tests...
   ✅ 8/8 passed

📊 Checking code quality...
   ✅ 0 issues, 2 warnings

🔒 Running security scan...
   ✅ 0 vulnerabilities

🚦 HUMAN CHECKPOINT: Validation Review
   All Tests Passed: ✅ Yes
   Unit Tests: 15 tests, 85% coverage
   Security: 0 vulnerabilities

❓ Approve? [yes/no/modify]:
```

**Type 'yes' to continue.**

### Phase 5: Integrate
```
🔀 Integrate: Merging to main
============================================================

🔀 Merging implement-implement-user-authentication into main...
   Merge complete

🗑️  Removing worktree...
   Worktree removed

🗑️  Deleting branch...
   Branch deleted

✅ Integration complete!
```

## Key Concepts

### 1. Context Firewalls (90% Token Reduction)
Agents save full output to files, pass only summaries:
- **Full output**: `.autoflow/context-firewalls/research-topic-timestamp.md` (20,000 tokens)
- **Summary**: Passed to next agent (2,000 tokens)
- **Savings**: 90%

### 2. Git Worktrees (Parallel Execution)
Each implementation happens in isolated directory:
- **Main branch**: `main/` (untouched during implementation)
- **Worktree**: `worktrees/implement-feature/` (isolated work)
- **Merge**: Only after human approval

### 3. GitHub Issues (Git-Native Tasks)
Tasks are GitHub Issues:
- **[RESEARCH]** = Phase 1 research issue
- **[PLAN]** = Phase 2 planning issue
- **[IMPLEMENT]** = Phase 3 implementation issue
- Labels: `phase:research`, `status:in-progress`, `status:done`

### 4. Human Checkpoints (Control)
4 critical approval points:
1. After research (approve direction)
2. After planning (approve plan)
3. After implementation (code review)
4. After validation (approve deployment)

## What's Next?

### Check Your Workflow State
```bash
# List all GitHub Issues
gh issue list

# Check active worktrees
git worktree list

# View context firewall summaries
ls -lt .autoflow/context-firewalls/
```

### Run Another Workflow
```bash
python .autoflow/agents/orchestrator.py "add payment processing"
```

### Customize Agents
Edit `.autoflow/agents/orchestrator.py` to:
- Connect to Archon MCP for real knowledge base search
- Use Claude SDK for intelligent task breakdown
- Add custom validation steps
- Integrate with your CI/CD pipeline

## Troubleshooting

### Issue: `gh: command not found`
```bash
# Install GitHub CLI
brew install gh  # macOS
# or visit: https://cli.github.com/

# Authenticate
gh auth login
```

### Issue: `git worktree add` fails
```bash
# Check Git version (need 2.25+)
git --version

# List existing worktrees
git worktree list

# Remove stale worktrees
git worktree prune
```

### Issue: Context firewall directory not found
```bash
# Create directory
mkdir -p .autoflow/context-firewalls
```

## Integration with ProductionForge Design System

For UI tasks, AutoFlow integrates with ProductionForge design system automatically:

```bash
python .autoflow/agents/orchestrator.py "build dashboard UI"
```

This will:
1. Load design tokens (spacing, colors, typography)
2. Load component guide (decision tree)
3. Load responsive rules (mobile-first)
4. Load accessibility standards (WCAG 2.1 AA)
5. Prevent UI hallucination (no magic numbers, hardcoded colors)

## Next Steps

- Read [GETTING_STARTED.md](./GETTING_STARTED.md) for detailed explanation
- Read [DOCUMENTATION.md](./DOCUMENTATION.md) for architecture details
- Read [README.md](./README.md) for research background

## Support

- GitHub Issues: Report bugs, request features
- Documentation: Read full docs in `/docs/`
- Examples: See `/examples/` for real workflows

---

**You now have a complete git-native AI agent workflow system!**

- ✅ No external databases (Git + GitHub)
- ✅ 90% token reduction (Context firewalls)
- ✅ Parallel execution (Git worktrees)
- ✅ Human control (4 checkpoints)
- ✅ UI hallucination prevention (Design system)
- ✅ Context preservation (PreCompact hook)
