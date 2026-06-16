import os
import json
import re
import xml.etree.ElementTree as ET

print("Starting validation checks on the 55 split course pages...")

# Load courses
courses_path = os.path.join("src", "courses.json")
with open(courses_path, "r", encoding="utf-8") as f:
    courses = json.load(f)

# File names mapping helper
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

for course in courses:
    slug = course["slug"]
    name = course["name"]
    pages = get_pages(slug)
    
    print(f"\nAuditing Course Cluster: {name} (Slug: {slug})")
    
    for key, filename in pages.items():
        total_pages += 1
        # 1. Existence check
        if not os.path.exists(filename):
            print(f" [FAIL] File does not exist: {filename}")
            continue
            
        # 2. File size check (should be substantial)
        size_kb = os.path.getsize(filename) / 1024
        if size_kb < 10:
            print(f" [FAIL] File is too small: {filename} ({size_kb:.2f} KB)")
            continue
            
        # Read file content
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 3. Interlinking verification (check that it contains links to all other 4 pages in the cluster)
        links_ok = True
        for other_key, other_filename in pages.items():
            # URL relative check
            if other_filename not in content:
                print(f" [FAIL] Link to {other_filename} is missing in {filename}!")
                links_ok = False
                broken_links += 1
        
        # 4. Tab bar existence
        if "course-tabs-container" not in content:
            print(f" [FAIL] course-tabs-container placeholder missing in {filename}!")
            links_ok = False
            
        # 5. Schema verification based on type
        schema_ok = False
        schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        
        for s in schemas:
            try:
                js = json.loads(s.strip())
                # Check BreadcrumbList exists on all pages
                if js.get("@type") == "BreadcrumbList":
                    # Check position lengths
                    items = js.get("itemListElement", [])
                    expected_len = 3 if key != "overview" else 2
                    if len(items) != expected_len:
                        print(f" [WARNING] BreadcrumbList in {filename} has {len(items)} items, expected {expected_len}.")
                
                # Check page specific schema
                if key == "overview" and js.get("@type") == "Course" and "review" in js:
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

print(f"\n--- Summary of Verification ---")
print(f"Total Pages Checked: {total_pages}")
print(f"Passed All Assertions: {passed_pages} / {total_pages}")
print(f"Broken Interlinks: {broken_links}")
print(f"Missing schemas: {missing_schemas}")

# 6. Sitemap.xml verify
sitemap_path = "sitemap.xml"
if os.path.exists(sitemap_path):
    print(f"\nAuditing sitemap.xml...")
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # namespaces
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [loc.text for loc in root.findall('.//sm:loc', ns)]
    
    print(f" [INFO] sitemap.xml contains {len(urls)} registered URLs.")
    
    # Check that all 55 course URLs are present in sitemap
    missing_urls = 0
    for course in courses:
        slug = course["slug"]
        pages = get_pages(slug)
        for key, filename in pages.items():
            expected_url = f"https://cactslearn.github.io/{filename}"
            if expected_url not in urls:
                print(f" [FAIL] Missing URL in sitemap: {expected_url}")
                missing_urls += 1
                
    if missing_urls == 0:
        print(" [OK] sitemap.xml contains all 55 generated course URLs.")
    else:
        print(f" [FAIL] sitemap.xml is missing {missing_urls} URLs!")
else:
    print(f" [FAIL] sitemap.xml does not exist at {sitemap_path}!")

print("\nValidation script finished.")
