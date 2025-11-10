# How to Start AutoFlow

## Option 1: Direct Command (Recommended)

**In any new terminal:**

```bash
/Users/samiullah/AutoFlow/start-autoflow.sh "your task here"
```

**Example:**
```bash
/Users/samiullah/AutoFlow/start-autoflow.sh "build a contact form with email validation"
```

This will:
1. Open a new Claude Code session
2. Execute the full AutoFlow 5-phase workflow
3. Create GitHub Issue, implement, commit, and close issue

---

## Option 2: Add Global Alias (Convenience)

**Add to your `~/.zshrc`:**

```bash
# AutoFlow launcher
alias autoflow="/Users/samiullah/AutoFlow/start-autoflow.sh"
```

**Then reload:**
```bash
source ~/.zshrc
```

**Now you can use:**
```bash
autoflow "build a contact form"
```

From anywhere in your terminal!

---

## Option 3: Continue Existing Claude Session

**If you're already in a Claude Code session:**

Just type your request naturally:

```
Execute AutoFlow workflow: build a contact form with validation
```

I (Claude Code) will execute the 5-phase workflow for you.

---

## How It Works

### Archon vs AutoFlow

**When terminal opens:**
- `claude-continuity.sh` runs (loads Archon projects)
- This is for **task management** and **project tracking**

**When you want to BUILD something:**
- Run `start-autoflow.sh "task"` (opens new Claude Code session)
- Claude Code executes AutoFlow workflow
- This is for **actual implementation**

### Both Systems Work Together:
- **Archon**: Project management, task tracking, knowledge base
- **AutoFlow**: Implementation workflow with GitHub Issues + Git

---

## What Happens When You Run AutoFlow

```
1. Creates GitHub Issue → #4, #5, etc.
2. Phase 1: Research → Claude analyzes patterns
3. Phase 2: Plan → Claude creates implementation plan
4. Phase 3: Implement → Claude writes actual code
5. Phase 4: Validate → Claude tests the result
6. Phase 5: Integrate → Claude commits & pushes to GitHub
7. Closes Issue → Marks complete with summary
```

All tracked in: https://github.com/curiousguyinhis30s/AutoFlow

---

## Examples

### Build UI Component
```bash
autoflow "create a responsive navbar with logo and menu items"
```

### Add Backend Feature
```bash
autoflow "implement user authentication with JWT tokens"
```

### Create Documentation
```bash
autoflow "write API documentation for all endpoints"
```

### Fix Issues
```bash
autoflow "fix the login bug where password validation fails"
```

---

## Difference from Archon

| System | Purpose | How to Use |
|--------|---------|------------|
| **Archon** | Task management, knowledge base | Loads automatically, use Archon MCP tools |
| **AutoFlow** | Implementation workflow | Run `start-autoflow.sh "task"` explicitly |

Both systems are independent and can run in parallel!

---

## Quick Reference

**Start AutoFlow:**
```bash
/Users/samiullah/AutoFlow/start-autoflow.sh "task"
```

**View Issues:**
```bash
cd /Users/samiullah/AutoFlow
gh issue list
```

**Check Repository:**
https://github.com/curiousguyinhis30s/AutoFlow

---

**Ready to build something? Try it now!**
