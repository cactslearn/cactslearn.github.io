import os
import glob
from bs4 import BeautifulSoup

def verify():
    print("=== Complete Verification Audit (Courses + Locations + Guides + Tools + Comparisons + Showcase) ===")
    
    # 1. Check directories
    folders = ['courses', 'locations', 'guides', 'tools', 'comparisons', 'showcase']
    for f in folders:
        if os.path.exists(f):
            count = len(glob.glob(f'{f}/**/*.html', recursive=True))
            print(f"Directory '{f}/': {count} HTML files")
        else:
            print(f"ERROR: '{f}/' missing!")

    # 2. Remaining root HTML files
    root_files = glob.glob('*.html')
    print(f"\nRemaining HTML files at root: {len(root_files)} ({', '.join(root_files)})")

    # 3. Check asset links in moved files
    asset_issues = 0
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for f in files:
                if f.endswith('.html'):
                    file_path = os.path.join(root, f)
                    with open(file_path, 'r', encoding='utf-8') as handle:
                        soup = BeautifulSoup(handle.read(), 'html.parser')
                    
                    for tag in soup.find_all(['link', 'script', 'img']):
                        href_src = tag.get('href') or tag.get('src')
                        if href_src:
                            if href_src.startswith('css/') or href_src.startswith('images/') or href_src.startswith('js/'):
                                print(f"[ASSET ISSUE] {file_path}: {tag.name} has non-relative asset path '{href_src}'")
                                asset_issues += 1

    print(f"Asset path issues in moved files: {asset_issues}")

    # 4. Check for broken links across published site pages
    all_html_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.replace('\\', '/').startswith('src/')]
    all_html_set = set([f.replace('\\', '/') for f in all_html_files])
    
    broken_links = 0
    for fpath in all_html_files:
        norm_fpath = fpath.replace('\\', '/')
        dir_name = os.path.dirname(norm_fpath)
        with open(fpath, 'r', encoding='utf-8') as handle:
            soup = BeautifulSoup(handle.read(), 'html.parser')
            
        for a in soup.find_all('a', href=True):
            href = a['href']
            clean_link = href.split('#')[0].split('?')[0]
            if not clean_link or clean_link.startswith('http://') or clean_link.startswith('https://') or clean_link.startswith('mailto:') or clean_link.startswith('tel:'):
                continue
                
            if clean_link.startswith('/'):
                target_path = clean_link.lstrip('/')
            elif dir_name:
                target_path = os.path.normpath(os.path.join(dir_name, clean_link)).replace('\\', '/')
            else:
                target_path = clean_link
                
            if os.path.isdir(target_path):
                target_file = os.path.join(target_path, 'index.html').replace('\\', '/')
            else:
                target_file = target_path
                
            if target_file not in all_html_set and not os.path.exists(target_file):
                print(f"[BROKEN LINK] In '{norm_fpath}' -> '{href}' (resolved to '{target_file}')")
                broken_links += 1

    print(f"Broken links across published site pages: {broken_links}")
    
    # 5. Check sitemap.xml
    with open('sitemap.xml', 'r', encoding='utf-8') as handle:
        sitemap_txt = handle.read()
    print(f"sitemap.xml size: {len(sitemap_txt)} bytes. Contains '/guides/': {'/guides/' in sitemap_txt}, Contains '/tools/': {'/tools/' in sitemap_txt}")

    # 6. Check llms.txt
    for lfile in ['llms.txt', 'llms-full.txt']:
        if os.path.exists(lfile):
            with open(lfile, 'r', encoding='utf-8') as handle:
                ltxt = handle.read()
            print(f"{lfile} size: {len(ltxt)} bytes. Contains 'guides/': {'guides/' in ltxt}, Contains 'tools/': {'tools/' in ltxt}")

    print("=== Verification Audit Finished ===")

if __name__ == '__main__':
    verify()
