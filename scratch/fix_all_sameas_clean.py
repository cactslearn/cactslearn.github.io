import glob
import re

def fix_sameas_arrays():
    files = glob.glob('**/*.html', recursive=True) + glob.glob('scripts/*.py', recursive=True) + glob.glob('src/*.html', recursive=True)
    fixed = 0

    clean_sameas = """"sameAs": [
    "https://www.facebook.com/cactspune/",
    "https://www.linkedin.com/company/cacts/",
    "https://www.instagram.com/cacts_pune/",
    "https://www.youtube.com/@CACTSPune"
  ]"""

    # Regex matches any sameAs array containing facebook
    pattern = re.compile(r'"sameAs":\s*\[\s*"https://www\.facebook\.com/cactspune/[^\]]*\]', re.DOTALL)

    for pf in files:
        if pf.startswith('.gemini/'):
            continue
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content

        content = pattern.sub(clean_sameas, content)

        if content != orig:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1

    print(f"Cleanly updated sameAs arrays in {fixed} files.")

if __name__ == '__main__':
    fix_sameas_arrays()
