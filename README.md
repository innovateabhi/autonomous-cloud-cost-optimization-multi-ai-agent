# Autonomous Cloud Cost Optimization Through Multi-Agent AI Systems

An intelligent cloud cost optimization platform that automatically discovers AWS resources, collects utilization and cost data, analyzes resource efficiency using multiple AI agents, generates optimization recommendations, performs risk assessment, and presents the results through a web-based dashboard.

---

## 📌 Project Overview

Cloud infrastructure can become expensive when resources are:

- Underutilized
- Over-provisioned
- Running unnecessarily
- Using inefficient instance types
- Generating unexpected costs
- Not being monitored continuously

This project addresses these problems using an **autonomous multi-agent AI architecture**.

The system connects to AWS and PostgreSQL, collects cloud resource information and monitoring metrics, retrieves AWS billing information, analyzes resource utilization, estimates optimization opportunities, evaluates risks, and generates AI-powered recommendations using a local LLM through Ollama.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Automatically discover AWS EC2 resources.
2. Store discovered resources in PostgreSQL.
3. Collect EC2 utilization metrics from Amazon CloudWatch.
4. Collect AWS cost information using AWS Cost Explorer.
5. Attribute AWS costs to individual resources whenever AWS provides resource-level billing data.
6. Analyze CPU utilization.
7. Identify underutilized cloud resources.
8. Generate optimization recommendations.
9. Perform risk assessment before recommending actions.
10. Simulate/prepare execution decisions.
11. Generate natural-language recommendations using a local LLM.
12. Store analysis and audit information.
13. Provide a web dashboard for monitoring the entire system.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │        AWS Cloud      │
                         │                      │
                         │  EC2 Instances       │
                         │  CloudWatch          │
                         │  Cost Explorer       │
                         └──────────┬───────────┘
                                    │
                                    │ AWS API
                                    ▼
                         ┌──────────────────────┐
                         │    AWS Data Layer    │
                         │                      │
                         │ EC2 Discovery        │
                         │ CloudWatch Metrics   │
                         │ Cost Explorer        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      PostgreSQL      │
                         │                      │
                         │ Resources            │
                         │ Metrics              │
                         │ Costs                │
                         │ Recommendations      │
                         │ Audit Logs           │
                         └──────────┬───────────┘
                                    │
                                    ▼
                  ┌────────────────────────────────────┐
                  │       Multi-Agent AI System        │
                  │                                    │
                  │ Utilization Agent                  │
                  │ Optimization Agent                 │
                  │ Risk Agent                         │
                  │ Execution Agent                    │
                  │ LLM Recommendation Agent           │
                  └────────────────┬───────────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │   Ollama Local LLM   │
                         │                      │
                         │ Qwen / Other Model   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Flask Dashboard    │
                         │                      │
                         │ Resources            │
                         │ CPU Metrics          │
                         │ Costs                │
                         │ Recommendations      │
                         │ Risk                  │
                         │ Audit Logs            │
                         └──────────────────────┘
```

---

# 🧠 Multi-Agent Architecture

The project uses multiple specialized agents.

## 1. Utilization Agent

Analyzes resource utilization metrics.

Currently the primary metric is:

```text
CPUUtilization
```

The agent determines whether a resource appears:

* Healthy
* Underutilized
* Overutilized
* Unknown

---

## 2. Optimization Agent

Uses resource information, utilization information, and cost information to determine possible optimization actions.

Example recommendations:

```text
Downsize instance
Change instance type
Stop unused resource
Review resource
Keep current configuration
```

---

## 3. Risk Agent

Evaluates the potential risk associated with an optimization recommendation.

Possible risk levels include:

```text
LOW
MEDIUM
HIGH
```

The risk analysis helps prevent aggressive automated changes to production resources.

---

## 4. Execution Agent

Determines what action should be taken based on:

* Optimization recommendation
* Risk level
* Resource state
* Execution policy

The project is designed so that real AWS execution can be integrated safely in future versions.

---

## 5. LLM Recommendation Agent

The LLM agent converts the technical analysis into a human-readable recommendation.

The project uses **Ollama** so that the LLM can run locally without requiring a paid OpenAI API.

---

# 🛠️ Technology Stack

## Cloud

* Amazon Web Services
* Amazon EC2
* Amazon CloudWatch
* AWS Cost Explorer
* AWS IAM

## Backend

* Python
* Flask
* SQLAlchemy
* boto3
* psycopg

## Database

* PostgreSQL

## AI

* Multi-Agent Architecture
* Ollama
* Qwen / compatible local LLM

## Frontend

* HTML
* CSS
* JavaScript
* Flask Templates

## Development Environment

* Linux
* Fedora / RHEL / Ubuntu
* Python Virtual Environment
* Git
* GitHub

---

# 📁 Project Structure

```text
autonomous-cloud-cost-optimization/
│
├── app/
│   │
│   ├── agents/
│   │   ├── utilization_agent.py
│   │   ├── optimization_agent.py
│   │   ├── risk_agent.py
│   │   ├── execution_agent.py
│   │   └── llm_agent.py
│   │
│   ├── aws/
│   │   ├── ec2.py
│   │   ├── cloudwatch.py
│   │   └── cost_explorer.py
│   │
│   ├── database/
│   │   ├── models.py
│   │   ├── session.py
│   │   │
│   │   └── repositories/
│   │       ├── resource_repository.py
│   │       ├── metrics_repository.py
│   │       └── cost_repository.py
│   │
│   ├── services/
│   │   ├── resource_service.py
│   │   ├── analysis_service.py
│   │   ├── cost_service.py
│   │   └── cost_attribution_service.py
│   │
│   ├── config.py
│   └── ...
│
├── dashboard/
│   │
│   ├── app.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       └── js/
│
├── tests/
│   ├── test_agents.py
│   └── test_llm.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# ⚙️ Prerequisites

