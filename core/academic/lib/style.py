import json
from pathlib import Path
from typing import List, Optional
from .paths import get_templates_dir

class StyleManager:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.templates_dir = get_templates_dir()

    def list_styles(self) -> List[str]:
        if not self.templates_dir.exists():
            return []
        return [f.stem for f in self.templates_dir.glob("*.typ")]

    def get_current_style(self) -> str:
        config_path = self.project_dir / "delphi.json"
        if not config_path.exists(): return "default_thesis"
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8"))
            return cfg.get("metadata", {}).get("template", "default_thesis")
        except:
            return "default_thesis"

    def set_style(self, style_name: str) -> bool:
        # Verify existence
        target = self.templates_dir / f"{style_name}.typ"
        if not target.exists():
            return False
            
        # Update config
        config_path = self.project_dir / "delphi.json"
        cfg = {"metadata": {}, "order": []}
        if config_path.exists():
             try:
                 cfg = json.loads(config_path.read_text(encoding="utf-8"))
             except: pass
        
        if "metadata" not in cfg: cfg["metadata"] = {}
        cfg["metadata"]["template"] = style_name
        
        config_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
