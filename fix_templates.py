import os
import re

for root, dirs, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace url_for('static', path='...') with '/static/...'
            new_content = re.sub(r"\{\{\s*url_for\('static',\s*path='([^']+)'\)\s*\}\}", r"/static/\1", content)
            
            # Replace url_for('authors'), url_for('books'), etc. with absolute-ish paths
            # Actually, let's just keep the routes as they are, but for static files, /static/ is safer.
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Fixed {filepath}')
