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

def build():
    # Ensure current working directory is the project root
    os.chdir(project_root)

    # Paths
    src_json = os.path.join("src", "courses.json")
    src_template = os.path.join("src", "template.html")
    sitemap_file = "sitemap.xml"

    # Load course configurations
    with open(src_json, "r", encoding="utf-8") as f:
        courses = json.load(f)

    # Load master HTML template
    with open(src_template, "r", encoding="utf-8") as f:
        template = f.read()

    generated_pages = []

    for course in courses:
        slug = course["slug"]
        name = course["name"]
        price = course["price"]
        price_num = course["price_num"]
        duration = course["duration"]
        seo_title = course["seo_title"]
        meta_description = course["meta_description"]
        h1 = course["h1"]
        h2 = course["h2"]
        overview = course["overview"]
        skills = course["skills"]
        modules = course["modules"]
        faqs = course["faqs"]

        base_slug = slug.replace("-training", "")
        name_encoded = urllib.parse.quote(name)

        # Get subpage content database
        data = SUBPAGES_DATA.get(slug, {})

        # 1. Build Skills Bubbles
        skills_bubbles = ""
        for s in skills:
            skills_bubbles += f'<span class="skill-bubble">{s}</span>\n'

        # 2. Build Curriculum Modules summary
        curr_html = ""
        for mod in modules:
            topics_li = "".join([f"<li>{t}</li>" for t in mod["topics"]])
            curr_html += f"""
            <div class="curriculum-module">
                <div class="module-header">
                    <h4>{mod['title']}</h4>
                    <span class="module-duration">{mod['duration']}</span>
                </div>
                <div class="module-content">
                    <div class="module-content-inner">
                        <ul>
                            {topics_li}
                        </ul>
                    </div>
                </div>
            </div>
            """

        # 3. Build Course FAQs
        faq_html = ""
        for faq in faqs:
            faq_html += f"""
            <div class="curriculum-module">
                <div class="module-header faq-header">
                    <h4>{faq['q']}</h4>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="faq-content module-content">
                    <div class="module-content-inner">
                        <p style="color: var(--text-secondary); font-size: 0.95rem;">{faq['a']}</p>
                    </div>
                </div>
            </div>
            """

        # 4. Generate Reviews Block
        reviews = course.get("reviews", [])
        reviews_html = ""
        for r in reviews:
            reviews_html += f"""
            <div class="card" style="padding: 2rem; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="display: flex; gap: 0.25rem; align-items: center; margin-bottom: 1rem;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" style="color: var(--warning);"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                </div>
                <p style="font-style: italic; color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.95rem; line-height: 1.6; flex-grow: 1;">
                    "{r['text']}"
                </p>
                <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 0.5rem;">
                    <div>
                        <h4 style="color: var(--primary-light); margin: 0; font-size: 1rem;">{r['name']}</h4>
                        <span style="font-size: 0.8rem; color: var(--text-secondary);">{r['role']}, {r['location']}</span>
                    </div>
                    <a href="https://g.page/r/CaTs8mGD9uaoEBM/review" target="_blank" rel="noopener" style="color: var(--accent); text-decoration: none; font-size: 0.75rem; font-weight: 500; display: inline-flex; align-items: center; gap: 0.25rem; white-space: nowrap;">
                        Verify Review ↗
                    </a>
                </div>
            </div>
            """

        # Define active links list tabs generator
        def get_tabs_html(active_type):
            tabs_config = [
                {"type": "overview", "label": "Overview", "url": f"{slug}.html"},
                {"type": "syllabus", "label": "Syllabus", "url": f"{base_slug}-syllabus.html"},
                {"type": "fees", "label": "Fees & Options", "url": f"{base_slug}-course-fees.html"},
                {"type": "interview", "label": "Interview Qs", "url": f"{base_slug}-interview-questions.html"},
                {"type": "roadmap", "label": "Roadmap", "url": f"{base_slug}-roadmap.html"}
            ]
            html = ""
            for tab in tabs_config:
                active_class = "active" if tab["type"] == active_type else ""
                html += f'<a href="{tab["url"]}" class="tab-link {active_class}">{tab["label"]}</a>\n'
            return html

        # Get course implementation assets (code & schemas)
        asset = COURSE_ASSETS_DATA.get(slug, {})
        asset_html = ""
        if asset:
            import html
            code_escaped = html.escape(asset["code"])
            schema_escaped = html.escape(asset["schema"])
            asset_html = f"""
        <!-- Practical Code & Schema Implementation Assets -->
        <div style="margin-top: 3.5rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2.5rem; overflow: hidden;">
            <h2 style="margin-bottom: 1rem; font-family: var(--font-heading); color: var(--accent-light); display: inline-flex; align-items: center; gap: 0.5rem;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); flex-shrink: 0;"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="2" y1="20" x2="22" y2="20"></line><line x1="12" y1="17" x2="12" y2="20"></line></svg>Hands-On Implementation Preview</h2>
            <p style="color: var(--text-secondary); margin-bottom: 2rem; font-size: 0.98rem;">
                Here is a concrete preview of the production-level code assets and system schemas you will design, write, and deploy during our 1-to-1 live project sessions.
            </p>
            
            <h3 style="color: var(--text-primary); margin-bottom: 0.75rem; font-size: 1.1rem; display: inline-flex; align-items: center; gap: 0.5rem;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); flex-shrink: 0;"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>{html.escape(asset["code_title"])}</h3>
            <div style="margin-bottom: 2rem; border-radius: 8px; overflow: hidden; border: 1px solid var(--border);">
                <pre style="margin: 0; background: #060913; padding: 1.25rem; overflow-x: auto; font-family: monospace; font-size: 0.88rem; color: #a5f3fc; white-space: pre;"><code class="language-{asset["lang"]}">{code_escaped}</code></pre>
            </div>
            
            <h3 style="color: var(--text-primary); margin-bottom: 0.75rem; font-size: 1.1rem; display: inline-flex; align-items: center; gap: 0.5rem;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); flex-shrink: 0;"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line><line x1="15" y1="3" x2="15" y2="21"></line><line x1="3" y1="9" x2="21" y2="9"></line><line x1="3" y1="15" x2="21" y2="15"></line></svg>{html.escape(asset["schema_title"])}</h3>
            <div style="border-radius: 8px; overflow: hidden; border: 1px solid var(--border); background: #060913; padding: 1.5rem; font-family: monospace; font-size: 0.88rem; color: #34d399; overflow-x: auto; line-height: 1.5; white-space: pre-wrap;">
                <pre style="margin: 0; white-space: pre-wrap;">{schema_escaped}</pre>
            </div>
        </div>
            """

        # Collect related resources from EXTRA_PAGES
        related_resources = []
        for pg in EXTRA_PAGES:
            if pg.get("related_course_slug") == slug:
                related_resources.append(pg)

        resources_html = ""
        if related_resources:
            resources_li = ""
            for res in related_resources:
                res_url = f"{res['slug']}.html"
                resources_li += f"""
                <li style="margin-bottom: 0.75rem;">
                    <a href="{res_url}" style="color: var(--accent); text-decoration: none; font-weight: 600;">{res['h1']}</a> 
                    <span style="color: var(--text-secondary); font-size: 0.9rem;">— {res['h2']}</span>
                </li>
                """
            resources_html = f"""
        <!-- Related Technical & Career Resources -->
        <div style="margin-top: 3.5rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2rem; margin-bottom: 3rem;">
            <h3 style="margin-bottom: 1rem; font-family: var(--font-heading); color: var(--text-primary); display: inline-flex; align-items: center; gap: 0.5rem;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); flex-shrink: 0;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>Related Career &amp; Technical Resource Guides
            </h3>
            <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1.5rem;">
                Explore our developer-vetted glossary definitions, industry comparison analyses, and career roadmap guides for {name}.
            </p>
            <ul style="list-style-type: none; padding-left: 0; display: flex; flex-direction: column; gap: 0.5rem; margin: 0;">
                {resources_li}
            </ul>
        </div>
            """

        # ----------------------------------------------------
        # PAGE 1: Commercial Overview Page ([slug].html)
        # ----------------------------------------------------
        overview_left_column = f"""
        <h2 id="details-heading" style="margin-bottom: 1.5rem;">Course Overview</h2>
        <p style="font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 2.5rem;">{overview}</p>

        <!-- Market Comparison Checklist -->
        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2rem; margin-bottom: 2.5rem;">
            <h3 style="margin-bottom: 1rem; font-family: var(--font-heading); color: var(--text-primary);">
                Why train with CACTS vs the typical market?</h3>
            <div class="grid-2" style="gap: 1.5rem; align-items: start;">
                <div>
                    <h4 style="color: var(--warning); font-size: 0.95rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--warning); flex-shrink: 0;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>Typical Market Courses</h4>
                    <ul style="color: var(--text-secondary); font-size: 0.9rem; list-style-type: none; display: flex; flex-direction: column; gap: 0.4rem; padding-left: 0;">
                        <li style="display: flex; align-items: center; gap: 0.35rem;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--warning); flex-shrink: 0; display: inline-block; vertical-align: middle;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> 30-50 student batches</li>
                        <li style="display: flex; align-items: center; gap: 0.35rem;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--warning); flex-shrink: 0; display: inline-block; vertical-align: middle;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> Passive recorded lecture video playback</li>
                        <li style="display: flex; align-items: center; gap: 0.35rem;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--warning); flex-shrink: 0; display: inline-block; vertical-align: middle;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> Hardcoded, outdated mock sandbox templates</li>
                        <li style="display: flex; align-items: center; gap: 0.35rem;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--warning); flex-shrink: 0; display: inline-block; vertical-align: middle;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> No direct code feedback from developers</li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: var(--success); font-size: 0.95rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--success); flex-shrink: 0;"><polyline points="20 6 9 17 4 12"></polyline></svg>CACTS 1-to-1 Training</h4>
                    <ul style="color: var(--text-secondary); font-size: 0.9rem; list-style-type: none; display: flex; flex-direction: column; gap: 0.4rem; padding-left: 0;">
                        <li style="display: flex; align-items: center; gap: 0.35rem;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--success); flex-shrink: 0; display: inline-block; vertical-align: middle;"><polyline points="20 6 9 17 4 12"></polyline></svg> Strictly individual 1-to-1 virtual attention</li>
                        <li style="display: flex; align-items: center; gap: 0.35rem;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--success); flex-shrink: 0; display: inline-block; vertical-align: middle;"><polyline points="20 6 9 17 4 12"></polyline></svg> Fully active dynamic pacing based on your grasp</li>
                        <li style="display: flex; align-items: center; gap: 0.35rem;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--success); flex-shrink: 0; display: inline-block; vertical-align: middle;"><polyline points="20 6 9 17 4 12"></polyline></svg> Real company git repositories and developer commits</li>
                        <li style="display: flex; align-items: center; gap: 0.35rem;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--success); flex-shrink: 0; display: inline-block; vertical-align: middle;"><polyline points="20 6 9 17 4 12"></polyline></svg> Screen-sharing, live code writing, and peer PR reviews</li>
                    </ul>
                </div>
            </div>
        </div>

        <h2 style="margin-bottom: 1.5rem;">Key Skills You Will Acquire</h2>
        <div class="skills-grid" style="margin-bottom: 2.5rem;">
            {skills_bubbles}
        </div>

        <div class="curriculum-section">
            <h2 style="margin-bottom: 1.5rem;">Curriculum Outline</h2>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">This curriculum is fully customized for you. We adapt the pace based on your learning speed. Our trainers work 1-to-1, detailing every line of code.</p>
            <div class="curriculum-accordion">
                {curr_html}
            </div>
        </div>

        <!-- Live Company Project Block -->
        <div style="background: rgba(20, 184, 166, 0.05); border: 1px solid var(--accent); border-radius: var(--border-radius); padding: 2.5rem; margin-top: 3rem; margin-bottom: 3rem;">
            <h3 style="color: var(--accent-light); margin-bottom: 1rem; font-family: var(--font-heading); display: flex; align-items: center; gap: 0.5rem;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); flex-shrink: 0;"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="9" y2="16"></line><line x1="15" y1="22" x2="15" y2="16"></line><line x1="9" y1="16" x2="15" y2="16"></line><path d="M8 6h2v2H8V6zm0 4h2v2H8v-2zm0 4h2v2H8v-2zm6-8h2v2h-2V6zm0 4h2v2h-2v-2zm0 4h2v2h-2v-2z"></path></svg>Live Project Internship Integration
            </h3>
            <p style="color: var(--text-secondary); font-size: 1rem; margin-bottom: 1.25rem;">
                Unlike institutes that assign mock projects or simple copy-paste tasks, CACTS bridges the learning gap by placing you on real company software development environments. You will coordinate with active developers, write production code, submit code reviews, and deploy test cases.
            </p>
            <ul style="color: var(--text-secondary); margin-left: 1.5rem; margin-bottom: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem;">
                <li>Hands-on Git access and branch merge policies.</li>
                <li>Real-world debugging under senior developer code review loops.</li>
                <li>Staging pipeline deployments.</li>
            </ul>
            <a href="internship-on-live-projects.html" class="btn btn-secondary" style="border-color: var(--accent); color: var(--text-primary);">Learn About Our Live Project Internships &gt;</a>
        </div>

        {resources_html}

        {asset_html}

        <!-- Course Specific FAQs -->
        <div style="margin-top: 4rem;">
            <h2 style="margin-bottom: 1.5rem;">Course FAQs</h2>
            <div class="course-faqs-accordion">
                {faq_html}
            </div>
        </div>
        """

        course_schema = {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": name,
            "description": meta_description,
            "provider": {
                "@type": "Organization",
                "name": "CACTS - Centre of Advanced Computer Training and Studies",
                "url": "https://cactslearn.github.io/"
            },
            "offers": {
                "@type": "Offer",
                "price": str(price_num),
                "priceCurrency": "INR",
                "category": "Value-Driven Professional Programming Training"
            }
        }
        schema_reviews = []
        for r in reviews:
            schema_reviews.append({
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
        if schema_reviews:
            course_schema["review"] = schema_reviews
            course_schema["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": "5.0",
                "bestRating": "5",
                "reviewCount": str(len(schema_reviews))
            }

        faq_entities = []
        for faq in faqs:
            faq_entities.append({
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["a"]
                }
            })
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }

        breadcrumb_schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cactslearn.github.io/index.html"},
                {"@type": "ListItem", "position": 2, "name": name, "item": f"https://cactslearn.github.io/{slug}.html"}
            ]
        }

        schema_markup = f"""
        <script type="application/ld+json">
        {json.dumps(course_schema, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps(faq_schema, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps(breadcrumb_schema, indent=2)}
        </script>
        """

        page_html1 = template
        page_html1 = page_html1.replace("{{seo_title}}", seo_title)
        page_html1 = page_html1.replace("{{meta_description}}", meta_description)
        page_html1 = page_html1.replace("{{canonical}}", f"https://cactslearn.github.io/{slug}.html")
        page_html1 = page_html1.replace("{{schema_markup}}", schema_markup)
        page_html1 = page_html1.replace("{{course_name}}", name)
        page_html1 = page_html1.replace("{{course_name_encoded}}", name_encoded)
        page_html1 = page_html1.replace("{{h1}}", h1)
        page_html1 = page_html1.replace("{{h2}}", h2)
        page_html1 = page_html1.replace("{{duration}}", duration)
        page_html1 = page_html1.replace("{{price}}", price)
        page_html1 = page_html1.replace("{{course_reviews}}", reviews_html)
        page_html1 = page_html1.replace("{{course_tabs}}", get_tabs_html("overview"))
        page_html1 = page_html1.replace("{{course_left_column}}", overview_left_column)

        with open(f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(page_html1)
        generated_pages.append(slug)

        # ----------------------------------------------------
        # PAGE 2: Syllabus Page ([base_slug]-syllabus.html)
        # ----------------------------------------------------
        syllabus_projects_html = "".join([f"<li>{proj}</li>" for proj in data.get("syllabus_projects", [])])
        syllabus_tools_html = "".join([f'<span class="skill-bubble">{tool}</span>' for tool in data.get("syllabus_tools", [])])

        expanded_curr_html = ""
        for mod in modules:
            topics_li = "".join([f"<li>{t}</li>" for t in mod["topics"]])
            expanded_curr_html += f"""
            <div class="curriculum-module">
                <div class="module-header" style="cursor: default;">
                    <h4 style="color: var(--accent-light);">{mod['title']}</h4>
                    <span class="module-duration">{mod['duration']}</span>
                </div>
                <div class="module-content active" style="max-height: none; background: rgba(6, 9, 19, 0.15);">
                    <div class="module-content-inner">
                        <ul>
                            {topics_li}
                        </ul>
                    </div>
                </div>
            </div>
            """

        syllabus_faq_html = ""
        syllabus_faq_entities = []
        for faq in data.get("syllabus_faqs", []):
            syllabus_faq_html += f"""
            <div class="curriculum-module">
                <div class="module-header faq-header">
                    <h4>{faq['q']}</h4>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="faq-content module-content">
                    <div class="module-content-inner">
                        <p style="color: var(--text-secondary); font-size: 0.95rem;">{faq['a']}</p>
                    </div>
                </div>
            </div>
            """
            syllabus_faq_entities.append({
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}
            })

        syllabus_left_column = f"""
        <h2 style="margin-bottom: 1.5rem;">Detailed Syllabus</h2>
        <p style="font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 2.5rem;">Below is the comprehensive, module-by-module curriculum. As this training is strictly 1-to-1, we can adjust the syllabus scope or spend more time on specific modules based on your learning speed.</p>

        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2rem; margin-bottom: 2.5rem;">
            <h3 style="margin-bottom: 0.75rem; color: var(--text-primary); font-family: var(--font-heading);">Course Prerequisites</h3>
            <p style="color: var(--text-secondary); line-height: 1.6; font-size: 0.98rem; margin: 0;">{data.get('syllabus_prerequisites', '')}</p>
        </div>

        <h3 style="margin-bottom: 1.5rem; font-family: var(--font-heading);">Full Curriculum Structure</h3>
        <div class="curriculum-accordion" style="margin-bottom: 3rem;">
            {expanded_curr_html}
        </div>

        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2.5rem; margin-bottom: 3rem;">
            <h3 style="color: var(--accent-light); margin-bottom: 1.25rem; font-family: var(--font-heading); display: flex; align-items: center; gap: 0.5rem;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); flex-shrink: 0;"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>Tools & Technologies Mastered</h3>
            <div class="skills-grid" style="margin-bottom: 1.5rem;">
                {syllabus_tools_html}
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">You will gain hands-on operational capability in these tools during screenshare coding loops, creating real repositories.</p>
        </div>

        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2.5rem; margin-bottom: 3rem;">
            <h3 style="color: var(--primary-light); margin-bottom: 1.25rem; font-family: var(--font-heading); display: flex; align-items: center; gap: 0.5rem;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); flex-shrink: 0;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>Hands-on Lab Assignments & Projects</h3>
            <ul style="color: var(--text-secondary); margin-left: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem;">
                {syllabus_projects_html}
            </ul>
        </div>

        <div style="margin-top: 4rem;">
            <h2 style="margin-bottom: 1.5rem;">Syllabus FAQs</h2>
            <div class="course-faqs-accordion">
                {syllabus_faq_html}
            </div>
        </div>
        """

        syllabus_parts = []
        for idx, mod in enumerate(modules):
            syllabus_parts.append({
                "@type": "CreativeWork",
                "name": mod["title"],
                "timeRequired": f"P{mod['duration'].replace(' Weeks', 'W')}" if "Weeks" in mod["duration"] else "P1M"
            })
        course_schema_syllabus = {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": f"{name} Syllabus",
            "description": f"Detailed topic-by-topic Syllabus for {name} in Pune.",
            "provider": {
                "@type": "Organization",
                "name": "CACTS - Centre of Advanced Computer Training and Studies",
                "url": "https://cactslearn.github.io/"
            },
            "hasPart": syllabus_parts
        }

        syllabus_breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cactslearn.github.io/index.html"},
                {"@type": "ListItem", "position": 2, "name": name, "item": f"https://cactslearn.github.io/{slug}.html"},
                {"@type": "ListItem", "position": 3, "name": "Syllabus", "item": f"https://cactslearn.github.io/{base_slug}-syllabus.html"}
            ]
        }

        schema_markup2 = f"""
        <script type="application/ld+json">
        {json.dumps(course_schema_syllabus, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": syllabus_faq_entities}, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps(syllabus_breadcrumb, indent=2)}
        </script>
        """

        page_html2 = template
        page_html2 = page_html2.replace("{{seo_title}}", f"{name} Syllabus | Detailed Course Topics | CACTS Pune")
        page_html2 = page_html2.replace("{{meta_description}}", f"Read the complete, detailed course syllabus for 1-to-1 {name} training in Pune. Explore modules, prerequisites, and live tools.")
        page_html2 = page_html2.replace("{{canonical}}", f"https://cactslearn.github.io/{base_slug}-syllabus.html")
        page_html2 = page_html2.replace("{{schema_markup}}", schema_markup2)
        page_html2 = page_html2.replace("{{course_name}}", name)
        page_html2 = page_html2.replace("{{course_name_encoded}}", name_encoded)
        page_html2 = page_html2.replace("{{h1}}", f"{name} Syllabus & Modules")
        page_html2 = page_html2.replace("{{h2}}", f"Complete dynamic pacing topics, hand-on tools, and project milestones.")
        page_html2 = page_html2.replace("{{duration}}", duration)
        page_html2 = page_html2.replace("{{price}}", price)
        page_html2 = page_html2.replace("{{course_reviews}}", reviews_html)
        page_html2 = page_html2.replace("{{course_tabs}}", get_tabs_html("syllabus"))
        page_html2 = page_html2.replace("{{course_left_column}}", syllabus_left_column)
        page_html2 = page_html2.replace('href="#register"', f'href="contact.html?course={name_encoded}"')
        page_html2 = page_html2.replace('Request Free Trial Demo', 'Schedule Syllabus Consultation')

        with open(f"{base_slug}-syllabus.html", "w", encoding="utf-8") as f:
            f.write(page_html2)
        generated_pages.append(f"{base_slug}-syllabus")

        # ----------------------------------------------------
        # PAGE 3: Fees Page ([base_slug]-course-fees.html)
        # ----------------------------------------------------
        fees_faq_html = ""
        fees_faq_entities = []
        for faq in data.get("fees_faqs", []):
            fees_faq_html += f"""
            <div class="curriculum-module">
                <div class="module-header faq-header">
                    <h4>{faq['q']}</h4>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="faq-content module-content">
                    <div class="module-content-inner">
                        <p style="color: var(--text-secondary); font-size: 0.95rem;">{faq['a']}</p>
                    </div>
                </div>
            </div>
            """
            fees_faq_entities.append({
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}
            })

        fees_left_column = f"""
        <h2 style="margin-bottom: 1.5rem;">Course Fees & Flexible Options</h2>
        <p style="font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 2.5rem;">We offer transparent, value-driven pricing structures for our individual 1-to-1 virtual mentoring. No hidden registration fees or laboratory charges.</p>

        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2.5rem; margin-bottom: 3rem;">
            <h3 style="color: var(--accent-light); margin-bottom: 1rem; font-family: var(--font-heading);">Tuition Fees Structure</h3>
            <p style="color: var(--text-primary); font-size: 1.2rem; font-weight: 700; margin-bottom: 0.75rem;">Price: {price} <span style="font-size: 0.9rem; font-weight: normal; color: var(--text-secondary);">(All-inclusive tuition fee)</span></p>
            <p style="color: var(--text-secondary); line-height: 1.6; margin: 0;">{data.get('fees_structure', '')}</p>
        </div>

        <!-- Comparative pricing card -->
        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2.5rem; margin-bottom: 3rem;">
            <h3 style="color: var(--warning); margin-bottom: 1.25rem; font-family: var(--font-heading);">Market Cost Comparison (Pune)</h3>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; color: var(--text-secondary); font-size: 0.95rem; min-width: 400px;">
                    <thead>
                        <tr style="border-bottom: 2px solid var(--border); color: var(--text-primary);">
                            <th style="padding: 0.75rem 0.5rem;">Feature</th>
                            <th style="padding: 0.75rem 0.5rem;">Typical Pune Institutes</th>
                            <th style="padding: 0.75rem 0.5rem; color: var(--success);">CACTS Training</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid var(--border);">
                            <td style="padding: 0.75rem 0.5rem; font-weight: 600;">Average Fees</td>
                            <td style="padding: 0.75rem 0.5rem;">{data.get('fees_comparison', {}).get('typical_pune_fees', '₹40,000')}</td>
                            <td style="padding: 0.75rem 0.5rem; color: var(--success); font-weight: 600;">{price}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border);">
                            <td style="padding: 0.75rem 0.5rem; font-weight: 600;">Batch Size</td>
                            <td style="padding: 0.75rem 0.5rem;">{data.get('fees_comparison', {}).get('pune_batch_size', '30+')}</td>
                            <td style="padding: 0.75rem 0.5rem; color: var(--success); font-weight: 600;">Strictly 1-to-1 (Private)</td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border);">
                            <td style="padding: 0.75rem 0.5rem; font-weight: 600;">Learning Mode</td>
                            <td style="padding: 0.75rem 0.5rem;">Passive batch listening</td>
                            <td style="padding: 0.75rem 0.5rem; color: var(--success); font-weight: 600;">Active screenshare coding</td>
                        </tr>
                        <tr>
                            <td style="padding: 0.75rem 0.5rem; font-weight: 600;">Code Review</td>
                            <td style="padding: 0.75rem 0.5rem;">Rare or automated tools</td>
                            <td style="padding: 0.75rem 0.5rem; color: var(--success); font-weight: 600;">Direct senior dev comments</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.88rem; margin-top: 1.5rem; line-height: 1.5;">{data.get('fees_comparison', {}).get('cacts_value', '')}</p>
        </div>

        <div style="margin-top: 4rem;">
            <h2 style="margin-bottom: 1.5rem;">Fees & Payment FAQs</h2>
            <div class="course-faqs-accordion">
                {fees_faq_html}
            </div>
        </div>
        """

        course_schema_fees = {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": f"{name} Course Fees",
            "description": f"Transparent tuition and installment fees for {name} in Pune.",
            "provider": {
                "@type": "Organization",
                "name": "CACTS - Centre of Advanced Computer Training and Studies",
                "url": "https://cactslearn.github.io/"
            },
            "offers": {
                "@type": "Offer",
                "price": str(price_num),
                "priceCurrency": "INR",
                "category": "Value-Driven Professional Programming Training"
            }
        }

        fees_breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cactslearn.github.io/index.html"},
                {"@type": "ListItem", "position": 2, "name": name, "item": f"https://cactslearn.github.io/{slug}.html"},
                {"@type": "ListItem", "position": 3, "name": "Course Fees", "item": f"https://cactslearn.github.io/{base_slug}-course-fees.html"}
            ]
        }

        schema_markup3 = f"""
        <script type="application/ld+json">
        {json.dumps(course_schema_fees, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": fees_faq_entities}, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps(fees_breadcrumb, indent=2)}
        </script>
        """

        page_html3 = template
        page_html3 = page_html3.replace("{{seo_title}}", f"{name} Course Fees in Pune | Transparent Pricing | CACTS")
        page_html3 = page_html3.replace("{{meta_description}}", f"Check current fees, installment structures, and pricing discounts for 1-to-1 {name} training in Pune. Zero hidden charges.")
        page_html3 = page_html3.replace("{{canonical}}", f"https://cactslearn.github.io/{base_slug}-course-fees.html")
        page_html3 = page_html3.replace("{{schema_markup}}", schema_markup3)
        page_html3 = page_html3.replace("{{course_name}}", name)
        page_html3 = page_html3.replace("{{course_name_encoded}}", name_encoded)
        page_html3 = page_html3.replace("{{h1}}", f"{name} Course Fees")
        page_html3 = page_html3.replace("{{h2}}", f"Affordable pricing, flexible installment formats, and 1-on-1 mentor value.")
        page_html3 = page_html3.replace("{{duration}}", duration)
        page_html3 = page_html3.replace("{{price}}", price)
        page_html3 = page_html3.replace("{{course_reviews}}", reviews_html)
        page_html3 = page_html3.replace("{{course_tabs}}", get_tabs_html("fees"))
        page_html3 = page_html3.replace("{{course_left_column}}", fees_left_column)
        page_html3 = page_html3.replace('href="#register"', f'href="contact.html?course={name_encoded}"')
        page_html3 = page_html3.replace('Request Free Trial Demo', 'Inquire About Installments')

        with open(f"{base_slug}-course-fees.html", "w", encoding="utf-8") as f:
            f.write(page_html3)
        generated_pages.append(f"{base_slug}-course-fees")

        # ----------------------------------------------------
        # PAGE 4: Interview Questions ([base_slug]-interview-questions.html)
        # ----------------------------------------------------
        interview_list_html = ""
        interview_schema_entities = []
        for idx, item in enumerate(data.get("interview_questions", [])):
            interview_list_html += f"""
            <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2rem; margin-bottom: 1.5rem;">
                <h3 style="font-size: 1.1rem; color: var(--accent-light); margin-bottom: 1rem; line-height: 1.4; font-family: var(--font-heading);">Q{idx+1}: {item['q']}</h3>
                <p style="color: var(--text-secondary); line-height: 1.6; font-size: 0.98rem; margin: 0; white-space: pre-wrap;"><strong>Answer:</strong> {item['a']}</p>
            </div>
            """
            interview_schema_entities.append({
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]}
            })

        interview_faq_html = ""
        for faq in data.get("interview_faqs", []):
            interview_faq_html += f"""
            <div class="curriculum-module">
                <div class="module-header faq-header">
                    <h4>{faq['q']}</h4>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="faq-content module-content">
                    <div class="module-content-inner">
                        <p style="color: var(--text-secondary); font-size: 0.95rem;">{faq['a']}</p>
                    </div>
                </div>
            </div>
            """
            interview_schema_entities.append({
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}
            })

        interview_left_column = f"""
        <h2 style="margin-bottom: 1.5rem;">Technical Interview Questions</h2>
        <p style="font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 2.5rem;">Review the top developer interview questions for {name} asked by IT hiring managers in Pune. We practice these live during mock interview sessions.</p>

        <div style="margin-bottom: 3rem;">
            {interview_list_html}
        </div>

        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2.5rem; margin-bottom: 3rem;">
            <h3 style="color: var(--primary-light); margin-bottom: 1rem; font-family: var(--font-heading);">1-to-1 Corporate Mock Interview Loops</h3>
            <p style="color: var(--text-secondary); line-height: 1.6; margin: 0;">During the final modules of the course, we schedule dedicated screensharing mock interviews. You write code live on shared editors, explaining your runtime complexity and database designs to prepare for real technical rounds.</p>
        </div>

        <div style="margin-top: 4rem;">
            <h2 style="margin-bottom: 1.5rem;">Interview & Career FAQs</h2>
            <div class="course-faqs-accordion">
                {interview_faq_html}
            </div>
        </div>
        """

        interview_breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cactslearn.github.io/index.html"},
                {"@type": "ListItem", "position": 2, "name": name, "item": f"https://cactslearn.github.io/{slug}.html"},
                {"@type": "ListItem", "position": 3, "name": "Interview Questions", "item": f"https://cactslearn.github.io/{base_slug}-interview-questions.html"}
            ]
        }

        schema_markup4 = f"""
        <script type="application/ld+json">
        {json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": interview_schema_entities}, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps(interview_breadcrumb, indent=2)}
        </script>
        """

        page_html4 = template
        page_html4 = page_html4.replace("{{seo_title}}", f"Top {name} Interview Questions & Answers | CACTS Pune")
        page_html4 = page_html4.replace("{{meta_description}}", f"Master technical programming, data, and system questions for {name} interviews. Screen-sharing answers vetted by developers.")
        page_html4 = page_html4.replace("{{canonical}}", f"https://cactslearn.github.io/{base_slug}-interview-questions.html")
        page_html4 = page_html4.replace("{{schema_markup}}", schema_markup4)
        page_html4 = page_html4.replace("{{course_name}}", name)
        page_html4 = page_html4.replace("{{course_name_encoded}}", name_encoded)
        page_html4 = page_html4.replace("{{h1}}", f"{name} Interview Preparation")
        page_html4 = page_html4.replace("{{h2}}", f"Technical mock interview code answers, core logic structures, and resume guides.")
        page_html4 = page_html4.replace("{{duration}}", duration)
        page_html4 = page_html4.replace("{{price}}", price)
        page_html4 = page_html4.replace("{{course_reviews}}", reviews_html)
        page_html4 = page_html4.replace("{{course_tabs}}", get_tabs_html("interview"))
        page_html4 = page_html4.replace("{{course_left_column}}", interview_left_column)
        page_html4 = page_html4.replace('href="#register"', f'href="contact.html?course={name_encoded}"')
        page_html4 = page_html4.replace('Request Free Trial Demo', 'Book 1-to-1 Demo Slot')

        with open(f"{base_slug}-interview-questions.html", "w", encoding="utf-8") as f:
            f.write(page_html4)
        generated_pages.append(f"{base_slug}-interview-questions")

        # ----------------------------------------------------
        # PAGE 5: Roadmap Page ([base_slug]-roadmap.html)
        # ----------------------------------------------------
        roadmap_milestones_html = ""
        for m in data.get("roadmap_milestones", []):
            roadmap_milestones_html += f"""
            <div class="curriculum-module">
                <div class="module-header" style="cursor: default;">
                    <h4 style="color: var(--accent-light); font-family: var(--font-heading);">{m['phase']}: {m['title']}</h4>
                    <span class="module-duration">{m['duration']}</span>
                </div>
                <div class="module-content active" style="max-height: none; background: rgba(6, 9, 19, 0.15);">
                    <div class="module-content-inner">
                        <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 0.5rem;"><strong>Skills Focus:</strong> {m['skills']}</p>
                        <p style="color: var(--text-primary); font-size: 0.95rem; margin: 0;"><strong>Milestone Project:</strong> {m['project']}</p>
                    </div>
                </div>
            </div>
            """

        roadmap_faq_html = ""
        roadmap_faq_entities = []
        for faq in data.get("roadmap_faqs", []):
            roadmap_faq_html += f"""
            <div class="curriculum-module">
                <div class="module-header faq-header">
                    <h4>{faq['q']}</h4>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="faq-content module-content">
                    <div class="module-content-inner">
                        <p style="color: var(--text-secondary); font-size: 0.95rem;">{faq['a']}</p>
                    </div>
                </div>
            </div>
            """
            roadmap_faq_entities.append({
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}
            })

        roadmap_left_column = f"""
        <h2 style="margin-bottom: 1.5rem;">{name} Career Roadmap</h2>
        <p style="font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 2.5rem;">Below is the step-by-step milestone learning path from absolute beginner to production-ready software developer, including average developer salaries in Pune.</p>

        <h3 style="margin-bottom: 1.5rem; font-family: var(--font-heading);">Milestone Learning Timeline</h3>
        <div class="curriculum-accordion" style="margin-bottom: 3rem;">
            {roadmap_milestones_html}
        </div>

        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 2.5rem; margin-bottom: 3rem;">
            <h3 style="color: var(--success); margin-bottom: 1rem; font-family: var(--font-heading);">Pune IT Salary & Career Outlook</h3>
            <p style="color: var(--text-secondary); line-height: 1.6; margin: 0;">Pune is a major IT destination, with tech parks in Hinjewadi, Kharadi, and Baner. Full stack, Data Science, and DevOps developers who can configure environments, run Git workflows, and write clean database queries are in high demand across mid-sized companies and MNCs.</p>
        </div>

        <div style="margin-top: 4rem;">
            <h2 style="margin-bottom: 1.5rem;">Career Path FAQs</h2>
            <div class="course-faqs-accordion">
                {roadmap_faq_html}
            </div>
        </div>
        """

        steps = []
        for idx, m in enumerate(data.get("roadmap_milestones", [])):
            steps.append({
                "@type": "HowToStep",
                "position": idx + 1,
                "name": m["title"],
                "text": f"Skills: {m['skills']}. Milestone Project: {m['project']}"
            })
        roadmap_howto = {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": f"How to become a {name} Specialist",
            "description": f"Step-by-step career path and roadmap milestones for {name}.",
            "step": steps
        }

        roadmap_breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cactslearn.github.io/index.html"},
                {"@type": "ListItem", "position": 2, "name": name, "item": f"https://cactslearn.github.io/{slug}.html"},
                {"@type": "ListItem", "position": 3, "name": "Career Roadmap", "item": f"https://cactslearn.github.io/{base_slug}-roadmap.html"}
            ]
        }

        schema_markup5 = f"""
        <script type="application/ld+json">
        {json.dumps(roadmap_howto, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": roadmap_faq_entities}, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps(roadmap_breadcrumb, indent=2)}
        </script>
        """

        page_html5 = template
        page_html5 = page_html5.replace("{{seo_title}}", f"{name} Career Roadmap | Step-by-Step Guide | CACTS Pune")
        page_html5 = page_html5.replace("{{meta_description}}", f"Explore the complete learning and employment roadmap for {name}. Follow salary phases, milestones, and local Pune tech timelines.")
        page_html5 = page_html5.replace("{{canonical}}", f"https://cactslearn.github.io/{base_slug}-roadmap.html")
        page_html5 = page_html5.replace("{{schema_markup}}", schema_markup5)
        page_html5 = page_html5.replace("{{course_name}}", name)
        page_html5 = page_html5.replace("{{course_name_encoded}}", name_encoded)
        page_html5 = page_html5.replace("{{h1}}", f"{name} Learning Roadmap")
        page_html5 = page_html5.replace("{{h2}}", f"Phase-by-phase timeline milestones, Pune starting salaries, and job roles.")
        page_html5 = page_html5.replace("{{duration}}", duration)
        page_html5 = page_html5.replace("{{price}}", price)
        page_html5 = page_html5.replace("{{course_reviews}}", reviews_html)
        page_html5 = page_html5.replace("{{course_tabs}}", get_tabs_html("roadmap"))
        page_html5 = page_html5.replace("{{course_left_column}}", roadmap_left_column)
        page_html5 = page_html5.replace('href="#register"', f'href="contact.html?course={name_encoded}"')
        page_html5 = page_html5.replace('Request Free Trial Demo', 'Schedule Career Guidance')

        with open(f"{base_slug}-roadmap.html", "w", encoding="utf-8") as f:
            f.write(page_html5)
        generated_pages.append(f"{base_slug}-roadmap")

    # Generate Extra Resource Pages
    resource_template_path = os.path.join("src", "resource_template.html")
    with open(resource_template_path, "r", encoding="utf-8") as f:
        res_template = f.read()

    for pg in EXTRA_PAGES:
        category = pg["category"]
        slug = pg["slug"]
        seo_title = pg["seo_title"]
        meta_description = pg["meta_description"]
        h1 = pg["h1"]
        h2 = pg["h2"]
        related_course = pg["related_course"]
        related_course_slug = pg["related_course_slug"]
        key_takeaways = pg["key_takeaways"]
        content_blocks = pg["content_blocks"]
        faqs = pg["faqs"]
        category_label = pg["category_label"]

        if category in ["glossary", "projects", "certifications"]:
            category_index = "free-learning-resources.html"
        elif category == "comparison":
            category_index = "technology-comparisons.html"
        else:
            category_index = "technology-career-guides.html"

        key_takeaways_html = "\n".join([f"<li>{item}</li>" for item in key_takeaways])

        content_html = ""
        for block in content_blocks:
            text_formatted = block["text"].replace("\n", "<br>")
            content_html += f"""
                    <div style="margin-bottom: 2rem;">
                        <h2 style="font-size: 1.6rem; color: var(--text-primary); margin-bottom: 1rem; font-family: var(--font-heading);">{block['title']}</h2>
                        <p style="color: var(--text-secondary); line-height: 1.7; font-size: 1rem;">{text_formatted}</p>
                    </div>
            """

        # Append technical code block and documentation outlinks
        snippet_data = CODE_SNIPPETS_DATA.get(slug, {})
        if snippet_data:
            if "code_snippet" in snippet_data:
                code_info = snippet_data["code_snippet"]
                escaped_code = code_info["code"].replace("<", "&lt;").replace(">", "&gt;")
                content_html += f"""
                    <div class="code-snippet-container">
                        <h3 class="code-snippet-title">{code_info['title']}</h3>
                        <pre><code class="language-{code_info['language']}">{escaped_code}</code></pre>
                    </div>
                """
            
            if "official_doc" in snippet_data:
                doc_info = snippet_data["official_doc"]
                content_html += f"""
                    <div class="official-doc-container">
                        <div>
                            <h4 class="official-doc-title">Official Documentation</h4>
                            <p class="official-doc-desc">Access official code repositories and developer documentation.</p>
                        </div>
                        <a href="{doc_info['url']}" target="_blank" rel="noopener" class="btn btn-secondary official-doc-link">
                            {doc_info['label']} ↗
                        </a>
                    </div>
                """

            if "internal_links" in snippet_data:
                links_html = ""
                for link in snippet_data["internal_links"]:
                    links_html += f"""
                    <li style="margin-bottom: 0.75rem; line-height: 1.5;">
                        {link['context'].replace(link['label'], f'<a href="{link["url"]}" style="color: var(--accent); text-decoration: none; font-weight: 600;">{link["label"]}</a>')}
                    </li>
                    """
                content_html += f"""
                    <div class="related-guides-container">
                        <h4 class="related-guides-title">Related Practical Guides</h4>
                        <ul class="related-guides-list">
                            {links_html}
                        </ul>
                    </div>
                """


        faq_html = ""
        faq_entities = []
        for faq in faqs:
            faq_html += f"""
                    <div class="curriculum-module">
                        <div class="module-header faq-header">
                            <h4>{faq['q']}</h4>
                            <span class="accordion-icon">+</span>
                        </div>
                        <div class="faq-content module-content">
                            <div class="module-content-inner">
                                <p style="color: var(--text-secondary); font-size: 0.95rem;">{faq['a']}</p>
                            </div>
                        </div>
                    </div>
            """
            faq_entities.append({
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["a"]
                }
            })

        breadcrumb_schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cactslearn.github.io/index.html"},
                {"@type": "ListItem", "position": 2, "name": category_label, "item": f"https://cactslearn.github.io/{category_index}"},
                {"@type": "ListItem", "position": 3, "name": h1, "item": f"https://cactslearn.github.io/{slug}.html"}
            ]
        }

        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }

        article_schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": seo_title,
            "description": meta_description,
            "author": {
                "@type": "Person",
                "name": "Hambirrao P",
                "url": "https://cactslearn.github.io/about.html#hambirrao",
                "sameAs": [
                    "https://www.linkedin.com/in/hambirrao/"
                ]
            },
            "publisher": {
                "@type": "Organization",
                "name": "CACTS - Centre of Advanced Computer Training and Studies",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://cactslearn.github.io/images/cacts-logo.png"
                }
            },
            "mainEntityOfPage": f"https://cactslearn.github.io/{slug}.html"
        }

        schema_markup = f"""
        <script type="application/ld+json">
        {json.dumps(article_schema, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps(faq_schema, indent=2)}
        </script>
        <script type="application/ld+json">
        {json.dumps(breadcrumb_schema, indent=2)}
        </script>
        """

        page_html = res_template
        page_html = page_html.replace("{{seo_title}}", seo_title)
        page_html = page_html.replace("{{meta_description}}", meta_description)
        page_html = page_html.replace("{{canonical}}", f"https://cactslearn.github.io/{slug}.html")
        page_html = page_html.replace("{{schema_markup}}", schema_markup)
        page_html = page_html.replace("{{category_index}}", category_index)
        page_html = page_html.replace("{{category_label}}", category_label)
        page_html = page_html.replace("{{h1}}", h1)
        page_html = page_html.replace("{{h2}}", h2)
        page_html = page_html.replace("{{h1_encoded}}", urllib.parse.quote(h1))
        page_html = page_html.replace("{{key_takeaways_html}}", key_takeaways_html)
        page_html = page_html.replace("{{content_html}}", content_html)
        page_html = page_html.replace("{{faq_html}}", faq_html)
        page_html = page_html.replace("{{related_course}}", related_course)
        page_html = page_html.replace("{{related_course_slug}}", related_course_slug)
        page_html = page_html.replace("{{related_course_encoded}}", urllib.parse.quote(related_course))

        with open(f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(page_html)
        generated_pages.append(slug)

    # 5. Generate sitemap.xml
    current_date = datetime.now().strftime("%Y-%m-%d")
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://cactslearn.github.io/</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/about.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/contact.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/internship-on-live-projects.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/one-to-one-software-training.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/free-career-guidance.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/reviews.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/faqs.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/sitemap.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/privacy-policy.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/terms-conditions.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/free-skill-assessment.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/course-recommendation-quiz.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/career-roadmaps.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/student-projects.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/internship-showcase.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/project-portfolios.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/technology-comparisons.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/free-learning-resources.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/technology-career-guides.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/software-training-institute-pune.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/software-training-institute-shivane.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/software-training-institute-karvenagar.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/software-training-institute-warje.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/software-training-institute-kothrud.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://cactslearn.github.io/software-training-institute-sinhagad-road.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""

    for pg in generated_pages:
        sitemap_xml += f"""    <url>
        <loc>https://cactslearn.github.io/{pg}.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
"""

    sitemap_xml += "</urlset>"

    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
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
                    <a href="https://g.page/r/CaTs8mGD9uaoEBM/review" target="_blank" rel="noopener" style="color: var(--accent); text-decoration: none; font-size: 0.75rem; font-weight: 500; display: inline-flex; align-items: center; gap: 0.25rem; white-space: nowrap;">
                        Verify Review ↗
                    </a>
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
                "streetAddress": "Shivane",
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

        with open(reviews_page_path, "w", encoding="utf-8") as f:
            f.write(reviews_content)
        print("Updated central reviews.html with all 33 reviews and injected LocalBusiness schema.")

if __name__ == "__main__":
    build()
