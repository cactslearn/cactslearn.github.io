# subpages_content.py - Dynamic Content Data for CACTS Course Split Pages

SUBPAGES_DATA = {
    "java-full-stack-developer-training": {
        "syllabus_prerequisites": "Basic logical thinking and computer operations. No prior programming background is required, as we start from absolute variables and loops.",
        "syllabus_projects": [
            "Project 1: Custom Library Management CLI app using Collections & JVM files.",
            "Project 2: Multi-threaded Banking Transaction Simulator with JDBC connection pool.",
            "Project 3: E-Commerce REST API Engine incorporating Spring Security & JWT keys.",
            "Project 4: Collaborative Live Internship Platform deployed with React Axios integration."
        ],
        "syllabus_tools": ["IntelliJ IDEA", "Apache Maven", "MySQL Workbench", "Postman API client", "Git & GitHub", "Docker Containers"],
        "syllabus_faqs": [
            {"q": "Can I customize the Java syllabus based on my college project?", "a": "Yes. Since our training is strictly 1-to-1, your mentor can customize the final module projects to match your engineering graduation project requirements."},
            {"q": "Do you cover Java 21 or Java 17?", "a": "We teach Java 17/21 LTS versions, focusing on modern language features like Record types, pattern matching, and virtual threads."}
        ],
        "fees_structure": "The Java Full Stack Developer Training fee is ₹19,999 (all-inclusive). You can split this into 2 equal monthly installments of ₹10,000. We offer a 5% discount (₹18,999 final fee) for one-time upfront payments.",
        "fees_comparison": {
            "typical_pune_fees": "₹45,000 - ₹60,000",
            "pune_batch_size": "30 to 50 students",
            "cacts_value": "Strictly individual 1-to-1 virtual coaching, screensharing, and direct developer code reviews at less than half the market rate."
        },
        "fees_faqs": [
            {"q": "Are there any hidden lab or exam fees at CACTS?", "a": "No, the ₹19,999 fee is all-inclusive. It covers all 1-to-1 mentorship, live project staging environments, and career training support."},
            {"q": "What happens if I miss a scheduled 1-to-1 session?", "a": "Since it is individual training, there are no missed classes. We simply reschedule the session to your next available slot without any penalty."}
        ],
        "interview_questions": [
            {"q": "What is the difference between HashMap and ConcurrentHashMap in Java?", "a": "HashMap is not thread-safe and can cause infinite loops during rehashing under multi-threaded operations. ConcurrentHashMap is thread-safe, utilizing lock striping or bucket-level locking, which allows concurrent reads and safe writes without blocking the entire table."},
            {"q": "How does Spring Boot resolve dependency injection?", "a": "Spring Boot uses an Inversion of Control (IoC) container. Beans are scanned via @ComponentScan and registered. Dependencies are resolved using constructor injection, setter injection, or field injection marked with @Autowired at startup."},
            {"q": "Explain the life cycle of a React hook like useEffect.", "a": "useEffect runs after the component renders. If the dependency array is empty, it runs once. If it has dependencies, it runs whenever those values change. The return function acts as a cleanup phase, running before the component unmounts or before the effect runs again."},
            {"q": "What is Hibernate Lazy Loading and how do you prevent LazyInitializationException?", "a": "Lazy loading fetches child entities from the database only when accessed. If the Hibernate session is closed, accessing them throws LazyInitializationException. To resolve this, you can use eager fetching, execute JOIN FETCH queries, or keep the session open during the rendering lifecycle."},
            {"q": "What are the common HTTP response codes used in Spring Boot REST controllers?", "a": "Common codes include 200 OK (successful request), 201 Created (resource successfully generated), 400 Bad Request (invalid payload parameters), 401 Unauthorized (invalid JWT tokens), 404 Not Found (resource missing), and 500 Internal Server Error."}
        ],
        "interview_faqs": [
            {"q": "Do you conduct mock interviews during this training?", "a": "Yes. You get 3 dedicated 1-to-1 mock interview sessions with active corporate developers to review your coding logic, resume project highlights, and communications."},
            {"q": "Will I get help building my technical resume?", "a": "Yes. We help you draft a resume that highlights your real Git commits, spring boot APIs, and internship project details rather than dry copy-pasted bullet points."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Java Object-Oriented Foundations", "duration": "4 Weeks", "skills": "Core Java, JVM memory structure, Generic Collections, File I/O", "project": "CLI Database Simulation app"},
            {"phase": "Phase 2", "title": "Databases & Web APIs", "duration": "4 Weeks", "skills": "MySQL Workbench, SQL Joins, JDBC, Servlets, Hibernate ORM mappings", "project": "Relational Inventory Tracker backend"},
            {"phase": "Phase 3", "title": "Spring Boot & RESTful APIs", "duration": "4 Weeks", "skills": "Spring DI/IoC, Spring Boot MVC, JPA Repositories, JWT security", "project": "Secure User Authentication server"},
            {"phase": "Phase 4", "title": "React UI Integration & Live Deployment", "duration": "4 Weeks", "skills": "React hooks, state routers, Axios calls, Git merge branches, Staging deploy", "project": "Deploying Full-Stack app on Live Internship"}
        ],
        "roadmap_faqs": [
            {"q": "What is the average starting salary for a Java Full Stack developer in Pune?", "a": "As of 2026, entry-level salaries in Pune for full-stack developers range from ₹3.6 LPA to ₹5.5 LPA. Candidates with active company internship code commits can negotiate higher packages."},
            {"q": "How long does it take to get job-ready in Java Full Stack?", "a": "On average, it takes 16 weeks of dedicated 1-to-1 training and active coding (12-15 hours/week) to build production-ready projects and master interview topics."}
        ]
    },
    "full-stack-development-training": {
        "syllabus_prerequisites": "No programming knowledge is required. You should know basic web browsing and have a passion for building websites.",
        "syllabus_projects": [
            "Project 1: Responsive Restaurant Landing page using HTML5 Grid & Flexbox.",
            "Project 2: JavaScript Dynamic Task Manager using Web Storage & Fetch APIs.",
            "Project 3: Collaborative Chat App using Express, Node.js and MongoDB models.",
            "Project 4: Complete MERN Dashboard deployed on Netlify / Render pipelines."
        ],
        "syllabus_tools": ["VS Code", "Node Package Manager", "Postman", "MongoDB Atlas", "Git & GitHub", "Netlify / Render"],
        "syllabus_faqs": [
            {"q": "Is the MERN stack better than PHP or Java for freshers?", "a": "MERN is highly popular for startup roles in Pune due to JavaScript continuity (same language on frontend and backend). It is excellent for rapid prototyping and modern reactive UI engineering."},
            {"q": "Do we cover TypeScript in the syllabus?", "a": "Yes, we cover TypeScript integration with React.js in the final front-end module."}
        ],
        "fees_structure": "The Full Stack (MERN) Development Training tuition is ₹17,999 (all-inclusive). You can pay in 2 installments of ₹9,000. Upfront full payment offers a 5% discount (₹17,099 final fee).",
        "fees_comparison": {
            "typical_pune_fees": "₹40,000 - ₹55,000",
            "pune_batch_size": "35 to 50 students",
            "cacts_value": "1-to-1 private virtual trainer, no crowded batches, and live staging deploy checks at nearly 40% of standard institute pricing."
        },
        "fees_faqs": [
            {"q": "Is there a refund policy if I discontinue the training?", "a": "We offer a 100% refund after your first demo class if you choose not to proceed. Once formal training modules begin, fees are non-refundable but can be paused and resumed anytime."},
            {"q": "Do you accept credit cards and monthly UPI?", "a": "Yes, we accept UPI, Google Pay, NetBanking, and credit card payments."}
        ],
        "interview_questions": [
            {"q": "Explain Event Loop in Node.js.", "a": "Node.js runs on a single thread. The Event Loop delegates asynchronous tasks (like disk reads or database queries) to the system kernel or thread pool. When completed, callbacks are queued and executed sequentially in phases (timers, pending callbacks, poll, check, close callbacks)."},
            {"q": "What is the difference between Virtual DOM and Real DOM in React?", "a": "The Real DOM updates elements directly, causing expensive repaints. React's Virtual DOM is a lightweight memory representation. When state changes, React updates the Virtual DOM, performs 'diffing' to compare it with the previous state, and updates only the changed nodes in the Real DOM (reconciliation)."},
            {"q": "How does MongoDB store data and what is a NoSQL document?", "a": "MongoDB stores data in flexible BSON (Binary JSON) documents. Unlike relational rows, documents can contain nested sub-documents or arrays, allowing hierarchical data mapping without rigid schema constraints or complex joins."},
            {"q": "What is CORS error and how do you resolve it in Express?", "a": "CORS (Cross-Origin Resource Sharing) prevents clients from accessing APIs hosted on different domains. To resolve this, you must configure the CORS middleware in Express to explicitly allow incoming headers from your frontend domain (e.g. app.use(cors({ origin: 'http://localhost:3000' })))."},
            {"q": "What is the difference between state and props in React?", "a": "State is internal mutable data managed within the component itself. Props are immutable read-only parameters passed down from a parent component."}
        ],
        "interview_faqs": [
            {"q": "What kind of interview preparation is provided?", "a": "We provide mock interviews, technical review sheets, resume alignment, and a review of your GitHub project repositories to make sure your code stands out."},
            {"q": "How many recruiters contact CACTS students?", "a": "We share your verified project portfolio links directly with local hiring partners and recruiters in Pune tech zones."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Semantic Frontend Layouts", "duration": "4 Weeks", "skills": "HTML5, CSS3 Grid, Flexbox, Vanilla JS, DOM, Fetch APIs", "project": "Responsive Corporate Web Portal"},
            {"phase": "Phase 2", "title": "React.js Component Architecture", "duration": "4 Weeks", "skills": "React Components, State hooks, Props, Router, Axios APIs", "project": "Dynamic Product Catalog App"},
            {"phase": "Phase 3", "title": "Node.js & Express API Engine", "duration": "3 Weeks", "skills": "Node loops, Express Routing, middleware, REST response JSON", "project": "REST API Booking Engine"},
            {"phase": "Phase 4", "title": "NoSQL Database & Production Deploy", "duration": "3 Weeks", "skills": "MongoDB Atlas, Mongoose validation, JWT security, Git commits", "project": "Deploying Full MERN Web app on Internship"}
        ],
        "roadmap_faqs": [
            {"q": "Can a career switcher learn Web Development in 14 weeks?", "a": "Yes. Our individual 1-to-1 pacing means you don't get left behind. We make sure you write and understand every line of code before moving to backend modules."},
            {"q": "What junior roles can I apply for after completing MERN Stack?", "a": "You can apply for Junior Frontend Developer, MERN Stack Developer, JavaScript Engineer, or Associate Software Engineer positions."}
        ]
    },
    "ai-machine-learning-training": {
        "syllabus_prerequisites": "Basic Python programming concept. Linear Algebra and Calculus basics are helpful but fully covered in our math modules.",
        "syllabus_projects": [
            "Project 1: Real estate pricing predictor using Linear Regression and Scikit-Learn.",
            "Project 2: Customer Churn Classification app using Decision Trees & Random Forests.",
            "Project 3: Image Classifier using Convolutional Neural Networks (CNN) in TensorFlow.",
            "Project 4: Custom API Deployment of an NLP text classification system."
        ],
        "syllabus_tools": ["Jupyter Notebooks", "Scikit-Learn", "TensorFlow / Keras", "Pandas & NumPy", "FastAPI / Flask", "Google Colab"],
        "syllabus_faqs": [
            {"q": "Do we write pure code or use auto-ML libraries?", "a": "We teach you to write algorithms and custom Scikit-Learn pipelines from scratch. Understanding hyperparameter tuning and loss optimization is crucial for technical interviews."},
            {"q": "Is computer vision covered in the syllabus?", "a": "Yes, we cover image classification, edge detection, and basic CNN architectures using TensorFlow."}
        ],
        "fees_structure": "The AI & Machine Learning Course fee is ₹24,999 (all-inclusive). We offer an installment option of ₹12,500 × 2 months. Upfront full payment grants a 5% discount (₹23,749 total).",
        "fees_comparison": {
            "typical_pune_fees": "₹60,000 - ₹90,000",
            "pune_batch_size": "40 to 60 students",
            "cacts_value": "Personalized 1-to-1 math & code debugging sessions with a senior AI engineer at less than a third of typical institute costs."
        },
        "fees_faqs": [
            {"q": "Why is the AI/ML course priced higher than Python?", "a": "The course involves advanced mathematical concepts, deep learning configurations, and specialized neural network deployments that require longer mentor-guided laboratory hours."},
            {"q": "Are staging cloud server fees included?", "a": "Yes, we guide you to use free-tier cloud environments (like Google Colab, HuggingFace spaces, and Render) so you don't incur extra hosting costs."}
        ],
        "interview_questions": [
            {"q": "Explain the difference between L1 and L2 regularization.", "a": "L1 (Lasso) adds the absolute values of coefficients as a penalty. It leads to sparse feature matrices, effectively performing feature selection. L2 (Ridge) adds the squared values of coefficients. It shrinks weights close to zero but doesn't eliminate features entirely."},
            {"q": "What is the Overfitting problem and how do you resolve it?", "a": "Overfitting happens when a model learns noise in training data instead of general patterns, causing poor validation performance. To resolve it, you can simplify the model architecture, use cross-validation, apply regularization (L1/L2, dropout), or collect more training data."},
            {"q": "How does gradient descent work in deep learning?", "a": "Gradient descent is an optimization algorithm that minimizes the loss function. It calculates the partial derivatives (gradients) of the loss function relative to model parameters and updates weights in the opposite direction of the gradient by a step size defined by the learning rate."},
            {"q": "What is the difference between Precision and Recall?", "a": "Precision measures the proportion of true positive predictions out of all predicted positives (True Positives / (True Positives + False Positives)). Recall measures the proportion of actual positives correctly identified (True Positives / (True Positives + False Negatives))."},
            {"q": "What are activation functions and why is ReLU preferred over Sigmoid?", "a": "Activation functions introduce non-linearity into neural networks. ReLU (Rectified Linear Unit, f(x)=max(0, x)) is preferred over Sigmoid in deep networks because it solves the vanishing gradient problem, enabling faster training during backpropagation."}
        ],
        "interview_faqs": [
            {"q": "What ML portfolios will I build?", "a": "You will build 4 real-world projects, including predictive analytical servers and deep learning classifiers, complete with FastAPI endpoints committed to GitHub."},
            {"q": "Do you help with Kaggle or Hackathon prep?", "a": "Yes, your mentor can guide you through structuring data pipelines for Kaggle challenges."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Mathematical foundations & Python tools", "duration": "4 Weeks", "skills": "NumPy, Pandas, Matplotlib, linear algebra vectors, calculus optimization", "project": "Exploratory Data Analysis Report"},
            {"phase": "Phase 2", "title": "Classical Machine Learning", "duration": "4 Weeks", "skills": "Scikit-Learn, regressions, Random Forests, SVM, model metrics, pipelines", "project": "Predictive Scoring Engine API"},
            {"phase": "Phase 3", "title": "Deep Learning & Neural Nets", "duration": "4 Weeks", "skills": "TensorFlow, Keras, Perceptrons, backpropagation, CNN architectures", "project": "Image Classification Web App"},
            {"phase": "Phase 4", "title": "FastAPI Deployment & Staging", "duration": "4 Weeks", "skills": "Model pickling, FastAPI endpoints, HuggingFace pipelines, git branches", "project": "Deploying ML Microservice on Internship"}
        ],
        "roadmap_faqs": [
            {"q": "What is the starting salary for an ML Associate in Pune?", "a": "ML roles typically start between ₹4.5 LPA and ₹7 LPA in Pune. Candidates with a strong understanding of Python deployment and model API integration command premium rates."},
            {"q": "Can I learn AI/ML without learning Data Science first?", "a": "Yes. While Data Science helps, our syllabus starts with numerical data pipelines, covering all requisite statistics before jumping into ML algorithms."}
        ]
    },
    "data-science-training": {
        "syllabus_prerequisites": "Basic understanding of school-level algebra and Excel formulas. No prior database or python coding background is required.",
        "syllabus_projects": [
            "Project 1: Sales Analysis interactive dashboard built in Power BI.",
            "Project 2: Structured SQL analytical reporting on database transactions.",
            "Project 3: Descriptive & predictive analysis on hospital datasets using Python.",
            "Project 4: A/B testing analytics pipeline committed to Git."
        ],
        "syllabus_tools": ["Python (Pandas)", "SQL (MySQL)", "Power BI Desktop", "Jupyter Notebooks", "Git & GitHub", "Google Sheets"],
        "syllabus_faqs": [
            {"q": "Why do we cover both Power BI and Python?", "a": "In industry roles, Power BI is used for rapid business intelligence reporting, while Python is used for advanced data cleaning, statistical modeling, and forecasting. Knowing both is critical for data science positions."},
            {"q": "Do we cover data extraction using web APIs?", "a": "Yes, we teach you how to fetch data from JSON REST APIs and load it into Pandas dataframes."}
        ],
        "fees_structure": "The Data Science Training fee is ₹22,999 (all-inclusive). Payment can be split into 2 installments of ₹11,500. Upfront full payment grants a 5% discount (₹21,849 final fee).",
        "fees_comparison": {
            "typical_pune_fees": "₹50,000 - ₹75,000",
            "pune_batch_size": "40 to 50 students",
            "cacts_value": "1-on-1 virtual sessions where you share your screen and write data scripts with a dedicated mentor, at less than half of standard classroom prices."
        },
        "fees_faqs": [
            {"q": "Does the course fee cover the Power BI license?", "a": "Power BI Desktop is free for learning and dashboard construction. We show you how to use the free tier options so you do not incur extra software fees."},
            {"q": "Can I pause my Data Science training if I have college exams?", "a": "Yes. Since it is 1-to-1 training, you can pause your schedule for exams or holidays and resume from the exact same point without losing any classes."}
        ],
        "interview_questions": [
            {"q": "Explain the difference between Inner Join, Left Join, and Self Join in SQL.", "a": "Inner Join returns records that have matching values in both tables. Left Join returns all records from the left table and matched records from the right table. Self Join is a join where a table is joined with itself (useful for querying hierarchical organizational schemas)."},
            {"q": "What is the difference between supervised and unsupervised learning?", "a": "Supervised learning models are trained on labeled datasets where the target variable is known (e.g. regression, classification). Unsupervised learning models analyze unlabeled datasets to find hidden patterns or groupings (e.g. clustering with K-Means)."},
            {"q": "How do you handle missing values in a Pandas DataFrame?", "a": "You can identify missing values with `.isnull()`. To handle them, you can drop records (`.dropna()`) if they are minimal, or impute them (`.fillna()`) with statistical values (mean, median, mode) or forward/backward fills depending on the context."},
            {"q": "What is a p-value in hypothesis testing?", "a": "A p-value is the probability of obtaining test results at least as extreme as the observed results, assuming the null hypothesis is true. A lower p-value (typically < 0.05) indicates strong evidence to reject the null hypothesis."},
            {"q": "Explain the concept of exploratory data analysis (EDA).", "a": "EDA is the process of examining a dataset to summarize its main characteristics, identify anomalies, check assumptions, and visualize variables using statistical charts and plots before formal modeling."}
        ],
        "interview_faqs": [
            {"q": "Do you provide SQL query preparation for interviews?", "a": "Yes. SQL query execution is the first round of most analyst interviews. We provide a workbook of 50+ real-world query problems (joins, window functions, subqueries) for hands-on practice."},
            {"q": "Will my internship project be listed on my resume?", "a": "Yes. You will list your active project commits, detailing how you cleaned and modeled real datasets during the internship."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Statistics & Analytical Querying", "duration": "3 Weeks", "skills": "Probability, descriptive statistics, SQL database queries, joins, aggregates", "project": "SQL E-Commerce Sales Audit"},
            {"phase": "Phase 2", "title": "Python Data Manipulation", "duration": "4 Weeks", "skills": "Pandas, NumPy, EDA workflows, dealing with outliers, data wrangling", "project": "Python Customer Demographic Analysis"},
            {"phase": "Phase 3", "title": "Data Visualization & Dashboards", "duration": "3 Weeks", "skills": "Power BI Desktop, Power Query ETL, DAX measures, interactive reports", "project": "Corporate Executive BI Dashboard"},
            {"phase": "Phase 4", "title": "Predictive Modeling & Staging Deploy", "duration": "4 Weeks", "skills": "Regressions, linear forecasting, Git commits, collaborating on active data tasks", "project": "Deploying Analytics Model on Internship"}
        ],
        "roadmap_faqs": [
            {"q": "What is the average salary for a Junior Data Analyst in Pune?", "a": "Entry-level analyst salaries in Pune range from ₹3.5 LPA to ₹5.2 LPA. Candidates with strong SQL skills and Power BI dashboard portfolios are highly sought after."},
            {"q": "How is Data Science different from Data Analytics?", "a": "Data Analytics focuses on analyzing historical data to answer business questions. Data Science includes analytics but also covers predictive machine learning modeling and data pipeline engineering."}
        ]
    },
    "data-engineering-training": {
        "syllabus_prerequisites": "Intermediate programming concepts (preferably Python) and basic SQL understanding.",
        "syllabus_projects": [
            "Project 1: Python ETL pipeline connecting web REST APIs to SQL databases.",
            "Project 2: Apache Spark data transformation pipeline processing JSON feeds.",
            "Project 3: Designing a star schema data warehouse in cloud environment.",
            "Project 4: Pipeline scheduling workflow deployed during the live internship."
        ],
        "syllabus_tools": ["Apache Spark", "Hadoop HDFS", "PostgreSQL / MySQL", "Python (PySpark)", "Docker", "Git & GitHub"],
        "syllabus_faqs": [
            {"q": "Do we write code in PySpark?", "a": "Yes. We use PySpark (Spark with Python) to write distributed data transformation pipelines."},
            {"q": "What is covered under data warehousing?", "a": "We cover OLAP vs OLTP architectures, dimensional modeling (star and snowflake schemas), indexing, and query optimization."}
        ],
        "fees_structure": "The Data Engineering Training fee is ₹24,999 (all-inclusive). Payment can be split into 2 monthly installments of ₹12,500. Upfront full payment grants a 5% discount (₹23,749 total).",
        "fees_comparison": {
            "typical_pune_fees": "₹65,000 - ₹85,000",
            "pune_batch_size": "30 to 45 students",
            "cacts_value": "1-to-1 custom pacing with a senior data architect, writing real ETL scripts, at a fraction of typical institute fees."
        },
        "fees_faqs": [
            {"q": "Are there extra costs for running Hadoop or Spark labs?", "a": "No. We show you how to configure single-node clusters locally on your laptop and utilize free cloud platforms so there are no extra laboratory fees."},
            {"q": "Do you offer job placement services for Data Engineers?", "a": "No. We do not provide job placement guarantees or placement services. However, we guide you to build a public GitHub portfolio of your internship pipelines, which you can share directly with recruiters."}
        ],
        "interview_questions": [
            {"q": "Explain the difference between OLTP and OLAP systems.", "a": "OLTP (Online Transaction Processing) systems are optimized for transactional, rapid write/read operations, usually highly normalized (e.g. operational databases). OLAP (Online Analytical Processing) systems are optimized for complex, aggregate queries, usually denormalized using star or snowflake schemas (e.g. data warehouses)."},
            {"q": "What is the difference between map and flatMap in Apache Spark?", "a": "In Spark, `map` applies a transformation to each element of a DataFrame/RDD and returns a new collection of the same size. `flatMap` transforms each element into zero or more elements and flattens the output collection, changing the size."},
            {"q": "What is database normalization and why do we denormalize data warehouses?", "a": "Normalization reduces redundancy and dependency by splitting tables (e.g., 3NF). We denormalize data warehouses into star schemas to minimize table joins, dramatically speeding up read query performance for business analytics."},
            {"q": "Explain how partitioning improves query performance in Hive/Spark.", "a": "Partitioning divides data into directories based on columns (e.g. year/month). When a query filters by the partition column, Spark/Hive reads only that specific directory, skipping all other files (partition pruning), which saves time and compute resources."},
            {"q": "What is an ETL pipeline?", "a": "ETL stands for Extract (reading data from source APIs/databases), Transform (cleaning, filtering, joining data), and Load (writing the output data into a target database or warehouse)."}
        ],
        "interview_faqs": [
            {"q": "What technical rounds should I expect for Data Engineer roles?", "a": "You will face advanced SQL querying (window functions, Joins), Python scripting, and conceptual questions on Spark performance tuning and schema design."},
            {"q": "Do you help with mock interviews?", "a": "Yes. You get 1-to-1 mock interviews focused on writing optimized SQL queries and PySpark pipelines."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Advanced SQL & Database Schema Design", "duration": "4 Weeks", "skills": "Complex joins, window functions, indexing, normal forms, star schema designs", "project": "Transactional Database Schema Model"},
            {"phase": "Phase 2", "title": "Python ETL Scripting & Automation", "duration": "4 Weeks", "skills": "Python API requests, JSON parsing, logging, writing automated ETL scripts", "project": "Python Web API-to-SQL Pipeline"},
            {"phase": "Phase 3", "title": "Distributed Big Data Systems", "duration": "4 Weeks", "skills": "Hadoop architecture, HDFS storage, Apache Spark DataFrames, PySpark", "project": "Spark Big Data Batch Processor"},
            {"phase": "Phase 4", "title": "Cloud Warehousing & Pipeline Staging", "duration": "4 Weeks", "skills": "Cloud database integration, staging ETL pipelines, Git workflow", "project": "ETL Pipeline Optimization Project"}
        ],
        "roadmap_faqs": [
            {"q": "What is the salary outlook for Data Engineers in Pune?", "a": "Data Engineering is one of the highest-paying entry roles. Starting salaries in Pune range from ₹5 LPA to ₹8 LPA, driven by a shortage of candidates who can write clean ETL code."},
            {"q": "Is Data Engineering harder than Data Science?", "a": "It is more software-engineering-focused. If you enjoy building systems, writing SQL, and managing data flows rather than statistical analysis, you will excel here."}
        ]
    },
    "python-programming-training": {
        "syllabus_prerequisites": "No programming background is required. Absolute beginners are welcome.",
        "syllabus_projects": [
            "Project 1: Text-based RPG Game using Python control flow & lists.",
            "Project 2: Employee Database System using OOP classes and JSON files.",
            "Project 3: Custom Web Scraper extracting live data using BeautifulSoup.",
            "Project 4: Automated Desktop Task Script deployed locally."
        ],
        "syllabus_tools": ["Python IDE (IDLE/VS Code)", "pip manager", "Git & GitHub", "MySQL Workbench"],
        "syllabus_faqs": [
            {"q": "Is Python sufficient to get a job?", "a": "Core Python is excellent for automation, scripting, and QA roles. For core developer roles, we recommend upgrading to Django/Flask or transitioning to Data Science/ML pipelines."},
            {"q": "Do you teach Object-Oriented Programming (OOP) in detail?", "a": "Yes. We focus heavily on OOP concepts (Classes, Inheritance, Polymorphism, Encapsulation) since they are the foundations of all enterprise software."}
        ],
        "fees_structure": "The Python Programming Training tuition is ₹9,999 (all-inclusive). Payment can be split into 2 installments of ₹5,000. Upfront full payment grants a 5% discount (₹9,499 final fee).",
        "fees_comparison": {
            "typical_pune_fees": "₹20,000 - ₹30,000",
            "pune_batch_size": "40+ students in large batches",
            "cacts_value": "Private 1-on-1 coaching where the developer writes code with you on screen, at less than half of standard classroom prices."
        },
        "fees_faqs": [
            {"q": "Can I upgrade to Data Science later?", "a": "Yes. You can upgrade your training path to Data Science or AI/ML by paying the pro-rata fee difference."}
        ],
        "interview_questions": [
            {"q": "What is the difference between list and tuple in Python?", "a": "Lists are mutable (can be modified after creation) and use square brackets `[]`. Tuples are immutable (cannot be modified) and use parentheses `()`. Tuples are faster and safer for read-only data structures."},
            {"q": "How does memory management work in Python?", "a": "Python uses a private heap to store objects. Memory management is handled by the Python Memory Manager and an automatic Garbage Collector that uses reference counting to deallocate memory when references to an object hit zero."},
            {"q": "Explain the concept of decorators in Python.", "a": "A decorator is a design pattern in Python that allows you to modify the behavior of a function or class. It takes a function as an argument, extends its functionality without modifying the original code, and returns the modified function."},
            {"q": "What is the difference between deep copy and shallow copy?", "a": "A shallow copy constructs a new compound object and inserts references to the original nested objects. A deep copy recursively constructs a new object and inserts copies of the nested objects, making it completely independent."},
            {"q": "Explain exceptions handling blocks in Python.", "a": "Exceptions are handled using `try`, `except`, `else`, and `finally` blocks. Code that might raise an error is placed in `try`. The error is caught in `except`. If no error occurs, `else` runs. `finally` runs regardless, usually for cleanup (like closing files)."}
        ],
        "interview_faqs": [
            {"q": "What kind of coding challenges do we solve?", "a": "We solve 30+ logical coding problems (arrays, string manipulation, sorting) to ensure you can clear entry-level screening rounds."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Core Syntax & Pacing", "duration": "3 Weeks", "skills": "Variables, types, control flow loops, functions, lists, dicts", "project": "CLI Text Adventure Game"},
            {"phase": "Phase 2", "title": "Object-Oriented Programming & File I/O", "duration": "3 Weeks", "skills": "Classes, encapsulation, inheritance, reading/writing files, exceptions", "project": "Student Record OOP System"},
            {"phase": "Phase 3", "title": "Database Connection & Script Automation", "duration": "2 Weeks", "skills": "SQL integration, Web Scraping with BeautifulSoup, API fetching, scripting", "project": "Live Price Tracker Automation Script"}
        ],
        "roadmap_faqs": [
            {"q": "What is the starting salary for a Python script developer in Pune?", "a": "Entry roles start between ₹3 LPA and ₹4.5 LPA, often in automation, testing, or operations groups."}
        ]
    },
    "power-bi-training": {
        "syllabus_prerequisites": "Basic understanding of spreadsheets (like Excel) and data reports. No prior coding is required.",
        "syllabus_projects": [
            "Project 1: Sales Analysis dashboard connecting Excel feeds.",
            "Project 2: HR Operations report with complex table relationships.",
            "Project 3: Executive Financial dashboard with DAX Measures.",
            "Project 4: Real-world database reporting pipeline."
        ],
        "syllabus_tools": ["Power BI Desktop", "Power Query ETL", "SQL Server Express", "Power BI Service"],
        "syllabus_faqs": [
            {"q": "What is DAX?", "a": "DAX (Data Analysis Expressions) is the formula language used in Power BI to create custom measures and calculations."}
        ],
        "fees_structure": "The Power BI Training tuition is ₹7,999 (all-inclusive). We offer a 5% discount (₹7,599 final fee) for one-time upfront payments.",
        "fees_comparison": {
            "typical_pune_fees": "₹15,000 - ₹25,000",
            "pune_batch_size": "35+ students in crowded batches",
            "cacts_value": "1-to-1 virtual screenshare support with a BI consultant to build custom dashboards, at a fraction of typical coaching rates."
        },
        "fees_faqs": [
            {"q": "Is there a certificate provided?", "a": "Yes, you get a verified Course Completion Certificate detailing your dashboard projects."}
        ],
        "interview_questions": [
            {"q": "Explain the difference between calculated columns and measures in Power BI.", "a": "Calculated columns are computed row-by-row during data load, stored in the model, and consume memory. Measures are calculated dynamically on the fly during query evaluation based on the report filters, saving memory but using CPU resources."},
            {"q": "What is Power Query and what language does it use?", "a": "Power Query is the data transformation engine in Power BI used for ETL. It uses the 'M' language to write query transformation steps."},
            {"q": "Explain the difference between Star Schema and Snowflake Schema.", "a": "A Star Schema has a central fact table directly connected to denormalized dimension tables. A Snowflake Schema has normalized dimension tables, splitting them into sub-tables, which reduces redundancy but requires more complex joins."},
            {"q": "What is the CALCULATE function in DAX?", "a": "CALCULATE is the most powerful function in DAX. It evaluates an expression in a modified filter context, allowing you to override or add specific filters to the calculation."},
            {"q": "What is the purpose of the Active and Inactive relationships?", "a": "Power BI allows only one active relationship between two tables at a time. If there are multiple relationships (e.g., Order Date and Ship Date), one is marked active (default), and the others are inactive, which can be activated in DAX using `USERELATIONSHIP`."}
        ],
        "interview_faqs": [
            {"q": "Do we practice dashboard design scenarios?", "a": "Yes. We review dashboard layouts, color schemas, and filter contexts to ensure you design reports that executives can read easily."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Data Extraction & Power Query", "duration": "2 Weeks", "skills": "Connecting data sources, Power Query transformations, cleaning rows, merging tables", "project": "Cleaned Dataset Audit"},
            {"phase": "Phase 2", "title": "Data Modeling & DAX Formulas", "duration": "2 Weeks", "skills": "Table relationships, active vs inactive joins, writing DAX measures and columns", "project": "Fully Modeled Financial Report"},
            {"phase": "Phase 3", "title": "Visualization & Staging Deploy", "duration": "2 Weeks", "skills": "Selecting charts, filters, slicers, drill-downs, publishing to Power BI Service", "project": "Live Executive Sales Dashboard"}
        ],
        "roadmap_faqs": [
            {"q": "What is the starting salary for a Power BI Analyst in Pune?", "a": "Entry analyst roles range from ₹3.5 LPA to ₹5 LPA, with high demand across consultancy and IT firms."}
        ]
    },
    "cloud-computing-training": {
        "syllabus_prerequisites": "Basic understanding of networking concepts (IP addresses, DNS). No prior cloud experience is required.",
        "syllabus_projects": [
            "Project 1: Hosting a static portfolio website using AWS S3 & CloudFront.",
            "Project 2: Launching a secure multi-tier web application using EC2 & RDS.",
            "Project 3: Designing a highly available, load-balanced system with Auto Scaling.",
            "Project 4: Real company project cloud sandbox deployment."
        ],
        "syllabus_tools": ["AWS Management Console", "AWS CLI", "Visual Studio Code", "Git"],
        "syllabus_faqs": [
            {"q": "Which cloud provider do we focus on?", "a": "We focus on Amazon Web Services (AWS), which holds the largest market share, and cover core architectural concepts of Microsoft Azure."}
        ],
        "fees_structure": "The Cloud Computing Training fee is ₹14,999 (all-inclusive). Payment can be split into 2 installments of ₹7,500. Upfront full payment offers a 5% discount (₹14,249 final fee).",
        "fees_comparison": {
            "typical_pune_fees": "₹35,000 - ₹50,000",
            "pune_batch_size": "40+ students in large batches",
            "cacts_value": "Private 1-to-1 virtual sandbox guidance with a cloud engineer at less than half of typical institute rates."
        },
        "fees_faqs": [
            {"q": "Do I have to pay for AWS resources during practice?", "a": "No. We guide you to set up your account under the AWS Free Tier, teaching you how to configure alerts so you don't exceed free usage limits."}
        ],
        "interview_questions": [
            {"q": "Explain the difference between a Public Subnet and a Private Subnet in AWS VPC.", "a": "A Public Subnet has a route to an Internet Gateway, allowing resources inside (like web servers) to receive public traffic. A Private Subnet does not have a direct route to the Internet Gateway. To access the internet (e.g. for updates), resources in a private subnet must route traffic through a NAT Gateway located in a public subnet."},
            {"q": "What is AWS IAM and how do you implement the principle of least privilege?", "a": "IAM (Identity and Access Management) manages access to AWS resources. To implement least privilege, you avoid using root credentials, create specific IAM users, group them by role, and attach policies that grant only the minimum permissions required to perform their specific tasks."},
            {"q": "Explain the difference between Horizontal Scaling and Vertical Scaling.", "a": "Vertical Scaling (scaling up) means adding more power (CPU, RAM) to an existing server. Horizontal Scaling (scaling out) means adding more servers to your infrastructure resource pool, distributing load using a load balancer (more resilient)."},
            {"q": "What is AWS S3 and what are its storage classes?", "a": "S3 (Simple Storage Service) is an object storage service. Storage classes include S3 Standard (frequent access), S3 Standard-IA (infrequent access), S3 One Zone-IA (low-cost infrequent access), and S3 Glacier (archival storage with varying retrieval times)."},
            {"q": "What is an Elastic Load Balancer (ELB)?", "a": "ELB automatically distributes incoming application traffic across multiple targets, such as EC2 instances, containers, and IP addresses, ensuring high availability and fault tolerance."}
        ],
        "interview_faqs": [
            {"q": "What AWS certification should I target?", "a": "This course aligns with the AWS Certified Solutions Architect - Associate curriculum guidelines."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Cloud Fundamentals & Virtual Networks", "duration": "3 Weeks", "skills": "VPC design, public/private subnets, security groups, route tables, internet gateways", "project": "Secure Custom Virtual Network Design"},
            {"phase": "Phase 2", "title": "Compute & Object Storage Operations", "duration": "3 Weeks", "skills": "EC2 provisioning, storage volumes, S3 buckets, policies, load balancers, auto-scaling", "project": "Highly Available Web Infrastructure"},
            {"phase": "Phase 3", "title": "Cloud Databases, Identity & Monitoring", "duration": "4 Weeks", "skills": "RDS database setup, IAM policies, MFA keys, CloudWatch logs, staging deployment", "project": "Deployed Multi-Tier Web app on Internship"}
        ],
        "roadmap_faqs": [
            {"q": "What is the average starting salary for an AWS Associate in Pune?", "a": "Starting salaries range from ₹4 LPA to ₹6 LPA in infrastructure operations and system analyst tracks."}
        ]
    },
    "devops-training": {
        "syllabus_prerequisites": "Basic understanding of Linux command-line operations and Git concepts.",
        "syllabus_projects": [
            "Project 1: Writing Dockerfiles to containerize a web application.",
            "Project 2: Configuring a Jenkins CI/CD pipeline for automated test builds.",
            "Project 3: Deploying a multi-container app cluster using Kubernetes.",
            "Project 4: Automated server deployment using Ansible playbook."
        ],
        "syllabus_tools": ["Docker", "Kubernetes", "Jenkins", "Ansible", "Linux (Ubuntu)", "Git & GitHub"],
        "syllabus_faqs": [
            {"q": "Do we cover Kubernetes in detail?", "a": "Yes. We cover Kubernetes pods, services, deployments, replica sets, and basic cluster configurations in our dedicated module."}
        ],
        "fees_structure": "The DevOps Training fee is ₹14,999 (all-inclusive). Payment can be split into 2 installments of ₹7,500. Upfront full payment offers a 5% discount (₹14,249 final fee).",
        "fees_comparison": {
            "typical_pune_fees": "₹40,000 - ₹55,000",
            "pune_batch_size": "35 to 50 students in large batches",
            "cacts_value": "Private 1-to-1 virtual labs, building real automation pipelines with direct mentor feedback, at nearly a third of market pricing."
        },
        "fees_faqs": [
            {"q": "Are staging lab fees included?", "a": "Yes, we guide you to set up free tier staging environments so there are no extra operational costs."}
        ],
        "interview_questions": [
            {"q": "Explain the difference between a Docker Image and a Docker Container.", "a": "A Docker Image is a read-only, static template containing instructions for creating a container (built from a Dockerfile). A Docker Container is a runnable, isolated runtime instance of an image (created using `docker run`)."},
            {"q": "What is the difference between a Kubernetes Pod and a Deployment?", "a": "A Pod is the smallest deployable unit in Kubernetes, representing a single running container instance. A Deployment is a higher-level controller that manages the lifecycle of Pods, enabling declarative updates, scaling, and rolling updates."},
            {"q": "What is CI/CD and why is it used?", "a": "CI (Continuous Integration) is the practice of automating code integration from multiple developers into a shared repository, running automated tests. CD (Continuous Delivery/Deployment) is the practice of automating the deployment of that code to staging or production environments."},
            {"q": "What is Infrastructure as Code (IaC)?", "a": "IaC is the practice of managing and provisioning computing infrastructure (networks, VMs, load balancers) through machine-readable configuration files (like Terraform or Ansible), enabling automation and version control."},
            {"q": "How does Ansible differ from Jenkins?", "a": "Ansible is a configuration management tool used to automate server setups and package installations. Jenkins is a build automation tool used to orchestrate CI/CD pipelines."}
        ],
        "interview_faqs": [
            {"q": "What DevOps rounds are common in Pune?", "a": "Expect hands-on scripting, writing Dockerfiles, and detailing CI/CD pipeline automation workflows."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Linux Operations & Git Workflows", "duration": "3 Weeks", "skills": "Linux shell scripting, folder permissions, Git branches, PR review policies", "project": "Server Cleanup Automation Script"},
            {"phase": "Phase 2", "title": "Containerization with Docker", "duration": "3 Weeks", "skills": "Writing Dockerfiles, multi-container compose setups, volumes, network routing", "project": "Containerized Web App Stack"},
            {"phase": "Phase 3", "title": "Orchestration & Configuration Management", "duration": "3 Weeks", "skills": "Kubernetes pods, services, deployments, writing Ansible playbooks", "project": "Ansible Server Setup Automation"},
            {"phase": "Phase 4", "title": "CI/CD Pipelines & Cloud Staging", "duration": "3 Weeks", "skills": "Jenkins setups, GitHub Actions pipelines, automated test runs, staging deployment", "project": "CI/CD Pipeline Automation Project"}
        ],
        "roadmap_faqs": [
            {"q": "What is the average starting salary for a DevOps Associate in Pune?", "a": "DevOps roles start between ₹4.5 LPA and ₹7 LPA, driven by high demand for pipeline automation skills."}
        ]
    },
    "software-testing-training": {
        "syllabus_prerequisites": "Basic logical thinking. No prior programming background is required.",
        "syllabus_projects": [
            "Project 1: Detailed Test Plan and Bug Report using Jira templates.",
            "Project 2: Writing OOP Java test scripts for Selenium WebDriver.",
            "Project 3: Designing a Page Object Model (POM) testing framework.",
            "Project 4: Automated API test suite in Postman."
        ],
        "syllabus_tools": ["Selenium WebDriver", "Jira", "Eclipse / IntelliJ", "Postman API", "TestNG / JUnit", "Git"],
        "syllabus_faqs": [
            {"q": "Do we cover both manual and automation testing?", "a": "Yes. We cover manual testing processes, test case design, and Jira bug tracking, then transition into writing Selenium automation scripts in Java."}
        ],
        "fees_structure": "The Software Testing Training tuition is ₹9,999 (all-inclusive). We offer a 5% discount (₹9,499 final fee) for one-time upfront payments.",
        "fees_comparison": {
            "typical_pune_fees": "₹20,000 - ₹35,000",
            "pune_batch_size": "40+ students in large batches",
            "cacts_value": "1-to-1 virtual screenshare sessions to write and debug test scripts directly with a developer, at nearly half the market price."
        },
        "fees_faqs": [
            {"q": "Do I need to pay for Jira or test tools?", "a": "No. We use free open-source testing tools (Selenium, Java, Postman) and show you how to use Jira's free trial accounts."}
        ],
        "interview_questions": [
            {"q": "What is the difference between Verification and Validation in Software Testing?", "a": "Verification is the process of evaluating documentation, plans, and code structure (static testing, 'Are we building the product right?'). Validation is the process of executing the actual software to ensure it meets requirements (dynamic testing, 'Are we building the right product?')."},
            {"q": "What is the Page Object Model (POM) in Selenium?", "a": "POM is a design pattern where each web page is represented as a Class file. Page elements are defined as variables, and interactions are defined as methods in the class. This makes test scripts highly reusable and easy to maintain."},
            {"q": "Explain the difference between Implicit Wait and Explicit Wait in Selenium.", "a": "Implicit Wait sets a global timeout for the WebDriver to wait for all elements to load before throwing NoSuchElementException. Explicit Wait sets a specific wait condition (e.g. elementToBeClickable) for a particular element, resuming execution as soon as the condition is met, saving execution time."},
            {"q": "What is a bug lifecycle?", "a": "A bug lifecycle is the sequence of states a defect goes through: New (detected), Assigned (to developer), Open (under review), Fixed (code updated), Pending Retest (waiting for QA), Retesting, Verified (approved), and Closed (archived)."},
            {"q": "How do you perform API testing using Postman?", "a": "We send HTTP requests (GET, POST, PUT, DELETE) to endpoint URLs, pass headers/payloads, execute the request, and validate response status codes, headers, and JSON body payloads using Postman assertions."}
        ],
        "interview_faqs": [
            {"q": "What coding questions are asked in QA interviews?", "a": "Expect basic Java coding questions (string reversals, array searches) and locator writing challenges (XPath, CSS selectors)."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Manual QA & Defect Tracking", "duration": "3 Weeks", "skills": "SDLC, STLC, writing test plans, scenarios, logging defects in Jira templates", "project": "Manual Test Suite Execution"},
            {"phase": "Phase 2", "title": "Java Programming for Automation", "duration": "3 Weeks", "skills": "Java syntax, OOP classes, TestNG testing framework annotations", "project": "Core Java Logical Code Set"},
            {"phase": "Phase 3", "title": "Selenium Automation Frameworks", "duration": "2 Weeks", "skills": "Selenium locators, handling alerts, waits, designing Page Object Models", "project": "E-Commerce Page Object Framework"},
            {"phase": "Phase 4", "title": "API Testing & Database QA", "duration": "2 Weeks", "skills": "Postman API requests, validating JSON payloads, SQL verification queries", "project": "API Test Suite Staging"}
        ],
        "roadmap_faqs": [
            {"q": "What is the starting salary for a QA Engineer in Pune?", "a": "Starting salaries in Pune range from ₹3 LPA to ₹4.5 LPA, with automation roles fetching higher rates than manual testing."}
        ]
    },
    "cybersecurity-training": {
        "syllabus_prerequisites": "Basic computer operation and networking concepts (ports, IP addresses). No prior security background is required.",
        "syllabus_projects": [
            "Project 1: Penetration testing audit reports on local sandbox labs.",
            "Project 2: Configuring firewall rules and security groups in Linux.",
            "Project 3: Cryptographic hashing and key exchange scripts.",
            "Project 4: OWASP Web application vulnerability assessment project."
        ],
        "syllabus_tools": ["Kali Linux", "Wireshark", "Nmap port scanner", "Metasploit Framework", "Burp Suite"],
        "syllabus_faqs": [
            {"q": "Is this an ethical hacking course?", "a": "Yes. We focus on ethical hacking methodologies to identify vulnerabilities, configure defenses, and document patch recommendations."}
        ],
        "fees_structure": "The Cybersecurity Training fee is ₹19,999 (all-inclusive). Payment can be split into 2 installments of ₹10,000. Upfront full payment grants a 5% discount (₹18,999 final fee).",
        "fees_comparison": {
            "typical_pune_fees": "₹45,000 - ₹65,000",
            "pune_batch_size": "30 to 45 students in large classes",
            "cacts_value": "Strictly individual 1-to-1 virtual labs, running scans and exploits directly with a security specialist, at half the market price."
        },
        "fees_faqs": [
            {"q": "Do I need high-performance hardware for security labs?", "a": "A standard computer with 8GB RAM and virtualization support (VirtualBox/VMware) is sufficient for lab setups."}
        ],
        "interview_questions": [
            {"q": "What is the difference between Symmetric and Asymmetric encryption?", "a": "Symmetric encryption uses the same key for both encryption and decryption (fast, e.g. AES). Asymmetric encryption uses a public key to encrypt and a private key to decrypt (secure key exchange, e.g. RSA)."},
            {"q": "Explain the OWASP Top 10 concept.", "a": "OWASP Top 10 is a standard awareness document for web application security, listing the top 10 most critical security risks (such as SQL Injection, Broken Authentication, Cross-Site Scripting, and Security Misconfiguration)."},
            {"q": "What is a SQL Injection attack and how do you prevent it?", "a": "SQL Injection occurs when malicious SQL statements are inserted into input entry fields, executing unauthorized database commands. It is prevented by using parameterized queries (Prepared Statements), input validation, and ORM libraries."},
            {"q": "Explain how a man-in-the-middle (MITM) attack works.", "a": "An attacker intercepts communications between two parties (e.g. client and server) without their knowledge, allowing the attacker to read or modify messages before forwarding them (prevented by using HTTPS/TLS)."},
            {"q": "What is the difference between a Vulnerability Scan and a Penetration Test?", "a": "A Vulnerability Scan is an automated search that identifies known security gaps. A Penetration Test is a manual, authorized simulation of a cyberattack to actively exploit security gaps and verify their impact."}
        ],
        "interview_faqs": [
            {"q": "What rounds are standard for Security Analyst roles?", "a": "Expect questions on networking protocols, Linux configurations, and OWASP web vulnerability remediation."}
        ],
        "roadmap_milestones": [
            {"phase": "Phase 1", "title": "Network Security & Linux Basics", "duration": "3 Weeks", "skills": "Linux shell administration, TCP/IP protocols, running Nmap port scans", "project": "Network Infrastructure Security Audit"},
            {"phase": "Phase 2", "title": "Vulnerability Analysis & Exploitation", "duration": "3 Weeks", "skills": "Running Nessus scans, Metasploit console exploits in sandbox environments", "project": "System Vulnerability Assessment"},
            {"phase": "Phase 3", "title": "Web Application Security", "duration": "3 Weeks", "skills": "OWASP vulnerabilities, SQL injection, XSS payloads, Burp Suite intercepting", "project": "Web API Security Penetration Report"},
            {"phase": "Phase 4", "title": "Cryptography & Defenses Operations", "duration": "3 Weeks", "skills": "Encryption models, firewalls setup, log analysis, staging audits", "project": "Infrastructure Security Plan Project"}
        ],
        "roadmap_faqs": [
            {"q": "What is the starting salary for a Security Analyst in Pune?", "a": "Starting salaries in Pune range from ₹4 LPA to ₹6 LPA, driven by a global focus on digital security audits."}
        ]
    }
}
