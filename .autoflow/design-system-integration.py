#!/usr/bin/env python3
"""
ProductionForge Design System Integration

When task type is UI, this module integrates the ProductionForge design
system to prevent UI hallucination.

Uses the complete design system I built earlier:
- design-tokens.ts (spacing, colors, typography)
- components-guide.md (component decision tree)
- responsive-rules.md (mobile-first patterns)
- accessibility.md (WCAG 2.1 AA standards)
- anti-patterns.md (what NOT to do)
"""

from pathlib import Path
from typing import Dict, Optional


class DesignSystemIntegration:
    """Integrate ProductionForge design system for UI tasks"""

    def __init__(self):
        # Path to ProductionForge design system
        self.design_system_path = Path(__file__).parent.parent.parent / "ProductionForge" / ".productionforge" / "design-system"

        if not self.design_system_path.exists():
            print(f"⚠️  Design system not found at: {self.design_system_path}")
            print("   UI hallucination prevention disabled")
            self.enabled = False
        else:
            self.enabled = True

    def load_design_system(self) -> Dict[str, str]:
        """Load complete design system into agent context"""
        if not self.enabled:
            return {}

        files = {
            'design_tokens': 'design-tokens.ts',
            'components_guide': 'components-guide.md',
            'responsive_rules': 'responsive-rules.md',
            'accessibility': 'accessibility.md',
            'anti_patterns': 'anti-patterns.md',
        }

        design_system = {}

        for key, filename in files.items():
            file_path = self.design_system_path / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    design_system[key] = f.read()

        print(f"✅ Loaded design system: {len(design_system)} files")
        return design_system

    def create_ui_specialist_prompt(self, base_prompt: str) -> str:
        """Create UI specialist prompt with design system loaded"""
        if not self.enabled:
            return base_prompt

        design_system = self.load_design_system()

        ui_prompt = f"""{base_prompt}

# CRITICAL: Design System Integration (UI Hallucination Prevention)

You are implementing UI with **STRICT adherence to design system**.

## DESIGN TOKENS (ONLY USE THESE)

{design_system.get('design_tokens', '')}

## COMPONENTS GUIDE (DECISION TREE)

{design_system.get('components_guide', '')}

## RESPONSIVE RULES (MOBILE-FIRST)

{design_system.get('responsive_rules', '')}

## ACCESSIBILITY STANDARDS (WCAG 2.1 AA)

{design_system.get('accessibility', '')}

## ANTI-PATTERNS (NEVER DO THESE)

{design_system.get('anti_patterns', '')}

## VALIDATION CHECKLIST

Before committing UI code, verify:
- [ ] Used design tokens (no magic numbers)
- [ ] Used shadcn/ui components (no raw HTML)
- [ ] Mobile responsive (375px, 768px, 1920px)
- [ ] Accessible (keyboard nav, ARIA, contrast)
- [ ] No hardcoded colors
- [ ] Touch targets 44×44px minimum
- [ ] Focus indicators visible
- [ ] Alt text on all images
- [ ] Labels on all inputs

**Result**: Perfect UI on first try. No rework. No hallucination.
"""

        return ui_prompt

    def validate_ui_code(self, code: str) -> Dict[str, any]:
        """Validate UI code against design system"""
        violations = []

        # Check for magic numbers
        import re
        magic_pattern = r'\[(\d+)px\]'
        matches = re.findall(magic_pattern, code)
        allowed = {'0', '4', '8', '12', '16', '20', '24', '32', '40', '48', '64', '80', '96'}

        for match in matches:
            if match not in allowed:
                violations.append(f"Magic number: [{match}px]")

        # Check for hardcoded colors
        color_pattern = r'#[0-9a-fA-F]{3,6}'
        colors = re.findall(color_pattern, code)
        if colors:
            violations.append(f"Hardcoded colors: {', '.join(colors)}")

        return {
            "valid": len(violations) == 0,
            "violations": violations
        }


if __name__ == '__main__':
    # Demo integration
    integration = DesignSystemIntegration()

    if integration.enabled:
        print("✅ Design system integration enabled")

        # Load design system
        ds = integration.load_design_system()
        print(f"\n📚 Loaded {len(ds)} design system files")

        # Test validation
        bad_code = '<div className="p-[17px] bg-[#3b82f6]">Test</div>'
        result = integration.validate_ui_code(bad_code)

        print(f"\n🔍 Validation test:")
        print(f"   Valid: {result['valid']}")
        if result['violations']:
            print(f"   Violations:")
            for v in result['violations']:
                print(f"     - {v}")
    else:
        print("❌ Design system not found")
        print("   Run from AutoFlow directory with ProductionForge as sibling")
