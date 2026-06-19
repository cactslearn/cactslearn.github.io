# course_assets.py - Technical implementation previews (code snippets & schemas) for CACTS courses

COURSE_ASSETS_DATA = {
    "java-full-stack-developer-training": {
        "code_title": "Spring Boot REST Controller with Security Integration",
        "lang": "java",
        "code": """@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {
    private final OrderService orderService;
    
    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }
    
    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(
        @Valid @RequestBody OrderRequest req,
        @AuthenticationPrincipal UserPrincipal user
    ) {
        OrderResponse response = orderService.process(req, user.getId());
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}""",
        "schema_title": "Enterprise Java Microservices Architecture",
        "schema": """[Client App] --> (React Frontend / Axios API Calls)
                    |
                    v
[API Gateway] (Spring Cloud Gateway / JWT Authentication)
                    |
       +------------+------------+
       |                         |
       v                         v
[Order-Service]           [Payment-Service]
(Spring Boot REST API)    (Spring Boot Microservice)
       |                         |
       v                         v
[MySQL Database]          [Stripe Payment API]
(Orders star schema)"""
    },
    "full-stack-development-training": {
        "code_title": "Express.js Router with MongoDB Aggregation Pipeline",
        "lang": "javascript",
        "code": """const router = require('express').Router();
const Order = require('../models/Order');
const auth = require('../middleware/auth');

router.get('/revenue-report', auth, async (req, res) => {
  try {
    const report = await Order.aggregate([
      { $match: { status: 'completed' } },
      { $group: { _id: '$productId', totalRev: { $sum: '$price' } } }
    ]);
    res.json(report);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});""",
        "schema_title": "MERN Stack NoSQL Document Schema Mapping",
        "schema": """+---------------------------------------------+
|               User Document                 |
| _id: ObjectId (PK)                          |
| name: String                                |
| email: String (Unique)                      |
| role: String (default: 'student')           |
+---------------------+-----------------------+
                      | (1-to-Many Relationship)
                      v
+---------------------+-----------------------+
|              Order Document                 |
| _id: ObjectId (PK)                          |
| userId: ObjectId (FK -> User)               |
| productId: String                           |
| status: String ('pending', 'completed')     |
+---------------------------------------------+"""
    },
    "ai-machine-learning-training": {
        "code_title": "Scikit-Learn Predictive Model Pipeline with Scaling",
        "lang": "python",
        "code": """from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Define ML Pipeline with feature scaling & classifier
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Fit train dataset
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)""",
        "schema_title": "Machine Learning Pipeline & Random Forest Architecture",
        "schema": """[Input Vector] (Raw features: pricing, dimensions, etc.)
       |
       v
[StandardScaler] (Normalize feature distributions)
       |
       v
[RandomForestClassifier] (Ensemble of 100 Decision Trees)
       |
  +----+----+
  |    |    |
 [T1] [T2] [T3] ... (Parallel Tree Voting Evaluation)
  |    |    |
  +----+----+
       |
       v
[ArgMax Output] (Final Ensemble Predicted Classification)"""
    },
    "data-science-training": {
        "code_title": "Pandas Data Cleaning Pipeline & Outlier Filtering",
        "lang": "python",
        "code": """import pandas as pd
import numpy as np

def clean_sales_data(filepath):
    df = pd.read_csv(filepath)
    # Filter missing revenue records
    df = df.dropna(subset=['revenue'])
    # Remove outliers using Interquartile Range (IQR) method
    q1, q3 = df['amount'].quantile([0.25, 0.75])
    iqr = q3 - q1
    df = df[~((df['amount'] < (q1 - 1.5 * iqr)) | (df['amount'] > (q3 + 1.5 * iqr)))]
    return df""",
        "schema_title": "Dimensional Star Schema Modeling (MySQL / BI)",
        "schema": """+---------------------------+     +---------------------------+
|      DimCustomers         |     |        DimProducts        |
| CustomerID (PK)           |     | ProductID (PK)            |
| Name                      |     | ProductName               |
| City                      |     | UnitPrice                 |
+------------+--------------+     +-------------+-------------+
             | (1)                              | (1)
             |                                  |
             |             +-----+              |
             +------------>| (*) |<-------------+
                           | FactSales          |
                           | SalesID (PK)       |
                           | CustomerID (FK)    |
                           | ProductID (FK)     |
                           | Quantity           |
                           | Revenue            |
                           +--------------------+"""
    },
    "data-engineering-training": {
        "code_title": "PySpark ETL Job with Schema Parsing & Parquet Write",
        "lang": "python",
        "code": """from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

schema = StructType([
    StructField("user_id", StringType(), False),
    StructField("page", StringType(), True),
    StructField("latency", DoubleType(), True)
])

spark = SparkSession.builder.appName("ETLPipeline").getOrCreate()
df = spark.read.schema(schema).json("s3a://raw-logs/*.json")
df.write.partitionBy("page").parquet("s3a://data-lake/processed/")""",
        "schema_title": "Modern Cloud Data Lakehouse System Architecture",
        "schema": """[Raw JSON Feeds] (S3 Landing Zone / Web Logs)
       |
       v
[Apache Spark] (PySpark ETL Transformations Worker)
       |
       v
[Data Lakehouse] (Optimized Parquet files partitioned by page)
       |
       v
[AWS Glue / Redshift] (Analytical Star Schema Warehouse)
       |
       v
[BI Dashboards] (Power BI / Business Reports)"""
    },
    "python-programming-training": {
        "code_title": "Python Object-Oriented Class with JSON Serialization",
        "lang": "python",
        "code": """import json

class Employee:
    def __init__(self, emp_id, name, salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary
        
    def to_json(self):
        return json.dumps(self.__dict__)

# Custom error handling block
class InvalidSalaryException(Exception):
    pass""",
        "schema_title": "Object-Oriented Programming (OOP) Class Inheritance Diagram",
        "schema": """        +----------------------------+
        |          Employee          |  (Base Class)
        +----------------------------+
        | - emp_id: int              |
        | - name: str                |
        | - salary: float            |
        +----------------------------+
        | + to_json() -> str         |
        +-------------+--------------+
                      |
                      v (Inherits / Extends)
        +----------------------------+
        |          Manager           |
        +----------------------------+
        | - department: str          |
        +----------------------------+"""
    },
    "power-bi-training": {
        "code_title": "Advanced DAX Running Total over Dates Calendar",
        "lang": "dax",
        "code": """// DAX Running Total for Financial Reports
SalesRunningTotal = 
CALCULATE(
    SUM('FactSales'[Revenue]),
    FILTER(
        ALLSELECTED('DimDate'),
        'DimDate'[Date] <= MAX('DimDate'[Date])
    )
)""",
        "schema_title": "Data Modeling Relationship Schema (Star Schema)",
        "schema": """+-------------------+           +-------------------+
|      DimDate      |           |     FactSales     |
| DateKey (PK)      | (1)   (*) | SalesID (PK)      |
| Date              |---------->| DateKey (FK)      |
| Month             |           | ProductID (FK)    |
| Year              |           | Revenue           |
+-------------------+           +-------------------+"""
    },
    "cloud-computing-training": {
        "code_title": "Terraform Infrastructure as Code (VPC & Subnet)",
        "lang": "hcl",
        "code": """resource "aws_vpc" "custom_vpc" {
  cidr_block = "10.0.0.0/16"
  tags       = { Name = "CACTS-VPC" }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.custom_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}""",
        "schema_title": "3-Tier AWS High-Availability VPC Architecture",
        "schema": """+-------------------------------------------------------------+
|                       AWS Cloud VPC                         |
|  +-------------------------------------------------------+  |
|  |                    Public Subnet                      |  |
|  |  [Internet Gateway] <-> [ELB Load Balancer]           |  |
|  +---------------------------+---------------------------+  |
|                              |                              |
|  +---------------------------v---------------------------+  |
|  |                    Private Subnet                     |  |
|  |  [EC2 Instance 1]         [EC2 Instance 2]            |  |
|  |  (Application Cluster behind Auto-Scaling Group)       |  |
|  +---------------------------+---------------------------+  |
+------------------------------|------------------------------+
                               v
                       [RDS Database]"""
    },
    "devops-training": {
        "code_title": "Kubernetes Pod Deployment Configurations (YAML)",
        "lang": "yaml",
        "code": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: main
        image: cacts-api:v1.2
        ports:
        - containerPort: 8080""",
        "schema_title": "CI/CD Deployment Automation Infrastructure pipeline",
        "schema": """[Developer Commits] --> [GitHub Repository]
                               | (Webhook)
                               v
                       [Jenkins Pipeline]
                               | (Builds Docker Image)
                               v
                     [Docker Registry] (ECR)
                               | (Rollout Update)
                               v
                    [Kubernetes Cluster]
             +-----------------+-----------------+
             |                 |                 |
         [Pod Replica 1]   [Pod Replica 2]   [Pod Replica 3]"""
    },
    "software-testing-training": {
        "code_title": "Selenium WebDriver Page Object Model Pattern (Java)",
        "lang": "java",
        "code": """public class LoginPage {
    private WebDriver driver;
    private By usernameField = By.id("user_login");
    private By loginBtn = By.id("submit_btn");
    
    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }
    
    public void submitCredentials(String user) {
        driver.findElement(usernameField).sendKeys(user);
        driver.findElement(loginBtn).click();
    }
}""",
        "schema_title": "Automation Testing Suite Execution Stack",
        "schema": """       [TestRunner (JUnit / TestNG)]
                    | (Triggers execution)
                    v
    [Test Classes (e.g. LoginTest.java)]
                    | (Calls methods from page objects)
                    v
     [Page Object Classes (LoginPage.java)]
                    | (Identifies elements / performs actions)
                    v
  [Selenium WebDriver] <--> [Browser Driver] <--> [Web Browser]"""
    },
    "cybersecurity-training": {
        "code_title": "Python Custom Network Port Scanner for SecAuditing",
        "lang": "python",
        "code": """import socket

def audit_ports(target_host, ports):
    print(f"Auditing security perimeter for: {target_host}")
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target_host, port))
        if result == 0:
            print(f"WARNING: Port {port} is OPEN / Vulnerable!")
        s.close()""",
        "schema_title": "Threat Modeling and Zero-Trust Network Boundaries",
        "schema": """[External Web Traffic]
         |
         v
 [WAF / Firewall] (Port Audit Filtering)
         |
         v
[Application Gateway] (JWT Access Tokens Verify)
         |
    +----+----+ (Internal Virtual Network)
    |         |
    v         v
[Server]   [Database]
(Port 80)  (Port 3306 - Firewalled / Restricted access)"""
    }
}
