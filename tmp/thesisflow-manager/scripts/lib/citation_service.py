from pathlib import Path
from typing import List, Dict, Optional, Any
from .bib_parser import BibParser

class BibliographyService:
    def __init__(self):
        self.references: List[Dict] = []
        self._cache_path: Optional[Path] = None

    def load_bibliography(self, path: Path):
        self._cache_path = path
        if path.exists():
            self.references = BibParser.parse_file(str(path))
        else:
            self.references = []

    def get_references(self) -> List[Dict]:
        return self.references

    def search(self, query: str) -> List[Dict]:
        if not query: return self.references
        q = query.lower()
        results = []
        for ref in self.references:
            # Flexible search
            # Bibtex keys are case insensitive usually
            match = False
            for key, val in ref.items():
                if q in str(val).lower():
                    match = True
                    break
            if match:
                results.append(ref)
        return results

    def get_citation_keys(self) -> List[str]:
        return [f"@{ref['ID']}" for ref in self.references if 'ID' in ref]
        
    def add_reference(self, bibtex_str: str) -> bool:
        """Appends reference to file if valid and not duplicate."""
        if not self._cache_path: return False
        
        # 1. Parse Input
        entries = BibParser.parse_string(bibtex_str)
        if not entries:
            # print("Invalid BibTeX syntax.")
            return False
            
        # 2. Check Duplicates
        current_keys = set(self.get_citation_keys()) # "@key" format
        new_entries_to_add = []
        
        for entry in entries:
            # "ID" is the key without @
            if "ID" not in entry: continue
            key = f"@{entry['ID']}"
            
            if key in current_keys:
                # print(f"Duplicate key found: {key}")
                continue
            new_entries_to_add.append(entry)
            
        if not new_entries_to_add:
            return False # Nothing new to add
            
        # 3. Append to File
        try:
            with open(self._cache_path, "a", encoding="utf-8") as f:
                f.write("\n")
                # We write the original string if it was valid? 
                # Or reconstruction? 
                # Since bibtexparser.loads might not preserve exact formatting but parse_string returns dicts.
                # To keep it simple, if the input string contained multiple entries and some were dupes,
                # we technically should only write the non-dupes.
                # But reconstruction from dict is hard without a writer.
                # Given the typical use case is adding ONE citation at a time.
                
                # If we have mixed dupes/new in one string, it's tricky.
                # Let's assume input is usually one entry.
                # If we validated at least one new entry exists, let's write the whole string?
                # No, that writes duplicates.
                
                # Ideally we use bibtexparser to dump the new entries.
                # But BibParser wrapper doesn't have dump.
                # Let's just append the string IF all entries are new.
                # If mixed, we reject?
                
                if len(new_entries_to_add) != len(entries):
                    # Partial duplicate. Reject to be safe/clean?
                    # Or just return False?
                    return False
                
                f.write(bibtex_str.strip() + "\n")
            
            # Reload to sync
            self.load_bibliography(self._cache_path)
            return True
            return False
        except Exception as e:
            # print(f"Error adding reference: {e}")
            return False

    def patch_reference(self, citation_key: str, field: str, value: str) -> bool:
        """
        Safely updates a single field in a citation using bibtexparser.
        Preserves other fields and formatting as much as possible.
        """
        if not self._cache_path or not self._cache_path.exists():
             return False

        # Load with bibtexparser
        import bibtexparser
        from bibtexparser.bparser import BibTexParser
        from bibtexparser.customization import convert_to_unicode
        
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        
        try:
            with open(self._cache_path, "r", encoding="utf-8") as f:
                bib_db = bibtexparser.load(f, parser=parser)
                
            # Find entry
            entry_found = False
            # Strip @ from key if present
            target_key = citation_key.lstrip("@")
            
            for entry in bib_db.entries:
                if entry.get("ID") == target_key:
                    entry[field] = value
                    entry_found = True
                    break
            
            if not entry_found:
                return False
                
            # Write back
            with open(self._cache_path, "w", encoding="utf-8") as f:
                bibtexparser.dump(bib_db, f)
            
            # Reload cache
            self.load_bibliography(self._cache_path)
            return True
            
        except Exception as e:
            # print(f"Error patching reference: {e}")
            return False

    def deduplicate(self) -> Dict[str, Any]:
        """
        Removes entries with duplicate IDs or very similar titles.
        Returns stats on what was removed.
        """
        if not self._cache_path or not self._cache_path.exists():
            return {"success": False, "message": "No bibliography file found."}

        import bibtexparser
        from bibtexparser.bparser import BibTexParser
        from bibtexparser.customization import convert_to_unicode
        
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        
        try:
            with open(self._cache_path, "r", encoding="utf-8") as f:
                bib_db = bibtexparser.load(f, parser=parser)
            
            initial_count = len(bib_db.entries)
            unique_entries = []
            seen_keys = set()
            seen_titles = set()
            removed_keys = []

            for entry in bib_db.entries:
                key = entry.get("ID")
                title = entry.get("title", "").lower().strip()
                # Normalize title slightly (remove non-alphanum)
                norm_title = "".join([c for c in title if c.isalnum()])
                
                if key in seen_keys:
                    removed_keys.append(f"{key} (duplicate ID)")
                    continue
                
                if norm_title and norm_title in seen_titles:
                    removed_keys.append(f"{key} (duplicate title)")
                    continue
                
                unique_entries.append(entry)
                seen_keys.add(key)
                if norm_title: seen_titles.add(norm_title)
            
            bib_db.entries = unique_entries
            
            if len(removed_keys) > 0:
                with open(self._cache_path, "w", encoding="utf-8") as f:
                    bibtexparser.dump(bib_db, f)
                self.load_bibliography(self._cache_path)
            
            return {
                "success": True, 
                "initial_count": initial_count,
                "final_count": len(unique_entries),
                "removed": removed_keys
            }
        except Exception as e:
            return {"success": False, "message": f"Error during deduplication: {e}"}

    def check_files(self, project_root: Path) -> List[Dict[str, Any]]:
        """Verifies that 'file' paths in entries exist on disk."""
        issues = []
        for ref in self.references:
            file_field = ref.get("file")
            if not file_field:
                continue
                
            # Multiple files possible, separated by ;
            files = file_field.split(";")
            for f_entry in files:
                parts = f_entry.split(":")
                path_part = None
                if len(parts) == 1: path_part = parts[0]
                elif len(parts) >= 2:
                    if not parts[0].strip():
                         if len(parts) >= 2: path_part = parts[1]
                    else:
                        if len(parts[0]) == 1 and parts[0].isalpha(): path_part = f_entry
                        else: path_part = parts[1]
                
                if path_part:
                    p = Path(path_part)
                    if not p.is_absolute():
                        p = project_root / p
                    
                    if not p.exists():
                        issues.append({
                            "key": ref.get("ID"),
                            "file": path_part,
                            "full_path": str(p),
                            "issue": "File not found"
                        })
        return issues