Before starting, install the following:

* Python 3.11+
* PostgreSQL
* Git
* AWS Account
* AWS CLI
* Ollama
* Internet connection

Linux is recommended.

---

# 1. Clone the Repository

Clone the project:

```bash
git clone https://github.com/YOUR_USERNAME/autonomous-cloud-cost-optimization.git
```

Enter the project:

```bash
cd autonomous-cloud-cost-optimization
```

Check the files:

```bash
ls
```

Expected structure:

```text
app
dashboard
tests
README.md
requirements.txt
```

---

# 2. Create Python Virtual Environment

Create the virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Verify:

```bash
which python
```

Expected:

```text
.../autonomous-cloud-cost-optimization/venv/bin/python
```

---

# 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 4. Install Python Dependencies

Install project dependencies:

```bash
pip install -r requirements.txt
```

If the project does not yet have a complete requirements file, install the main packages manually:

```bash
pip install boto3
pip install flask
pip install sqlalchemy
pip install psycopg[binary]
pip install requests
```

---

# 5. Configure PostgreSQL

Install PostgreSQL.

For Fedora:

```bash
sudo dnf install postgresql-server postgresql-contrib -y
```

Initialize PostgreSQL:

```bash
sudo postgresql-setup --initdb
```

Enable PostgreSQL:

```bash
sudo systemctl enable postgresql
```

Start PostgreSQL:

```bash
sudo systemctl start postgresql
```

Check status:

```bash
sudo systemctl status postgresql
```

---

# 6. Create PostgreSQL Database

Switch to the PostgreSQL user:

```bash
sudo -u postgres psql
```

Create the database:

```sql
CREATE DATABASE cloud_optimizer;
```

Create the application user:

```sql
CREATE USER optimizer_user WITH PASSWORD 'YOUR_DATABASE_PASSWORD';
```

Grant permissions:

```sql
GRANT ALL PRIVILEGES ON DATABASE cloud_optimizer TO optimizer_user;
```

Exit:

```sql
\q
```

---

# 7. Test PostgreSQL Connection

Run:

```bash
psql -U optimizer_user -d cloud_optimizer -h localhost
```

Enter the password.

If successful:

```text
cloud_optimizer=>
```

Exit:

```sql
\q
```

---

# 8. Configure AWS

The application requires access to AWS APIs.

The following AWS services are used:

```text
EC2
CloudWatch
Cost Explorer
```

---

# 9. Create AWS IAM User

Create an IAM user specifically for the application.

The user should have permissions required for:

```text
EC2 discovery
CloudWatch metric reading
Cost Explorer access
```

For development/testing, you can use an appropriate IAM policy that allows read-only access to these services.

For production, follow the principle of least privilege and grant only the exact API permissions required.

---

# 10. Configure AWS Credentials

Install AWS CLI if necessary.

Verify installation:

```bash
aws --version
```

Configure credentials:

```bash
aws configure
```

Enter:

```text
AWS Access Key ID
AWS Secret Access Key
Default region name
Default output format
```

Example:

```text
AWS Access Key ID: ********
AWS Secret Access Key: ********
Default region name: ap-south-2
Default output format: json
```

---

# 11. Verify AWS Access

