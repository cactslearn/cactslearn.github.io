import os
import json
import re
import sys
import xml.etree.ElementTree as ET

# Ensure working directory is the project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

print("Starting validation checks on the 55 split course pages and 37 resource pages...")

# Load courses
courses_path = os.path.join("src", "courses.json")
with open(courses_path, "r", encoding="utf-8") as f:
    courses = json.load(f)

# Load extra pages content database
from src.extra_pages_content import EXTRA_PAGES

# File names mapping helper for course cluster
def get_pages(slug):
    base_slug = slug.replace("-training", "")
    return {
        "overview": f"{slug}.html",
        "syllabus": f"{base_slug}-syllabus.html",
        "fees": f"{base_slug}-course-fees.html",
        "interview": f"{base_slug}-interview-questions.html",
        "roadmap": f"{base_slug}-roadmap.html"
    }

total_pages = 0
passed_pages = 0
broken_links = 0
missing_schemas = 0

# 1. Audit Course Pages (55 pages)
print("\n--- Auditing 55 Split Course Pages ---")
for course in courses:
    slug = course["slug"]
    name = course["name"]
    pages = get_pages(slug)
    
    for key, filename in pages.items():
        total_pages += 1
        # Existence check
        if not os.path.exists(filename):
            print(f" [FAIL] File does not exist: {filename}")
            continue
            
        # File size check (should be substantial)
        size_kb = os.path.getsize(filename) / 1024
        if size_kb < 10:
            print(f" [FAIL] File is too small: {filename} ({size_kb:.2f} KB)")
            continue
            
        # Read file content
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Interlinking verification within cluster
        links_ok = True
        for other_key, other_filename in pages.items():
            if other_filename not in content:
                print(f" [FAIL] Link to {other_filename} is missing in {filename}!")
                links_ok = False
                broken_links += 1
        
        # Tab bar existence
        if "course-tabs-container" not in content:
            print(f" [FAIL] course-tabs-container placeholder missing in {filename}!")
            links_ok = False
            
        # Schema verification based on type
        schema_ok = False
        schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        
        for s in schemas:
            try:
                js = json.loads(s.strip())
                if js.get("@type") == "BreadcrumbList":
                    items = js.get("itemListElement", [])
                    expected_len = 3 if key != "overview" else 2
                    if len(items) != expected_len:
                        print(f" [WARNING] BreadcrumbList in {filename} has {len(items)} items, expected {expected_len}.")
                
                # Check page specific schema
                if key == "overview" and js.get("@type") == "Course" and "provider" in js:
                    schema_ok = True
                elif key == "syllabus" and js.get("@type") == "Course" and "hasPart" in js:
                    schema_ok = True
                elif key == "fees" and js.get("@type") == "Course" and "offers" in js:
                    schema_ok = True
                elif key == "interview" and js.get("@type") == "FAQPage":
                    schema_ok = True
                elif key == "roadmap" and js.get("@type") == "HowTo":
                    schema_ok = True
            except Exception as e:
                print(f" [FAIL] JSON parsing error in schema of {filename}: {e}")
                
        if not schema_ok:
            print(f" [FAIL] Missing or invalid page-specific schema in {filename}!")
            missing_schemas += 1
        else:
            passed_pages += 1

# 2. Audit Resource Pages (37 pages)
print("\n--- Auditing 37 Resource Pages ---")
total_res_pages = 0
passed_res_pages = 0
broken_res_links = 0
missing_res_schemas = 0

for pg in EXTRA_PAGES:
    total_res_pages += 1
    slug = pg["slug"]
    filename = f"{slug}.html"
    related_course_slug = pg["related_course_slug"]
    
    # Existence check
    if not os.path.exists(filename):
        print(f" [FAIL] File does not exist: {filename}")
        continue
        
    # File size check (should be > 5KB)
    size_kb = os.path.getsize(filename) / 1024
    if size_kb < 5.0:
        print(f" [FAIL] File is too small: {filename} ({size_kb:.2f} KB)")
        continue
        
    # Read content
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check link back to its respective course page
    expected_course_link = f"{related_course_slug}.html"
    if expected_course_link not in content:
        print(f" [FAIL] Link to related course {expected_course_link} is missing in {filename}!")
        broken_res_links += 1
        
    # Schema checks: Article, FAQPage, BreadcrumbList
    has_article = False
    has_faq = False
    has_breadcrumb = False
    
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    for s in schemas:
        try:
            js = json.loads(s.strip())
            t = js.get("@type")
            if t == "Article":
                has_article = True
            elif t == "FAQPage":
                has_faq = True
            elif t == "BreadcrumbList":
                has_breadcrumb = True
        except Exception as e:
            print(f" [FAIL] JSON parsing error in schema of {filename}: {e}")
            
    if not (has_article and has_faq and has_breadcrumb):
        print(f" [FAIL] Missing required schema in {filename} (Article: {has_article}, FAQPage: {has_faq}, BreadcrumbList: {has_breadcrumb})")
        missing_res_schemas += 1
    else:
        passed_res_pages += 1

