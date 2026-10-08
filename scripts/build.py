
def get_course_alternate_names(slug, name, page_type="index"):
    topic = name.replace(" Training", "").replace(" Course", "").replace(" Developer", "").strip()
    if page_type == "fees":
        return [
            f"{topic} Classes Fees",
            f"{topic} Course Fees",
            f"{topic} Training Fees",
            f"{topic} Certification Fees",
            f"{topic} Online Classes Fees",
            f"{topic} Course Fee Structure",
            f"{topic} Training Cost in Pune",
            f"{topic} Coaching Fees"
        ]
    elif page_type == "syllabus":
        return [
            f"{topic} Syllabus",
            f"{topic} Course Syllabus",
            f"{topic} Training Syllabus",
            f"{topic} Curriculum",
            f"{topic} Learning Modules",
            f"{topic} Course Outline",
            f"{topic} Training Topics",
            f"{topic} Syllabus PDF"
        ]
    elif page_type == "roadmap":
        return [
            f"{topic} Career Roadmap",
            f"{topic} Learning Roadmap",
            f"{topic} Developer Roadmap",
            f"{topic} Learning Path",
            f"{topic} Career Guide",
            f"{topic} Skill Roadmap",
            f"{topic} Step-by-Step Learning Guide"
        ]
    elif page_type == "interview-questions":
        return [
            f"{topic} Interview Questions",
            f"{topic} Interview Questions and Answers",
            f"{topic} Technical Interview Prep",
            f"{topic} Coding Interview Questions",
            f"{topic} Developer Interview Answers",
            f"{topic} Mock Interview Practice"
        ]
    else:
        return [
            f"{topic} Training",
            f"{topic} Classes",
            f"{topic} Course",
            f"{topic} Online Course",
            f"{topic} Certification",
            f"{topic} Certification Course",
            f"{topic} Training in Pune",
            f"{topic} Classes in Pune",
            f"{topic} Online Classes",
            f"{topic} Coaching Institute Pune",
            f"{topic} Learning Path"
        ]


def get_course_potential_actions(slug, name):
    encoded_name = name.replace('&', '%26').replace(' ', '%20')
    return [
        {
            "@type": "RegisterAction",
            "name": f"Enroll & Book Free 1-to-1 {name} Mentoring Session",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"https://cactslearn.github.io/contact.html?course={slug}#register",
                "actionPlatform": [
                    "https://schema.org/DesktopWebPlatform",
                    "https://schema.org/MobileWebPlatform"
                ],
                "inLanguage": "en"
            }
        },
        {
            "@type": "CommunicateAction",
            "name": f"Direct WhatsApp {name} Mentor Chat",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"https://wa.me/919665566357?text=Hello%20CACTS%2C%20I%20want%20information%20about%20{encoded_name}.",
                "actionPlatform": [
                    "https://schema.org/DesktopWebPlatform",
                    "https://schema.org/MobileWebPlatform",
                    "https://schema.org/AndroidPlatform",
                    "https://schema.org/IOSPlatform"
                ],
                "inLanguage": "en"
            }
        },
        {
            "@type": "CommunicateAction",
            "name": "Direct Phone Call to Training Lab",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": "tel:+919665566357",
                "actionPlatform": [
                    "https://schema.org/MobileWebPlatform",
                    "https://schema.org/AndroidPlatform",
                    "https://schema.org/IOSPlatform"
                ]
            }
        },
        {
            "@type": "CommunicateAction",
            "name": f"Direct SMS {name} Course Inquiry",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"sms:+919665566357?body=Hi%20CACTS%2C%20please%20send%20details%20for%20{encoded_name}.",
                "actionPlatform": [
                    "https://schema.org/MobileWebPlatform",
                    "https://schema.org/AndroidPlatform",
                    "https://schema.org/IOSPlatform"
                ]
            }
        }
    ]

import json
import os
import sys
import re
import urllib.parse
from datetime import datetime

# Set up project root and path for import
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.subpages_content import SUBPAGES_DATA
from src.extra_pages_content import EXTRA_PAGES
from src.resource_code_snippets import CODE_SNIPPETS_DATA
from src.course_assets import COURSE_ASSETS_DATA
from src.jobs_data import JOBS_DATA

import subprocess

modified_files_this_run = set()

def generate_job_pages():
    jobs_dir = os.path.join(project_root, "jobs")
    os.makedirs(jobs_dir, exist_ok=True)
    
    template_path = os.path.join(project_root, "src", "job_template.html")
    if not os.path.exists(template_path):
        print("Warning: src/job_template.html not found.")
        return []

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    generated_job_files = []

    for job in JOBS_DATA:
        slug = job["slug"]
        out_path = os.path.join(jobs_dir, f"{slug}.html")
        rel_path = f"jobs/{slug}.html"

        res_li = "".join([f"<li>{r}</li>" for r in job["responsibilities"]])
        req_li = "".join([f"<li>{r}</li>" for r in job["requirements"]])

        job_summary_json = job["summary"].replace('"', '\\"')
        job_title_json = job["title"].replace('"', '\\"')

        # Construct Google Jobs compliant full HTML description
        full_desc_html = f"""<p><strong>Role Overview:</strong> {job['summary']}</p><p>CACTS (Centre of Advanced Computer Training and Studies) Pune is inviting applications for the position of <strong>{job['title']}</strong> ({job['category']} - {job['experience']}).</p><h3>Key Responsibilities:</h3><ul>{res_li}</ul><h3>Candidate Requirements &amp; Qualifications:</h3><ul>{req_li}</ul><h3>Stipend &amp; Working Environment:</h3><p><strong>Stipend:</strong> {job['stipend']}</p><p>Trainees work on active company software applications under 1-to-1 senior mentor code reviews, Git staging commits, and production software engineering practices at CACTS Pune HQ / Remote.</p>"""
        job_full_desc_json = json.dumps(full_desc_html)

        # Parse numeric stipend range for baseSalary schema
        stipend_nums = re.findall(r'(\d+[\d,]*)', job["stipend"])
        clean_nums = [int(n.replace(',', '')) for n in stipend_nums if int(n.replace(',', '')) > 100]
        stipend_min = clean_nums[0] if len(clean_nums) > 0 else 12000
        stipend_max = clean_nums[1] if len(clean_nums) > 1 else stipend_min + 5000

        date_posted = job.get("date_posted", "2026-08-01")
        valid_through = job.get("valid_through", "2026-12-31T23:59:59Z")
        status = job.get("status", "ACTIVE")

        if status != "ACTIVE":
            # Skip building page or mark closed if expired
            continue

        content = template
        content = content.replace("{{JOB_SLUG}}", slug)
        content = content.replace("{{JOB_TITLE}}", job["title"])
        content = content.replace("{{JOB_TITLE_JSON}}", job_title_json)
        content = content.replace("{{JOB_CATEGORY}}", job["category"])
        content = content.replace("{{JOB_EXPERIENCE}}", job["experience"])
        content = content.replace("{{JOB_LOCATION}}", job["location"])
        content = content.replace("{{JOB_EMPLOYMENT_TYPE}}", job["employment_type"])
        content = content.replace("{{JOB_META_TITLE}}", job["meta_title"])
        content = content.replace("{{JOB_META_DESCRIPTION}}", job["meta_description"])
        content = content.replace("{{JOB_SUMMARY}}", job["summary"])
        content = content.replace("{{JOB_SUMMARY_JSON}}", job_summary_json)
        content = content.replace("{{JOB_FULL_DESCRIPTION_JSON}}", job_full_desc_json)
        content = content.replace("{{JOB_STIPEND_MIN}}", str(stipend_min))
        content = content.replace("{{JOB_STIPEND_MAX}}", str(stipend_max))
        content = content.replace("{{JOB_RESPONSIBILITIES_LI}}", res_li)
        content = content.replace("{{JOB_REQUIREMENTS_LI}}", req_li)
        content = content.replace("{{BRIDGE_HEADLINE}}", job["bridge_headline"])
        content = content.replace("{{BRIDGE_DESCRIPTION}}", job["bridge_description"])
        content = content.replace("{{RELATED_COURSE_NAME}}", job["related_course_name"])
        content = content.replace("{{RELATED_COURSE_SLUG}}", job["related_course_slug"])
        content = content.replace("{{JOB_DATE_POSTED}}", date_posted)
        content = content.replace("{{JOB_VALID_THROUGH}}", valid_through)

        write_if_changed(out_path, content)
        generated_job_files.append((slug, rel_path, job["title"]))

    return generated_job_files