Check the configured identity:

```bash
aws sts get-caller-identity
```

You should receive a response containing:

```json
{
    "UserId": "...",
    "Account": "...",
    "Arn": "..."
}
```

---

# 12. Verify EC2 Access

Run:

```bash
aws ec2 describe-instances --region ap-south-2
```

If your EC2 instances are returned, AWS authentication is working.

---

# 13. Configure the Environment File

Create:

```bash
nano .env
```

Example:

```env
AWS_REGION=ap-south-2

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=cloud_optimizer
DATABASE_USER=optimizer_user
DATABASE_PASSWORD=YOUR_DATABASE_PASSWORD

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3:1.7b
```

Replace:

```text
YOUR_DATABASE_PASSWORD
```

with your PostgreSQL password.

---

# ⚠️ Important Security Rule

Never commit `.env` to GitHub.

Add it to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

Check:

```bash
git status
```

The `.env` file should not appear as a file to commit.

---

# 14. Database Tables

The project uses PostgreSQL tables for storing:

```text
resources
metrics
costs
recommendations
audit_logs
```

Check tables:

```bash
psql -U optimizer_user -d cloud_optimizer -c "\dt"
```

---

# 15. Resources Table

The `resources` table stores discovered AWS resources.

Typical fields include:

```text
id
resource_id
resource_type
name
region
state
instance_type
environment
tags
discovered_at
updated_at
```

Example resource:

```text
resource_id: i-0123456789abcdef
resource_type: EC2
instance_type: t3.micro
state: running
region: ap-south-2
```

---

# 16. EC2 Resource Discovery

The EC2 collector uses boto3 to retrieve EC2 instances.

Run it from the project root:

```bash
python -m app.aws.ec2
```

Do not run:

```bash
python app/aws/ec2.py
```

because Python may not correctly resolve the project-level `app` package.

---

# 17. Verify EC2 Discovery

The collector should print:

```text
Starting EC2 collection...
Found X EC2 instance(s).

✓ Saved: i-xxxxxxxxxxxxxxxxx
✓ Saved: i-yyyyyyyyyyyyyyyyy

EC2 collection completed.
```

---

# 18. Verify Resources in PostgreSQL

Run:

```bash
psql -U optimizer_user -d cloud_optimizer
```

Then:

```sql
SELECT
    id,
    resource_id,
    resource_type,
    name,
    region,
    state,
    instance_type
FROM resources
ORDER BY id;
```

You should see your EC2 instances.

---

# 19. Automatic EC2 Discovery

The dashboard automatically runs EC2 discovery whenever the analysis process starts.

The flow is:

```text
Run Analysis
      ↓
Discover EC2 Instances
      ↓
Update PostgreSQL
      ↓
Analyze Resources
      ↓
Generate AI Recommendations
```

If an existing instance is found, its information is updated instead of creating a duplicate.

If a new instance is created in AWS, the next analysis run discovers it.

---

# 20. CloudWatch Configuration

The application retrieves EC2 metrics from CloudWatch.

Currently supported metrics include:

```text
CPUUtilization
NetworkIn
NetworkOut
```

The primary metric used by the utilization agent is:

```text
CPUUtilization
```

---

# 21. Verify CloudWatch Access

Run:

```bash
aws cloudwatch list-metrics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --region ap-south-2
```

You should see metrics associated with your EC2 instances.

---

# 22. CPU Utilization Collection

The application requests:

```text
Average
Maximum
Minimum
```

CPU utilization values.

The default analysis period is:

```text
24 hours
```

Metrics are collected using a:

```text
1 hour
```

period.

---

# 23. AWS Cost Explorer

The application uses AWS Cost Explorer to retrieve billing information.

Cost Explorer provides:

```text
Daily costs
Service-level costs
Resource-level costs
```

depending on AWS account configuration and available billing data.

---

# ⚠️ Cost Explorer Data Delay

AWS billing information is not real-time.

New Cost Explorer resource-level billing data can take time to become available.

If resource-level Cost Explorer data has just been enabled, AWS may return:

```text
DataUnavailableException
```

with a message indicating that data is not available yet.

This is an AWS-side data availability issue, not a PostgreSQL or Flask problem.

Wait for AWS billing data to become available and retry the request later.

---

# 24. Service-Level Cost Collection

The project can collect service-level costs using:

```text
get_cost_by_service()
```

Examples of services returned by AWS include:

```text
EC2 - Other
AWS Data Transfer
Amazon Relational Database Service
```

These records are initially stored with:

```text
resource_id = NULL
```

