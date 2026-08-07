import os
import glob
import re
from bs4 import BeautifulSoup

BASE_URL = "https://cactslearn.github.io"

def build_complete_target_map():
    # Map from old flat basename OR full relative path to new absolute repo path
    target_map = {}

    # 1. Core Root Files
    for rf in ['index.html', 'about.html', 'contact.html', 'reviews.html', 'faqs.html', 'sitemap.html', 'privacy-policy.html', 'terms-conditions.html', '404.html']:
        target_map[rf] = rf

    # 2. Courses Mapping
    COURSES = [
        'ai-ml', 'blockchain', 'cloud', 'cybersecurity', 'data-engineering',
        'data-science', 'devops', 'full-stack', 'java-fullstack', 'power-bi',
        'python', 'react-js', 'react-native', 'software-architect', 'software-testing'
    ]

    for c in COURSES:
        # Overview / Main index
        target_map[f"{c}-training.html"] = f"courses/{c}/index.html"
        target_map[f"{c}-course.html"] = f"courses/{c}/index.html"
        target_map[f"{c}.html"] = f"courses/{c}/index.html"
        target_map[f"{c}-certification.html"] = f"courses/{c}/index.html"

        # Specific subpages
        target_map[f"{c}-syllabus.html"] = f"courses/{c}/syllabus.html"
        target_map[f"{c}-course-syllabus.html"] = f"courses/{c}/syllabus.html"

        target_map[f"{c}-course-fees.html"] = f"courses/{c}/fees.html"
        target_map[f"{c}-fees.html"] = f"courses/{c}/fees.html"

        target_map[f"{c}-interview-questions.html"] = f"courses/{c}/interview-questions.html"
        target_map[f"{c}-roadmap.html"] = f"courses/{c}/roadmap.html"

        target_map[f"{c}-project-ideas.html"] = f"courses/{c}/projects.html"
        target_map[f"{c}-projects.html"] = f"courses/{c}/projects.html"

        target_map[f"{c}-beginner-guide.html"] = f"courses/{c}/beginner.html"
        target_map[f"{c}-beginner.html"] = f"courses/{c}/beginner.html"

        target_map[f"best-{c}-certifications.html"] = f"courses/{c}/certifications.html"
        target_map[f"{c}-certifications.html"] = f"courses/{c}/certifications.html"

        target_map[f"{c}-comparison.html"] = f"courses/{c}/comparison.html"

    # Specific Course Comparison Overrides
    target_map['ai-vs-ml-vs-dl-comparison.html'] = 'courses/ai-ml/comparison.html'
    target_map['python-vs-java-vs-cpp-comparison.html'] = 'courses/python/comparison.html'
    target_map['java-vs-python-fullstack-comparison.html'] = 'courses/java-fullstack/comparison.html'
    target_map['react-js-vs-angular-vs-vue-comparison.html'] = 'courses/react-js/comparison.html'
    target_map['react-native-vs-flutter-comparison.html'] = 'courses/react-native/comparison.html'
    target_map['power-bi-vs-tableau-vs-excel-comparison.html'] = 'courses/power-bi/comparison.html'
    target_map['software-testing-manual-vs-automation-comparison.html'] = 'courses/software-testing/comparison.html'
    target_map['software-architect-vs-senior-developer-comparison.html'] = 'courses/software-architect/comparison.html'
    target_map['one-to-one-software-training.html'] = 'courses/index.html'
    target_map['one-to-one-software'] = 'courses/index.html'

    # 3. Locations Mapping
    if os.path.exists('locations'):
        for lf in glob.glob('locations/*.html'):
            lf_norm = lf.replace('\\', '/')
            base = os.path.basename(lf_norm)
            loc_slug = base.replace('.html', '')
            target_map[base] = lf_norm
            target_map[f"software-training-institute-{loc_slug}.html"] = lf_norm

        target_map['shivane.html'] = 'locations/index.html'
        target_map['software-training-institute-shivane.html'] = 'locations/index.html'

    # 4. Guides Mapping
    if os.path.exists('guides'):
        for gf in glob.glob('guides/*.html'):
            gf_norm = gf.replace('\\', '/')
            base = os.path.basename(gf_norm)
            target_map[base] = gf_norm

    # 5. Tools Mapping
    if os.path.exists('tools'):
        for tf in glob.glob('tools/*.html'):
            tf_norm = tf.replace('\\', '/')
            base = os.path.basename(tf_norm)
            target_map[base] = tf_norm

    # 6. Comparisons Mapping
    if os.path.exists('comparisons'):
        for cf in glob.glob('comparisons/*.html'):
            cf_norm = cf.replace('\\', '/')
            base = os.path.basename(cf_norm)
            target_map[base] = cf_norm

    # 7. Showcase Mapping
    if os.path.exists('showcase'):
        for sf in glob.glob('showcase/*.html'):
            sf_norm = sf.replace('\\', '/')
            base = os.path.basename(sf_norm)
            target_map[base] = sf_norm

    # 8. Jobs Mapping
    if os.path.exists('jobs'):
        for jf in glob.glob('jobs/*.html'):
            jf_norm = jf.replace('\\', '/')
            base = os.path.basename(jf_norm)
            target_map[base] = jf_norm
        target_map['careers.html'] = 'jobs/index.html'

    return target_map


