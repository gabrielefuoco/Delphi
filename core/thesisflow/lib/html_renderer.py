# Ported from src/utils/html_renderer.py
# Simplified to match the skill environment (no Theme dependency unless we port Theme too)

class HTMLRenderer:
    @staticmethod
    def get_styles() -> str:
        """Generates a CSS <style> block."""
        # Hardcode some nice defaults since we don't have Theme class
        bg = "#ffffff"
        text = "#1a1a1a"
        accent = "#2563eb"
        font = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        
        return f"""
        <style>
            body {{
                background-color: {bg};
                color: {text};
                font-family: {font};
                font-size: 16px;
                line-height: 1.6;
                margin: 0 auto;
                max_width: 800px;
                padding: 20px;
            }}
            h1, h2, h3 {{ color: {accent}; margin-top: 1.5em; }}
            h1 {{ border-bottom: 1px solid #eee; padding-bottom: 0.3em; }}
            code {{ background-color: #f1f5f9; padding: 2px 4px; border-radius: 4px; font-family: monospace; }}
            pre {{ background-color: #f1f5f9; padding: 15px; border-radius: 8px; overflow-x: auto; }}
            blockquote {{ border-left: 4px solid {accent}; margin: 0; padding-left: 15px; color: #666; font-style: italic; }}
            img {{ max-width: 100%; border-radius: 8px; }}
            a {{ color: {accent}; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
        """

    @classmethod
    def render(cls, md_text: str, project_path: str = None) -> str:
        """Converts markdown to HTML string."""
        import markdown # Standard markdown or markdown2 if installed.
        # User had markdown2 in source. We might not have it in agent env.
        # For agent skill, usually better to stick to standard lib or simple replacement if possible.
        # But let's assume `markdown` package is available or we use simple substitution for now if it fails.
        
        try:
            import markdown
            html_content = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
        except ImportError:
            # Fallback
            html_content = f"<pre>{md_text}</pre>"
        
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            {cls.get_styles()}
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        return full_html