because service-level billing information does not identify an individual EC2 instance.

---

# 25. Resource-Level Cost Attribution

The project also supports AWS Cost Explorer resource-level billing using:

```text
GetCostAndUsageWithResources
```

This allows the application to associate billing information with specific AWS resources when AWS provides that information.

The intended flow is:

```text
AWS Cost Explorer
        ↓
EC2 Resource ARN / Resource ID
        ↓
Match with resources.resource_id
        ↓
Store resource_id in costs
        ↓
Dashboard displays actual cost
```

---

# 26. Why Costs Can Appear as "Not Attributed"

If PostgreSQL contains records like:

```text
resource_id | service      | amount
------------+--------------+--------
NULL        | EC2 - Other  | 0.001234
```

the cost is considered:

```text
UNATTRIBUTED
```

The system cannot safely assign that service-level cost to a particular EC2 instance.

Do not manually divide the cost equally among EC2 instances unless you explicitly want an estimated allocation.

The project distinguishes:

```text
Actual AWS resource-level cost
```

from:

```text
Estimated / allocated cost
```

---

# 27. Verify Cost Data

Run:

```bash
psql -U optimizer_user -d cloud_optimizer
```

Then:

```sql
SELECT *
FROM costs
ORDER BY cost_date DESC
LIMIT 20;
```

Check whether:

```text
resource_id
```

contains a database resource ID.

If it is:

```text
NULL
```

the record is not attributed to a specific resource.

---

# 28. Check Resource IDs

Run:

```sql
SELECT
    id,
    resource_id,
    name,
    instance_type,
    region
FROM resources;
```

Example:

```text
id | resource_id          | name       | instance_type
---+----------------------+------------+--------------
1  | i-0123456789abcdef   | WebServer  | t3.micro
2  | i-0987654321abcdef   | AppServer  | t3.small
```

The AWS resource-level billing system must match the AWS resource identifier to the corresponding record.

---

# 29. Cost Repository

The cost repository provides functions for:

```text
Create cost
Get service costs
Get resource costs
Calculate resource monthly cost
Calculate EC2 service monthly cost
Get unattributed costs
```

The important query for resource-specific cost is:

```python
Cost.resource_id == resource_id
```

---

# 30. Cost Attribution Service

The cost attribution service checks whether costs can be associated with individual EC2 resources.

It separates:

```text
Attributed costs
```

from:

```text
Unattributed costs
```

This allows the dashboard to distinguish actual resource-level billing data from service-level billing data.

---

# 31. Multi-Agent Analysis Flow

The main analysis pipeline is:

```text
PostgreSQL Resources
        ↓
CPU Metrics
        ↓
Utilization Agent
        ↓
Cost Repository
        ↓
Optimization Agent
        ↓
Risk Agent
        ↓
Execution Agent
        ↓
Analysis Result
```

---

# 32. Running Resource Analysis

The analysis service can analyze all resources:

```python
analyze_all_resources(hours=24)
```

It retrieves all resources from PostgreSQL.

Each resource is processed independently.

If analysis fails for one resource, the system continues processing the remaining resources.

---

# 33. Utilization Analysis

For every EC2 instance:

```text
CPU metrics
      ↓
Utilization Agent
      ↓
CPU status
```

Example:

```json
{
    "status": "UNDERUTILIZED"
}
```

---

# 34. Cost Analysis

For each resource, the application attempts to retrieve resource-specific cost.

If actual resource-level cost exists:

```text
Cost Source = RESOURCE_COST
```

If no resource-specific AWS billing record exists, the current project can fall back to a local estimate.

Example:

```text
Cost Source = LOCAL_ESTIMATE
```

This fallback should not be confused with actual AWS billing.

---

# 35. Optimization Analysis

The optimization agent receives:

```text
Resource information
Utilization information
Cost information
```

It then produces an optimization recommendation.

---

# 36. Risk Analysis

The risk agent receives:

```text
Resource
Utilization
Optimization recommendation
```

and determines the risk level.

Example:

```text
LOW
MEDIUM
HIGH
```

---

# 37. Execution Analysis

The execution agent receives:

```text
Resource
Optimization
Risk
```

and determines whether an action should be:

```text
EXECUTE
REVIEW
SKIP
```

The system is designed with safety in mind and should not automatically terminate or modify production infrastructure without an explicit execution policy.

---

# 38. Install Ollama

Install Ollama according to the official installation instructions for your operating system.

After installation, verify:

```bash
ollama --version
```

---

# 39. Start Ollama

Start the Ollama service according to your operating system.

