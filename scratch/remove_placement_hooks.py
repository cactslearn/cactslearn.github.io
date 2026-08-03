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
    content = re.sub(r'& 100% placement support\.?', '& 100% technical competence.', content, flags=re.IGNORECASE)
    content = re.sub(r'and 100% placement support\.?', 'and 100% technical competence.', content, flags=re.IGNORECASE)
    content = re.sub(r',? & placement coaching near you\.?', ', & career readiness near you.', content, flags=re.IGNORECASE)
    content = re.sub(r',? live internship & placement support\.?', ', live internship & technical code reviews.', content, flags=re.IGNORECASE)
    content = re.sub(r',? live project internship & placement assistance\.?', ', live project internship & technical portfolio building.', content, flags=re.IGNORECASE)
    content = re.sub(r'with guaranteed live project internship and placement assistance near you\.?', 'with guaranteed live project internship and verified technical competence.', content, flags=re.IGNORECASE)
    content = re.sub(r'with live company project internship and placement assistance near you\.?', 'with live company project internship and 1-to-1 mentor reviews.', content, flags=re.IGNORECASE)
    content = re.sub(r'and placement coaching near you\.?', 'and technical code reviews near you.', content, flags=re.IGNORECASE)
    content = re.sub(r'and placement help\.?', 'and technical portfolio building.', content, flags=re.IGNORECASE)
    content = re.sub(r'and career placement support\.?', 'and 1-to-1 developer mentorship.', content, flags=re.IGNORECASE)
    content = re.sub(r'and career placement coaching\.?', 'and technical portfolio audits.', content, flags=re.IGNORECASE)
    content = re.sub(r'and 100% dedicated placement assistance\.?', 'and 100% practical technical competence.', content, flags=re.IGNORECASE)
    content = re.sub(r'placement assistance', 'technical readiness', content, flags=re.IGNORECASE)
    content = re.sub(r'placement support', 'technical portfolio building', content, flags=re.IGNORECASE)
    content = re.sub(r'placement coaching', 'career readiness coaching', content, flags=re.IGNORECASE)
    content = re.sub(r'placement help', 'technical verification', content, flags=re.IGNORECASE)

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Scrubbed placement hooks from src/courses.json.")

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

            content = re.sub(r'placement support', 'technical competence', content, flags=re.IGNORECASE)
            content = re.sub(r'placement assistance', 'technical readiness', content, flags=re.IGNORECASE)
            content = re.sub(r'placement coaching', 'career readiness', content, flags=re.IGNORECASE)
            content = re.sub(r'placement help', 'technical verification', content, flags=re.IGNORECASE)
            content = re.sub(r'placement guarantee', 'technical competence', content, flags=re.IGNORECASE)

            with open(sp, "w", encoding="utf-8") as f:
                f.write(content)

    print("Scrubbed placement hooks from script generator files.")

def clean_all_html_files():
    html_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('src/') and not f.startswith('.gemini/')]
    modified_files = 0

    for pf in html_files:
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        orig_content = content

        # Replace placement hooks in meta tags and copy
        content = re.sub(r'& 100% placement support\.?', '& 100% technical competence.', content, flags=re.IGNORECASE)
        content = re.sub(r'and 100% placement support\.?', 'and 100% technical competence.', content, flags=re.IGNORECASE)
        content = re.sub(r'100% placement assistance', '100% Technical Competence', content, flags=re.IGNORECASE)
        content = re.sub(r'placement assistance', 'technical readiness support', content, flags=re.IGNORECASE)
        content = re.sub(r'placement support', 'technical portfolio building', content, flags=re.IGNORECASE)
        content = re.sub(r'placement coaching', 'career readiness coaching', content, flags=re.IGNORECASE)
        content = re.sub(r'placement help', 'technical verification', content, flags=re.IGNORECASE)
        content = re.sub(r'placement guarantee', 'technical competence', content, flags=re.IGNORECASE)

        if content != orig_content:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            modified_files += 1

    print(f"Scrubbed placement hooks across {modified_files} HTML files.")

if __name__ == '__main__':
    clean_courses_json()
    clean_script_files()
    clean_all_html_files()
