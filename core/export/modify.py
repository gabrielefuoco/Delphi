import re

with open("a.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace css background from #09090b to transparent
content = content.replace("background-color: #09090b;", "background-color: transparent;")

# Replace body text color from #f8fafc to #000000
content = content.replace("color: #f8fafc;", "color: #000000;")

# Grid
content = content.replace("rgba(255, 255, 255, 0.03)", "rgba(0, 0, 0, 0.05)")

# Orbs - make them gray gradients
content = content.replace("linear-gradient(135deg, #2563eb, #06b6d4)", "linear-gradient(135deg, #e2e8f0, #f8fafc)")
content = content.replace("linear-gradient(135deg, #7c3aed, #db2777)", "linear-gradient(135deg, #cbd5e1, #f1f5f9)")
content = content.replace("linear-gradient(135deg, #059669, #84cc16)", "linear-gradient(135deg, #94a3b8, #e2e8f0)")

# Line numbers
content = content.replace("background-color: rgba(255, 255, 255, 0.02);", "background-color: rgba(0, 0, 0, 0.02);")
content = content.replace("border-right: 1px solid rgba(255, 255, 255, 0.1);", "border-right: 1px solid rgba(0, 0, 0, 0.1);")
content = content.replace("color: #334155;", "color: #94a3b8;")

# Dots
content = content.replace("background-color: #ef4444;", "background-color: #cbd5e1;")
content = content.replace("background-color: #f59e0b;", "background-color: #94a3b8;")
content = content.replace("background-color: #10b981;", "background-color: #64748b;")

# Header
content = content.replace("color: #64748b;", "color: #475569;")

# Syntax
content = content.replace("color: #c678dd;", "color: #000000; font-weight: bold;")
content = content.replace("color: #e5c07b;", "color: #333333;")
content = content.replace("color: #98c379;", "color: #475569; font-style: italic;")
content = content.replace("color: #61afef;", "color: #0f172a; font-weight: bold;")
content = content.replace("color: #56b6c2;", "color: #000000;")

# H1
content = content.replace("color: #ffffff;", "color: #000000;")

# Vol Tags
content = content.replace("color: #09090b;", "color: #ffffff;")
content = content.replace("linear-gradient(90deg, #3b82f6, #06b6d4)", "linear-gradient(90deg, #64748b, #94a3b8)")
content = content.replace("linear-gradient(90deg, #8b5cf6, #d946ef)", "linear-gradient(90deg, #475569, #64748b)")
content = content.replace("linear-gradient(90deg, #10b981, #a3e635)", "linear-gradient(90deg, #334155, #475569)")
content = content.replace("box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);", "box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")
content = content.replace("box-shadow: 0 0 15px rgba(217, 70, 239, 0.4);", "box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")
content = content.replace("box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);", "box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")

# Subtitle
content = content.replace("color: #cbd5e1;", "color: #334155;")
content = content.replace("border-left: 3px solid rgba(255, 255, 255, 0.2);", "border-left: 3px solid rgba(0, 0, 0, 0.2);")

# SVGs
content = content.replace('stroke="#22d3ee"', 'stroke="#1e293b"')
content = content.replace('stroke="#e879f9"', 'stroke="#1e293b"')
content = content.replace('stroke="#4ade80"', 'stroke="#1e293b"')

content = content.replace('fill="#0ea5e9"', 'fill="#475569"')
content = content.replace('fill="#e879f9"', 'fill="#475569"')
content = content.replace('fill="#d946ef"', 'fill="#64748b"')
content = content.replace('fill="#4ade80"', 'fill="#475569"')
content = content.replace('fill="#22c55e"', 'fill="#64748b"')

content = content.replace('stroke="rgba(34, 211, 238, 0.5)"', 'stroke="rgba(0, 0, 0, 0.4)"')
content = content.replace('stroke="rgba(232, 121, 249, 0.5)"', 'stroke="rgba(0, 0, 0, 0.4)"')

# Footer / lines
content = content.replace("border-top: 1px dashed rgba(255, 255, 255, 0.15);", "border-top: 1px dashed rgba(0, 0, 0, 0.2);")
content = content.replace('<title>PRO Python - Cyber/Dark Mode</title>', '<title>PRO Python - Light/Print Mode</title>')
content = content.replace('output_pdf = "Copertine_Python_DarkNeon_Cyber.pdf"', 'output_pdf = "Copertine_Python_Print.pdf"')
content = content.replace('Copertine_Python_DarkNeon_Cyber.html', 'Copertine_Python_Print.html')

with open("a.py", "w", encoding="utf-8") as f:
    f.write(content)