Verify the API:

```bash
curl http://localhost:11434/api/tags
```

A successful response indicates that Ollama is running.

---

# 40. Download the LLM

Example:

```bash
ollama pull qwen3:1.7b
```

Verify:

```bash
ollama list
```

You should see:

```text
qwen3:1.7b
```

---

# 41. Test Ollama

Run:

```bash
ollama run qwen3:1.7b
```

Test a prompt:

```text
Analyze this EC2 resource for cloud cost optimization.
```

Exit the model using:

```text
/bye
```

---

# 42. LLM Configuration

The `.env` configuration is:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3:1.7b
```

You can replace the model with another compatible Ollama model.

---

# 43. Test the LLM Agent

Run:

```bash
python test_llm.py
```

or, if the test is located inside the tests directory:

```bash
python -m pytest tests/test_llm.py
```

---

# 44. Test the Agents

Run:

```bash
python -m pytest tests/test_agents.py
```

If pytest is not installed:

```bash
pip install pytest
```

---

# 45. Start the Dashboard

From the project root:

```bash
python dashboard/app.py
```

The application should display:

```text
AUTONOMOUS CLOUD COST OPTIMIZATION DASHBOARD
```

and:

```text
Dashboard:
http://localhost:5000
```

---

# 46. Open the Dashboard

Open a browser and visit:

```text
http://localhost:5000
```

---

# 47. Dashboard API

The dashboard provides the following APIs.

## Dashboard

```text
GET /api/dashboard
```

Example:

```bash
curl http://localhost:5000/api/dashboard
```

---

## Resources

```text
GET /api/resources
```

Example:

```bash
curl http://localhost:5000/api/resources
```

---

## Recommendations

```text
GET /api/recommendations
```

Example:

```bash
curl http://localhost:5000/api/recommendations
```

---

## Audit Logs

```text
GET /api/audit-logs
```

Example:

```bash
curl http://localhost:5000/api/audit-logs
```

---

## Health Check

```text
GET /api/health
```

Example:

```bash
curl http://localhost:5000/api/health
```

---

## Configuration

```text
GET /api/config
```

Example:

```bash
curl http://localhost:5000/api/config
```

Sensitive information such as the PostgreSQL password is not returned.

---

# 48. Run Analysis from Dashboard

The dashboard provides:

```text
Run Analysis
```

When the button is pressed, the system performs:

```text
1. Discover AWS EC2 instances
2. Update PostgreSQL resources
3. Collect/analyze resource information
4. Retrieve CPU metrics
5. Retrieve available cost information
6. Run Utilization Agent
7. Run Optimization Agent
8. Run Risk Agent
9. Run Execution Agent
10. Run Ollama LLM
11. Generate recommendations
12. Store/return results
13. Refresh dashboard
```

---

# 49. Run Analysis API

The primary endpoint is:

```text
POST /api/run-analysis
```

Example:

```bash
curl -X POST http://localhost:5000/api/run-analysis
```

The project also supports:

```text
POST /api/analyze
```

for frontend compatibility.

---

# 50. Complete Project Workflow

The complete workflow is:

```text
User opens dashboard
        ↓
User clicks "Run Analysis"
        ↓
EC2 Discovery
        ↓
AWS EC2 API
        ↓
New/Existing resources updated
        ↓
PostgreSQL resources table
        ↓
CloudWatch CPU metrics
        ↓
Utilization Agent
        ↓
AWS Cost Explorer
        ↓
Cost Repository
        ↓
Optimization Agent
        ↓
Risk Agent
        ↓
Execution Agent
        ↓
Ollama LLM
        ↓
AI Recommendation
        ↓
Audit Logs
        ↓
Dashboard Refresh
```

---

# 51. Adding a New EC2 Instance

If you launch another EC2 instance in AWS:

```text
AWS EC2
   ↓
Run Analysis
   ↓
EC2 Discovery
   ↓
New instance detected
   ↓
resources table updated
   ↓
Dashboard updated
```

You do not need to manually insert the EC2 instance into PostgreSQL.

---

# 52. Verify New EC2 Instance

After launching an instance:

```bash
aws ec2 describe-instances \
    --region ap-south-2 \
    --query 'Reservations[].Instances[].InstanceId'
```

Then run the dashboard analysis.

Verify PostgreSQL:

```sql
SELECT
    resource_id,
    name,
    instance_type,
    state
FROM resources
ORDER BY id;
```

---

# 53. Dashboard Resource Count

The dashboard calculates:

```text
Total Resources
Running Resources
Stopped Resources
```

based on the PostgreSQL `resources` table.

Therefore:

```text
AWS EC2
   ↓
