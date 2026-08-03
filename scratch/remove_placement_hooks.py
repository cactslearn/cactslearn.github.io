import os
import glob
import json
import re

def clean_courses_json():
    json_path = os.path.join("src", "courses.json")
    if not os.path.exists(json_path):
        return

    with open(json_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace placement hooks in courses.json
    content = content.replace('& placement guidance.', '& technical portfolio building.')
    content = content.replace('& internship placement.', '& live project internship.')
    content = re.sub(r'placement guidance', 'technical portfolio building', content, flags=re.IGNORECASE)
    content = re.sub(r'placement drives', 'developer hiring referrals', content, flags=re.IGNORECASE)
    content = re.sub(r'placement opportunities', 'career opportunities', content, flags=re.IGNORECASE)
    content = re.sub(r'placement demand', 'industry demand', content, flags=re.IGNORECASE)
    content = re.sub(r'placement preparation', 'career readiness', content, flags=re.IGNORECASE)
    content = re.sub(r'job placements', 'developer careers', content, flags=re.IGNORECASE)
    content = re.sub(r'campus placements', 'technical hiring', content, flags=re.IGNORECASE)

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Scrubbed placement guidance from src/courses.json.")

def clean_script_files():
    scripts_to_clean = [
        os.path.join("scratch", "enrich_course_keywords.py"),
        os.path.join("scripts", "build.py"),
        os.path.join("scripts", "generate_neighborhood_pages.py"),
        os.path.join("src", "template.html"),
        os.path.join("src", "job_template.html")
    ]

    for sp in scripts_to_clean:
        if os.path.exists(sp):
            with open(sp, "r", encoding="utf-8") as f:
                content = f.read()

            content = content.replace('& placement guidance.', '& technical portfolio building.')
            content = content.replace('& internship placement.', '& live project internship.')
            content = re.sub(r'placement guidance', 'technical portfolio building', content, flags=re.IGNORECASE)
            content = re.sub(r'placement drives', 'developer hiring referrals', content, flags=re.IGNORECASE)
            content = re.sub(r'placement opportunities', 'career opportunities', content, flags=re.IGNORECASE)
            content = re.sub(r'placement demand', 'industry demand', content, flags=re.IGNORECASE)
            content = re.sub(r'placement preparation', 'career readiness', content, flags=re.IGNORECASE)
            content = re.sub(r'job placements', 'developer careers', content, flags=re.IGNORECASE)
            content = re.sub(r'campus placements', 'technical hiring', content, flags=re.IGNORECASE)

            with open(sp, "w", encoding="utf-8") as f:
                f.write(content)

    print("Scrubbed placement guidance from script generator files.")

def clean_all_html_files():
    html_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('src/') and not f.startswith('.gemini/')]
    modified_files = 0

    for pf in html_files:
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        orig_content = content

        content = content.replace('& placement guidance.', '& technical portfolio building.')
        content = content.replace('& internship placement.', '& live project internship.')
        content = re.sub(r'placement guidance', 'technical portfolio building', content, flags=re.IGNORECASE)
        content = re.sub(r'placement drives', 'developer hiring referrals', content, flags=re.IGNORECASE)
        content = re.sub(r'placement opportunities', 'career opportunities', content, flags=re.IGNORECASE)
        content = re.sub(r'placement demand', 'industry demand', content, flags=re.IGNORECASE)
        content = re.sub(r'placement preparation', 'career readiness', content, flags=re.IGNORECASE)
        content = re.sub(r'job placements', 'developer careers', content, flags=re.IGNORECASE)
        content = re.sub(r'campus placements', 'technical hiring', content, flags=re.IGNORECASE)

        if content != orig_content:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            modified_files += 1

    print(f"Scrubbed placement guidance across {modified_files} HTML files.")

if __name__ == '__main__':
    clean_courses_json()
    clean_script_files()
    clean_all_html_files()
