import os
import json
import re

def enrich_courses():
    json_path = os.path.join("src", "courses.json")
    if not os.path.exists(json_path):
        print("courses.json not found!")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        courses = json.load(f)

    keyword_maps = {
        "java-fullstack-training": {
            "seo_title": "Java Fullstack Course & Coding Training in Pune | CACTS",
            "meta_description": "Master Java Fullstack coding & Spring Boot development in Pune with CACTS. 1-to-1 developer coaching, real project internship & 100% technical competence.",
            "h1": "Java Fullstack Course & Development Training in Pune",
            "h2": "Hands-On Coding & Development Bootcamp: Build Spring Boot, React & SQL microservices under 1-to-1 coaching with a guaranteed internship project near you in Pune."
        },
        "full-stack-training": {
            "seo_title": "Full Stack MERN Web Development Course in Pune | CACTS",
            "meta_description": "Join MERN Full Stack coding classes & web development training in Pune. Hands-on coding bootcamp, live project internship, & career readiness near you.",
            "h1": "MERN Full Stack Web Development Course in Pune",
            "h2": "Professional Web Development & Coding Bootcamp: Build React & Node.js web apps with guaranteed live project internship and technical readiness near you."
        },
        "python-training": {
            "seo_title": "Python Developer Course & Coding Classes in Pune | CACTS",
            "meta_description": "Premier Python programming course & development training in Pune. 1-to-1 coding coaching, Django/Flask projects, live internship & technical competence.",
            "h1": "Python Development Course & Coding Training in Pune",
            "h2": "Practical Python Coding Bootcamp: Learn backend development, REST APIs & data scripting with live company project internship and career career readiness near you."
        },
        "ai-ml-training": {
            "seo_title": "AI & Machine Learning Engineering Course in Pune | CACTS",
            "meta_description": "Advanced AI & ML course with Python coding in Pune. Master PyTorch, LLMs & Deep Learning with 1-to-1 coaching, live project internship & technical readiness.",
            "h1": "AI & Machine Learning Engineer Course in Pune",
            "h2": "Advanced AI Coding & Development Bootcamp: Build neural networks & LLM applications under 1-to-1 developer coaching with real-world internship project."
        },
        "data-science-training": {
            "seo_title": "Data Science & Analytics Course in Pune | CACTS Training",
            "meta_description": "Top Data Science course & Python analytics coaching near you in Pune. Learn SQL, Machine Learning, Power BI with live company internship & placement guidance.",
            "h1": "Data Science & Machine Learning Course in Pune",
            "h2": "Hands-On Analytics & Data Coding Bootcamp: Master pandas, ML algorithms & predictive modeling with real-world internship and career readiness."
        },
        "data-engineering-training": {
            "seo_title": "Data Engineering Course & ETL Training in Pune | CACTS",
            "meta_description": "Become a Data Engineer in Pune. Learn SQL, Python ETL, Apache Spark & Cloud Pipelines with 1-to-1 coding coaching, live internship project & technical verification.",
            "h1": "Data Engineering & Big Data Course in Pune",
            "h2": "Production Data Pipeline & Coding Bootcamp: Build PySpark ETL pipelines & cloud data lakes with real project internship and career technical competence."
        },
        "devops-training": {
            "seo_title": "DevOps & Cloud Engineering Course in Pune | CACTS Training",
            "meta_description": "Master DevOps & Cloud infrastructure in Pune. Docker, Kubernetes, Jenkins, Terraform & AWS coding bootcamp with 1-to-1 coaching & internship placement.",
            "h1": "DevOps & Cloud Engineering Course in Pune",
            "h2": "Automated Cloud & DevOps Development Bootcamp: Deploy CI/CD pipelines & Docker clusters with guaranteed live project internship and technical competence near you."
        },
        "cloud-training": {
            "seo_title": "AWS Cloud Architecture & Systems Course in Pune | CACTS",
            "meta_description": "AWS & Multi-Cloud engineering course in Pune. Learn EC2, S3, IAM, Serverless & Terraform with hands-on coding lab, live internship & career readiness.",
            "h1": "AWS Cloud Architecture & Systems Course in Pune",
            "h2": "Enterprise Cloud Systems Development Bootcamp: Architect scalable AWS cloud infrastructure with real-world company project internship near you."
        },
        "power-bi-training": {
            "seo_title": "Power BI & Business Analytics Course in Pune | CACTS",
            "meta_description": "Best Power BI analytics course near you in Pune. Learn DAX modeling, SQL & dashboard design with 1-to-1 coaching, live internship & technical readiness.",
            "h1": "Power BI Analytics & Dashboard Course in Pune",
            "h2": "Business Intelligence & Data Visualization Bootcamp: Design enterprise Power BI dashboards with real company dataset internships and technical verification."
        },
        "react-js-training": {
            "seo_title": "React JS Frontend Development Course in Pune | CACTS",
            "meta_description": "Master React 18 & JavaScript frontend coding in Pune. 1-to-1 web development training, Redux Toolkit, live company internship & technical readiness.",
            "h1": "React JS Frontend Coding Course in Pune",
            "h2": "Modern Frontend Development & React Bootcamp: Build high-performance web UIs with guaranteed live company project internship and career coaching near you."
        },
        "react-native-training": {
            "seo_title": "React Native Mobile App Development Course in Pune | CACTS",
            "meta_description": "Learn React Native mobile app development in Pune. Build cross-platform iOS & Android apps with 1-to-1 coding coaching, live internship & technical competence.",
            "h1": "React Native Mobile App Development Course in Pune",
            "h2": "Cross-Platform Mobile Coding & Development Bootcamp: Ship iOS & Android mobile apps with real company project internship near you in Pune."
        },
        "software-testing-training": {
            "seo_title": "Software Testing & Automation Course in Pune | CACTS",
            "meta_description": "Best Software Testing course near you in Pune. Learn Manual testing, Selenium Java automation, API testing with live internship project & 100% technical competence.",
            "h1": "Software Testing & QA Automation Course in Pune",
            "h2": "QA Automation & Test Development Bootcamp: Master Selenium, JUnit & REST Assured with real company staging server internship near you in Pune."
        },
        "cybersecurity-training": {
            "seo_title": "Cybersecurity & Ethical Hacking Course in Pune | CACTS",
            "meta_description": "Cybersecurity & SOC Analyst training course in Pune. Learn network security, penetration testing & SIEM with 1-to-1 coaching, live internship & technical competence.",
            "h1": "Cybersecurity Operations & Defense Course in Pune",
            "h2": "Information Security & SOC Analyst Development Bootcamp: Master vulnerability assessment & incident response with live company project internship."
        },
        "blockchain-training": {
            "seo_title": "Blockchain & Smart Contract Developer Course in Pune | CACTS",
            "meta_description": "Learn Blockchain development in Pune. Master Solidity, Ethereum & Web3.js coding with 1-to-1 coaching, live company project internship & technical readiness.",
            "h1": "Blockchain Development & Web3 Course in Pune",
            "h2": "Decentralized Smart Contract Coding Bootcamp: Build dApps & ERC-20 tokens on Ethereum testnets with live company project internship support near you."
        },
        "software-architect-training": {
            "seo_title": "Software Architect & Systems Design Course in Pune | CACTS",
            "meta_description": "Advanced Software Architect & High-Scale System Design course in Pune. Master microservices, distributed systems & clean coding with 1-to-1 senior coaching.",
            "h1": "Software Architecture & Systems Design Course in Pune",
            "h2": "Senior System Design & Enterprise Architecture Bootcamp: Design fault-tolerant microservices & cloud systems with live project internship & career readiness."
        }
    }

    for c in courses:
        slug = c.get("slug")
        if slug in keyword_maps:
            c["seo_title"] = keyword_maps[slug]["seo_title"]
            c["meta_description"] = keyword_maps[slug]["meta_description"]
            c["h1"] = keyword_maps[slug]["h1"]
            c["h2"] = keyword_maps[slug]["h2"]
            
            # Enrich overview paragraph organically
            if "course" not in c["overview"].lower():
                c["overview"] = f"Looking for a practical software development course or IT training near you in Pune? {c['overview']} Our hands-on coding bootcamp combines 1-to-1 developer coaching with guaranteed live company project internships and 100% dedicated technical readiness."
            elif "internship" not in c["overview"].lower():
                c["overview"] += " Every course includes hands-on coding labs, live project internships on active staging servers, and 1-to-1 career career readiness."

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(courses, f, indent=2)

    print("Successfully enriched courses.json with high-intent local search keywords!")

if __name__ == "__main__":
    enrich_courses()
