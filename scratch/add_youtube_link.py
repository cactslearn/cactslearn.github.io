import os
import glob
import re

youtube_icon_html = """                    <a href="https://www.youtube.com/@CACTSPune" target="_blank" aria-label="YouTube" style="color: var(--text-secondary); transition: var(--transition); display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 50%;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>
                    </a>"""

def fix_all_files():
    files = glob.glob('**/*.html', recursive=True) + glob.glob('**/*.py', recursive=True)
    fixed = 0

    for pf in files:
        if pf.startswith('.gemini/'):
            continue
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content

        # Fix broken facebook href if created
        content = content.replace(
            'https://www.facebook.com/cactspune/",\n        "https://www.youtube.com/@CACTSPune"',
            'https://www.facebook.com/cactspune/'
        )
        content = content.replace(
            'https://www.facebook.com/cactspune/",\r\n        "https://www.youtube.com/@CACTSPune"',
            'https://www.facebook.com/cactspune/'
        )

        # 1. Update sameAs JSON array cleanly (only inside schema JSON)
        if '"sameAs": [' in content and 'https://www.youtube.com/@CACTSPune' not in content:
            content = re.sub(
                r'("sameAs":\s*\[\s*"https://www\.facebook\.com/cactspune/")',
                r'\1,\n        "https://www.youtube.com/@CACTSPune"',
                content
            )

        # 2. Update footer-social block cleanly
        if '<div class="footer-social"' in content or 'footer-social' in content:
            # Check if YouTube icon is missing from footer-social
            # We can replace footer-social icon group to include Facebook, LinkedIn, Instagram, YouTube cleanly
            if 'youtube.com/@CACTSPune' not in content:
                instagram_link_regex = r'(<a href="https://www\.instagram\.com/cacts_pune/".*?</a>)'
                content = re.sub(instagram_link_regex, r'\1\n' + youtube_icon_html, content, flags=re.DOTALL)

        if content != orig:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1

    print(f"Cleanly updated YouTube links in {fixed} files.")

if __name__ == '__main__':
    fix_all_files()