print(f"\n--- Course Pages Verification Summary ---")
print(f"Total Pages Checked: {total_pages}")
print(f"Passed All Assertions: {passed_pages} / {total_pages}")
print(f"Broken Interlinks: {broken_links}")
print(f"Missing schemas: {missing_schemas}")

print(f"\n--- Resource Pages Verification Summary ---")
print(f"Total Resource Pages Checked: {total_res_pages}")
print(f"Passed All Assertions: {passed_res_pages} / {total_res_pages}")
print(f"Broken Course Links: {broken_res_links}")
print(f"Missing schemas: {missing_res_schemas}")

# 3. Sitemap.xml verify
sitemap_path = "sitemap.xml"
if os.path.exists(sitemap_path):
    print(f"\nAuditing sitemap.xml...")
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # namespaces
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [loc.text for loc in root.findall('.//sm:loc', ns)]
    
    print(f" [INFO] sitemap.xml contains {len(urls)} registered URLs.")
    
    # Check course pages
    missing_urls = 0
    for course in courses:
        slug = course["slug"]
        pages = get_pages(slug)
        for key, filename in pages.items():
            expected_url = f"https://cactslearn.github.io/{filename}"
            if expected_url not in urls:
                print(f" [FAIL] Missing course URL in sitemap: {expected_url}")
                missing_urls += 1
                
    # Check resource pages
    missing_res_urls = 0
    for pg in EXTRA_PAGES:
        slug = pg["slug"]
        expected_url = f"https://cactslearn.github.io/{slug}.html"
        if expected_url not in urls:
            print(f" [FAIL] Missing resource URL in sitemap: {expected_url}")
            missing_res_urls += 1
            
    if missing_urls == 0:
        print(" [OK] sitemap.xml contains all 55 generated course URLs.")
    else:
        print(f" [FAIL] sitemap.xml is missing {missing_urls} course URLs!")
        
    if missing_res_urls == 0:
        print(" [OK] sitemap.xml contains all 37 generated resource URLs.")
    else:
        print(f" [FAIL] sitemap.xml is missing {missing_res_urls} resource URLs!")
else:
    print(f" [FAIL] sitemap.xml does not exist at {sitemap_path}!")

# 4. Audit llms.txt
print("\n--- Auditing llms.txt ---")
llms_path = os.path.join(project_root, "llms.txt")
if os.path.exists(llms_path):
    with open(llms_path, "r", encoding="utf-8") as f:
        llms_content = f.read()
    
    required_terms = ["One-to-One", "Mentorship Lab", "Operational Parameters", "Course Tracks", "Interactive Tools"]
    missing_terms = [t for t in required_terms if t not in llms_content]
    
    if not missing_terms:
        print(" [OK] llms.txt contains all core diagnostic sections and descriptors.")
    else:
        print(f" [FAIL] llms.txt is missing key brand terms: {missing_terms}")
else:
    print(f" [FAIL] llms.txt does not exist at {llms_path}!")

# 5. Audit WebMCP Manifests
print("\n--- Auditing WebMCP Manifests ---")
webmcp_root_path = os.path.join(project_root, "webmcp.json")
webmcp_wellknown_path = os.path.join(project_root, ".well-known", "webmcp")

manifests_ok = True
for path in [webmcp_root_path, webmcp_wellknown_path]:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                js = json.load(f)
            if js.get("mcp") != "1.0" or not js.get("tools"):
                print(f" [FAIL] Manifest {path} has invalid WebMCP structure!")
                manifests_ok = False
        except Exception as e:
            print(f" [FAIL] JSON parsing error in manifest {path}: {e}")
            manifests_ok = False
    else:
        print(f" [FAIL] WebMCP Manifest does not exist at {path}!")
        manifests_ok = False

if manifests_ok:
    print(" [OK] Both WebMCP Discovery Manifest configurations are fully valid.")

print("\nValidation script finished.")

