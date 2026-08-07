import os
import glob
import re
from bs4 import BeautifulSoup

BASE_URL = "https://cactslearn.github.io"

def fix_all_one_to_one_references():
    print("=== Replacing all 'courses/one-to-one-software/' references with 'courses/' site-wide ===")
    all_html_files = [f.replace('\\', '/') for f in glob.glob('**/*.html', recursive=True) if not f.replace('\\', '/').startswith('src/')]

    fixed_count = 0

    for fpath in all_html_files:
        norm_path = fpath.replace('\\', '/')
        dir_parts = [p for p in norm_path.split('/')[:-1] if p]
        depth = len(dir_parts)

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'one-to-one-software' not in content:
            continue

        soup = BeautifulSoup(content, 'html.parser')
        modified = False

        # 1. Fix <a> hrefs
        for a in soup.find_all('a', href=True):
            href = a['href']
            if 'courses/one-to-one-software/' in href or 'one-to-one-software' in href:
                if depth == 0:
                    new_link = 'courses/index.html'
                elif depth == 1 and norm_path.startswith('courses/'):
                    new_link = 'index.html'
                else:
                    new_link = ('../' * depth) + 'courses/index.html'

                a['href'] = new_link
                modified = True

        # 2. Fix JSON-LD Schema scripts
        for script in soup.find_all('script', type='application/ld+json'):
            if script.string and 'one-to-one-software' in script.string:
                script.string = script.string.replace(f"{BASE_URL}/courses/one-to-one-software/", f"{BASE_URL}/courses/")
                script.string = script.string.replace(f"{BASE_URL}/courses/one-to-one-software", f"{BASE_URL}/courses/")
                script.string = script.string.replace("courses/one-to-one-software/", "courses/")
                script.string = script.string.replace("courses/one-to-one-software", "courses/")
                modified = True

        content_str = str(soup)
        if f"{BASE_URL}/courses/one-to-one-software/" in content_str:
            content_str = content_str.replace(f"{BASE_URL}/courses/one-to-one-software/", f"{BASE_URL}/courses/")
            modified = True

        if modified:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content_str)
            fixed_count += 1
            print(f"Fixed one-to-one-software reference in: {norm_path}")

    # Fix sitemap.xml, llms.txt, llms-full.txt
    if os.path.exists('sitemap.xml'):
        with open('sitemap.xml', 'r', encoding='utf-8') as f:
            stxt = f.read()
        stxt = stxt.replace(f"{BASE_URL}/courses/one-to-one-software/", f"{BASE_URL}/courses/")
        stxt = stxt.replace("courses/one-to-one-software/", "courses/")
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(stxt)
        print("Updated sitemap.xml")

    for lfile in ['llms.txt', 'llms-full.txt']:
        if os.path.exists(lfile):
            with open(lfile, 'r', encoding='utf-8') as f:
                ltxt = f.read()
            ltxt = ltxt.replace(f"{BASE_URL}/courses/one-to-one-software/", f"{BASE_URL}/courses/")
            ltxt = ltxt.replace("courses/one-to-one-software/", "courses/")
            with open(lfile, 'w', encoding='utf-8') as f:
                f.write(ltxt)
            print(f"Updated {lfile}")

    print(f"Total HTML files updated: {fixed_count}")

if __name__ == '__main__':
    fix_all_one_to_one_references()
