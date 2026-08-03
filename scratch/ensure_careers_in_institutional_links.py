import glob
import re

def fix_institutional_links():
    html_files = glob.glob('**/*.html', recursive=True) + glob.glob('src/*.html', recursive=True)
    updated = 0

    for pf in html_files:
        if pf.startswith('.gemini/'):
            continue
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content

        # Determine link target relative path
        if pf.startswith('jobs/') or pf.startswith('src/job_template.html'):
            careers_link = '<li><a href="../careers.html">Current Openings</a></li>'
        else:
            careers_link = '<li><a href="careers.html">Current Openings</a></li>'

        # Match <h4>Institutional Links</h4> list block
        pattern = r'(<h4>Institutional Links</h4>\s*<ul[^>]*>\s*<li><a href="[^"]*about\.html">[^<]*</a></li>)'
        
        if 'careers.html' not in content and re.search(pattern, content):
            content = re.sub(pattern, r'\1\n                    ' + careers_link, content)

        # Check if sitemap.html or any other file has Institutional Links missing careers.html
        if '<h4>Institutional Links</h4>' in content:
            m = re.search(r'<h4>Institutional Links</h4>\s*<ul[^>]*>(.*?)</ul>', content, re.DOTALL)
            if m and 'careers.html' not in m.group(1):
                # Insert after about.html <li>
                content = re.sub(
                    r'(<li><a href="[^"]*about\.html">[^<]*</a></li>)',
                    r'\1\n                    ' + careers_link,
                    content,
                    count=1
                )

        if content != orig:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1

    print(f"Updated careers link under Institutional Links in {updated} files.")

if __name__ == '__main__':
    fix_institutional_links()
