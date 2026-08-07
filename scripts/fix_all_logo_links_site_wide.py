import os
import glob
from bs4 import BeautifulSoup

def fix_all_logo_links():
    all_html_files = [f.replace('\\', '/') for f in glob.glob('**/*.html', recursive=True) if not f.replace('\\', '/').startswith('src/')]
    print(f"=== Fixing Logo Links Across {len(all_html_files)} HTML Files ===")

    fixed_files = 0
    total_logo_links_fixed = 0

    for fpath in all_html_files:
        norm_path = fpath.replace('\\', '/')
        parts = norm_path.split('/')
        depth = len(parts) - 1

        if depth == 0:
            expected_home_href = 'index.html'
        elif depth == 1:
            expected_home_href = '../index.html'
        elif depth == 2:
            expected_home_href = '../../index.html'

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        modified = False

        # Find logo links: inside .logo, .site-logo, .brand, .navbar-brand, or containing CACTS brand text
        logo_containers = soup.find_all(class_=lambda c: c and any(k in c.lower() for k in ['logo', 'brand', 'nav-brand']))

        logo_a_tags = []
        for container in logo_containers:
            if container.name == 'a':
                logo_a_tags.append(container)
            else:
                logo_a_tags.extend(container.find_all('a'))

        # Also search header for links containing 'CACTS' span/img
        header = soup.find('header')
        if header:
            for a in header.find_all('a'):
                if a not in logo_a_tags:
                    txt = a.text.strip().upper()
                    if 'CACTS' in txt or a.find('img') or ('logo' in str(a.get('class', '')).lower()):
                        logo_a_tags.append(a)

        for a in logo_a_tags:
            if a.has_attr('href'):
                curr_href = a['href']
                if curr_href != expected_home_href and not curr_href.startswith('http'):
                    a['href'] = expected_home_href
                    modified = True
                    total_logo_links_fixed += 1

        if modified:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            fixed_files += 1
            print(f"Fixed Logo link in: {norm_path}")

    print(f"\nSuccessfully fixed {total_logo_links_fixed} Logo links across {fixed_files} HTML files!")

if __name__ == '__main__':
    fix_all_logo_links()
