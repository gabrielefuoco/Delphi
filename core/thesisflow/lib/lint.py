import re
from pathlib import Path
from typing import List, Dict
from .models import Project
from .citation_service import BibliographyService

class Linter:
    def __init__(self, project: Project):
        self.project = project
        self.bib_service = BibliographyService()
        self.bib_service.load_bibliography(project.path / "references.bib")
        self.issues = []

    def check(self) -> List[Dict]:
        """Runs all checks and returns a list of issues."""
        self.issues = []
        self._check_content()
        return self.issues

    def _check_content(self):
        valid_bib_keys = set(self.bib_service.get_citation_keys()) # e.g., {'@smith2020', ...}
        # Normalize to just keys without @ for easier searching if needed, 
        # but standard pandoc citation is [@key].
        # Let's ensure keys in set match content usage.
        
        # Regexes
        # TODOs
        re_todo = re.compile(r'\b(TODO|FIXME|XXX)\b')
        # Assets: ![alt](path)
        re_asset = re.compile(r'!\[.*?\]\((.*?)\)')
        # Citations: [@key] or [@key; @key2]
        # Simplified: look for @(\w+) inside brackets? 
        # Pandoc syntax is complex, simplified: \[.*?@(\w+).*?\]
        re_cite = re.compile(r'@([a-zA-Z0-9_:-]+)') 

        for chapter in self.project.chapters:
            for p in chapter.paragraphs:
                lines = p.content.split('\n')
                for i, line in enumerate(lines):
                    ln = i + 1
                    location = f"{chapter.title}/{p.title}.md:{ln}"

                    # 1. TODO Check
                    if match := re_todo.search(line):
                        self.issues.append({
                            "type": "TODO",
                            "severity": "warning",
                            "message": f"Found {match.group(1)} marker.",
                            "location": location
                        })

                    # 2. Asset Check
                    for match in re_asset.finditer(line):
                        asset_path = match.group(1)
                        # Check strictly local assets in assets/ folder
                        if not asset_path.startswith("http") and not asset_path.startswith("www"):
                            # Resolve path relative to project root?
                            # Usually usage is 'assets/image.png'
                            full_path = self.project.path / asset_path
                            if not full_path.exists():
                                self.issues.append({
                                    "type": "BROKEN_LINK",
                                    "severity": "error",
                                    "message": f"Asset not found: {asset_path}",
                                    "location": location
                                })

                    # 3. Citation Check
                    # We scan for @key patterns. If it looks like a key, check bib.
                    # This is heuristical.
                    if '[' in line and ']' in line:
                         for match in re_cite.finditer(line):
                             key = match.group(1)
                             # Construct expected key format for set check
                             # valid_bib_keys has '@key'
                             if f"@{key}" not in valid_bib_keys:
                                  self.issues.append({
                                    "type": "MISSING_CITATION",
                                    "severity": "error",
                                    "message": f"Citation key '@{key}' missing in bibliography.",
                                    "location": location
                                })
