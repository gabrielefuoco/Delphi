import shutil
from pathlib import Path
import logging
import bibtexparser
import difflib
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from .research_service import ResearchService

from .utils import bibtex_escape

logger = logging.getLogger(__name__)

class BibCleaner:
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root).resolve()
        self.bib_path = self.project_root / "references.bib"
        self.research_service = ResearchService(self.project_root)

    def clean(self, force: bool = False):
        if not self.bib_path.exists():
            logger.error("No references.bib found.")
            return

        # 1. Backup
        backup_path = self.bib_path.with_suffix(".bib.bak")
        shutil.copy2(self.bib_path, backup_path)
        logger.info(f"Backup created at {backup_path.name}")

        # 2. Parse
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        with open(self.bib_path, "r", encoding="utf-8") as f:
            bib_db = bibtexparser.load(f, parser=parser)

        cleaned_count = 0
        total = len(bib_db.entries)
        
        logger.info(f"Analyzing {total} entries...")

        for entry in bib_db.entries:
            if force or self._is_dirty(entry):
                logger.info(f"Repairing: {entry.get('ID')} - {entry.get('title')[:30]}...")
                if self._repair_entry(entry):
                    cleaned_count += 1
        
        # 3. Save
        if cleaned_count > 0:
            with open(self.bib_path, "w", encoding="utf-8") as f:
                bibtexparser.dump(bib_db, f)
            logger.info(f"Successfully cleaned {cleaned_count} entries.")
        else:
            logger.info("No entries needed cleaning.")

    def _is_dirty(self, entry):
        journal = entry.get("journal", "").lower()
        title = entry.get("title", "")
        
        # Criteria for dirty
        if journal in ["pubmed", "arxiv", "biorxiv", "medrxiv"]:
            return True
        if " [pii]" in entry.get("doi", ""):
            return True
        if " [doi]" in entry.get("doi", ""):
            return True
            
        # Check for bad author formatting (e.g. "S. DF" pattern implies reversed First Last)
        # Check if comma is missing in author field (implies "Surname Initials" format which needs comma)
        # Only if there are authors
        authors = entry.get("author", "")
        if authors and "," not in authors and " and " in authors:
             # Multiple authors but no commas? Likely "Smith J and Doe A" -> Dirty
             return True
        
        # Check for initials-only authors (e.g. "Fernandez, R") to force full name fetch
        if authors:
            for au in authors.split(" and "):
                parts = au.strip().split(",")
                if len(parts) == 2:
                    given = parts[1].strip()
                    # If given name is just 1 or 2 chars (R or R.) -> Dirty
                    if len(given) <= 2:
                        return True

        return False

    def _repair_entry(self, entry):
        """Attempts to fetch fresh metadata and update the entry."""
        title = entry.get("title")
        if not title: return False

        # Use our improved ResearchService to look it up using Crossref (Strict)
        doi = entry.get("doi", "").strip()
        if "[" in doi: 
             doi = doi.split("[")[0].strip()
        
        fresh_paper = self.research_service.get_paper_metadata_crossref(doi=doi if doi else None, title=title)
        
        if not fresh_paper:
            logger.warning(f"  FAILED: Crossref could not find metadata for '{title}' (DOI: {doi})")
            return False
        
        # Verify it's likely the same paper (check title similarity)
        orig_title = title.strip().lower()
        new_title = fresh_paper.title.strip().lower()
        
        if len(orig_title) > 5:
            matcher = difflib.SequenceMatcher(None, orig_title, new_title)
            ratio = matcher.ratio()
            if ratio < 0.4:
                logger.warning(f"MATCH REJECTED: Similarity {ratio:.2f} too low.")
                logger.warning(f"  Orig: {orig_title[:50]}...")
                logger.warning(f"  New:  {new_title[:50]}...")
                return False

        # Update fields with LaTeX escaping
        entry["title"] = bibtex_escape(fresh_paper.title)
        entry["author"] = " and ".join([bibtex_escape(a) for a in fresh_paper.authors])
        entry["year"] = fresh_paper.year
        entry["journal"] = bibtex_escape(fresh_paper.source)
        if fresh_paper.doi:
            entry["doi"] = fresh_paper.doi
            
        logger.info(f"  -> Updated to: {fresh_paper.source}, {fresh_paper.year}")
        return True
