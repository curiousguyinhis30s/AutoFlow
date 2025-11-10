# AutoFlow - START HERE

## ✅ Migration Status

**Archon → AutoFlow migration complete!** Your Archon data has been safely saved to `.autoflow/migrations/`

- **2 projects migrated** (data saved)
- **Archon untouched** (both systems work in parallel)
- **See**: `.autoflow/MIGRATION-STATUS.md` for details

To create GitHub Issues from migration data:
1. Authenticate: `/opt/homebrew/bin/gh auth login`
2. Run: `python3 .autoflow/create-issues-from-migrations.py`

---

## What You Have

A complete AI agent workflow system powered by Claude that builds features for you.

## Setup (3 steps)

### Step 1: Run Setup Script

```bash
cd /Users/samiullah/AutoFlow
./setup.sh
```

This installs dependencies and checks your setup.

### Step 2: Set Your Claude API Key

Add to your `~/.zshrc` (since you're using Warp):

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Then reload:
```bash
source ~/.zshrc
```

**Don't have a Claude API key?**
Get one at: https://console.anthropic.com/settings/keys

### Step 3: Authenticate GitHub

```bash
/opt/homebrew/bin/gh auth login
```

Follow prompts:
- Select: GitHub.com
- Select: HTTPS
- Select: Login with a web browser
- Copy code, paste in browser

---

## Usage

### Quick Start

```bash
/Users/samiullah/AutoFlow/start-autoflow.sh "your task here"
```

**Example:**
```bash
/Users/samiullah/AutoFlow/start-autoflow.sh "build a contact form with validation"
```

### Add Global Alias (Optional)

Add to `~/.zshrc`:
```bash
alias autoflow="/Users/samiullah/AutoFlow/start-autoflow.sh"
```

Then use:
```bash
autoflow "build a contact form"
```

### What Happens

Claude Code will:
1. Create GitHub Issue for tracking
2. Research relevant patterns
3. Create implementation plan
4. Write the actual code
5. Test and validate
6. Commit and push to GitHub
7. Close issue with summary

**See:** `HOW-TO-START.md` for detailed instructions

---

## Examples

```bash
./autoflow "implement user authentication"
./autoflow "add payment processing with Stripe"
./autoflow "build admin dashboard"
./autoflow "add email notifications"
```

---

## Quick Demo (No API Key Needed)

```bash
./demo.sh
```

Shows you how the system works (uses mock data).

---

## What Makes This Different

**Uses Real Claude API**:
- ResearchAgent: Claude analyzes patterns
- PlanAgent: Claude breaks down tasks
- ImplementAgent: Claude writes code
- 90% token reduction via context firewalls

**Git-Native**:
- Tasks = GitHub Issues
- Parallel work = Git worktrees
- No external databases

**Human Control**:
- 4 approval checkpoints
- Stop anytime
- Review before merge

---

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

```bash
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

### "GitHub CLI not authenticated"

```bash
/opt/homebrew/bin/gh auth login
```

### Test if it works

```bash
./autoflow "test task"
```

Should start running. Press Ctrl+C if it works.

---

## Files

- `./autoflow` - Run workflows
- `./demo.sh` - Interactive demo
- `./setup.sh` - Setup script
- `.autoflow/agents/orchestrator.py` - Main system (now with Claude!)

---

**Ready? Run this in Warp:**

```bash
cd /Users/samiullah/AutoFlow
./setup.sh
```
