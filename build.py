import json
import os
import urllib.parse
from datetime import datetime

def build():
    # Paths
    src_json = os.path.join("src", "courses.json")
    src_template = os.path.join("src", "template.html")
    courses_dir = ""
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

        canonical = f"https://cactslearn.github.io/{slug}.html"
        name_encoded = urllib.parse.quote(name)

        # 1. Build Skills Bubbles
        skills_bubbles = ""
        for s in skills:
            skills_bubbles += f'<span class="skill-bubble">{s}</span>\n'

        # 2. Build Curriculum Modules
        curr_html = ""
        for mod in modules:
            topics_li = ""
            for t in mod["topics"]:
                topics_li += f'<li>{t}</li>\n'
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

        # 4. Generate Schema Markup
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
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://cactslearn.github.io/index.html"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": name,
                    "item": f"https://cactslearn.github.io/{slug}.html"
                }
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

        # Replace placeholders in template
        page_html = template
        page_html = page_html.replace("{{seo_title}}", seo_title)
        page_html = page_html.replace("{{meta_description}}", meta_description)
        page_html = page_html.replace("{{canonical}}", canonical)
        page_html = page_html.replace("{{schema_markup}}", schema_markup)
        page_html = page_html.replace("{{course_name}}", name)
        page_html = page_html.replace("{{course_name_encoded}}", name_encoded)
        page_html = page_html.replace("{{h1}}", h1)
        page_html = page_html.replace("{{h2}}", h2)
        page_html = page_html.replace("{{duration}}", duration)
        page_html = page_html.replace("{{price}}", price)
        page_html = page_html.replace("{{overview}}", overview)
        page_html = page_html.replace("{{skills_bubbles}}", skills_bubbles)
        page_html = page_html.replace("{{curriculum_modules}}", curr_html)
        page_html = page_html.replace("{{course_faqs}}", faq_html)

        # Write to courses directory
        output_path = f"{slug}.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        print(f"Generated page: {output_path}")
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

if __name__ == "__main__":
    build()
