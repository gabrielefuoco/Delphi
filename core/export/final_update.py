import re
import os

with open("a.py", "r", encoding="utf-8") as f:
    content = f.read()

# Make it light theme
content = content.replace("background-color: #09090b;", "background-color: transparent;")
content = content.replace("color: #f8fafc;", "color: #000000;")
content = content.replace("rgba(255, 255, 255, 0.03)", "rgba(0, 0, 0, 0.05)")

# Orbs
content = content.replace("linear-gradient(135deg, #2563eb, #06b6d4)", "linear-gradient(135deg, #e2e8f0, #f8fafc)")
content = content.replace("linear-gradient(135deg, #7c3aed, #db2777)", "linear-gradient(135deg, #cbd5e1, #f1f5f9)")
content = content.replace("linear-gradient(135deg, #059669, #84cc16)", "linear-gradient(135deg, #94a3b8, #e2e8f0)")

# Lines
content = content.replace("background-color: rgba(255, 255, 255, 0.02);", "background-color: rgba(0, 0, 0, 0.02);")
content = content.replace("border-right: 1px solid rgba(255, 255, 255, 0.1);", "border-right: 1px solid rgba(0, 0, 0, 0.1);")
content = content.replace("color: #334155;", "color: #94a3b8;")

# Dots
content = content.replace("background-color: #ef4444;", "background-color: #cbd5e1;")
content = content.replace("background-color: #f59e0b;", "background-color: #94a3b8;")
content = content.replace("background-color: #10b981;", "background-color: #64748b;")

# Text
content = content.replace("color: #64748b;", "color: #475569;")
content = content.replace("color: #c678dd;", "color: #000000; font-weight: bold;")
content = content.replace("color: #e5c07b;", "color: #333333;")
content = content.replace("color: #98c379;", "color: #475569; font-style: italic;")
content = content.replace("color: #61afef;", "color: #0f172a; font-weight: bold;")
content = content.replace("color: #56b6c2;", "color: #000000;")
content = content.replace("color: #ffffff;", "color: #000000;")
content = content.replace("color: #09090b;", "color: #ffffff;")

# Vol Tags shadows and backgrounds
content = content.replace("linear-gradient(90deg, #3b82f6, #06b6d4)", "linear-gradient(90deg, #64748b, #94a3b8)")
content = content.replace("linear-gradient(90deg, #8b5cf6, #d946ef)", "linear-gradient(90deg, #475569, #64748b)")
content = content.replace("linear-gradient(90deg, #10b981, #a3e635)", "linear-gradient(90deg, #334155, #475569)")
content = content.replace("box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);", "box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")
content = content.replace("box-shadow: 0 0 15px rgba(217, 70, 239, 0.4);", "box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")
content = content.replace("box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);", "box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")

# Subtitle
content = content.replace("color: #cbd5e1;", "color: #334155;")
content = content.replace("border-left: 3px solid rgba(255, 255, 255, 0.2);", "border-left: 3px solid rgba(0, 0, 0, 0.2);")

# Footer lines
content = content.replace("border-top: 1px dashed rgba(255, 255, 255, 0.15);", "border-top: 1px dashed rgba(0, 0, 0, 0.2);")

# Update filenames
content = content.replace('<title>PRO Python - Cyber/Dark Mode</title>', '<title>PRO Python - Light/Print Mode</title>')
content = content.replace('output_pdf = "Copertine_Python_DarkNeon_Cyber.pdf"', 'output_pdf = "Copertine_Python_Print.pdf"')
content = content.replace('Copertine_Python_DarkNeon_Cyber.html', 'Copertine_Python_Print.html')

