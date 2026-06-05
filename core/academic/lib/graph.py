from .models import Project

class GraphGenerator:
    def __init__(self, project: Project):
        self.project = project

    def generate_mermaid(self) -> str:
        """Generates a Mermaid.js graph valid string."""
        lines = ["graph TD"]
        root_id = "Root"
        lines.append(f'    {root_id}["{self.project.name}"]')
        
        # Style
        # lines.append("    style Root fill:#f9f,stroke:#333,stroke-width:2px")
        
        for i, chapter in enumerate(self.project.chapters):
            chap_id = f"C{i}"
            lines.append(f'    {root_id} --> {chap_id}["{chapter.title}"]')
            
            for j, para in enumerate(chapter.paragraphs):
                para_id = f"{chap_id}P{j}"
                lines.append(f'    {chap_id} --> {para_id}["{para.title}"]')
                
                # Optional: Add click events or logic flow if we were parsing content
                
        return "\n".join(lines)
