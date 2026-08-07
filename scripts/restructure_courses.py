import os
import glob
import re
from bs4 import BeautifulSoup

# Base URL
BASE_URL = "https://cactslearn.github.io"

# Define the exact mapping model: course_slug -> { old_root_filename: new_sub_filename }
COURSE_MAPPINGS = {
    'ai-ml': {
        'ai-ml-training.html': 'index.html',
        'ai-ml-syllabus.html': 'syllabus.html',
        'ai-ml-course-fees.html': 'fees.html',
        'ai-ml-interview-questions.html': 'interview-questions.html',
        'ai-ml-roadmap.html': 'roadmap.html',
        'beginner-to-ai-engineer-roadmap.html': 'beginner.html',
        'spark-vs-hadoop.html': 'comparison.html',
    },
    'blockchain': {
        'blockchain-training.html': 'index.html',
        'blockchain-syllabus.html': 'syllabus.html',
        'blockchain-course-fees.html': 'fees.html',
        'blockchain-interview-questions.html': 'interview-questions.html',
        'blockchain-roadmap.html': 'roadmap.html',
        'blockchain-project-ideas.html': 'projects.html',
        'beginner-to-blockchain-developer-roadmap.html': 'beginner.html',
        'best-blockchain-certifications.html': 'certifications.html',
    },
    'cloud': {
        'cloud-training.html': 'index.html',
        'cloud-syllabus.html': 'syllabus.html',
        'cloud-course-fees.html': 'fees.html',
        'cloud-interview-questions.html': 'interview-questions.html',
        'cloud-roadmap.html': 'roadmap.html',
        'best-aws-cloud-certifications.html': 'certifications.html',
        'aws-vs-azure.html': 'comparison.html',
    },
    'cybersecurity': {
        'cybersecurity-training.html': 'index.html',
        'cybersecurity-syllabus.html': 'syllabus.html',
        'cybersecurity-course-fees.html': 'fees.html',
        'cybersecurity-interview-questions.html': 'interview-questions.html',
        'cybersecurity-roadmap.html': 'roadmap.html',
        'cybersecurity-project-ideas.html': 'projects.html',
        'beginner-to-cybersecurity-analyst-roadmap.html': 'beginner.html',
        'best-cybersecurity-certifications.html': 'certifications.html',
    },
    'data-engineering': {
        'data-engineering-training.html': 'index.html',
        'data-engineering-syllabus.html': 'syllabus.html',
        'data-engineering-course-fees.html': 'fees.html',
        'data-engineering-interview-questions.html': 'interview-questions.html',
        'data-engineering-roadmap.html': 'roadmap.html',
        'data-engineering-project-ideas.html': 'projects.html',
        'beginner-to-data-engineer-roadmap.html': 'beginner.html',
        'best-data-engineering-certifications.html': 'certifications.html',
    },
    'data-science': {
        'data-science-training.html': 'index.html',
        'data-science-syllabus.html': 'syllabus.html',
        'data-science-course-fees.html': 'fees.html',
        'data-science-interview-questions.html': 'interview-questions.html',
        'data-science-roadmap.html': 'roadmap.html',
        'data-science-project-ideas.html': 'projects.html',
    },
    'devops': {
        'devops-training.html': 'index.html',
        'devops-syllabus.html': 'syllabus.html',
        'devops-course-fees.html': 'fees.html',
        'devops-interview-questions.html': 'interview-questions.html',
        'devops-roadmap.html': 'roadmap.html',
        'devops-project-ideas.html': 'projects.html',
        'beginner-to-devops-engineer-roadmap.html': 'beginner.html',
        'best-devops-certifications.html': 'certifications.html',
        'docker-vs-kubernetes.html': 'comparison.html',
    },
    'full-stack': {
        'full-stack-training.html': 'index.html',
        'full-stack-syllabus.html': 'syllabus.html',
        'full-stack-course-fees.html': 'fees.html',
        'full-stack-interview-questions.html': 'interview-questions.html',
        'full-stack-roadmap.html': 'roadmap.html',
    },
    'java-fullstack': {
        'java-fullstack-training.html': 'index.html',
        'java-fullstack-syllabus.html': 'syllabus.html',
        'java-fullstack-course-fees.html': 'fees.html',
        'java-fullstack-interview-questions.html': 'interview-questions.html',
        'java-fullstack-roadmap.html': 'roadmap.html',
        'java-fullstack-project-ideas.html': 'projects.html',
        'beginner-to-java-fullstack-developer-roadmap.html': 'beginner.html',
        'java-vs-python.html': 'comparison.html',
    },
    'one-to-one-software': {
        'one-to-one-software-training.html': 'index.html',
    },
    'power-bi': {
        'power-bi-training.html': 'index.html',
        'power-bi-syllabus.html': 'syllabus.html',
        'power-bi-course-fees.html': 'fees.html',
        'power-bi-interview-questions.html': 'interview-questions.html',
        'power-bi-roadmap.html': 'roadmap.html',
        'power-bi-dashboard-ideas.html': 'projects.html',
        'best-power-bi-certifications.html': 'certifications.html',
        'power-bi-vs-tableau.html': 'comparison.html',
    },
    'python': {
        'python-training.html': 'index.html',
        'python-syllabus.html': 'syllabus.html',
        'python-course-fees.html': 'fees.html',
        'python-interview-questions.html': 'interview-questions.html',
        'python-roadmap.html': 'roadmap.html',
        'beginner-to-python-developer-roadmap.html': 'beginner.html',
    },
    'react-js': {
        'react-js-training.html': 'index.html',
        'react-js-syllabus.html': 'syllabus.html',
        'react-js-course-fees.html': 'fees.html',
        'react-js-interview-questions.html': 'interview-questions.html',
        'react-js-roadmap.html': 'roadmap.html',
        'react-js-project-ideas.html': 'projects.html',
        'beginner-to-react-js-roadmap.html': 'beginner.html',
        'react-vs-angular.html': 'comparison.html',
    },
    'react-native': {
        'react-native-training.html': 'index.html',
        'react-native-syllabus.html': 'syllabus.html',
        'react-native-course-fees.html': 'fees.html',
        'react-native-interview-questions.html': 'interview-questions.html',
        'react-native-roadmap.html': 'roadmap.html',
        'react-native-project-ideas.html': 'projects.html',
        'beginner-to-react-native-roadmap.html': 'beginner.html',
        'react-native-vs-flutter.html': 'comparison.html',
    },
    'software-architect': {
        'software-architect-training.html': 'index.html',
        'software-architect-syllabus.html': 'syllabus.html',
        'software-architect-course-fees.html': 'fees.html',
        'software-architect-interview-questions.html': 'interview-questions.html',
        'software-architect-roadmap.html': 'roadmap.html',
    },
    'software-testing': {
        'software-testing-training.html': 'index.html',
        'software-testing-syllabus.html': 'syllabus.html',
        'software-testing-course-fees.html': 'fees.html',
        'software-testing-interview-questions.html': 'interview-questions.html',
        'software-testing-roadmap.html': 'roadmap.html',
        'jenkins-vs-github-actions.html': 'comparison.html',
    }
}