ALLOWED_ROOT_HTML = {
    "index.html", "about.html", "contact.html", "faqs.html",
    "reviews.html", "sitemap.html", "404.html", "privacy-policy.html",
    "terms-conditions.html", "verify.html", "planner.html",
    "googleadedb2cbaba8a8c6.html"
}

def write_if_changed(filepath, new_content):
    # Strict safeguard: Never allow flat HTML files to be created at the root directory
    norm = filepath.replace("\\", "/")
    basename = os.path.basename(norm)
    dirname = os.path.dirname(norm)
    if (not dirname or dirname == ".") and basename.endswith(".html"):
        if basename not in ALLOWED_ROOT_HTML:
            # Block the write permanently
            return False

    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = f.read()
            if existing == new_content:
                return False
        except Exception:
            pass
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    modified_files_this_run.add(filepath)
    return True

def parse_existing_sitemap_lastmods(sitemap_path):
    lastmods = {}
    if os.path.exists(sitemap_path):
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            for url_elem in root.findall('sm:url', ns):
                loc_elem = url_elem.find('sm:loc', ns)
                lastmod_elem = url_elem.find('sm:lastmod', ns)
                if loc_elem is not None and loc_elem.text and lastmod_elem is not None and lastmod_elem.text:
                    url = loc_elem.text.strip()
                    url_clean = re.sub(r'(?<!:)//+', '/', url)
                    lastmods[url] = lastmod_elem.text.strip()
                    lastmods[url_clean] = lastmod_elem.text.strip()
        except Exception:
            pass
    return lastmods

def get_git_modified_files():
    modified = set()
    try:
        res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=project_root)
        if res.returncode == 0:
            for line in res.stdout.splitlines():
                if line.strip():
                    filepath = line[3:].strip()
                    filename = os.path.basename(filepath)
                    modified.add(filepath)
                    modified.add(filename)
    except Exception:
        pass
    return modified

def get_url_lastmod(url, relative_file_path, existing_lastmods, git_modified_files):
    filename = os.path.basename(relative_file_path)
    
    if (relative_file_path in modified_files_this_run or 
        relative_file_path in git_modified_files or 
        filename in git_modified_files):
        return datetime.now().strftime("%Y-%m-%d")
    
    if url in existing_lastmods:
        return existing_lastmods[url]
    
    if os.path.exists(relative_file_path):
        mtime = os.path.getmtime(relative_file_path)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
    
    return datetime.now().strftime("%Y-%m-%d")