EC2 collector
   ↓
PostgreSQL
   ↓
Dashboard
```

must be working correctly for resource counts to update.

---

# 54. Audit Logs

The audit log records the analysis process.

Typical information includes:

```text
resource_id
event_type
agent_name
recommendation
priority
risk_level
decision
execution_action
execution_status
estimated_savings
llm_status
llm_model
llm_recommendation
confidence
status
message
created_at
```

Audit logs provide traceability for AI decisions.

---

# 55. Recommendations

Recommendations can include information such as:

```text
Recommendation Type
Current Configuration
Recommended Configuration
Estimated Monthly Savings
Risk Level
Reason
Confidence
Status
```

This allows users to understand why the system recommends a particular optimization.

---

# 56. Database Verification Commands

## View resources

```bash
psql -U optimizer_user -d cloud_optimizer \
-c "SELECT * FROM resources ORDER BY id;"
```

## View metrics

```bash
psql -U optimizer_user -d cloud_optimizer \
-c "SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 20;"
```

## View costs

```bash
psql -U optimizer_user -d cloud_optimizer \
-c "SELECT * FROM costs ORDER BY cost_date DESC LIMIT 20;"
```

## View recommendations

```bash
psql -U optimizer_user -d cloud_optimizer \
-c "SELECT * FROM recommendations ORDER BY created_at DESC LIMIT 20;"
```

## View audit logs

```bash
psql -U optimizer_user -d cloud_optimizer \
-c "SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 20;"
```

---

# 57. Useful PostgreSQL Queries

## Count EC2 resources

```sql
SELECT COUNT(*)
FROM resources
WHERE resource_type = 'EC2';
```

## Show running instances

```sql
SELECT
    resource_id,
    name,
    instance_type,
    region
FROM resources
WHERE state = 'running';
```

## Show stopped instances

```sql
SELECT
    resource_id,
    name,
    instance_type,
    region
FROM resources
WHERE state = 'stopped';
```

## Show unattributed costs

```sql
SELECT
    service,
    cost_date,
    amount
FROM costs
WHERE resource_id IS NULL
ORDER BY cost_date DESC;
```

## Show resource-attributed costs

```sql
SELECT
    resource_id,
    service,
    cost_date,
    amount
FROM costs
WHERE resource_id IS NOT NULL
ORDER BY cost_date DESC;
```

---

# 58. Troubleshooting

## Problem: `ModuleNotFoundError: No module named 'app'`

If you see:

```text
ModuleNotFoundError: No module named 'app'
```

make sure you are in the project root:

```bash
cd autonomous-cloud-cost-optimization
```

Use:

```bash
python -m app.aws.ec2
```

instead of:

```bash
python app/aws/ec2.py
```

---

# 59. Problem: AWS Authentication Error

Test:

```bash
aws sts get-caller-identity
```

If this fails:

```bash
aws configure
```

Verify:

```bash
aws configure list
```

---

# 60. Problem: EC2 Instances Not Appearing

Check:

```bash
aws ec2 describe-instances \
    --region ap-south-2
```

Then run:

```bash
python -m app.aws.ec2
```

Check PostgreSQL:

```sql
SELECT
    resource_id,
    name,
    state
FROM resources;
```

---

# 61. Problem: Dashboard Does Not Show New Instance

Run:

```bash
python -m app.aws.ec2
```

Then verify:

```sql
SELECT
    resource_id,
    name,
    state
FROM resources;
```

If the new instance exists in PostgreSQL but not in the browser, refresh the dashboard.

---

# 62. Problem: CloudWatch CPU Metrics Are Empty

Verify the instance ID:

```bash
aws cloudwatch list-metrics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --region ap-south-2
```

Make sure:

```text
InstanceId
```

matches the EC2 instance.

CloudWatch metrics can also require some time after a new instance starts.

---

# 63. Problem: Cost Shows "Not Attributed"

Check:

```sql
SELECT
    resource_id,
    service,
    cost_date,
    amount
