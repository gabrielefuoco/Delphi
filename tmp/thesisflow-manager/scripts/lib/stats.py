from pathlib import Path
from .models import Project

class StatsAnalyzer:
    def __init__(self, project: Project):
        self.project = project

    def count_words(self, text: str) -> int:
        return len(text.split())

    def analyze(self):
        print(f"\nProject Statistics: {self.project.name}")
        print(f"{'Chapter':<40} | {'Paragraphs':<10} | {'Words':<10} | {'Time (min)':<10}")
        print("-" * 80)
        
        total_words = 0
        total_time = 0
        
        for chapter in self.project.chapters:
            chap_words = 0
            for p in chapter.paragraphs:
                chap_words += self.count_words(p.content)
            
            # Estimate reading time (200 wpm)
            time_min = round(chap_words / 200, 1)
            
            total_words += chap_words
            total_time += time_min
            
            print(f"{chapter.title:<40} | {len(chapter.paragraphs):<10} | {chap_words:<10} | {time_min:<10}")
            
        print("-" * 80)
        print(f"{'TOTAL':<40} | {sum(len(c.paragraphs) for c in self.project.chapters):<10} | {total_words:<10} | {round(total_time, 1):<10}")