def build():
    # Ensure current working directory is the project root
    os.chdir(project_root)

    # Paths
    src_json = os.path.join("src", "courses.json")
    src_template = os.path.join("src", "template.html")
    sitemap_file = "sitemap.xml"

    # Load course configurations
    # Load course configurations
    with open(src_json, "r", encoding="utf-8") as f:
        courses = json.load(f)

    # Load master HTML template
    with open(src_template, "r", encoding="utf-8") as f:
        template = f.read()

    # -------------------------------------------------------------------------
    # Permanent Architecture Guard: Flat root HTML page generation is disabled.
    # All courses, guides, tools, and comparisons are maintained in their clean
    # canonical subdirectories (courses/*/, comparisons/, guides/, tools/, showcase/).
    # Legacy flat URLs are caught and dynamically routed by 404.html without clutter.
    # -------------------------------------------------------------------------

    # 5. Generate Job Pages
    job_pages = generate_job_pages()
    print(f"Generated {len(job_pages)} job posting pages in jobs/ directory.")

    # 6. Generate sitemap.xml
    existing_lastmods = parse_existing_sitemap_lastmods(sitemap_file)
    git_modified_files = get_git_modified_files()

    # Dynamically discover all HTML files across site directories for sitemap.xml
    all_site_pages = []
    excluded_dirs = {".git", ".github", "node_modules", "venv", "scratch", "css", "js", "scripts", "__pycache__", ".well-known", "api", "feeds", "src"}
    excluded_files = {"planner.html", "404.html", "googleadedb2cbaba8a8c6.html", "869002205afc4d0790cda34d8b759701.txt", "BingSiteAuth.xml"}

    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for f in sorted(files):
            if f.endswith(".html") and f not in excluded_files:
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, project_root).replace("\\", "/")
                
                if rel_path == "index.html":
                    url = "https://cactslearn.github.io/"
                    priority = "1.0"
                    changefreq = "monthly"
                elif rel_path.endswith("/index.html"):
                    # Subdirectory index: strip index.html and keep single trailing slash (e.g. 'courses/ai-ml/')
                    url = f"https://cactslearn.github.io/{rel_path[:-10]}"
                    if rel_path.startswith("courses/"):
                        priority = "0.9"
                        changefreq = "weekly"
                    elif rel_path.startswith("jobs/"):
                        priority = "0.8"
                        changefreq = "weekly"
                    elif rel_path.startswith("tools/"):
                        priority = "0.9"
                        changefreq = "weekly"
                    else:
                        priority = "0.8"
                        changefreq = "monthly"
                else:
                    url = f"https://cactslearn.github.io/{rel_path}"
                    if rel_path.startswith("jobs/"):
                        priority = "0.8"
                        changefreq = "weekly"
                    elif rel_path.startswith("courses/"):
                        priority = "0.9"
                        changefreq = "weekly"
                    elif rel_path.startswith("tools/"):
                        priority = "0.9"
                        changefreq = "weekly"
                    elif rel_path == "software-training-institute-pune.html":
                        priority = "0.9"
                        changefreq = "monthly"
                    else:
                        priority = "0.8"
                        changefreq = "monthly"

                # Normalize duplicate slashes in the path (excluding protocol https://)
                url = re.sub(r'(?<!:)//+', '/', url)

                all_site_pages.append((url, rel_path, priority, changefreq))

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, file_path, priority, changefreq in all_site_pages:
        lastmod_val = get_url_lastmod(url, file_path, existing_lastmods, git_modified_files)
        sitemap_xml += f"""    <url>
        <loc>{url}</loc>
        <lastmod>{lastmod_val}</lastmod>
        <changefreq>{changefreq}</changefreq>
        <priority>{priority}</priority>
    </url>
"""

    sitemap_xml += "</urlset>"

    write_if_changed(sitemap_file, sitemap_xml)
    print(f"Generated {sitemap_file}")

    # 6. Update central reviews.html with all compiled reviews
    all_reviews_html = ""
    all_reviews_schema_list = []

    for course in courses:
        reviews = course.get("reviews", [])
        course_name = course["name"]
        course_slug = course["slug"]
        for r in reviews:
            all_reviews_html += f"""
            <div class="card" style="padding: 2rem; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
                        <span class="course-badge" style="font-size: 0.75rem; padding: 0.2rem 0.6rem; background: rgba(20, 184, 166, 0.1); color: var(--accent-light); border-radius: 4px; font-weight: 600;">
                            <a href="{course_slug}.html" style="color: inherit; text-decoration: none;">{course_name}</a>
                        </span>
                        <div style="display: flex; gap: 0.25rem; align-items: center; color: var(--warning);">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                        </div>
                    </div>
                    <p style="font-style: italic; color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.95rem; line-height: 1.6;">
                        "{r['text']}"
                    </p>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 0.5rem;">
                    <div>
                        <h4 style="color: var(--primary-light); margin: 0; font-size: 1rem;">{r['name']}</h4>
                        <span style="font-size: 0.8rem; color: var(--text-secondary);">{r['role']}, {r['location']}</span>
                    </div>
                    <div style="display: inline-flex; align-items: center; gap: 0.6rem; flex-wrap: nowrap;">
                        <a href="https://g.page/r/CaTs8mGD9uaoEBM/review" target="_blank" rel="noopener" style="color: var(--accent); text-decoration: none; font-size: 0.75rem; font-weight: 500; display: inline-flex; align-items: center; gap: 0.25rem; white-space: nowrap;">
                            Verify Review ↗
                        </a>
                        <button onclick="shareReviewCard(this)" style="background: rgba(37, 99, 235, 0.15); border: 1px solid var(--accent); color: var(--accent-light); padding: 0.25rem 0.65rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 0.25rem; white-space: nowrap; transition: all 0.2s ease;">
                            Share Review ➔
                        </button>
                    </div>
                </div>
            </div>
            """
            all_reviews_schema_list.append({
                "@type": "Review",
                "author": {
                    "@type": "Person",
                    "name": r["name"]
                },
                "datePublished": r["date"],
                "reviewBody": r["text"],
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": str(r["rating"]),
                    "bestRating": "5"
                }
            })

    reviews_page_path = "reviews.html"
    if os.path.exists(reviews_page_path):
        with open(reviews_page_path, "r", encoding="utf-8") as f:
            reviews_content = f.read()

        start_comment = "<!-- GENERATED_REVIEWS_START -->"
        end_comment = "<!-- GENERATED_REVIEWS_END -->"
        reviews_grid_pattern = start_comment + ".*?" + end_comment
        replacement_grid = f"{start_comment}\n{all_reviews_html}\n{end_comment}"
        reviews_content = re.sub(reviews_grid_pattern, replacement_grid, reviews_content, flags=re.DOTALL)

        local_business_schema = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "CACTS - Centre of Advanced Computer Training and Studies",
            "url": "https://cactslearn.github.io/",
            "image": "https://cactslearn.github.io/images/cacts-logo.png",
            "telephone": "+919665566357",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "First Floor, Shinde Arcade, NDA Rd, Deshmukh Nagar, Shivane",
                "addressLocality": "Pune",
                "addressRegion": "Maharashtra",
                "postalCode": "411023",
                "addressCountry": "IN"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": "18.46655",
                "longitude": "73.77834"
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.9",
                "reviewCount": str(len(all_reviews_schema_list))
            },
            "review": all_reviews_schema_list
        }

        schema_start = "<!-- REVIEWS_SCHEMA_START -->"
        schema_end = "<!-- REVIEWS_SCHEMA_END -->"
        schema_pattern = schema_start + ".*?" + schema_end
        schema_script = f"""<script type="application/ld+json">
{json.dumps(local_business_schema, indent=2)}
</script>"""
        replacement_schema = f"{schema_start}\n    {schema_script}\n    {schema_end}"
        reviews_content = re.sub(schema_pattern, replacement_schema, reviews_content, flags=re.DOTALL)

        write_if_changed(reviews_page_path, reviews_content)
        print(f"Updated central reviews.html with all {len(all_reviews_schema_list)} reviews and injected LocalBusiness schema.")

        # Automatically update aggregateRating reviewCount across index.html and all 34 location landing pages
        locations_dir = os.path.join(project_root, "locations")
        loc_pages = [os.path.join("locations", f) for f in os.listdir(locations_dir) if f.endswith(".html")] if os.path.exists(locations_dir) else []
        site_pages_to_sync = ["index.html"] + loc_pages
        for sp in site_pages_to_sync:
            if os.path.exists(sp):
                with open(sp, "r", encoding="utf-8") as f:
                    sp_content = f.read()
                sp_updated = re.sub(r'("aggregateRating":\s*\{\s*"@type":\s*"AggregateRating",\s*"ratingValue":\s*"4\.9",\s*"reviewCount":\s*")\d+(")',
                                    rf'\g<1>{len(all_reviews_schema_list)}\g<2>', sp_content)
                if sp_updated != sp_content:
                    write_if_changed(sp, sp_updated)