# Build global old_file -> (slug, new_sub_file) reverse lookup
OLD_TO_NEW = {}
for slug, map_dict in COURSE_MAPPINGS.items():
    for old_file, new_sub_file in map_dict.items():
        if os.path.exists(old_file):
            OLD_TO_NEW[old_file] = (slug, new_sub_file)

print(f"Total existing root files to move: {len(OLD_TO_NEW)}")

# Helper to rewrite HTML content for moved course files
def process_moved_course_html(content, slug, new_sub_file, existing_sub_files_for_slug):
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Update Asset links (css/, images/, js/, favicon.ico, site.webmanifest)
    for tag in soup.find_all(['link', 'script', 'img', 'a', 'source']):
        # href
        if tag.has_attr('href'):
            href = tag['href']
            if href.startswith('css/'):
                tag['href'] = '../../' + href
            elif href.startswith('images/'):
                tag['href'] = '../../' + href
            elif href.startswith('js/'):
                tag['href'] = '../../' + href
            elif href == 'favicon.ico':
                tag['href'] = '../../favicon.ico'
            elif href == 'site.webmanifest':
                tag['href'] = '../../site.webmanifest'
        # src
        if tag.has_attr('src'):
            src = tag['src']
            if src.startswith('css/'):
                tag['src'] = '../../' + src
            elif src.startswith('images/'):
                tag['src'] = '../../' + src
            elif src.startswith('js/'):
                tag['src'] = '../../' + src
    
    # Also fix inline style background-image urls e.g., url('images/...') or url("images/...")
    html_str = str(soup)
    html_str = re.sub(r'url\(([\'"])?images/', r'url(\1../../images/', html_str)
    html_str = re.sub(r'url\(([\'"])?css/', r'url(\1../../css/', html_str)
    
    # Re-parse soup after regex edit if needed, or work with soup
    soup = BeautifulSoup(html_str, 'html.parser')
    
    # 2. Update Meta Tags (canonical and og:url)
    target_path = f"courses/{slug}/" if new_sub_file == 'index.html' else f"courses/{slug}/{new_sub_file}"
    full_url = f"{BASE_URL}/{target_path}"
    
    canonical = soup.find('link', rel='canonical')
    if canonical:
        canonical['href'] = full_url
    else:
        new_tag = soup.new_tag('link', rel='canonical', href=full_url)
        if soup.head: soup.head.append(new_tag)
        
    og_url = soup.find('meta', property='og:url')
    if og_url:
        og_url['content'] = full_url
        
    # 3. Update Course Navigation Tabs inside course-tabs-container / course-tabs-inner
    tab_container = soup.find(class_=re.compile(r'course-tabs|sub-nav', re.I))
    if tab_container:
        for a in tab_container.find_all('a', href=True):
            href = a['href']
            # If href matched an old root file belonging to this course
            if href in COURSE_MAPPINGS[slug]:
                target_sub = COURSE_MAPPINGS[slug][href]
                if target_sub in existing_sub_files_for_slug:
                    a['href'] = target_sub
                else:
                    # Target sub-file does NOT exist, remove/hide CTA link
                    a.decompose()
            elif href.endswith('.html') and not href.startswith('http'):
                # Check if it points to another moved course file or root file
                if href in OLD_TO_NEW:
                    other_slug, other_sub = OLD_TO_NEW[href]
                    a['href'] = f"../{other_slug}/{other_sub}"
                else:
                    # Root-level html file link
                    a['href'] = f"../../{href}"
                    
    # 4. Update all other <a> links in body (e.g. Header nav, Footer, Hero, CTA)
    for a in soup.find_all('a', href=True):
        href = a['href']
        # ignore tabs container as we already handled it
        if a.parent and a.parent.get('class') and any('tab' in c for c in a.parent.get('class')):
            continue
        if href in OLD_TO_NEW:
            other_slug, other_sub = OLD_TO_NEW[href]
            if other_slug == slug:
                a['href'] = other_sub
            else:
                a['href'] = f"../{other_slug}/{other_sub}"
        elif href.endswith('.html') and not href.startswith('http') and not href.startswith('#') and not href.startswith('../'):
            a['href'] = f"../../{href}"

    # 5. Update Breadcrumb Schema.org JSON-LD
    course_name = slug.replace('-', ' ').title().replace('Ai Ml', 'AI & ML').replace('Power Bi', 'Power BI')
    page_name = new_sub_file.replace('.html', '').replace('-', ' ').title()
    
    for script in soup.find_all('script', type='application/ld+json'):
        if script.string and 'BreadcrumbList' in script.string:
            items_json = f"""{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "{BASE_URL}/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Courses",
      "item": "{BASE_URL}/courses/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{course_name}",
      "item": "{BASE_URL}/courses/{slug}/"
    }}{f''',
    {{
      "@type": "ListItem",
      "position": 4,
      "name": "{page_name}",
      "item": "{full_url}"
    }}''' if new_sub_file != 'index.html' else ''}
  ]
}}"""
            script.string = items_json

    return str(soup)


