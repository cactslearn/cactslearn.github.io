# resource_code_snippets.py - Technical snippets and authority references for CACTS resource pages

CODE_SNIPPETS_DATA = {
    "what-is-apache-spark": {
        "code_snippet": {
            "title": "Example PySpark DataFrame Operations",
            "language": "python",
            "code": """from pyspark.sql import SparkSession

# Initialize Spark session on cluster
spark = SparkSession.builder \\
    .appName("CACTSBigDataSession") \\
    .getOrCreate()

# Load sales CSV from HDFS or S3
df = spark.read.csv("hdfs:///data/sales_pune.csv", header=True, inferSchema=True)

# Run in-memory aggregation queries
df.filter(df["revenue"] > 15000) \\
  .groupBy("category") \\
  .sum("revenue") \\
  .show()"""
        },
        "official_doc": {
            "label": "Official Apache Spark Documentation",
            "url": "https://spark.apache.org/docs/latest/"
        },
        "internal_links": [
            {"label": "Spark vs Hadoop", "url": "spark-vs-hadoop.html", "context": "Understand the architectural differences between in-memory computation and distributed file systems in our side-by-side comparison."},
            {"label": "Beginner to Data Engineer Roadmap", "url": "beginner-to-data-engineer-roadmap.html", "context": "See how learning Apache Spark fits into your long-term data engineering learning timeline."}
        ]
    },
    "what-is-kafka": {
        "code_snippet": {
            "title": "Kafka CLI Commands for Partition & Message Ingestion",
            "language": "bash",
            "code": """# Start the Kafka event broker daemon
bin/kafka-server-start.sh config/server.properties

# Create a multi-partition topic for IoT clickstream events
bin/kafka-topics.sh --create --topic clickstream-events \\
    --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092

# Listen to the event stream in real-time from console consumer
bin/kafka-console-consumer.sh --topic clickstream-events \\
    --from-beginning --bootstrap-server localhost:9092"""
        },
        "official_doc": {
            "label": "Official Apache Kafka Documentation",
            "url": "https://kafka.apache.org/documentation/"
        },
        "internal_links": [
            {"label": "Data Engineering Project Ideas", "url": "data-engineering-project-ideas.html", "context": "Discover how to build real-time event streaming pipelines using Kafka as a message broker in our project blueprint guides."}
        ]
    },
    "what-is-docker": {
        "code_snippet": {
            "title": "Production Node.js Dockerfile Setup",
            "language": "dockerfile",
            "code": """# Use a lightweight official parent container
FROM node:18-alpine

# Configure working directory
WORKDIR /usr/src/app

# Pre-install dependencies to leverage cached layers
COPY package*.json ./
RUN npm ci --only=production

# Copy application files
COPY . .

# Expose microservice port and define entry point
EXPOSE 3000
CMD [ "node", "index.js" ]"""
        },
        "official_doc": {
            "label": "Official Docker Documentation",
            "url": "https://docs.docker.com/get-started/"
        },
        "internal_links": [
            {"label": "Docker vs Kubernetes", "url": "docker-vs-kubernetes.html", "context": "Learn when to stick with single-host Docker containers and when to switch to Kubernetes container orchestrators."},
            {"label": "Beginner to DevOps Engineer Roadmap", "url": "beginner-to-devops-engineer-roadmap.html", "context": "Explore how containerization skills act as a foundational milestone in our structured DevOps learning plan."}
        ]
    },
    "what-is-kubernetes": {
        "code_snippet": {
            "title": "Declarative YAML Manifest for a Pod Deployment",
            "language": "yaml",
            "code": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: cacts-web-deployment
  labels:
    app: secure-web
spec:
  replicas: 3 # Tells Kubernetes to run 3 active redundant instances
  selector:
    matchLabels:
      app: secure-web
  template:
    metadata:
      labels:
        app: secure-web
    spec:
      containers:
      - name: nginx-web
        image: nginx:alpine
        ports:
        - containerPort: 80"""
        },
        "official_doc": {
            "label": "Official Kubernetes Documentation",
            "url": "https://kubernetes.io/docs/home/"
        },
        "internal_links": [
            {"label": "Docker vs Kubernetes", "url": "docker-vs-kubernetes.html", "context": "Read our direct analysis comparing container isolation on a single machine with container orchestration across cloud clusters."}
        ]
    },
    "what-is-jenkins": {
        "code_snippet": {
            "title": "Declarative Jenkins Pipeline Configuration (Jenkinsfile)",
            "language": "groovy",
            "code": """pipeline {
    agent any
    stages {
        stage('Repository Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/cacts/sample-api.git'
            }
        }
        stage('Unit Testing') {
            steps {
                sh 'npm run test'
            }
        }
        stage('Containerize & Deploy') {
            steps {
                sh 'docker build -t cacts-api:latest .'
                sh 'docker run -d -p 8080:8080 cacts-api:latest'
            }
        }
    }
}"""
        },
        "official_doc": {
            "label": "Official Jenkins Documentation",
            "url": "https://www.jenkins.io/doc/"
        },
        "internal_links": [
            {"label": "Jenkins vs GitHub Actions", "url": "jenkins-vs-github-actions.html", "context": "Read our comparative analysis evaluating self-hosted Jenkins automation servers against cloud-native GitHub Actions."}
        ]
    },
    "what-is-terraform": {
        "code_snippet": {
            "title": "AWS EC2 Infrastructure Provisioning Manifest (HCL)",
            "language": "hcl",
            "code": """# Configure provider requirements
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1" # Mumbai local region
}

# Deploy an Ubuntu server instance automatically
resource "aws_instance" "pune_staging" {
  ami           = "ami-03f4878755434977f"
  instance_type = "t2.micro"

  tags = {
    Name = "CACTS-Pune-DevOps-Staging"
  }
}"""
        },
        "official_doc": {
            "label": "Official Terraform Documentation",
            "url": "https://developer.hashicorp.com/terraform/docs"
        },
        "internal_links": [
            {"label": "Best DevOps Certifications", "url": "best-devops-certifications.html", "context": "Check out where the HashiCorp Certified Terraform Associate rank falls in our industry-accredited certifications index."}
        ]
    },
    "what-is-power-bi": {
        "code_snippet": {
            "title": "DAX Calculation for Year-to-Date Net Sales",
            "language": "dax",
            "code": """// DAX Measure to sum sales amounts over the calendar year
TotalSalesYTD = 
CALCULATE(
    SUM(Sales[Amount]),
    DATESYTD(Calendar[Date])
)"""
        },
        "official_doc": {
            "label": "Official Microsoft Power BI Docs",
            "url": "https://learn.microsoft.com/en-us/power-bi/"
        },
        "internal_links": [
            {"label": "Power BI vs Tableau", "url": "power-bi-vs-tableau.html", "context": "Examine how Microsoft Power BI's DAX formula engine measures up against Tableau's visual calculation features."}
        ]
    },
    "what-is-hadoop": {
        "code_snippet": {
            "title": "HDFS File Management Shell Operations",
            "language": "bash",
            "code": """# Create a partitioned analytics folder structure on HDFS
hdfs dfs -mkdir -p /analytics/cacts/input

# Transfer local data lake CSV from local machine to Hadoop
hdfs dfs -put client_records.csv /analytics/cacts/input/

# Read files and verify HDFS directory structures
hdfs dfs -ls /analytics/cacts/input/"""
        },
        "official_doc": {
            "label": "Official Apache Hadoop Documentation",
            "url": "https://hadoop.apache.org/docs/stable/"
        },
        "internal_links": [
            {"label": "Spark vs Hadoop", "url": "spark-vs-hadoop.html", "context": "Understand the performance advantages of Spark's RAM-based model over MapReduce's disk operations."}
        ]
    },
    "java-vs-python": {
        "code_snippet": {
            "title": "Side-by-Side Object Definition Comparison",
            "language": "java",
            "code": """// Java class syntax (Static Typing)
public class Dev {
    private String name;
    public Dev(String name) { this.name = name; }
    public void hello() { System.out.println("Hello, " + name); }
}

# Python class syntax (Dynamic Typing)
class Dev:
    def __init__(self, name):
        self.name = name
    def hello(self):
        print(f"Hello, {self.name}")"""
        },
        "official_doc": {
            "label": "Official Java & Python Sites",
            "url": "https://docs.oracle.com/"
        },
        "internal_links": [
            {"label": "Java Fullstack Project Ideas", "url": "java-fullstack-project-ideas.html", "context": "Explore full stack projects you can build using Java for enterprise-grade backend stability."}
        ]
    },
    "power-bi-vs-tableau": {
        "code_snippet": {
            "title": "Aggregations comparison (DAX vs Tableau Calculated Fields)",
            "language": "dax",
            "code": """// Power BI: DAX Measure
GrossProfitMargin = DIVIDE(SUM(Transactions[Profit]), SUM(Transactions[Revenue]), 0)

// Tableau: Calculated Field
SUM([Profit]) / SUM([Revenue])"""
        },
        "official_doc": {
            "label": "Power BI & Tableau Help Desks",
            "url": "https://learn.microsoft.com/en-us/power-bi/"
        },
        "internal_links": [
            {"label": "Power BI Dashboard Ideas", "url": "power-bi-dashboard-ideas.html", "context": "Get dashboard design templates and blueprints for professional data portfolios."}
        ]
    },
    "docker-vs-kubernetes": {
        "code_snippet": {
            "title": "Infrastructure Formats (Dockerfile vs Kubernetes YAML Pod)",
            "language": "dockerfile",
            "code": """# Dockerfile: Build environment
FROM alpine:latest
RUN apk update && apk add curl
CMD ["curl", "https://cactslearn.github.io"]

# Kubernetes YAML Pod manifest: Coordinates replicas
apiVersion: v1
kind: Pod
metadata:
  name: curl-pod
spec:
  containers:
  - name: curl-container
    image: custom-curl-app:latest"""
        },
        "official_doc": {
            "label": "Docker & Kubernetes Documentation Portals",
            "url": "https://kubernetes.io/"
        },
        "internal_links": [
            {"label": "what-is-docker.html", "url": "what-is-docker.html", "context": "Read our comprehensive glossary entry detailing Docker containers, images, and layers."},
            {"label": "what-is-kubernetes.html", "url": "what-is-kubernetes.html", "context": "Read our detailed introduction to Kubernetes cluster nodes and self-healing pods."}
        ]
    },
    "spark-vs-hadoop": {
        "code_snippet": {
            "title": "Data Processing Methods (PySpark vs Java MapReduce)",
            "language": "python",
            "code": """# Apache Spark DataFrame aggregation (In-Memory Processing)
df.groupBy("year").avg("salary").write.parquet("hdfs://...")

// Java MapReduce Map Function (Disk-bound pipeline setup)
public void map(LongWritable key, Text value, Context context) throws IOException {
    String[] parts = value.toString().split(",");
    context.write(new Text(parts[0]), new IntWritable(Integer.parseInt(parts[1])));
}"""
        },
        "official_doc": {
            "label": "Spark & Hadoop Homepages",
            "url": "https://spark.apache.org/"
        },
        "internal_links": [
            {"label": "what-is-apache-spark.html", "url": "what-is-apache-spark.html", "context": "Get introduced to Apache Spark architecture and its speed advantages over standard databases."},
            {"label": "what-is-hadoop.html", "url": "what-is-hadoop.html", "context": "Learn about HDFS file storage nodes, clusters, and MapReduce processing structures."}
        ]
    },
    "aws-vs-azure": {
        "code_snippet": {
            "title": "Cloud Instance Provisioning (AWS CLI vs Azure CLI)",
            "language": "bash",
            "code": """# AWS CLI: Boot instance
aws ec2 run-instances --image-id ami-03f4878755434977f --instance-type t2.micro

# Azure CLI: Boot VM instance
az vm create --resource-group cacts-rg --name staging-vm --image Ubuntu2204 --generate-ssh-keys"""
        },
        "official_doc": {
            "label": "AWS & Azure Resource Documentation",
            "url": "https://docs.aws.amazon.com"
        },
        "internal_links": [
            {"label": "Cloud Training", "url": "cloud-training.html", "context": "Read detailed training courses for learning enterprise cloud networks."}
        ]
    },
    "jenkins-vs-github-actions": {
        "code_snippet": {
            "title": "CI Job Pipelines (Jenkinsfile vs GitHub Actions YAML Workflow)",
            "language": "groovy",
            "code": """// Jenkinsfile pipeline script
stage('Test') { steps { sh 'npm test' } }

# GitHub Actions pipeline workflow (.github/workflows/main.yml)
jobs:
  run-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - run: npm install && npm test"""
        },
        "official_doc": {
            "label": "Jenkins & GitHub Actions Documentations",
            "url": "https://www.jenkins.io/doc/"
        },
        "internal_links": [
            {"label": "what-is-jenkins.html", "url": "what-is-jenkins.html", "context": "Learn more about Jenkins pipelines and plugins in our Jenkins glossary page."}
        ]
    },
    "react-js-project-ideas": {
        "code_snippet": {
            "title": "Interactive Kanban Task Shift Logic (React Hooks)",
            "language": "javascript",
            "code": """import React, { useState } from 'react';

export function KanbanBoard() {
  const [tasks, setTasks] = useState([
    { id: 1, title: 'Configure Redux Store', stage: 'todo' },
    { id: 2, title: 'Integrate Axios Client', stage: 'in_progress' }
  ]);

  const moveTask = (taskId, targetStage) => {
    setTasks(tasks.map(task => 
      task.id === taskId ? { ...task, stage: targetStage } : task
    ));
  };

  return (
    <div style={{ display: 'flex', gap: '1rem' }}>
      {/* Board columns and card rendering logic */}
    </div>
  );
}"""
        },
        "official_doc": {
            "label": "Official React JS Documentation",
            "url": "https://react.dev/"
        },
        "internal_links": [
            {"label": "React JS Training", "url": "react-js-training.html", "context": "Learn React state management and modular design in our dedicated frontend syllabus."},
            {"label": "React JS Roadmap", "url": "react-js-roadmap.html", "context": "See how project milestones fit into your frontend career trajectory."}
        ]
    },
    "react-native-project-ideas": {
        "code_snippet": {
            "title": "Expo Location GPS coordinates Logger (React Native)",
            "language": "javascript",
            "code": """import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';
import * as Location from 'expo-location';

export default function GeoTracker() {
  const [location, setLocation] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const getCoordinates = async () => {
    let { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      setErrorMsg('Permission to access location was denied');
      return;
    }
    let loc = await Location.getCurrentPositionAsync({});
    setLocation(loc.coords);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>GPS Logger</Text>
      <Button title="Get Position" onPress={getCoordinates} />
      {location && <Text>Lat: {location.latitude}, Lon: {location.longitude}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' }
});"""
        },
        "official_doc": {
            "label": "Official React Native Documentation",
            "url": "https://reactnative.dev/"
        },
        "internal_links": [
            {"label": "React Native Training", "url": "react-native-training.html", "context": "Learn device camera, GPS, and push notification integrations in our hands-on course."},
            {"label": "React Native Roadmap", "url": "react-native-roadmap.html", "context": "Check the mobile development phases from configuration to store deployment."}
        ]
    },
    "react-vs-angular": {
        "code_snippet": {
            "title": "Profile Fetching (React useState/useEffect vs Angular TypeScript Component)",
            "language": "javascript",
            "code": """// React (Functional Component with Lifecycle Hook)
function Profile({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch(`/api/user/${userId}`).then(res => res.json()).then(setUser);
  }, [userId]);
  return <div>{user?.name}</div>;
}

// Angular (TypeScript Component with Dependency Injection)
@Component({
  selector: 'app-profile',
  template: `<div>{{ user?.name }}</div>`
})
export class ProfileComponent implements OnInit {
  @Input() userId!: string;
  user: any;
  constructor(private http: HttpClient) {}
  ngOnInit() {
    this.http.get(`/api/user/${this.userId}`).subscribe(data => this.user = data);
  }
}"""
        },
        "official_doc": {
            "label": "React & Angular Documentation Guides",
            "url": "https://angular.dev/"
        },
        "internal_links": [
            {"label": "React JS Project Ideas", "url": "react-js-project-ideas.html", "context": "Check frontend app ideas you can build to master React Hooks and state management."}
        ]
    },
    "react-native-vs-flutter": {
        "code_snippet": {
            "title": "Basic Container Styling (React Native Flexbox vs Flutter Widgets)",
            "language": "javascript",
            "code": """// React Native: JavaScript Styling objects mapping to host views
<View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
  <Text style={{ fontSize: 16 }}>React Native Container</Text>
</View>

// Flutter: Dart Widget layout rendering via custom graphics engine
Widget build(BuildContext context) {
  return Center(
    child: Text(
      'Flutter Container',
      style: TextStyle(fontSize: 16),
    ),
  );
}"""
        },
        "official_doc": {
            "label": "React Native & Flutter Developers Homes",
            "url": "https://flutter.dev"
        },
        "internal_links": [
            {"label": "React Native Project Ideas", "url": "react-native-project-ideas.html", "context": "Explore mobile application blueprints incorporating local SQLite and hardware APIs."}
        ]
    }
}

