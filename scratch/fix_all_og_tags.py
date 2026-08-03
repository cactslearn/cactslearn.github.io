import os
import glob
import re

def fix_all_html_files():
    html_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('src/') and not f.startswith('.gemini/')]
    fixed_count = 0

    for pf in html_files:
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        orig_content = content
        clean_rel_path = pf.replace('\\', '/')

        # Extract actual title and meta description from THIS specific file
        m_title = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        m_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        if not m_desc:
            m_desc = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', content, re.IGNORECASE)

        if not m_title or not m_desc:
            continue

        page_title = m_title.group(1).strip()
        page_desc = m_desc.group(1).strip()

        # Update og:title
        content = re.sub(
            r'<meta\s+property=["\']og:title["\']\s+content=["\'][^"\']*["\']\s*>',
            f'<meta property="og:title" content="{page_title}">',
            content
        )

        # Update og:description
        content = re.sub(
            r'<meta\s+property=["\']og:description["\']\s+content=["\'][^"\']*["\']\s*>',
            f'<meta property="og:description" content="{page_desc}">',
            content
        )

        # Update og:url
        content = re.sub(
            r'<meta\s+property=["\']og:url["\']\s+content=["\'][^"\']*["\']\s*>',
            f'<meta property="og:url" content="https://cactslearn.github.io/{clean_rel_path}">',
            content
        )

        if content != orig_content:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1

    print(f"Directly updated OpenGraph tags across {fixed_count} HTML files.")

if __name__ == '__main__':
    fix_all_html_files()