def main():
    # Phase 1: Move & Process Course Files
    print("--- Phase 1: Moving & Updating Course HTML Files ---")
    for slug, map_dict in COURSE_MAPPINGS.items():
        dir_path = os.path.join('courses', slug)
        os.makedirs(dir_path, exist_ok=True)
        
        # determine existing target sub-files for this course
        existing_sub_files = set([new_sub for old_f, new_sub in map_dict.items() if os.path.exists(old_f)])
        
        for old_file, new_sub_file in map_dict.items():
            if not os.path.exists(old_file):
                print(f"Skipping non-existent file: {old_file}")
                continue
            
            with open(old_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            processed_content = process_moved_course_html(content, slug, new_sub_file, existing_sub_files)
            
            target_file_path = os.path.join(dir_path, new_sub_file)
            with open(target_file_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
                
            print(f"Moved {old_file} -> {target_file_path}")

    # Phase 2: Delete Original Root Files
    print("\n--- Phase 2: Removing Original Root HTML Files ---")
    for old_file in OLD_TO_NEW.keys():
        if os.path.exists(old_file):
            os.remove(old_file)
            print(f"Deleted root file: {old_file}")

    # Phase 3: Update Site-wide Links in Remaining HTML Files
    print("\n--- Phase 3: Updating Site-Wide Navigation & Links ---")
    all_remaining_html = glob.glob('**/*.html', recursive=True)
    
    for file_path in all_remaining_html:
        # compute depth relative to root
        norm_path = file_path.replace('\\', '/')
        depth = norm_path.count('/')
        prefix = '../' * depth
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        soup = BeautifulSoup(content, 'html.parser')
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Clean href of trailing hash or params if matching old root files
            clean_href = href.split('#')[0].split('?')[0]
            if clean_href in OLD_TO_NEW:
                slug, new_sub = OLD_TO_NEW[clean_href]
                new_target = f"{prefix}courses/{slug}/" if new_sub == 'index.html' else f"{prefix}courses/{slug}/{new_sub}"
                # preserve hash/params if any
                suffix = href[len(clean_href):]
                a['href'] = new_target + suffix
                modified = True
                
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated site-wide links in: {file_path}")

    # Phase 4: Update sitemap.xml
    print("\n--- Phase 4: Updating sitemap.xml ---")
    if os.path.exists('sitemap.xml'):
        with open('sitemap.xml', 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
            
        # Replace old root URLs with new course URLs
        for old_file, (slug, new_sub) in OLD_TO_NEW.items():
            old_url = f"{BASE_URL}/{old_file}"
            new_url = f"{BASE_URL}/courses/{slug}/" if new_sub == 'index.html' else f"{BASE_URL}/courses/{slug}/{new_sub}"
            sitemap_content = sitemap_content.replace(old_url, new_url)
            
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        print("Updated sitemap.xml successfully.")

    # Phase 5: Update llms.txt and llms-full.txt
    print("\n--- Phase 5: Updating llms.txt & llms-full.txt ---")
    for txt_file in ['llms.txt', 'llms-full.txt']:
        if os.path.exists(txt_file):
            with open(txt_file, 'r', encoding='utf-8') as f:
                txt_content = f.read()
                
            for old_file, (slug, new_sub) in OLD_TO_NEW.items():
                old_url = f"{BASE_URL}/{old_file}"
                new_url = f"{BASE_URL}/courses/{slug}/" if new_sub == 'index.html' else f"{BASE_URL}/courses/{slug}/{new_sub}"
                txt_content = txt_content.replace(old_url, new_url)
                
                old_rel = old_file
                new_rel = f"courses/{slug}/" if new_sub == 'index.html' else f"courses/{slug}/{new_sub}"
                txt_content = txt_content.replace(old_rel, new_rel)
                
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(txt_content)
            print(f"Updated {txt_file} successfully.")

    print("\n=== Course Restructuring Complete ===")

if __name__ == '__main__':
    main()