FROM costs
ORDER BY cost_date DESC;
```

If:

```text
resource_id = NULL
```

the cost is currently service-level/unattributed.

Resource-level Cost Explorer data may not yet be available.

Wait for AWS billing data ingestion and retry resource-level cost collection.

---

# 64. Problem: `DataUnavailableException`

Example:

```text
DataUnavailableException:
Data is not available.
Please try to adjust the time period.
If just enabled Cost Explorer,
data might not be ingested yet.
```

This means AWS does not currently have the requested resource-level billing data available.

Possible causes:

* Cost Explorer resource-level data was recently enabled.
* AWS billing data has not finished processing.
* The requested time range does not contain resource-level data.
* AWS has not yet ingested the required billing information.

Wait and retry later.

---

# 65. Problem: PostgreSQL Authentication Failed

Example:

```text
password authentication failed
```

Verify:

```bash
psql -U optimizer_user -d cloud_optimizer -h localhost
```

If necessary, change the PostgreSQL password:

```bash
sudo -u postgres psql
```

Then:

```sql
ALTER USER optimizer_user WITH PASSWORD 'NEW_PASSWORD';
```

Update `.env`:

```env
DATABASE_PASSWORD=NEW_PASSWORD
```

---

# 66. Problem: Ollama Not Running

Check:

```bash
curl http://localhost:11434/api/tags
```

If connection fails, start Ollama.

Then verify:

```bash
ollama list
```

---

# 67. Problem: LLM Model Missing

Run:

```bash
ollama pull qwen3:1.7b
```

Then:

```bash
ollama list
```

Verify `.env`:

```env
OLLAMA_MODEL=qwen3:1.7b
```

---

# 68. Problem: Flask Dashboard Cannot Connect to Database

Check:

```bash
curl http://localhost:5000/api/health
```

The response contains database and Ollama status.

Example:

```json
{
    "status": "healthy",
    "database": true,
    "ollama": true
}
```

If database is:

```json
"database": false
```

check PostgreSQL and `.env`.

---

# 69. Problem: Dashboard Returns HTTP 500

Check the terminal where Flask is running.

The dashboard prints:

```text
DASHBOARD API ERROR
```

followed by the exception.

Also test:

```bash
curl http://localhost:5000/api/dashboard
```

---

# 70. Running the Complete System

Every time you want to work on the project:

## Step 1

Enter the project:

```bash
cd autonomous-cloud-cost-optimization
```

## Step 2

Activate virtual environment:

```bash
source venv/bin/activate
```

## Step 3

Make sure PostgreSQL is running:

```bash
sudo systemctl status postgresql
```

## Step 4

Make sure Ollama is running:

```bash
curl http://localhost:11434/api/tags
```

## Step 5

Verify AWS:

```bash
aws sts get-caller-identity
```

## Step 6

Start dashboard:

```bash
python dashboard/app.py
```

## Step 7

Open:

```text
http://localhost:5000
```

## Step 8

Click:

```text
Run Analysis
```

---

# 71. Development Workflow

The recommended development workflow is:

```text
1. Launch / manage AWS resources
          ↓
2. Run dashboard
          ↓
3. Click Run Analysis
          ↓
4. Discover resources
          ↓
5. Collect CloudWatch metrics
          ↓
6. Collect available AWS costs
          ↓
7. Analyze utilization
          ↓
8. Generate optimization recommendation
          ↓
9. Perform risk analysis
          ↓
10. Generate LLM recommendation
          ↓
11. Store audit information
          ↓
12. Review dashboard
```

---

# 72. Git Workflow

Check changes:

```bash
git status
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Update cloud cost optimization system"
```

Push:

```bash
git push origin main
```

---

# 73. Important Files

## EC2 Discovery

```text
app/aws/ec2.py
```

## CloudWatch

```text
app/aws/cloudwatch.py
```

## Cost Explorer

```text
app/aws/cost_explorer.py
```

## Resource Service

```text
app/services/resource_service.py
```

## Cost Service

```text
app/services/cost_service.py
```

## Cost Attribution

```text
app/services/cost_attribution_service.py
```

## Analysis Service

```text
app/services/analysis_service.py
```

## Utilization Agent

```text
app/agents/utilization_agent.py
```

## Optimization Agent

```text
app/agents/optimization_agent.py
```

## Risk Agent

```text
app/agents/risk_agent.py
```

## Execution Agent

```text
app/agents/execution_agent.py
```

## LLM Agent

```text
app/agents/llm_agent.py
```

## Dashboard

```text
dashboard/app.py
```

---

# 74. Security Considerations

Never commit:

```text
AWS Access Keys
AWS Secret Keys
Database Passwords
.env
Private credentials
```

Use:

```text
.env
```

for local development.

Use IAM least privilege.

Do not use AWS root credentials for application access.

For production deployment, use:

```text
IAM Roles
AWS Secrets Manager
Environment Variables
Managed Identity / Instance Roles
```

where appropriate.

---

# 75. Cost Safety

The system is designed primarily as a **decision-support and optimization recommendation platform**.

Before enabling automatic infrastructure modification:

* Validate recommendations.
* Implement approval policies.
* Add resource allowlists/denylists.
* Protect production environments.
* Add rollback mechanisms.
* Require human approval for high-risk actions.

Never automatically terminate production resources without safeguards.

---

# 76. Current Cost Attribution Limitation

AWS service-level billing data does not necessarily identify individual EC2 instances.

Therefore:

```text
Service-level cost
        ≠
