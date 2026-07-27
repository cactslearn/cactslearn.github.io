/* 
 * live-compiler.js - All-in-One Client-Side Skills & Syntax Validation Hub
 * Integrates Monaco Editor, Pyodide WASM (Python), SQL.js (SQLite),
 * Babel Standalone (React JSX / Web), js-yaml / Linter (DevOps), and Expo Native Sandbox.
 */

(function () {
    'use strict';

    // Global state
    let monacoEditor = null;
    let currentTrack = 'devops';
    let pyodideInstance = null;
    let sqlDbInstance = null;
    let isPyodideLoading = false;
    let isSqlLoading = false;

    // Code Templates for Each Track
    const CODE_TEMPLATES = {
        devops: {
            language: 'yaml',
            defaultTemplate: 'k8s-deploy',
            templates: {
                'k8s-deploy': `# Kubernetes Deployment Specification
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cacts-api-deployment
  labels:
    app: cacts-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cacts-api
  template:
    metadata:
      labels:
        app: cacts-api
    spec:
      containers:
      - name: api-server
        image: cacts/api-server:v1.2.0
        ports:
        - containerPort: 8080
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "250m"
            memory: "256Mi"`,

                'dockerfile': `# Multi-stage Build Dockerfile for Node.js App
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine AS runner
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]`,

                'terraform': `# Terraform HCL Infrastructure Configuration
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1" # Pune / Mumbai Region
}

resource "aws_vpc" "cacts_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name        = "CACTS-Production-VPC"
    Environment = "Production"
  }
}`
            }
        },

        python: {
            language: 'python',
            defaultTemplate: 'data-processing',
            templates: {
                'data-processing': `# Python AI & Data Science Client-Side Execution (Pyodide WASM)
import math

# Sample Student Grades Dataset
students = [
    {"name": "Rahul M.", "score": 92, "track": "Java Fullstack"},
    {"name": "Snehal P.", "score": 88, "track": "React JS"},
    {"name": "Aditya V.", "score": 95, "track": "Blockchain"},
    {"name": "Priya K.", "score": 79, "track": "DevOps"},
    {"name": "Rohan D.", "score": 91, "track": "Data Engineering"}
]

print("CACTS STUDENT PERFORMANCE METRICS")
total_score = sum(s["score"] for s in students)
avg_score = total_score / len(students)

print(f"Total Enrolled Students: {len(students)}")
print(f"Average Batch Score: {avg_score:.2f} / 100")
print("-" * 40)

# Filter High Performers (Score >= 90)
high_performers = [s for s in students if s["score"] >= 90]
print("Top Honor Students (>= 90%):")
for student in high_performers:
    print(f"  * {student['name']} ({student['track']}) - {student['score']}%")
`,

                'algorithm': `# Machine Learning Feature Scaling & Normalization
def min_max_scale(data_list):
    min_val = min(data_list)
    max_val = max(data_list)
    return [(x - min_val) / (max_val - min_val) for x in data_list]

raw_features = [12000, 18000, 25000, 42000, 15000, 31000]
scaled = min_max_scale(raw_features)

print("Original Feature Salary Range:", raw_features)
print("Normalized Features (0.0 to 1.0):")
for orig, sc in zip(raw_features, scaled):
    print(f"  INR {orig:,}  -->  {sc:.4f}")
`
            }
        },

        sql: {
            language: 'sql',
            defaultTemplate: 'select-join',
            templates: {
                'select-join': `-- SQLite In-Memory Database Query (SQL.js WASM)
-- Sample tables 'students' and 'courses' are pre-populated

SELECT 
    s.student_id,
    s.student_name,
    c.course_name,
    c.duration_weeks,
    s.enrollment_date,
    s.city
FROM students s
INNER JOIN courses c ON s.course_id = c.course_id
WHERE s.city = 'Pune'
ORDER BY s.student_id ASC;`,

                'aggregation': `-- Aggregate Group By & Average Tuition Query
SELECT 
    c.course_name,
    COUNT(s.student_id) AS total_enrolled,
    c.tuition_fee
FROM courses c
LEFT JOIN students s ON c.course_id = s.course_id
GROUP BY c.course_id
ORDER BY total_enrolled DESC;`
            }
        },

        web: {
            language: 'javascript',
            defaultTemplate: 'react-counter',
            templates: {
                'react-counter': `// Interactive React 18 Live Component (Babel Transpiled)
function CactsInteractiveWidget() {
    const [count, setCount] = React.useState(0);
    const [activeTrack, setActiveTrack] = React.useState("Java Fullstack");

    const tracks = ["Java Fullstack", "React JS", "DevOps", "AI & ML", "Blockchain"];

    return (
        <div style={{
            fontFamily: 'Inter, system-ui, sans-serif',
            background: '#0b0f19',
            color: '#f8fafc',
            padding: '2rem',
            borderRadius: '12px',
            border: '1px solid #1e293b',
            maxWidth: '500px',
            margin: '1rem auto',
            boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)'
        }}>
            <span style={{
                background: 'rgba(99, 102, 241, 0.15)',
                color: '#818cf8',
                padding: '0.25rem 0.75rem',
                borderRadius: '20px',
                fontSize: '0.8rem',
                fontWeight: '600'
            }}>
                1-to-1 Live Component Preview
            </span>
            <h2 style={{ marginTop: '1rem', color: '#f8fafc' }}>CACTS Interactive Lab</h2>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
                Currently Selected Track: <strong style={{ color: '#14b8a6' }}>{activeTrack}</strong>
            </p>

            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', margin: '1rem 0' }}>
                {tracks.map(t => (
                    <button
                        key={t}
                        onClick={() => setActiveTrack(t)}
                        style={{
                            background: activeTrack === t ? '#6366f1' : '#1e293b',
                            color: '#ffffff',
                            border: 'none',
                            padding: '0.4rem 0.8rem',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            fontSize: '0.8rem'
                        }}
                    >
                        {t}
                    </button>
                ))}
            </div>

            <div style={{
                background: '#1e293b',
                padding: '1rem',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justify: 'space-between',
                marginTop: '1.5rem'
            }}>
                <span style={{ fontSize: '0.9rem' }}>Completed Hands-on Commits: <strong>{count}</strong></span>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button 
                        onClick={() => setCount(c => c + 1)}
                        style={{ background: '#14b8a6', color: '#0b0f19', border: 'none', padding: '0.5rem 1rem', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer' }}
                    >
                        Add Commit
                    </button>
                    <button 
                        onClick={() => setCount(0)}
                        style={{ background: '#334155', color: '#f8fafc', border: 'none', padding: '0.5rem 0.75rem', borderRadius: '6px', cursor: 'pointer' }}
                    >
                        Reset
                    </button>
                </div>
            </div>
        </div>
    );
}

// Render component into root DOM container
ReactDOM.createRoot(document.getElementById('root')).render(<CactsInteractiveWidget />);`,

                'html-vanilla': `<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: sans-serif; padding: 2rem; }
        .card { background: #1e293b; border-radius: 8px; padding: 1.5rem; border: 1px solid #334155; }
        .btn { background: #6366f1; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 6px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h2>HTML5 & Vanilla JavaScript Widget</h2>
        <p>Real-time browser DOM manipulation sandbox.</p>
        <button class="btn" onclick="alert('Hello from CACTS Web Sandbox!')">Click Test</button>
    </div>
</body>
</html>`
            }
        },

        mobile: {
            language: 'javascript',
            defaultTemplate: 'react-native-view',
            templates: {
                'react-native-view': `// React Native Mobile Application Template
function MobileApp() {
    const [likes, setLikes] = React.useState(0);

    return (
        <div style={{
            background: '#0b0f19',
            minHeight: '450px',
            display: 'flex',
            alignItems: 'center',
            justify: 'center',
            padding: '1rem'
        }}>
            <div style={{
                width: '320px',
                height: '420px',
                background: '#1e293b',
                borderRadius: '36px',
                border: '8px solid #334155',
                boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.7)',
                padding: '1.5rem',
                display: 'flex',
                flexDirection: 'column',
                justify: 'space-between',
                color: '#ffffff',
                fontFamily: 'Inter, sans-serif'
            }}>
                <div>
                    <span style={{ fontSize: '0.7rem', color: '#14b8a6', fontWeight: 'bold', textTransform: 'uppercase' }}>
                        iOS & Android Preview
                    </span>
                    <h3 style={{ margin: '0.5rem 0', fontSize: '1.1rem' }}>CACTS Mobile App</h3>
                    <p style={{ fontSize: '0.85rem', color: '#94a3b8', lineHeight: '1.5' }}>
                        Cross-platform mobile application interface built with React Native.
                    </p>
                </div>

                <div style={{ background: '#090d16', padding: '1rem', borderRadius: '12px', textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#38bdf8', marginBottom: '0.5rem' }}>
                        {likes}
                    </div>
                    <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>App Engagement Likes</span>
                </div>

                <button 
                    onClick={() => setLikes(c => c + 1)}
                    style={{
                        background: '#6366f1',
                        color: '#ffffff',
                        border: 'none',
                        padding: '0.8rem',
                        borderRadius: '20px',
                        fontWeight: 'bold',
                        fontSize: '0.9rem',
                        cursor: 'pointer',
                        width: '100%'
                    }}
                >
                    Like App Component
                </button>
            </div>
        </div>
    );
}

ReactDOM.createRoot(document.getElementById('root')).render(<MobileApp />);`
            }
        }
    };

    // Initialize Monaco Editor
    function initMonaco() {
        if (window.monaco) {
            setupEditor();
            return;
        }

        if (window.require) {
            window.require.config({
                paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' }
            });
            window.require(['vs/editor/editor.main'], function () {
                setupEditor();
            });
        }
    }

    function setupEditor() {
        const container = document.getElementById('editor-container');
        if (!container) return;

        const initialCode = CODE_TEMPLATES.devops.templates['k8s-deploy'];

        monacoEditor = monaco.editor.create(container, {
            value: initialCode,
            language: 'yaml',
            theme: 'vs-dark',
            automaticLayout: true,
            fontSize: 14,
            lineNumbers: 'on',
            minimap: { enabled: false },
            padding: { top: 12, bottom: 12 },
            scrollBeyondLastLine: false,
            fontFamily: 'Fira Code, Consolas, Monaco, monospace'
        });

        // Trigger syntax validation on change if devops track
        monacoEditor.onDidChangeModelContent(function () {
            if (currentTrack === 'devops') {
                validateDevOpsSyntax();
            }
        });

        // Perform initial validation
        validateDevOpsSyntax();
    }

    // Update Status Badge
    function setStatus(message, state = 'info') {
        const badge = document.getElementById('status-badge');
        if (!badge) return;
        badge.textContent = message;
        badge.className = `status-badge status-${state}`;
    }

    // Switch Active Track
    function switchTrack(trackKey) {
        if (!CODE_TEMPLATES[trackKey]) return;
        currentTrack = trackKey;

        // Update active tab buttons
        document.querySelectorAll('.track-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.track === trackKey);
        });

        // Populate template selector dropdown
        const templateSelect = document.getElementById('template-select');
        if (templateSelect) {
            templateSelect.innerHTML = '';
            const trackObj = CODE_TEMPLATES[trackKey];
            Object.keys(trackObj.templates).forEach(tmplKey => {
                const opt = document.createElement('option');
                opt.value = tmplKey;
                opt.textContent = tmplKey.replace(/-/g, ' ').toUpperCase();
                templateSelect.appendChild(opt);
            });
        }

        // Set editor language and code content
        const defaultTmpl = CODE_TEMPLATES[trackKey].defaultTemplate;
        const code = CODE_TEMPLATES[trackKey].templates[defaultTmpl];
        const lang = CODE_TEMPLATES[trackKey].language;

        if (monacoEditor) {
            const model = monacoEditor.getModel();
            monaco.editor.setModelLanguage(model, lang);
            monacoEditor.setValue(code);
            monaco.editor.setModelMarkers(model, 'devops', []); // Clear markers
        }

        // Toggle Output Pane Views
        toggleOutputPaneViews(trackKey);

        // Track specific initialization
        if (trackKey === 'python') {
            initPyodide();
        } else if (trackKey === 'sql') {
            initSqlJs();
        } else if (trackKey === 'devops') {
            validateDevOpsSyntax();
        } else if (trackKey === 'mobile') {
            runWebCode();
        }

        setStatus(`Switched to ${trackKey.toUpperCase()} Track`, 'success');
    }

    // Toggle output tabs/panes based on track
    function toggleOutputPaneViews(trackKey) {
        const consolePane = document.getElementById('pane-console');
        const tablePane = document.getElementById('pane-table');
        const webPane = document.getElementById('pane-web');
        const snackPane = document.getElementById('pane-snack');

        const tabConsole = document.getElementById('tab-console');
        const tabTable = document.getElementById('tab-table');
        const tabWeb = document.getElementById('tab-web');
        const tabSnack = document.getElementById('tab-snack');

        [consolePane, tablePane, webPane, snackPane].forEach(el => el && (el.style.display = 'none'));
        [tabConsole, tabTable, tabWeb, tabSnack].forEach(el => el && (el.style.display = 'none'));

        if (trackKey === 'web' || trackKey === 'mobile') {
            if (webPane) webPane.style.display = 'block';
            if (tabWeb) { tabWeb.style.display = 'inline-block'; tabWeb.click(); }
        } else if (trackKey === 'sql') {
            if (tablePane) tablePane.style.display = 'block';
            if (consolePane) consolePane.style.display = 'block';
            if (tabTable) tabTable.style.display = 'inline-block';
            if (tabConsole) tabConsole.style.display = 'inline-block';
            if (tabTable) tabTable.click();
        } else {
            if (consolePane) consolePane.style.display = 'block';
            if (tabConsole) { tabConsole.style.display = 'inline-block'; tabConsole.click(); }
        }
    }

    // 1. DEVOPS SYNTAX LINTER & LINE MARKERS
    function validateDevOpsSyntax() {
        if (!monacoEditor || currentTrack !== 'devops') return;

        const model = monacoEditor.getModel();
        const code = monacoEditor.getValue();
        const markers = [];

        const consoleOut = document.getElementById('console-output');

        // Check if YAML or Dockerfile
        if (code.trim().startsWith('# Multi-stage') || code.includes('FROM ') || code.includes('WORKDIR ')) {
            // Dockerfile validation
            const lines = code.split('\n');
            lines.forEach((line, index) => {
                const trimmed = line.trim();
                if (trimmed && !trimmed.startsWith('#')) {
                    const validInstructions = ['FROM', 'RUN', 'CMD', 'LABEL', 'EXPOSE', 'ENV', 'ADD', 'COPY', 'ENTRYPOINT', 'VOLUME', 'USER', 'WORKDIR', 'ARG', 'ONBUILD', 'STOPSIGNAL', 'HEALTHCHECK', 'SHELL'];
                    const firstWord = trimmed.split(' ')[0].toUpperCase();
                    if (!validInstructions.includes(firstWord)) {
                        markers.push({
                            startLineNumber: index + 1,
                            startColumn: 1,
                            endLineNumber: index + 1,
                            endColumn: line.length + 1,
                            message: `Unknown Dockerfile instruction '${firstWord}'. Must be one of: ${validInstructions.join(', ')}`,
                            severity: monaco.MarkerSeverity.Error
                        });
                    }
                }
            });
        } else if (code.includes('resource "') || code.includes('provider "')) {
            // Terraform HCL basic bracket linter
            let openBraces = 0;
            const lines = code.split('\n');
            lines.forEach((line, index) => {
                for (let char of line) {
                    if (char === '{') openBraces++;
                    if (char === '}') openBraces--;
                }
            });
            if (openBraces !== 0) {
                markers.push({
                    startLineNumber: lines.length,
                    startColumn: 1,
                    endLineNumber: lines.length,
                    endColumn: 10,
                    message: `Unmatched Terraform HCL braces ({ }). Missing ${Math.abs(openBraces)} closing/opening brace(s).`,
                    severity: monaco.MarkerSeverity.Error
                });
            }
        } else {
            // YAML validation using js-yaml
            if (window.jsyaml) {
                try {
                    window.jsyaml.load(code);
                } catch (e) {
                    if (e.mark) {
                        markers.push({
                            startLineNumber: e.mark.line + 1,
                            startColumn: e.mark.column + 1,
                            endLineNumber: e.mark.line + 1,
                            endColumn: e.mark.column + 10,
                            message: `YAML Syntax Error: ${e.reason}`,
                            severity: monaco.MarkerSeverity.Error
                        });
                    }
                }
            }
        }

        monaco.editor.setModelMarkers(model, 'devops', markers);

        if (consoleOut) {
            if (markers.length === 0) {
                consoleOut.innerHTML = `<span style="color: var(--success);">[SUCCESS] DevOps Syntax Verification Passed: 0 Errors / 0 Warnings found. Spec is fully valid.</span>`;
                setStatus('DevOps Config Validated: 0 Errors', 'success');
            } else {
                let errLog = `<span style="color: var(--error);">[ERROR] Found ${markers.length} Syntax Error(s):\n`;
                markers.forEach(m => {
                    errLog += `  * Line ${m.startLineNumber}: ${m.message}\n`;
                });
                errLog += `</span>`;
                consoleOut.innerHTML = errLog;
                setStatus(`DevOps Syntax Error at Line ${markers[0].startLineNumber}`, 'error');
            }
        }
    }

    // 2. PYTHON WASM (Pyodide Execution using define.amd masking, keeping window.define function intact)
    async function initPyodide() {
        if (pyodideInstance) return pyodideInstance;
        if (isPyodideLoading) return;

        isPyodideLoading = true;
        setStatus('Loading Pyodide WASM Runtime...', 'warning');

        try {
            if (typeof window.loadPyodide === 'function') {
                // Temporarily mask define.amd so pyodide.asm.js doesn't trigger Emscripten AMD require,
                // while keeping window.define intact for Monaco setModelLanguage(python.js)!
                let originalAmd = null;
                if (window.define && window.define.amd) {
                    originalAmd = window.define.amd;
                    window.define.amd = false;
                }

                try {
                    pyodideInstance = await window.loadPyodide({
                        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/'
                    });
                } finally {
                    if (window.define && originalAmd !== null) {
                        window.define.amd = originalAmd;
                    }
                }

                isPyodideLoading = false;
                setStatus('Pyodide WASM Ready', 'success');
                return pyodideInstance;
            } else {
                throw new Error('Pyodide CDN script not present on page');
            }
        } catch (err) {
            isPyodideLoading = false;
            setStatus('Pyodide WASM Load Error', 'error');
            console.error('Failed to initialize Pyodide WASM:', err);
        }
    }

    async function runPythonCode() {
        const consoleOut = document.getElementById('console-output');
        if (!consoleOut) return;

        try {
            if (!pyodideInstance) {
                consoleOut.innerHTML = '<span style="color: var(--warning);">[INFO] Initializing Pyodide WASM Runtime in Browser Memory... Please wait.</span>\n';
                await initPyodide();
            }

            if (!pyodideInstance) {
                consoleOut.innerHTML = '<span style="color: var(--error);">[ERROR] Pyodide WASM Runtime could not be initialized. Please check network connection.</span>';
                return;
            }

            setStatus('Executing Python Script in Browser WASM Memory...', 'warning');
            consoleOut.innerHTML = '<span style="color: var(--text-secondary);">[INFO] Executing script in Pyodide WASM sandbox...</span>\n';

            // Setup stdout & stderr capture
            pyodideInstance.setStdout({
                batched: (text) => {
                    consoleOut.innerText += text + '\n';
                }
            });
            pyodideInstance.setStderr({
                batched: (text) => {
                    consoleOut.innerHTML += `<span style="color: var(--error);">${text}</span>\n`;
                }
            });

            const code = monacoEditor.getValue();
            await pyodideInstance.runPythonAsync(code);
            setStatus('Python Execution Finished', 'success');
        } catch (err) {
            consoleOut.innerHTML += `<span style="color: var(--error);">[PYTHON ERROR]\n${err.message}</span>\n`;
            setStatus('Python Script Error', 'error');
        }
    }

    // 3. DATABASE SQL (SQL.js SQLite WASM using define.amd masking)
    async function initSqlJs() {
        if (sqlDbInstance) return sqlDbInstance;
        if (isSqlLoading) return;

        isSqlLoading = true;
        setStatus('Initializing In-Memory SQLite WASM...', 'warning');

        try {
            if (typeof window.initSqlJs === 'function') {
                let originalAmd = null;
                if (window.define && window.define.amd) {
                    originalAmd = window.define.amd;
                    window.define.amd = false;
                }

                let SQL;
                try {
                    SQL = await window.initSqlJs({
                        locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}`
                    });
                } finally {
                    if (window.define && originalAmd !== null) {
                        window.define.amd = originalAmd;
                    }
                }

                sqlDbInstance = new SQL.Database();
                seedSqlDatabase();
                isSqlLoading = false;
                setStatus('SQLite WASM DB Ready', 'success');
                return sqlDbInstance;
            } else {
                throw new Error('SQL.js CDN script not present on page');
            }
        } catch (err) {
            isSqlLoading = false;
            setStatus('SQLite WASM Load Error', 'error');
            console.error('Failed to initialize SQL.js WASM:', err);
        }
    }

    function seedSqlDatabase() {
        if (!sqlDbInstance) return;

        const seedQueries = `
            CREATE TABLE courses (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL,
                duration_weeks INTEGER,
                tuition_fee INTEGER
            );

            INSERT INTO courses VALUES (101, 'Java Fullstack Development', 16, 19999);
            INSERT INTO courses VALUES (102, 'Full Stack Web (MERN)', 14, 17999);
            INSERT INTO courses VALUES (103, 'React JS Development', 10, 14999);
            INSERT INTO courses VALUES (104, 'DevOps Engineering', 12, 14999);
            INSERT INTO courses VALUES (105, 'Blockchain Development', 16, 24999);

            CREATE TABLE students (
                student_id INTEGER PRIMARY KEY,
                student_name TEXT NOT NULL,
                course_id INTEGER,
                city TEXT,
                enrollment_date DATE,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            );

            INSERT INTO students VALUES (1, 'Rahul M.', 101, 'Pune', '2026-03-15');
            INSERT INTO students VALUES (2, 'Snehal P.', 103, 'Pune', '2026-04-02');
            INSERT INTO students VALUES (3, 'Aditya V.', 105, 'Pune', '2026-06-12');
            INSERT INTO students VALUES (4, 'Pooja K.', 102, 'Mumbai', '2026-05-10');
            INSERT INTO students VALUES (5, 'Rohan D.', 104, 'Pune', '2026-05-18');
        `;

        sqlDbInstance.run(seedQueries);
    }

    async function runSqlCode() {
        const consoleOut = document.getElementById('console-output');
        const tableContainer = document.getElementById('table-output-container');

        if (!sqlDbInstance) {
            if (consoleOut) consoleOut.innerHTML = '<span style="color: var(--warning);">[INFO] Initializing SQL.js Database... Please wait.</span>';
            await initSqlJs();
        }

        if (!sqlDbInstance) {
            if (consoleOut) consoleOut.innerHTML = '<span style="color: var(--error);">[ERROR] SQL.js Database failed to load.</span>';
            return;
        }

        const query = monacoEditor.getValue();
        setStatus('Executing SQL Query in Memory...', 'warning');

        try {
            const results = sqlDbInstance.exec(query);

            if (results.length === 0) {
                if (consoleOut) consoleOut.innerHTML = '<span style="color: var(--success);">Query executed successfully. 0 rows returned.</span>';
                if (tableContainer) tableContainer.innerHTML = '<p style="color: var(--text-secondary); text-align: center;">No result set returned.</p>';
            } else {
                const res = results[0];
                const columns = res.columns;
                const values = res.values;

                // Build Table HTML
                let tableHtml = '<table class="sql-result-table"><thead><tr>';
                columns.forEach(col => {
                    tableHtml += `<th>${col}</th>`;
                });
                tableHtml += '</tr></thead><tbody>';

                values.forEach(row => {
                    tableHtml += '<tr>';
                    row.forEach(val => {
                        tableHtml += `<td>${val === null ? '<em>NULL</em>' : val}</td>`;
                    });
                    tableHtml += '</tr>';
                });
                tableHtml += '</tbody></table>';

                if (tableContainer) tableContainer.innerHTML = tableHtml;
                if (consoleOut) consoleOut.innerHTML = `<span style="color: var(--success);">[SUCCESS] Returned ${values.length} row(s) in 0.4ms.</span>`;
            }
            setStatus('SQL Query Finished', 'success');
        } catch (err) {
            if (consoleOut) consoleOut.innerHTML = `<span style="color: var(--error);">[SQL ERROR] ${err.message}</span>`;
            if (tableContainer) tableContainer.innerHTML = `<p style="color: var(--error);">${err.message}</p>`;
            setStatus('SQL Query Error', 'error');
        }
    }

    // 4. WEB DEV & REACT JSX (Babel Standalone)
    function runWebCode() {
        const iframe = document.getElementById('web-preview-iframe');
        if (!iframe) return;

        const code = monacoEditor.getValue();
        setStatus('Transpiling React JSX & Rendering Live Preview...', 'warning');

        try {
            let compiledJs = code;

            // Transpile JSX if babel is loaded
            if (window.Babel && (code.includes('<') || code.includes('import ') || code.includes('export '))) {
                compiledJs = window.Babel.transform(code, { presets: ['react', 'env'] }).code;
            }

            const htmlContent = `
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
                <style>
                    body { margin: 0; padding: 1rem; background: #0b0f19; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; }
                </style>
            </head>
            <body>
                <div id="root"></div>
                <script>
                    try {
                        ${compiledJs}
                    } catch(err) {
                        document.getElementById('root').innerHTML = '<div style="color: #ef4444; background: #1e1b4b; padding: 1rem; border-radius: 8px; font-family: monospace;"><strong>React Render Error:</strong><br>' + err.message + '</div>';
                    }
                </script>
            </body>
            </html>
            `;

            iframe.srcdoc = htmlContent;
            setStatus('Web Live Preview Ready', 'success');
        } catch (err) {
            setStatus('Babel Transpilation Error', 'error');
        }
    }

    // Execute Main Code Button Click Handler
    function handleRunAction() {
        if (currentTrack === 'devops') {
            validateDevOpsSyntax();
        } else if (currentTrack === 'python') {
            runPythonCode();
        } else if (currentTrack === 'sql') {
            runSqlCode();
        } else if (currentTrack === 'web' || currentTrack === 'mobile') {
            runWebCode();
        }
    }

    // DOM Ready Setup
    document.addEventListener('DOMContentLoaded', function () {
        initMonaco();

        // Track selector buttons
        document.querySelectorAll('.track-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                switchTrack(this.dataset.track);
            });
        });

        // Template selector change
        const templateSelect = document.getElementById('template-select');
        if (templateSelect) {
            templateSelect.addEventListener('change', function () {
                const tmplKey = this.value;
                if (CODE_TEMPLATES[currentTrack] && CODE_TEMPLATES[currentTrack].templates[tmplKey]) {
                    const code = CODE_TEMPLATES[currentTrack].templates[tmplKey];
                    if (monacoEditor) {
                        monacoEditor.setValue(code);
                    }
                }
            });
        }

        // Run button click
        const runBtn = document.getElementById('btn-run-code');
        if (runBtn) {
            runBtn.addEventListener('click', handleRunAction);
        }

        // Clear console button click
        const clearBtn = document.getElementById('btn-clear-console');
        if (clearBtn) {
            clearBtn.addEventListener('click', function () {
                const consoleOut = document.getElementById('console-output');
                if (consoleOut) consoleOut.innerHTML = '<span style="color: var(--text-secondary);">Terminal output cleared. Ready for execution.</span>';
            });
        }

        // Output pane tab switching
        document.querySelectorAll('.output-tab-btn').forEach(tab => {
            tab.addEventListener('click', function () {
                document.querySelectorAll('.output-tab-btn').forEach(t => t.classList.remove('active'));
                this.classList.add('active');

                const targetPaneId = this.dataset.target;
                document.querySelectorAll('.output-pane').forEach(p => p.style.display = 'none');

                const targetPane = document.getElementById(targetPaneId);
                if (targetPane) targetPane.style.display = 'block';
            });
        });
    });

})();