def compute_relative_path(source_file, target_file):
    source_dir = os.path.dirname(source_file.replace('\\', '/'))
    target_norm = target_file.replace('\\', '/')

    if not source_dir:
        return target_norm

    rel = os.path.relpath(target_norm, source_dir).replace('\\', '/')
    return rel


def fix_all_hrefs():
    target_map = build_complete_target_map()
    all_html_files = [f.replace('\\', '/') for f in glob.glob('**/*.html', recursive=True) if not f.replace('\\', '/').startswith('src/')]
    all_existing_files = set(all_html_files)

    for f in list(all_existing_files):
        if f.endswith('/index.html'):
            all_existing_files.add(f[:-11] + '/')
            all_existing_files.add(f[:-10])

    print(f"=== Auditing and Fixing Hrefs Across {len(all_html_files)} HTML Files ===")

    fixed_count = 0
    links_fixed_total = 0

    for fpath in all_html_files:
        dir_name = os.path.dirname(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        modified = False

        for a in soup.find_all('a', href=True):
            href = a['href']
            clean_href = href.split('#')[0].split('?')[0]
            if not clean_href or clean_href.startswith('http://') or clean_href.startswith('https://') or clean_href.startswith('mailto:') or clean_href.startswith('tel:'):
                continue

            if clean_href.startswith('/'):
                resolved = clean_href.lstrip('/')
            elif dir_name:
                resolved = os.path.normpath(os.path.join(dir_name, clean_href)).replace('\\', '/')
            else:
                resolved = clean_href

            if os.path.isdir(resolved):
                resolved_file = os.path.join(resolved, 'index.html').replace('\\', '/')
            else:
                resolved_file = resolved

            # If resolved file does NOT exist, attempt fixing using target_map
            if resolved_file not in all_existing_files and not os.path.exists(resolved_file):
                base = os.path.basename(clean_href)
                if base in target_map:
                    new_target = target_map[base]
                    new_rel = compute_relative_path(fpath, new_target)
                    suffix = href[len(clean_href):]
                    a['href'] = new_rel + suffix
                    modified = True
                    links_fixed_total += 1
                    print(f"  In {fpath}: '{href}' -> '{new_rel + suffix}'")
                else:
                    print(f"  UNRESOLVED in {fpath}: href='{href}' (base: '{base}')")

        if modified:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            fixed_count += 1

    print(f"\nFixed {links_fixed_total} broken/old flat links across {fixed_count} HTML files.")

if __name__ == '__main__':
    fix_all_hrefs()