Individual EC2 cost
```

The project supports resource-level billing when AWS Cost Explorer makes that data available.

Until resource-level data is available, costs may remain:

```text
UNATTRIBUTED
```

This is expected behavior.

---

# 77. Future Enhancements

Possible future improvements include:

### Resource-Level Cost Attribution

Automatically map:

```text
AWS Resource ARN
        ↓
EC2 Instance ID
        ↓
PostgreSQL Resource
        ↓
Actual Cost
```

### More AWS Services

Support:

```text
S3
RDS
Lambda
EBS
ECS
EKS
DynamoDB
```

### More Metrics

Add:

```text
Memory utilization
Disk utilization
Network utilization
EBS utilization
Request counts
Latency
```

### Advanced AI

Add:

```text
Reinforcement Learning
Predictive Cost Forecasting
Time-Series Models
Anomaly Detection
Demand Prediction
```

### Autonomous Execution

Add controlled actions such as:

```text
Stop unused EC2
Resize instance
Change instance family
Delete unused resources
Modify schedules
```

with approval and rollback mechanisms.

---

# 78. Future Digital Twin Integration

A future version can introduce a digital twin of the AWS infrastructure.

Example:

```text
Real AWS Infrastructure
        ↓
Digital Twin
        ↓
Simulated Resource Changes
        ↓
AI Optimization
        ↓
Cost Prediction
        ↓
Risk Evaluation
        ↓
Recommended Action
```

This would allow optimization strategies to be tested before applying them to real AWS resources.

---

# 79. Future Reinforcement Learning Integration

The system can eventually use reinforcement learning.

Example:

```text
State
 ↓
Current EC2 configuration
CPU utilization
Memory utilization
Cost
Traffic
 ↓
RL Agent
 ↓
Action
 ↓
Resize / Stop / Keep
 ↓
Reward
 ↓
Cost savings + performance
```

The reinforcement learning agent can learn which optimization actions provide the best balance between:

```text
Cost
Performance
Availability
Risk
```

---

# 80. Expected Final Result

After completing the setup, the dashboard should provide an overview containing:

```text
Total Resources
Running Resources
Stopped Resources
Potential Savings
Review Required
LLM Success Rate
```

It should also display:

```text
EC2 Resources
CPU Metrics
Costs
Recommendations
Audit Logs
AI Analysis
```

---

# 81. Quick Start

For an already configured machine:

```bash
git clone https://github.com/YOUR_USERNAME/autonomous-cloud-cost-optimization.git

cd autonomous-cloud-cost-optimization

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python -m app.aws.ec2

python dashboard/app.py
```

Open:

```text
http://localhost:5000
```

Then click:

```text
Run Analysis
```

---

# 82. Quick Verification Checklist

Before running the application, verify:

```text
[ ] Python installed
[ ] Virtual environment activated
[ ] Python dependencies installed
[ ] PostgreSQL installed
[ ] PostgreSQL running
[ ] cloud_optimizer database created
[ ] optimizer_user created
[ ] Database tables created
[ ] AWS CLI installed
[ ] AWS credentials configured
[ ] AWS IAM permissions configured
[ ] EC2 access working
[ ] CloudWatch access working
[ ] Cost Explorer enabled
[ ] AWS billing data available
[ ] Ollama installed
[ ] Ollama running
[ ] LLM model downloaded
[ ] .env configured
[ ] .env excluded from Git
[ ] Dashboard starts successfully
[ ] /api/health returns healthy
[ ] EC2 resources appear in PostgreSQL
[ ] Dashboard displays resources
[ ] Run Analysis works
```

---

# 83. Project Status

The project currently provides:

* AWS EC2 discovery
* Automatic resource synchronization
* PostgreSQL resource storage
* CloudWatch CPU monitoring
* AWS Cost Explorer integration
* Service-level cost collection
* Resource-level cost attribution support
* Multi-agent analysis pipeline (Utilization → Optimization → Risk → Execution)
* Local LLM-powered recommendations via Ollama
* Flask-based web dashboard
* Audit logging for traceability
