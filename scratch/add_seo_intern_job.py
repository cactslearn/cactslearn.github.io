import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.jobs_data import JOBS_DATA

seo_job = {
    'slug': 'seo-intern',
    'title': 'SEO & Digital Marketing Intern',
    'category': 'Digital Marketing',
    'related_course_name': 'Software & IT Training Programs',
    'related_course_slug': 'technology-career-guides',
    'experience': 'Freshers / Graduates',
    'employment_type': 'FULL_TIME',
    'stipend': '₹10,000 / month',
    'location': 'Pune (Aundh)',
    'summary': 'We are looking for a passionate SEO Intern to join our digital marketing team in Pune (Aundh). Learn search engine optimization techniques, keyword research, website analysis, and digital marketing strategies on real projects.',
    'responsibilities': [
        'Assist in keyword research and competitor analysis.',
        'Support on-page and off-page SEO activities.',
        'Optimize website content, meta titles, descriptions, and tags.',
        'Monitor website traffic and prepare SEO performance reports.',
        'Work on backlink creation and link-building activities.',
        'Assist in improving website ranking on search engines.',
        'Coordinate with content and development teams for SEO implementation.',
        'Stay updated with the latest SEO trends and digital marketing practices.'
    ],
    'requirements': [
        'Good verbal and written communication skills.',
        'Basic understanding of search engines and website optimization.',
        'Familiarity with tools like Google Search Console, Google Analytics, or SEO tools is a plus.',
        'Graduation pursuing/completed in Marketing, Business Administration, IT, or related field.',
        'Quick learner with a positive attitude and strong analytical skills.',
        'Certification in Digital Marketing/SEO will be an added advantage.'
    ],
    'bridge_headline': 'Want to master technical SEO, Web Architecture & Digital Marketing?',
    'bridge_description': 'Explore CACTS learning resources and developer guides to master website optimization, performance tuning, and technical search engine architecture.',
    'meta_title': 'SEO Intern Job Opening in Pune (Aundh) | CACTS',
    'meta_description': 'Apply for SEO Intern position at CACTS Pune (Aundh). Learn keyword research, on-page/off-page SEO & Google Analytics on real projects. Stipend: ₹10,000/month.'
}

# Add if not already present
if not any(j['slug'] == 'seo-intern' for j in JOBS_DATA):
    JOBS_DATA.append(seo_job)

    # Write updated JOBS_DATA back to src/jobs_data.py
    jobs_py_path = os.path.join(project_root, "src", "jobs_data.py")
    with open(jobs_py_path, "w", encoding="utf-8") as f:
        f.write(f"JOBS_DATA = {repr(JOBS_DATA)}\n")
    print("Appended SEO Intern job to src/jobs_data.py.")
else:
    print("SEO Intern job already exists in src/jobs_data.py.")
