#!/usr/bin/env python3
"""
AutoFlow MCP Server - Resource Pattern

Provides instructional resources (not just data) via MCP protocol.

Resources:
- workflow://overview → Complete workflow guide
- task://template/feature → Feature implementation template
- checkpoint://pre-merge → Pre-merge checklist
- firewall://summary-guide → How to create summaries
"""

import json
from typing import Dict, List


class AutoFlowMCPServer:
    """MCP Server for AutoFlow resources"""

    def list_resources(self) -> List[Dict]:
        """List available resources"""
        return [
            {
                "uri": "workflow://overview",
                "name": "AutoFlow Workflow Overview",
                "description": "Complete CCPM 5-phase workflow guide",
                "mimeType": "text/markdown"
            },
            {
                "uri": "task://template/feature",
                "name": "Feature Implementation Template",
                "description": "Step-by-step feature implementation guide",
                "mimeType": "text/markdown"
            },
            {
                "uri": "task://template/bugfix",
                "name": "Bug Fix Template",
                "description": "Systematic bug fixing workflow",
                "mimeType": "text/markdown"
            },
            {
                "uri": "checkpoint://pre-merge",
                "name": "Pre-Merge Checklist",
                "description": "Human approval checklist before merge",
                "mimeType": "text/markdown"
            },
            {
                "uri": "checkpoint://pre-deploy",
                "name": "Pre-Deployment Checklist",
                "description": "Final checks before deployment",
                "mimeType": "text/markdown"
            },
            {
                "uri": "firewall://summary-guide",
                "name": "Context Firewall Summary Guide",
                "description": "How to create effective summaries",
                "mimeType": "text/markdown"
            }
        ]

    def read_resource(self, uri: str) -> str:
        """Read resource content"""
        resources = {
            "workflow://overview": self._workflow_overview(),
            "task://template/feature": self._feature_template(),
            "task://template/bugfix": self._bugfix_template(),
            "checkpoint://pre-merge": self._pre_merge_checklist(),
            "checkpoint://pre-deploy": self._pre_deploy_checklist(),
            "firewall://summary-guide": self._summary_guide()
        }

        return resources.get(uri, f"Resource not found: {uri}")

    def _workflow_overview(self) -> str:
        return """# AutoFlow Workflow Overview

## CCPM 5-Phase Workflow

### Phase 1: Research
- Create GitHub Issue: [RESEARCH] Topic
- Agent searches knowledge base
- Agent searches code examples
- Agent reviews documentation
- **Output**: Summary (context firewall)
- **Checkpoint**: Approve research direction

### Phase 2: Plan
- Create GitHub Issue: [PLAN] Feature
- Agent creates implementation plan
- Agent identifies dependencies
- **Output**: Plan document (context firewall)
- **Checkpoint**: Approve implementation plan

### Phase 3: Implementation
- Create git worktree: `worktrees/implement-feature`
- Agent implements in isolation
- Agent commits incrementally
- **Output**: Working code + commits
- **Checkpoint**: Review code

### Phase 4: Validation
- Run tests in worktree
- Check quality gates
- **Output**: Test results + validation report
- **Checkpoint**: Approve validation

### Phase 5: Integration
- Merge worktree to main
- Close related GitHub Issues
- **Output**: Integrated feature
- **Checkpoint**: Approve deployment

## Key Principles

1. **Git is the database** - Everything in Git
2. **Context firewalls** - Summaries, not full context
3. **Human checkpoints** - Critical decisions require approval
4. **Parallel execution** - Git worktrees for agents
"""

    def _feature_template(self) -> str:
        return """# Feature Implementation Template

## 1. Research Phase
- [ ] Search knowledge base for similar features
- [ ] Review code examples
- [ ] Identify best practices
- [ ] Document findings

## 2. Planning Phase
- [ ] Break down into tasks
- [ ] Identify dependencies
- [ ] Estimate complexity
- [ ] Create implementation checklist

## 3. Implementation Phase
- [ ] Create git worktree
- [ ] Set up development environment
- [ ] Implement core functionality
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Commit incrementally

## 4. Validation Phase
- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Visual regression (if UI)
- [ ] Accessibility tests (if UI)
- [ ] Security scan
- [ ] Performance check

## 5. Integration Phase
- [ ] Merge to main branch
- [ ] Update documentation
- [ ] Close related issues
- [ ] Deploy to preview
- [ ] Monitor for issues
"""

    def _bugfix_template(self) -> str:
        return """# Bug Fix Template

## 1. Reproduce
- [ ] Create minimal reproduction case
- [ ] Document expected vs actual behavior
- [ ] Identify affected versions

## 2. Diagnose
- [ ] Read error logs
- [ ] Add debug logging
- [ ] Trace execution flow
- [ ] Identify root cause

## 3. Fix
- [ ] Create worktree
- [ ] Implement fix
- [ ] Add regression test
- [ ] Verify fix works

## 4. Validate
- [ ] Run all tests
- [ ] Test edge cases
- [ ] Verify no side effects

## 5. Deploy
- [ ] Merge to main
- [ ] Deploy hotfix
- [ ] Monitor for recurrence
"""

    def _pre_merge_checklist(self) -> str:
        return """# Pre-Merge Checklist

Before merging to main, verify:

## Code Quality
- [ ] Code follows style guide
- [ ] No commented-out code
- [ ] No console.log/print statements
- [ ] Meaningful variable/function names
- [ ] Proper error handling

## Tests
- [ ] All tests passing
- [ ] New tests added for new features
- [ ] Edge cases covered
- [ ] Test coverage acceptable

## Documentation
- [ ] README updated if needed
- [ ] API docs updated if needed
- [ ] Comments on complex logic
- [ ] Changelog updated

## Security
- [ ] No hardcoded secrets
- [ ] No SQL injection vulnerabilities
- [ ] Input validation present
- [ ] Authentication/authorization correct

## Performance
- [ ] No N+1 queries
- [ ] Reasonable response times
- [ ] No memory leaks
- [ ] Database queries optimized

## UI (if applicable)
- [ ] Mobile responsive (375px, 768px, 1920px)
- [ ] Accessible (WCAG 2.1 AA)
- [ ] Visual regression tests pass
- [ ] Design tokens used (no magic numbers)
"""

    def _pre_deploy_checklist(self) -> str:
        return """# Pre-Deployment Checklist

Final checks before production deployment:

## Environment
- [ ] Environment variables set
- [ ] Database migrations ready
- [ ] API keys configured
- [ ] SSL certificates valid

## Testing
- [ ] All tests passing in CI/CD
- [ ] Preview deployment tested
- [ ] Smoke tests passed
- [ ] Load testing done (if high traffic)

## Monitoring
- [ ] Error tracking configured
- [ ] Performance monitoring active
- [ ] Logs properly configured
- [ ] Alerts set up

## Rollback Plan
- [ ] Rollback procedure documented
- [ ] Database migrations reversible
- [ ] Previous version accessible
- [ ] Rollback tested

## Communication
- [ ] Team notified of deployment
- [ ] Stakeholders informed
- [ ] Support team briefed
- [ ] Documentation updated
"""

    def _summary_guide(self) -> str:
        return """# Context Firewall Summary Guide

How to create effective summaries (90% token reduction):

## Summary Structure

### 1. Key Points (Bullet List)
Extract the most important findings:
- Main conclusion
- Critical decisions
- Recommendations
- Blockers/risks

### 2. Metrics
Quantify the results:
- Number of patterns found
- Test pass rate
- Performance metrics
- Coverage percentage

### 3. Next Steps
What happens next:
- Recommended actions
- Open questions
- Dependencies

### 4. Full Document Link
Always include link to full output:
- Saved in: `.autoflow/context-firewalls/[agent]-[phase]-[timestamp].md`

## Example

**Without Summary** (20,000 tokens):
[Full 15,000 line research document...]

**With Summary** (2,000 tokens):
```
SUMMARY:
- 5 authentication patterns analyzed
- JWT + Passport.js recommended
- Security: token rotation + HTTPS required
- Implementation time: ~4 hours
- Code examples: 3 reviewed

NEXT STEPS:
- Approve JWT approach
- Begin implementation
- Security review needed

FULL DOCUMENT: .autoflow/context-firewalls/research-auth-20250110.md
```

**Token Savings**: 90%
"""


if __name__ == '__main__':
    server = AutoFlowMCPServer()

    # List resources
    print("Available Resources:")
    for resource in server.list_resources():
        print(f"  - {resource['uri']}: {resource['name']}")

    # Read example resource
    print("\n" + "="*60)
    print(server.read_resource("workflow://overview"))
