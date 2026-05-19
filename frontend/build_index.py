import os

html_template = """<!doctype html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Logix Numpy - Logistika Xaritasi</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <style>
{css_content}
    </style>
    
    <!-- React & ReactDOM -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <!-- Babel Standalone for in-browser JSX compilation -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  </head>
  <body>
    <div id="root"></div>
    <script type="text/babel">
{jsx_content}
    </script>
  </body>
</html>"""

with open('src/index.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    jsx_content = f.read()

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template.replace('{css_content}', css_content).replace('{jsx_content}', jsx_content))

print('index.html successfully updated')