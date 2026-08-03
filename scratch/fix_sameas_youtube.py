import glob
import re

target_sameas = """  "sameAs": [
    "https://www.facebook.com/cactspune/",
    "https://www.linkedin.com/company/cacts/",
    "https://www.instagram.com/cacts_pune/",
    "https://www.youtube.com/@CACTSPune"
  ],"""

def fix_sameas():
    files = glob.glob('**/*.html', recursive=True) + glob.glob('scripts/*.py', recursive=True) + glob.glob('src/*.html', recursive=True)
    fixed = 0

    sameas_regex = r'"sameAs":\s*\[\s*"https://www\.facebook\.com/cactspune/?[^"]*"\s*,\s*"https://www\.linkedin\.com/company/cacts/?"\s*,\s*"https://www\.instagram\.com/cacts_pune/?"\s*\]'

    for pf in files:
        if pf.startswith('.gemini/'):
            continue
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content

        # Fix broken sameAs array regex match
        content = re.sub(sameas_regex, target_sameas, content, flags=re.DOTALL)

        # Handle any broken quote lines like '"https://www.facebook.com/cactspune/,'
        content = content.replace('"https://www.facebook.com/cactspune/,', '"https://www.facebook.com/cactspune/"')

        if 'https://www.youtube.com/@CACTSPune' not in content and '"sameAs": [' in content:
            content = re.sub(
                r'("https://www\.instagram\.com/cacts_pune/?"\s*)(\n?\s*\])',
                r'\1,\n    "https://www.youtube.com/@CACTSPune"\2',
                content
            )

        if content != orig:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1

    print(f"Fixed sameAs array in {fixed} files.")

if __name__ == '__main__':
    fix_sameas()
