import os
import glob
import re

def clean_and_deduplicate():
    html_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('src/') and not f.startswith('.gemini/')]
    cleaned_count = 0

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

        # Step 1: Remove all comment headers for Open Graph / Social Media
        content = re.sub(r'<!--\s*Open Graph.*?-->\n?', '', content, flags=re.IGNORECASE | re.DOTALL)
        
        # Step 2: Remove all property="og:*" and name="twitter:*" meta tags
        content = re.sub(r'\s*<meta\s+property=["\']og:[^"\']*["\']\s+content=["\'][^"\']*["\']\s*/?>\n?', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\s*<meta\s+name=["\']twitter:[^"\']*["\']\s+content=["\'][^"\']*["\']\s*/?>\n?', '', content, flags=re.IGNORECASE)

        # Step 3: Inject ONE single clean social block right before </head>
        single_social_block = f"""    <!-- Open Graph (OG) & Twitter Card Social Tags -->
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{page_desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://cactslearn.github.io/{clean_rel_path}">
    <meta property="og:image" content="https://cactslearn.github.io/images/cacts-og-banner.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{page_desc}">
    <meta name="twitter:image" content="https://cactslearn.github.io/images/cacts-og-banner.jpg">
</head>"""

        if '</head>' in content:
            content = content.replace('</head>', single_social_block)

        if content != orig_content:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            cleaned_count += 1

    print(f"Cleaned duplicate social tags across {cleaned_count} HTML files.")

if __name__ == '__main__':
    clean_and_deduplicate()