# Replace SVGs with IMGs
# Python
svg_python = '''<svg class="animal-svg" viewBox="0 0 100 100" fill="none" stroke="#22d3ee" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15,50 C15,25 32,15 50,15 C68,15 85,25 85,45 C85,65 68,75 50,75 C35,75 25,65 25,52 C25,38 38,30 50,30 C60,30 68,38 68,48 C68,56 58,62 50,62 C44,62 40,56 42,51 C43,46 48,46 48,49" />
                <path d="M15,50 C13,52 10,50 9,47 C8,44 10,42 13,43" />
                <path d="M9,47 L4,47 M5,45 L1,44 M5,49 L1,50" />
                <circle cx="50" cy="15" r="2" fill="#0ea5e9" /><circle cx="68" cy="15" r="1.5" fill="#0ea5e9" /><circle cx="85" cy="45" r="2" fill="#0ea5e9" />
                <path d="M28,62 L32,59 M32,66 L36,63" stroke="rgba(34, 211, 238, 0.5)" />
            </svg>'''
img_python = '<img src="file:///c:/Users/gabri/APP/copertina/python.png" style="width: 100%; height: 100%; object-fit: contain;" />'
content = content.replace(svg_python, img_python)

# Octopus
svg_octopus = '''<svg class="animal-svg" viewBox="0 0 100 100" fill="none" stroke="#e879f9" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M25,20 L35,27 L65,27 L75,20 L80,40 C80,65 72,82 50,82 C28,82 20,65 20,40 Z" />
                <circle cx="40" cy="42" r="8" /><circle cx="60" cy="42" r="8" />
                <circle cx="40" cy="42" r="2.5" fill="#e879f9" /><circle cx="60" cy="42" r="2.5" fill="#e879f9" />
                <path d="M47,47 L53,47 L50,56 Z" fill="#e879f9" />
                <path d="M20,45 C26,52 32,52 37,45 M80,45 C74,52 68,52 63,45" />
                <line x1="45" y1="62" x2="42" y2="65" stroke="rgba(232, 121, 249, 0.5)" /><line x1="50" y1="62" x2="47" y2="65" stroke="rgba(232, 121, 249, 0.5)" />
                <circle cx="25" cy="20" r="2" fill="#d946ef" /><circle cx="75" cy="20" r="2" fill="#d946ef" />
                <circle cx="50" cy="82" r="2" fill="#d946ef" />
            </svg>'''
img_octopus = '<img src="file:///c:/Users/gabri/APP/copertina/octopus.png" style="width: 100%; height: 100%; object-fit: contain;" />'
content = content.replace(svg_octopus, img_octopus)

# Owl
svg_owl = '''<svg class="animal-svg" viewBox="0 0 100 100" fill="none" stroke="#4ade80" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M30,38 C30,12 70,12 70,38 C70,48 64,54 50,54 C36,54 30,48 30,38 Z" />
                <circle cx="42" cy="40" r="2" fill="#4ade80" /><circle cx="58" cy="40" r="2" fill="#4ade80" />
                <path d="M40,53 C30,62 18,58 12,45 C7,35 15,22 25,28" />
                <path d="M44,54 C34,69 16,72 8,60 C3,50 11,38 22,43" />
                <path d="M47,54 C38,75 22,85 14,75 C9,67 16,54 28,56" />
                <path d="M60,53 C70,62 82,58 88,45 C93,35 85,22 75,28" />
                <path d="M56,54 C66,69 84,72 92,60 C97,50 89,38 78,43" />
                <path d="M53,54 C62,75 78,85 86,75 C91,67 84,54 72,56" />
                <circle cx="12" cy="45" r="2" fill="#22c55e" /><circle cx="8" cy="60" r="2" fill="#22c55e" /><circle cx="14" cy="75" r="2" fill="#22c55e" />
                <circle cx="88" cy="45" r="2" fill="#22c55e" /><circle cx="92" cy="60" r="2" fill="#22c55e" /><circle cx="86" cy="75" r="2" fill="#22c55e" />
            </svg>'''
img_owl = '<img src="file:///c:/Users/gabri/APP/copertina/owl.png" style="width: 100%; height: 100%; object-fit: contain;" />'
content = content.replace(svg_owl, img_owl)

with open("a_print.py", "w", encoding="utf-8") as f:
    f.write(content)
