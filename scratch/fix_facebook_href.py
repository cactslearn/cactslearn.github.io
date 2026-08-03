import glob

def fix_facebook_quotes():
    files = glob.glob('**/*.html', recursive=True)
    fixed = 0
    for pf in files:
        if pf.startswith('.gemini/'):
            continue
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'https://www.facebook.com/cactspune/ target=' in content:
            content = content.replace(
                'https://www.facebook.com/cactspune/ target=',
                'https://www.facebook.com/cactspune/" target='
            )
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1

    print(f"Fixed facebook quote in {fixed} files.")

if __name__ == '__main__':
    fix_facebook_quotes()