def generate_careers_page():
    job_cards_html = ""
    job_item_list_schema = []

    for idx, job in enumerate(JOBS_DATA, 1):
        slug = job["slug"]
        job_url = f"https://cactslearn.github.io/jobs/{slug}.html"
        job_item_list_schema.append({
            "@type": "ListItem",
            "position": idx,
            "name": job["title"],
            "url": job_url
        })

        job_cards_html += f"""
            <div class="card" style="padding: 2rem; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem;">
                        <span style="background: var(--accent-glow); border: 1px solid var(--accent); color: var(--accent-light); font-size: 0.8rem; font-weight: 600; padding: 0.25rem 0.65rem; border-radius: 12px;">{job['category']}</span>
                        <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border); color: var(--text-secondary); font-size: 0.8rem; padding: 0.25rem 0.65rem; border-radius: 12px;">{job['experience']}</span>
                    </div>
                    <h3 style="font-size: 1.3rem; margin-bottom: 0.75rem; font-family: var(--font-heading); color: var(--text-primary);">
                        <a href="jobs/{slug}.html" style="color: var(--text-primary); text-decoration: none;">{job['title']}</a>
                    </h3>
                    <p style="color: var(--text-secondary); font-size: 0.92rem; line-height: 1.6; margin-bottom: 1.25rem;">
                        {job['summary']}
                    </p>
                    <div style="font-size: 0.88rem; color: var(--accent-light); font-weight: 700; margin-bottom: 1.5rem;">
                        Stipend: {job['stipend']}
                    </div>
                </div>
                <div>
                    <a href="jobs/{slug}.html" class="btn btn-primary" style="width: 100%; text-align: center; display: block; margin-bottom: 1rem;">
                        View Role &amp; Apply Direct &gt;
                    </a>
                    <div style="font-size: 0.82rem; color: var(--text-secondary); line-height: 1.4; border-top: 1px solid var(--border); padding-top: 0.75rem;">
                        Need skill upgrade? <a href="{job['related_course_slug']}.html" style="color: var(--accent-light); font-weight: 600;">Explore {job['related_course_name']} &gt;</a>
                    </div>
                </div>
            </div>
        """

    item_list_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "CACTS Careers & Current Openings",
        "numberOfItems": len(JOBS_DATA),
        "itemListElement": job_item_list_schema
    }, indent=2)

    careers_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Current Openings &amp; Job Opportunities | CACTS Pune</title>
    <meta name="description" content="Browse current job openings, internships, and trainee positions at CACTS Pune across Full Stack, Java, Python, AI, Cloud, and DevOps.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://cactslearn.github.io/careers.html">
    <link rel="stylesheet" href="css/style.css">
    
    <script type="application/ld+json">
{item_list_json}
    </script>
    
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://cactslearn.github.io/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Current Openings",
          "item": "https://cactslearn.github.io/careers.html"
        }}
      ]
    }}
    </script>
