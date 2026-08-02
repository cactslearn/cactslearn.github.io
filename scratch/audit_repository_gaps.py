import os
import glob
import re
import json

def audit():
    project_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('src/') and not f.startswith('.gemini/')]
    print(f"Total HTML files found in root: {len(project_files)}")

    # Check sitemap.xml
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        sm_xml = f.read()

    urls_in_xml = re.findall(r'<loc>https://cacts\.co\.in/([^<]+)</loc>', sm_xml)
    urls_in_xml_set = set(urls_in_xml)

    missing_from_xml = []
    for pf in project_files:
        pf_clean = pf.replace('\\', '/')
        if pf_clean not in urls_in_xml_set and pf_clean != '404.html':
            missing_from_xml.append(pf_clean)

    # Check sitemap.html
    with open('sitemap.html', 'r', encoding='utf-8') as f:
        sm_html = f.read()

    missing_from_sm_html = []
    for pf in project_files:
        pf_clean = pf.replace('\\', '/')
        if pf_clean not in sm_html and pf_clean != '404.html':
            missing_from_sm_html.append(pf_clean)

    # Audit meta titles, descriptions, canonicals, H1s, and schemas
    long_titles = []
    short_titles = []
    missing_descs = []
    long_descs = []
    short_descs = []
    missing_canonicals = []
    missing_schemas = []
    missing_h1 = []
    missing_og_tags = []

    for pf in project_files:
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Title
        m_title = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        if m_title:
            title = m_title.group(1).strip()
            if len(title) > 65:
                long_titles.append((pf, len(title), title))
            elif len(title) < 30:
                short_titles.append((pf, len(title), title))
        
        # Description
        m_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        if not m_desc:
            m_desc = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', content, re.IGNORECASE)
        if m_desc:
            desc = m_desc.group(1).strip()
            if len(desc) > 165:
                long_descs.append((pf, len(desc), desc))
            elif len(desc) < 70:
                short_descs.append((pf, len(desc), desc))
        else:
            missing_descs.append(pf)
        
        # Canonical
        if 'rel="canonical"' not in content and "rel='canonical'" not in content:
            missing_canonicals.append(pf)
            
        # Schema
        if 'type="application/ld+json"' not in content and "type='application/ld+json'" not in content:
            missing_schemas.append(pf)
            
        # H1
        if '<h1' not in content:
            missing_h1.append(pf)

        # OG Tags
        if 'og:title' not in content:
            missing_og_tags.append(pf)

    print("\n--- REPOSITORY GAP DIAGNOSTIC REPORT ---")
    print(f"1. Sitemap.xml Missing URLs ({len(missing_from_xml)}): {missing_from_xml}")
    print(f"2. Sitemap.html Missing Links ({len(missing_from_sm_html)}): {missing_from_sm_html}")
    print(f"3. Overly Long Titles (>65 chars): {len(long_titles)}")
    print(f"4. Short Titles (<30 chars): {len(short_titles)}")
    print(f"5. Missing Meta Descriptions: {len(missing_descs)}")
    print(f"6. Overly Long Descriptions (>165 chars): {len(long_descs)}")
    print(f"7. Short Descriptions (<70 chars): {len(short_descs)}")
    print(f"8. Missing Canonical Tags: {len(missing_canonicals)}")
    print(f"9. Missing JSON-LD Schemas ({len(missing_schemas)}): {missing_schemas}")
    print(f"10. Missing H1 Headings ({len(missing_h1)}): {missing_h1}")
    print(f"11. Missing OpenGraph (OG) Tags: {len(missing_og_tags)}")

    if long_titles:
        print("\n--- Sample Long Titles ---")
        for file, length, t in long_titles[:5]:
            print(f"[{file}] ({length} chars): {t}")

    if long_descs:
        print("\n--- Sample Long Meta Descriptions ---")
        for file, length, d in long_descs[:5]:
            print(f"[{file}] ({length} chars): {d}")

if __name__ == '__main__':
    audit()
