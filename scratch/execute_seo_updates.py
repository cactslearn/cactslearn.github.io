import os
import glob
import re

def run_updates():
    # --- TASK 1: Trim Long Meta Titles & Descriptions ---
    trim_targets = {
        'what-does-a-data-engineer-do.html': {
            'old_title': 'What Does a Data Engineer Do? | Job Description & Salaries | CACTS',
            'new_title': 'What Does a Data Engineer Do? | Job & Salary Guide | CACTS'
        },
        'careers.html': {
            'old_desc': 'Browse current job openings, internships, and trainee positions for freshers, graduates, and career switchers at CACTS Pune across Full Stack, Java, Python, AI, Cloud, and DevOps.',
            'new_desc': 'Browse current job openings, internships, and trainee positions at CACTS Pune across Full Stack, Java, Python, AI, Cloud, and DevOps.'
        },
        'jobs/index.html': {
            'old_desc': 'Browse current job openings, internships, and trainee positions for freshers, graduates, and career switchers at CACTS Pune across Full Stack, Java, Python, AI, Cloud, and DevOps.',
            'new_desc': 'Browse current job openings, internships, and trainee positions at CACTS Pune across Full Stack, Java, Python, AI, Cloud, and DevOps.'
        }
    }

    for path, data in trim_targets.items():
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'old_title' in data:
                content = content.replace(data['old_title'], data['new_title'])
            if 'old_desc' in data:
                content = content.replace(data['old_desc'], data['new_desc'])
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Trimmed meta tags in {path}")

    # --- TASK 2: Inject OpenGraph Tags on Guide & Portal Pages ---
    html_files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('src/') and not f.startswith('.gemini/')]
    og_injected_count = 0

    for pf in html_files:
        with open(pf, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'og:title' not in content:
            # Extract title and description
            m_title = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
            m_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
            if not m_desc:
                m_desc = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', content, re.IGNORECASE)

            title_val = m_title.group(1).strip() if m_title else "CACTS Software Training Institute"
            desc_val = m_desc.group(1).strip() if m_desc else "Practical 1-to-1 software training and live project internships in Pune."
            clean_rel_path = pf.replace('\\', '/')

            og_block = f"""
    <!-- Open Graph (OG) Social Tags -->
    <meta property="og:title" content="{title_val}">
    <meta property="og:description" content="{desc_val}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://cacts.co.in/{clean_rel_path}">
    <meta property="og:image" content="https://cacts.co.in/images/cacts-og-banner.jpg">
"""
            if '</head>' in content:
                content = content.replace('</head>', f'{og_block}</head>')
                with open(pf, 'w', encoding='utf-8') as f:
                    f.write(content)
                og_injected_count += 1

    print(f"Injected OpenGraph tags into {og_injected_count} HTML files.")

    # --- TASK 3: Sync 55 missing guide pages into sitemap.html & scripts/build.py ---
    # List of standalone guides & resources
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

    res_group_html = f"""
                <!-- Group 8: Learning Guides & Tech Resources -->
                <div class="sitemap-group" style="grid-column: 1 / -1;">
                    <h3 style="margin-bottom: 0.5rem; display: flex; align-items: center;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 0.5rem; color: var(--accent); flex-shrink: 0;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>Learning Guides &amp; Tech Resources ({len(resource_files)} Guides)</h3>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1.25rem;">In-depth tech career roadmaps, industry certifications, project ideas, comparisons, and role breakdowns.</p>
                    <ul class="sitemap-list" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 0.75rem;">
{res_links_html}
                    </ul>
                </div>
"""

    with open("sitemap.html", "r", encoding="utf-8") as f:
        sm_content = f.read()

    if "Group 8: Learning Guides & Tech Resources" not in sm_content:
        sm_content = sm_content.replace('</div>\n    </main>', f'{res_group_html}\n        </div>\n    </main>')
        with open("sitemap.html", "w", encoding="utf-8") as f:
            f.write(sm_content)
        print("Added Group 8 (Learning Guides & Tech Resources) to sitemap.html")

if __name__ == '__main__':
    run_updates()