</head>
<body>
    <header class="site-header">
        <div class="nav-container">
            <div class="logo">
                <a href="index.html">
                    <span>CACTS</span>
                </a>
            </div>
            <button class="mobile-menu-btn" aria-label="Toggle navigation menu">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
            </button>
            <nav class="nav-links" aria-label="Main Navigation">
                <a href="index.html">Home</a>
                <a href="about.html">About</a>
                <a href="internship-on-live-projects.html">Live Internship</a>
                <a href="one-to-one-software-training.html">1-to-1 Model</a>
                <a href="free-career-guidance.html">Career Guidance</a>
                <a href="reviews.html">Reviews</a>
                <a href="faqs.html">FAQs</a>
                <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle Theme">
                    <svg class="sun-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: block;"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
                    <svg class="moon-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: none;"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                </button>
                <a href="contact.html" class="btn btn-accent" style="padding: 0.5rem 1rem; color: #0b0f19;">Book Demo</a>
            </nav>
        </div>
    </header>

    <main style="padding-top: 8rem;">
        <section class="tech-section">
            <nav aria-label="Breadcrumb" style="margin-bottom: 1.5rem; font-size: 0.88rem; color: var(--text-secondary);">
                <a href="index.html" style="color: var(--accent);">Home</a> &gt;
                <span style="color: var(--text-primary);">Current Openings</span>
            </nav>

            <div style="max-width: 850px; margin-bottom: 3rem;">
                <span style="display: inline-block; padding: 0.35rem 0.75rem; background: var(--accent-glow); border: 1px solid var(--accent); color: var(--accent-light); font-size: 0.85rem; font-weight: 600; border-radius: 20px; margin-bottom: 1rem;">
                    CACTS Developer Team &amp; Live Project Positions
                </span>
                <h1 style="font-size: 2.8rem; line-height: 1.2; font-family: var(--font-heading); margin-bottom: 1rem;">
                    Current Job Openings &amp; Internships in Pune
                </h1>
                <p style="font-size: 1.1rem; color: var(--text-secondary); line-height: 1.7;">
                    Explore genuine 1-to-1 developer trainee positions, software apprenticeships, and live project internships across Web Development, Java, Python, Data Science, AI, Cloud, and DevOps.
                </p>
            </div>

            <div class="grid-3" style="gap: 1.75rem;">
{job_cards_html}
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="footer-container">
            <div class="footer-programs-row">
                <h4 style="color: var(--text-primary); margin-bottom: 1.5rem; font-size: 1rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase;">Engineering Labs &amp; Programs</h4>
                <ul class="footer-programs-grid">
                    <li><a href="java-fullstack-training.html">Java Fullstack Training</a></li>
                    <li><a href="full-stack-training.html">Full Stack Web (MERN)</a></li>
                    <li><a href="react-js-training.html">React JS Development</a></li>
                    <li><a href="react-native-training.html">React Native Mobile</a></li>
                    <li><a href="ai-ml-training.html">AI &amp; Machine Learning</a></li>
                    <li><a href="data-science-training.html">Data Science Analytics</a></li>
                    <li><a href="data-engineering-training.html">Data Engineering ETL</a></li>
                    <li><a href="python-training.html">Python Scripting Lab</a></li>
                    <li><a href="devops-training.html">DevOps Engineering</a></li>
                    <li><a href="cloud-training.html">Cloud Systems Architecture</a></li>
                    <li><a href="power-bi-training.html">Power BI Analytics</a></li>
                    <li><a href="software-testing-training.html">Software Testing Lab</a></li>
                    <li><a href="cybersecurity-training.html">Cybersecurity Operations</a></li>
                    <li><a href="blockchain-training.html">Blockchain Development</a></li>
                    <li><a href="software-architect-training.html">Software Architect Lab</a></li>
                </ul>
            </div>

            <div class="footer-brand">
                <a href="index.html"
                    style="font-family: var(--font-heading); font-size: 1.5rem; font-weight: 800; color: white;">CACTS</a>
                <p>Centre of Advanced Computer Training and Studies. Providing practical, one-to-one virtual software
                    training and internships on real company projects since 2012.</p>
                <div class="footer-social" style="margin-top: 1.5rem; display: flex; gap: 1rem;">
                    <a href="https://www.facebook.com/cactspune/" target="_blank" aria-label="Facebook" style="color: var(--text-secondary); transition: var(--transition); display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 50%;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
                    </a>
                    <a href="https://www.linkedin.com/company/cacts/" target="_blank" aria-label="LinkedIn" style="color: var(--text-secondary); transition: var(--transition); display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 50%;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
                    </a>
                    <a href="https://www.instagram.com/cacts_pune/" target="_blank" aria-label="Instagram" style="color: var(--text-secondary); transition: var(--transition); display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 50%;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
                    </a>
                    <a href="https://www.youtube.com/@CACTSPune" target="_blank" aria-label="YouTube" style="color: var(--text-secondary); transition: var(--transition); display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 50%;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>
                    </a>
                </div>
            </div>
            <div class="footer-links">
                <h4>Institutional Links</h4>
                <ul style="list-style: none;">
                    <li><a href="about.html">About CACTS</a></li>
                    <li><a href="courses/index.html">1-to-1 Mentoring Model</a></li>
                    <li><a href="showcase/internship-on-live-projects.html">Live Projects Internship</a></li>
                    <li><a href="comparisons/cacts-vs-classroom-vs-ai.html">CACTS vs Classroom vs AI</a></li>
                    <li><a href="reviews.html">Success Reviews</a></li>
                    <li><a href="faqs.html">Institutional FAQs</a></li>
                    <li><a href="jobs/index.html">Current Openings</a></li>
                    <li><a href="locations/index.html">Software Training Pune</a></li>
                    <li><a href="tools/free-career-guidance.html">Free Career Guidance</a></li>
                    <li><a href="contact.html">Contact Us</a></li>
                </ul>
            </div>
            <div class="footer-links">
                <h4>Learning Portals</h4>
                <ul style="list-style: none;">
                    <li><a href="tools/index.html">Interactive Tools Suite</a></li>
                    <li><a href="tools/pune-it-salary-calculator.html">Pune IT Salary Calculator</a></li>
                    <li><a href="tools/pune-it-salary-report.html">Pune IT Salary Report 2026</a></li>
                    <li><a href="tools/course-recommendation-quiz.html">Course Finder Quiz</a></li>
                    <li><a href="tools/free-skill-assessment.html">Skill Assessment</a></li>
                    <li><a href="tools/career-roadmaps.html">Career Roadmaps</a></li>
                    <li><a href="guides/index.html">Career &amp; Tech Guides</a></li>
                    <li><a href="showcase/index.html">Student Project Showcase</a></li>
                    <li><a href="comparisons/technology-comparisons.html">Tech Comparisons</a></li>
                    <li><a href="tools/live-code-compiler.html">Live Code &amp; Syntax Validator</a></li>
                </ul>
            </div>
            <div class="footer-contact">
                <h4>Contact CACTS</h4>
                <p style="margin-bottom: 0.5rem;">First Floor, Shinde Arcade, NDA Rd, Deshmukh Nagar, Shivane, Pune, Maharashtra 411023</p>
                <p style="margin-bottom: 0.5rem;"><strong>Phone:</strong> +91 96655 66357</p>
                <p><strong>Hours:</strong> Everyday: 8:00 AM - 10:00 PM</p>
            </div>
        </div>

        <div style="border-top: 1px solid var(--border); padding: 1.5rem 0; display: flex; justify-content: space-between; align-items: center; gap: 2rem; flex-wrap: wrap; margin-top: 2rem;">
            <div style="color: var(--text-secondary); font-size: 0.85rem; line-height: 1.5;">
                <strong>Pedagogical Standards &amp; Corporate Onboarding Alignment:</strong> Our curricula and git code review models are designed in alignment with ISO 29993:2017 standards for non-formal education training and software engineering industry practices. *Self-declared alignment for educational service quality.
            </div>
            <div style="display: flex; gap: 1.5rem; align-items: center; opacity: 0.75; flex-wrap: wrap;">
                <div title="Self-declared pedagogical alignment with standard ISO 29993:2017 parameters for non-formal learning providers." style="display: flex; align-items: center; gap: 0.5rem; border: 1px solid var(--border); padding: 0.4rem 0.75rem; border-radius: 8px; font-size: 0.75rem; font-weight: 700; color: var(--accent-light); cursor: help;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg> ISO 29993:2017 ALIGNED*
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; border: 1px solid var(--border); padding: 0.4rem 0.75rem; border-radius: 8px; font-size: 0.75rem; font-weight: 700; color: var(--primary-light);">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="2" y1="20" x2="22" y2="20"></line><line x1="12" y1="17" x2="12" y2="20"></line></svg> 100% DEVELOPER LED
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; border: 1px solid var(--border); padding: 0.4rem 0.75rem; border-radius: 8px; font-size: 0.75rem; font-weight: 700; color: var(--warning);">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="9" y2="16"></line><line x1="15" y1="22" x2="15" y2="16"></line><line x1="9" y1="16" x2="15" y2="16"></line><path d="M8 6h2v2H8V6zm0 4h2v2H8v-2zm0 4h2v2H8v-2zm6-8h2v2h-2V6zm0 4h2v2h-2v-2zm0 4h2v2h-2v-2z"></path></svg> ESTD. 2012 IN PUNE
                </div>
            </div>
        </div>

        <div class="footer-bottom">
            <div style="text-align: left;">
                <p>&copy; <span id="footer-year">2026</span> CACTS - Centre of Advanced Computer Training and Studies. All rights reserved.</p>
                <p style="margin-top: 0.25rem; font-size: 0.8rem; color: var(--text-secondary);">First Floor, Shinde Arcade, NDA Rd, Deshmukh Nagar, Shivane, Pune, Maharashtra 411023</p>
            </div>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <a href="sitemap.html" style="color: var(--text-secondary);">Sitemap</a>
                <span style="color: var(--border);">|</span>
                <a href="feeds/index.html" style="color: var(--text-secondary);">RSS Feeds</a>
                <span style="color: var(--border);">|</span>
                <a href="privacy-policy.html" style="color: var(--text-secondary);">Privacy Policy</a>
                <span style="color: var(--border);">|</span>
                <a href="terms-conditions.html" style="color: var(--text-secondary);">Terms &amp; Conditions</a>
            </div>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
