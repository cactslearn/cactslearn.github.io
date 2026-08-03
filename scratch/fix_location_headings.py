import os
import glob
import re

def fix_generator_script():
    gen_path = os.path.join("scripts", "generate_neighborhood_pages.py")
    if os.path.exists(gen_path):
        with open(gen_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Update hardcoded Kothrud headings in generate_neighborhood_pages.py
        code = code.replace('Software Engineering Courses in Kothrud', 'Software Engineering Courses in {loc_clean}')
        code = code.replace('practical fees for candidates in Kothrud.', 'practical fees for candidates in {loc_clean}.')

        with open(gen_path, "w", encoding="utf-8") as f:
            f.write(code)
        print("Updated scripts/generate_neighborhood_pages.py location headings logic.")

def fix_location_html_files():
    loc_files = glob.glob('software-training-institute-*.html')
    updated_count = 0

    for pf in loc_files:
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        orig_content = content
        
        # Extract location name from file name or h1
        m_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        if m_h1:
            h1_text = m_h1.group(1).strip()
            # Extract location name (e.g. "Software Training Institute Aundh" -> "Aundh")
            loc_name = h1_text.replace("Software Training Institute in ", "").replace("Software Training Institute ", "").replace("Software & IT Training Institute ", "").replace(" | CACTS Pune", "").replace(" | CACTS", "").strip()
            if loc_name.lower() == "pune":
                loc_clean = "Pune"
            else:
                loc_clean = loc_name
        else:
            loc_clean = "Pune"

        # Replace hardcoded Kothrud in section title and subtitle
        content = content.replace(
            '<h2 id="courses-heading" class="section-title">Software Engineering Courses in Kothrud</h2>',
            f'<h2 id="courses-heading" class="section-title">Software Engineering Courses in {loc_clean}</h2>'
        )
        content = content.replace(
            'practical fees for candidates in Kothrud.',
            f'practical fees for candidates in {loc_clean}.'
        )

        if content != orig_content:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1

    print(f"Fixed section headings across {updated_count} location landing pages.")

if __name__ == '__main__':
    fix_generator_script()
    fix_location_html_files()
