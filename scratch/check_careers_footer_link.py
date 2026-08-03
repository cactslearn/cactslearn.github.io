import glob
import re

def check_institutional_links():
    files = glob.glob('**/*.html', recursive=True)
    missing = []

    for pf in files:
        if pf.startswith('.gemini/'):
            continue
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract Institutional Links section
        m = re.search(r'<h4>Institutional Links</h4>\s*<ul[^>]*>(.*?)</ul>', content, re.DOTALL)
        if m:
            ul_content = m.group(1)
            if 'careers.html' not in ul_content:
                missing.append(pf)

    print(f"Total HTML files missing careers.html inside Institutional Links <ul>: {len(missing)}")
    for m in missing:
        print(f" - {m}")

if __name__ == '__main__':
    check_institutional_links()