"""

    write_if_changed("careers.html", careers_html)
    
    os.makedirs(os.path.join(project_root, "jobs"), exist_ok=True)
    jobs_index_html = careers_html.replace('href="jobs/', 'href="').replace('href="css/', 'href="../css/').replace('href="js/', 'href="../js/').replace('href="', 'href="../').replace('href="../https://', 'href="https://')
    write_if_changed(os.path.join(project_root, "jobs", "index.html"), jobs_index_html)
    print("Generated central careers.html and jobs/index.html listing page.")

def update_sitemap_html():
    sitemap_html_file = "sitemap.html"
    c_json_path = os.path.join("src", "courses.json")
    if os.path.exists(c_json_path) and os.path.exists(sitemap_html_file):
        with open(c_json_path, "r", encoding="utf-8") as f:
            c_data = json.load(f)
        split_links_html = ""
        for cd in c_data:
            cname = cd["name"]
            cslug = cd["slug"]
            cbase = cslug.replace("-training", "")
            split_links_html += f"""
                    <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 1.5rem; transition: var(--transition);">
                        <h4 style="color: var(--text-primary); font-size: 1.1rem; margin-bottom: 1rem; font-family: var(--font-heading); display: flex; align-items: center; gap: 0.5rem;">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); flex-shrink: 0;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                            {cname}
                        </h4>
                        <ul class="sitemap-list" style="gap: 0.6rem;">
                            <li>
                                <span class="sitemap-bullet" style="color: var(--accent);">•</span>
                                <a href="{cslug}.html" style="font-weight: 700; color: var(--accent-light);">{cname} Overview</a>
                            </li>
                            <li style="padding-left: 1.25rem;">
                                <span class="sitemap-bullet" style="color: var(--text-secondary);">↳</span>
                                <a href="{cbase}-syllabus.html">{cname} Syllabus</a>
                            </li>
                            <li style="padding-left: 1.25rem;">
                                <span class="sitemap-bullet" style="color: var(--text-secondary);">↳</span>
                                <a href="{cbase}-course-fees.html">{cname} Fees &amp; Tuition</a>
                            </li>
                            <li style="padding-left: 1.25rem;">
                                <span class="sitemap-bullet" style="color: var(--text-secondary);">↳</span>
                                <a href="{cbase}-interview-questions.html">{cname} Interview Q&amp;A</a>
                            </li>
                            <li style="padding-left: 1.25rem;">
                                <span class="sitemap-bullet" style="color: var(--text-secondary);">↳</span>
                                <a href="{cbase}-roadmap.html">{cname} Career Roadmap</a>
                            </li>
                        </ul>
                    </div>
            """
        with open(sitemap_html_file, "r", encoding="utf-8") as f:
            sm_content = f.read()

        start_marker = "<!-- COURSE_SPLIT_GRID_START -->"
        end_marker = "<!-- COURSE_SPLIT_GRID_END -->"
        replacement = f'{start_marker}\n                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem;" id="course-split-grid">\n{split_links_html}\n                    </div>\n                    {end_marker}'

        pattern = re.compile(rf'{re.escape(start_marker)}.*?{re.escape(end_marker)}', re.DOTALL)
        if pattern.search(sm_content):
            sm_content = pattern.sub(replacement, sm_content)

        # Update Careers section in sitemap.html
        careers_links_html = ""
        for job in JOBS_DATA:
            careers_links_html += f"""
                <li style="padding-left: 0.5rem;">
                    <span class="sitemap-bullet" style="color: var(--accent);">•</span>
                    <a href="jobs/{job['slug']}.html" style="font-weight: 600; color: var(--accent-light);">{job['title']}</a>
                    <span style="font-size: 0.8rem; color: var(--text-secondary); margin-left: 0.5rem;">({job['category']} - {job['experience']})</span>
                </li>
            """

        c_start_marker = "<!-- CAREERS_GRID_START -->"
        c_end_marker = "<!-- CAREERS_GRID_END -->"
        careers_replacement = f"""{c_start_marker}
                    <ul class="sitemap-list" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 0.75rem;">
{careers_links_html}
                    </ul>
                    {c_end_marker}"""

        c_pattern = re.compile(rf'{re.escape(c_start_marker)}.*?{re.escape(c_end_marker)}', re.DOTALL)
        if c_pattern.search(sm_content):
            sm_content = c_pattern.sub(careers_replacement, sm_content)
        else:
            careers_group = f"""
                <!-- Group 6: Careers & Current Openings -->
                <div class="sitemap-group" style="grid-column: 1 / -1; margin-top: 1.5rem;">
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <h3 style="margin-bottom: 0; display: flex; align-items: center;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 0.5rem; color: var(--accent); flex-shrink: 0;"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>Careers &amp; Current Job Openings ({len(JOBS_DATA)} Positions)</h3>
                        <a href="careers.html" style="color: var(--accent-light); font-size: 0.85rem; font-weight: 600; padding: 0.35rem 0.85rem; background: var(--accent-glow); border: 1px solid var(--accent); border-radius: 20px; text-decoration: none;">View All Openings &gt;</a>
                    </div>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1.25rem;">Explore live project internships, junior developer trainee positions, and developer apprenticeships at CACTS.</p>
                    {careers_replacement}
                </div>
            """
            sm_content = sm_content.replace('</div>\n    </main>', f'{careers_group}\n        </div>\n    </main>')

        # Update Locations section in sitemap.html
        from scripts.generate_neighborhood_pages import LOCATIONS_CONFIG
        loc_links_html = ""
        for loc in LOCATIONS_CONFIG:
            loc_links_html += f"""
                <li style="padding-left: 0.5rem;">
                    <span class="sitemap-bullet" style="color: var(--accent);">•</span>
                    <a href="{loc['slug']}.html" style="font-weight: 600; color: var(--accent-light);">{loc['h1']}</a>
                </li>
            """

        l_start_marker = "<!-- LOCATIONS_GRID_START -->"
        l_end_marker = "<!-- LOCATIONS_GRID_END -->"
        loc_replacement = f"""{l_start_marker}
                    <ul class="sitemap-list" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.75rem;">
{loc_links_html}
                    </ul>
                    {l_end_marker}"""

        l_pattern = re.compile(rf'{re.escape(l_start_marker)}.*?{re.escape(l_end_marker)}', re.DOTALL)
        if l_pattern.search(sm_content):
            sm_content = l_pattern.sub(loc_replacement, sm_content)
        else:
            loc_group = f"""
                <!-- Group 7: Pune & PCMC Location Training Hubs -->
                <div class="sitemap-group" style="grid-column: 1 / -1; margin-top: 1.5rem;">
                    <h3 style="margin-bottom: 0.5rem; display: flex; align-items: center;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 0.5rem; color: var(--accent); flex-shrink: 0;"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>Pune &amp; PCMC Location Training Hubs ({len(LOCATIONS_CONFIG)} Locations)</h3>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1.25rem;">Direct 1-to-1 software training and developer mentorship hubs across all major Pune &amp; PCMC technology corridors.</p>
                    {loc_replacement}
                </div>
            """
            sm_content = sm_content.replace('</div>\n    </main>', f'{loc_group}\n        </div>\n    </main>')

        # Update Learning Guides & Tech Resources section in sitemap.html
        resource_files = [
            ("beginner-to-ai-engineer-roadmap.html", "Beginner to AI Engineer Roadmap"),
            ("beginner-to-blockchain-developer-roadmap.html", "Beginner to Blockchain Developer Roadmap"),
            ("beginner-to-cybersecurity-analyst-roadmap.html", "Beginner to Cybersecurity Analyst Roadmap"),
            ("beginner-to-data-engineer-roadmap.html", "Beginner to Data Engineer Roadmap"),
            ("beginner-to-devops-engineer-roadmap.html", "Beginner to DevOps Engineer Roadmap"),
            ("beginner-to-java-fullstack-developer-roadmap.html", "Beginner to Java Fullstack Developer Roadmap"),
            ("beginner-to-python-developer-roadmap.html", "Beginner to Python Developer Roadmap"),
            ("beginner-to-react-js-roadmap.html", "Beginner to React JS Developer Roadmap"),
            ("beginner-to-react-native-roadmap.html", "Beginner to React Native Developer Roadmap"),
            ("best-aws-cloud-certifications.html", "Best AWS Cloud Certifications Guide"),
            ("best-blockchain-certifications.html", "Best Blockchain Certifications Guide"),
            ("best-cybersecurity-certifications.html", "Best Cybersecurity Certifications Guide"),
            ("best-data-engineering-certifications.html", "Best Data Engineering Certifications Guide"),
            ("best-devops-certifications.html", "Best DevOps Certifications Guide"),
            ("best-power-bi-certifications.html", "Best Power BI Certifications Guide"),
            ("blockchain-project-ideas.html", "Blockchain Project Ideas"),
            ("cybersecurity-project-ideas.html", "Cybersecurity Project Ideas"),
            ("data-engineering-project-ideas.html", "Data Engineering Project Ideas"),
            ("data-science-project-ideas.html", "Data Science Project Ideas"),
            ("devops-project-ideas.html", "DevOps Project Ideas"),
            ("java-fullstack-project-ideas.html", "Java Fullstack Project Ideas"),
            ("power-bi-dashboard-ideas.html", "Power BI Dashboard Ideas"),
            ("react-js-project-ideas.html", "React JS Project Ideas"),
            ("react-native-project-ideas.html", "React Native Project Ideas"),
            ("aws-vs-azure.html", "AWS vs Azure Cloud Comparison"),
            ("docker-vs-kubernetes.html", "Docker vs Kubernetes Comparison"),
            ("java-vs-python.html", "Java vs Python Comparison"),
            ("jenkins-vs-github-actions.html", "Jenkins vs GitHub Actions Comparison"),
            ("power-bi-vs-tableau.html", "Power BI vs Tableau Comparison"),
            ("react-native-vs-flutter.html", "React Native vs Flutter Comparison"),
            ("react-vs-angular.html", "React vs Angular Comparison"),
            ("spark-vs-hadoop.html", "Spark vs Hadoop Comparison"),
            ("how-ai-is-used-in-healthcare.html", "How AI is Used in Healthcare"),
            ("how-data-engineering-is-used-in-e-commerce.html", "How Data Engineering is Used in E-Commerce"),
            ("how-devops-is-used-in-software-companies.html", "How DevOps is Used in Software Companies"),
            ("how-power-bi-is-used-in-manufacturing.html", "How Power BI is Used in Manufacturing"),
            ("what-does-a-blockchain-developer-do.html", "What Does a Blockchain Developer Do?"),
            ("what-does-a-data-engineer-do.html", "What Does a Data Engineer Do?"),
            ("what-does-a-devops-engineer-do.html", "What Does a DevOps Engineer Do?"),
            ("what-does-a-power-bi-developer-do.html", "What Does a Power BI Developer Do?"),
            ("what-does-a-soc-analyst-do.html", "What Does a SOC Analyst Do?"),
            ("what-does-an-ai-engineer-do.html", "What Does an AI Engineer Do?"),
            ("what-is-apache-spark.html", "What is Apache Spark?"),
            ("what-is-docker.html", "What is Docker?"),
            ("what-is-hadoop.html", "What is Hadoop?"),
            ("what-is-jenkins.html", "What is Jenkins?"),
            ("what-is-kafka.html", "What is Kafka?"),
            ("what-is-kubernetes.html", "What is Kubernetes?"),
            ("what-is-power-bi.html", "What is Power BI?"),
            ("what-is-terraform.html", "What is Terraform?"),
            ("jobs/index.html", "CACTS Developer Job & Internship Directory")
        ]

        res_links_html = ""
        for href, label in resource_files:
            res_links_html += f"""
                <li style="padding-left: 0.5rem;">
                    <span class="sitemap-bullet" style="color: var(--accent);">•</span>
                    <a href="{href}" style="font-weight: 600; color: var(--accent-light);">{label}</a>
                </li>
            """

        r_start_marker = "<!-- RESOURCE_GUIDES_GRID_START -->"
        r_end_marker = "<!-- RESOURCE_GUIDES_GRID_END -->"
        res_replacement = f"""{r_start_marker}
                    <ul class="sitemap-list" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 0.75rem;">
{res_links_html}
                    </ul>
                    {r_end_marker}"""

        r_pattern = re.compile(rf'{re.escape(r_start_marker)}.*?{re.escape(r_end_marker)}', re.DOTALL)
        if r_pattern.search(sm_content):
            sm_content = r_pattern.sub(res_replacement, sm_content)
        else:
            res_group = f"""
                <!-- Group 8: Learning Guides & Tech Resources -->
                <div class="sitemap-group" style="grid-column: 1 / -1; margin-top: 1.5rem;">
                    <h3 style="margin-bottom: 0.5rem; display: flex; align-items: center;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 0.5rem; color: var(--accent); flex-shrink: 0;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>Learning Guides &amp; Tech Resources ({len(resource_files)} Guides)</h3>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1.25rem;">In-depth tech career roadmaps, industry certifications, project ideas, comparisons, and role breakdowns.</p>
                    {res_replacement}
                </div>
            """
            sm_content = sm_content.replace('</div>\n    </main>', f'{res_group}\n        </div>\n    </main>')

        write_if_changed(sitemap_html_file, sm_content)
        print(f"Automatically updated {sitemap_html_file} with hierarchical course split page directory, careers section, 34 location hubs, & 51 learning guides!")

import html
import math

def build_content_index(site_root="."):
    index_file = os.path.join(project_root, "js", "content-index.json")
    excluded_dirs = {".git", ".github", "node_modules", "venv", "scratch", "css", "js", "scripts", "__pycache__", ".well-known", "api", "feeds", "src"}
    excluded_files = {"planner.html", "404.html", "googleadedb2cbaba8a8c6.html", "869002205afc4d0790cda34d8b759701.txt", "BingSiteAuth.xml"}
    
    indexed_items = []
    
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            if not file.endswith(".html") or file in excluded_files:
                continue
                
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, project_root)
            norm_url = "/" + rel_path.replace("\\", "/").lstrip("/")
            
            try:
                mtime = os.path.getmtime(abs_path)
                mtime_iso = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
                
                with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                    html_content = f.read()
                
                title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
                raw_title = title_match.group(1).strip() if title_match else file.replace(".html", "").replace("-", " ").title()
                title = html.unescape(raw_title)
                
                # Strip branding suffixes (| CACTS, | CACTS Pune, etc.) to create a clean hook title
                clean_title = re.sub(r'\s*[|\-–—:]\s*(?:CACTS(?:\s+Pune|\s+Institute|\s+Training|\s+Careers)?|Centre\s+of\s+Advanced\s+Computer\s+Training\s+and\s+Studies).*$', '', title, flags=re.IGNORECASE).strip()
                if clean_title:
                    title = clean_title
                
                meta_desc_tag = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*>', html_content, re.IGNORECASE)
                if not meta_desc_tag:
                    meta_desc_tag = re.search(r'<meta\s+[^>]*name=["\']description["\'][\s\S]*?>', html_content, re.IGNORECASE)
                if not meta_desc_tag:
                    meta_desc_tag = re.search(r'<meta\s+[\s\S]*?name=["\']description["\'][\s\S]*?>', html_content, re.IGNORECASE)
                
                if meta_desc_tag:
                    tag_str = meta_desc_tag.group(0)
                    c_match = re.search(r'content=["\'](.*?)["\']', tag_str, re.IGNORECASE | re.DOTALL)
                    description = html.unescape(c_match.group(1).strip()) if c_match else title
                else:
                    description = title



                
                canon_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html_content, re.IGNORECASE | re.DOTALL)
                if not canon_match:
                    canon_match = re.search(r'<link\s+href=["\'](.*?)["\']\s+rel=["\']canonical["\']', html_content, re.IGNORECASE | re.DOTALL)
                canonical_url = canon_match.group(1).strip() if canon_match else f"https://cactslearn.github.io{norm_url}"
                
                og_img_match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', html_content, re.IGNORECASE | re.DOTALL)
                og_image = og_img_match.group(1).strip() if og_img_match else "https://cactslearn.github.io/images/cacts-logo.png"
                
                ld_types = set()
                ld_blocks = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html_content, re.IGNORECASE | re.DOTALL)
                for block in ld_blocks:
                    try:
                        data = json.loads(block.strip())
                        
                        def extract_types(obj):
                            if isinstance(obj, dict):
                                if "@graph" in obj and isinstance(obj["@graph"], list):
                                    for item in obj["@graph"]:
                                        extract_types(item)
                                if "@type" in obj:
                                    t = obj["@type"]
                                    if isinstance(t, list):
                                        for sub_t in t:
                                            ld_types.add(str(sub_t))
                                    elif isinstance(t, str):
                                        ld_types.add(t)
                            elif isinstance(obj, list):
                                for item in obj:
                                    extract_types(item)
                                    
                        extract_types(data)
                    except Exception:
                        pass
                
                ignored_types = {"WebPage", "WebSite", "Organization", "BreadcrumbList", "PostalAddress", "EntryPoint", "Offer", "AggregateRating", "ItemList", "ListItem"}
                primary_types = [t for t in ld_types if t not in ignored_types]
                
                schema_priority = ["JobPosting", "Course", "EducationalOccupationalCredential", "Article", "BlogPosting", "TechArticle", "Report", "WebApplication", "LocalBusiness"]
                detected_schema = "WebPage"
                for pref in schema_priority:
                    if pref in primary_types or pref in ld_types:
                        detected_schema = pref
                        break
                if detected_schema == "WebPage" and primary_types:
                    detected_schema = primary_types[0]
                    
                # Explicit URL path canonical schema overrides for guaranteed consistency
                if norm_url.startswith("/locations/"):
                    detected_schema = "LocalBusiness"
                elif norm_url.startswith("/jobs/"):
                    detected_schema = "JobPosting"
                elif norm_url.startswith("/courses/"):
                    detected_schema = "Course"
                elif norm_url.startswith("/guides/") or norm_url.startswith("/comparisons/"):
                    detected_schema = "Article"
                elif norm_url.startswith("/tools/") and "report" in norm_url:
                    detected_schema = "Report"
                elif norm_url.startswith("/tools/"):
                    detected_schema = "WebApplication"
                elif norm_url.startswith("/showcase/"):
                    detected_schema = "StudentShowcase"
                elif norm_url == "/verify.html":
                    detected_schema = "EducationalOccupationalCredential"
                elif norm_url == "/reviews.html":
                    detected_schema = "StudentReviews"

                plain_text = re.sub(r'<[^>]+>', ' ', html_content)
                words = re.findall(r'\w+', plain_text)
                word_count = len(words)
                read_time = f"{max(1, math.ceil(word_count / 200))} min read"
                
                indexed_items.append({
                    "url": norm_url,
                    "title": title,
                    "description": description,
                    "canonical_url": canonical_url,
                    "og_image": og_image,
                    "schema_type": detected_schema,
                    "word_count": word_count,
                    "reading_time": read_time,
                    "mtime": int(mtime),
                    "mtime_iso": mtime_iso,
                    "date": date_str
                })
            except Exception as e:
                print(f"Error indexing {abs_path}: {e}")
                
    indexed_items.sort(key=lambda x: x["mtime"], reverse=True)
    
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(indexed_items, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated {index_file} with {len(indexed_items)} indexed pages (Sorted newest first).")

if __name__ == "__main__":
    build()
    build_content_index()



