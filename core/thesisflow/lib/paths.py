import sys
import os
import shutil
from pathlib import Path

# Adapted from src/utils/paths.py for the skill environment
# We assume the skill might be run from anywhere, but binaries might be system-wide or relative to the agent.
# For simplicity, we check system path first, then maybe a local bin folder in the skill.

def get_skill_root() -> Path:
    """Returns the root directory of this skill."""
    return Path(__file__).resolve().parent.parent.parent

def get_bin_dir() -> Path:
    # Optional: could bundle binaries with the skill
    return get_skill_root() / "assets" / "bin"

def get_templates_dir() -> Path:
    return get_skill_root() / "assets" / "templates"

def get_pandoc_exe() -> Path:
    exe_name = "pandoc.exe" if sys.platform == "win32" else "pandoc"
    
    # 1. System Path (Preferred for skills)
    system_path = shutil.which("pandoc")
    if system_path:
        return Path(system_path)
        
    # 2. Bundled Bin
    bundled = get_bin_dir() / exe_name
    if bundled.exists():
        return bundled
        
    return Path(exe_name) # Return default to let it fail with a clear message or searching in PATH implicitly

def get_typst_exe() -> Path:
    exe_name = "typst.exe" if sys.platform == "win32" else "typst"
    
    # 1. System Path
    system_path = shutil.which("typst")
    if system_path:
        return Path(system_path)

    # 2. Bundled Bin
    bundled = get_bin_dir() / exe_name
    if bundled.exists():
        return bundled
        
    return Path(exe_name)
