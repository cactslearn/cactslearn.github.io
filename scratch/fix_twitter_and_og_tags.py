import os
import glob
import re

def inject_full_social_tags():
    html_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('src/') and not f.startswith('.gemini/')]
    updated_count = 0

    for pf in html_files:
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        orig_content = content
        clean_rel_path = pf.replace('\\', '/')

        # Extract title and description
        m_title = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        m_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        if not m_desc:
            m_desc = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', content, re.IGNORECASE)

        if not m_title or not m_desc:
            continue

        page_title = m_title.group(1).strip()
        page_desc = m_desc.group(1).strip()

        full_social_block = f"""<!-- Open Graph (OG) & Twitter Card Social Tags -->
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{page_desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://cactslearn.github.io/{clean_rel_path}">
    <meta property="og:image" content="https://cactslearn.github.io/images/cacts-og-banner.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{page_desc}">
    <meta name="twitter:image" content="https://cactslearn.github.io/images/cacts-og-banner.jpg">"""

        # Replace existing OG block (with or without Twitter card)
        if '<!-- Open Graph (OG) Social Tags -->' in content or '<!-- Open Graph (OG) & Twitter Card Social Tags -->' in content or '<!-- Open Graph -->' in content:
            content = re.sub(
                r'(<!-- Open Graph[^>]*-->)?\s*<meta property="og:title"[^>]*>\s*<meta property="og:description"[^>]*>\s*<meta property="og:type"[^>]*>\s*<meta property="og:url"[^>]*>\s*<meta property="og:image"[^>]*>(\s*<meta name="twitter:[^>]*>)*',
                full_social_block,
                content,
                flags=re.DOTALL
            )
        elif '</head>' in content:
            content = content.replace('</head>', f'    {full_social_block}\n</head>')

        if content != orig_content:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1

    print(f"Injected complete Open Graph & Twitter Card tags into {updated_count} HTML files.")

if __name__ == '__main__':
    inject_full_social_tags()
