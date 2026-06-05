from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

@dataclass
class Paragraph:
    path: Path
    title: str
    content: str = ""

@dataclass
class Chapter:
    path: Path
    title: str
    paragraphs: List[Paragraph] = field(default_factory=list)

@dataclass
class Project:
    path: Path
    name: str
    chapters: List[Chapter] = field(default_factory=list)
