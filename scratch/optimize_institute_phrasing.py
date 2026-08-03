import os
import glob
import re

def optimize_script_generators():
    # 1. Update scripts/generate_neighborhood_pages.py for local SEO dual keywords
    gen_path = os.path.join("scripts", "generate_neighborhood_pages.py")
    if os.path.exists(gen_path):
        with open(gen_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Update default meta title pattern
        code = code.replace('title = f"{h1} | CACTS Pune"', 'title = f"Software & IT Training Institute {loc_name.replace(\'Software Training Institute in \', \'\')} | CACTS"')
        code = code.replace('title = f"{h1} | CACTS Shivane HQ"', 'title = f"Software & IT Training Institute Shivane | CACTS HQ"')
        
        # Update meta description template
        code = code.replace('Software training institute near', 'Software & IT training institute near')
        code = code.replace('Software training institute in', 'Software & IT training institute in')
        code = code.replace('software training institute', 'software & IT training institute')
        
        with open(gen_path, "w", encoding="utf-8") as f:
            f.write(code)
        print("Updated scripts/generate_neighborhood_pages.py generator logic.")

def optimize_html_pages():
    html_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('src/') and not f.startswith('.gemini/')]
    updated_files = 0

    for pf in html_files:
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig_content = content

        # A. Optimize Meta Title (if generic institute / software training institute present)
        m_title = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        if m_title:
            t_text = m_title.group(1).strip()
            new_t_text = t_text
            
            # Replace standalone "Software Training Institute" in titles with "Software & IT Training Institute" where length permits
            if "Software Training Institute in " in t_text:
                candidate = t_text.replace("Software Training Institute in ", "Software & IT Training Institute ")
                if len(candidate) <= 65:
                    new_t_text = candidate
            elif "Software Training Institute " in t_text:
                candidate = t_text.replace("Software Training Institute ", "Software & IT Training Institute ")
                if len(candidate) <= 65:
                    new_t_text = candidate
            
            if new_t_text != t_text:
                content = content.replace(f"<title>{t_text}</title>", f"<title>{new_t_text}</title>")

        # B. Optimize Meta Description
        m_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        if not m_desc:
            m_desc = re.search(r'<meta\s+content=["\'](.*?)[\"\']\s+name=["\']description["\']', content, re.IGNORECASE)
        if m_desc:
            d_text = m_desc.group(1).strip()
            new_d_text = d_text
            
            if "Software training institute" in d_text:
                candidate = d_text.replace("Software training institute", "Software & IT training institute")
                if len(candidate) <= 165:
                    new_d_text = candidate
            elif "software training institute" in d_text:
                candidate = d_text.replace("software training institute", "software & IT training institute")
                if len(candidate) <= 165:
                    new_d_text = candidate

            if new_d_text != d_text:
                content = content.replace(m_desc.group(0), f'<meta name="description" content="{new_d_text}">')

        # C. Optimize Body Copy & Subtitles (Strategic Dual Keyword Combination)
        # Harmonize "software training institute" -> "software & IT training institute" or "IT & software training hub"
        content = re.sub(r'premier software training institute', 'premier IT & software training institute', content, flags=re.IGNORECASE)
        content = re.sub(r'leading software training institute', 'leading IT & software training institute', content, flags=re.IGNORECASE)
        content = re.sub(r'top software training institute', 'top IT & software training institute', content, flags=re.IGNORECASE)

        if content != orig_content:
            with open(pf, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_files += 1

    print(f"Optimized institute phrasing across {updated_files} HTML pages.")

if __name__ == '__main__':
    optimize_script_generators()
    optimize_html_pages()
