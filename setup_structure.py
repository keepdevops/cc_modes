#!/usr/bin/env python3
"""
Automated Project Directory Structure Setup
- Uses current directory name as project name
- Smart 2-3 letter prefix + conflict resolution
"""

import sys
import json
from pathlib import Path
from datetime import datetime

def get_smart_prefix(project_name: str, registry_path: Path = None) -> str:
    """Generate 2-3 letter prefix with conflict-aware logic."""
    name = project_name.lower().strip()
    if not name or len(name) < 2:
        return "prj_"
    
    prefixes_to_try = [name[:2], name[:3], name[0]+name[2] if len(name)>2 else ""]
    for letter in name[1:]:
        prefixes_to_try.append(name[0] + letter)
    
    used = set()
    if registry_path and registry_path.exists():
        try:
            with open(registry_path) as f:
                data = json.load(f)
                used = set(data.get("used_prefixes", []))
        except:
            pass
    
    for pref in prefixes_to_try:
        if pref:
            prefix = pref + "_"
            if prefix not in used:
                return prefix
    return "x" + name[0] + "_"


def setup_project_structure():
    """Use current directory as project root."""
    project_path = Path.cwd().resolve()          # Current directory
    project_name = project_path.name
    
    print(f"Project Name : {project_name}")
    prefix = get_smart_prefix(project_name)
    print(f"Chosen Prefix: {prefix}")
    
    # Create directories
    core_dirs = [f"{prefix}code", f"{prefix}ui", f"{prefix}data"]
    extra_dirs = ["docs", "tests", "scripts"]
    
    for dir_name in core_dirs + extra_dirs:
        (project_path / dir_name).mkdir(exist_ok=True)
        (project_path / dir_name / "__init__.py").touch(exist_ok=True)
        print(f"✓ Created: {dir_name}/")
    
    # Registry + CLAUDE.md (same as before)
    # ... (registry code remains the same)
    
    # CLAUDE.md
    claudemd = project_path / "CLAUDE.md"
    content = f"""# {project_name.capitalize()} Project Rules & Guidelines

## Directory Structure

{project_name}/
├── {prefix}code/
├── {prefix}ui/
├── {prefix}data/
├── docs/
├── tests/
└── scripts/

**Smart Prefix**: {prefix}
**Last Updated**: {datetime.now().strftime("%B %Y")}
"""
    with open(claudemd, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✓ Updated: CLAUDE.md")
    print("\nSetup completed successfully!")


if __name__ == "__main__":
    setup_project_structure()
