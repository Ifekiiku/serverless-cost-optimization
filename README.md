# 🧠 Intelligent AWS Cost Optimization Advisor

This repository contains a fully serverless, automated solution for detecting and reporting AWS cost anomalies, idle resources, and silent spenders such as idle EC2 instances and unattached EBS volumes.

---

## Architecture Overview
![Architecture Diagram](/workspaces/serverless-cost-optimization/cost-optimization.drawio.png)

## 🚀 What This Project Does
- 📉 Detects daily AWS service spend using Cost Explorer
- 💤 Identifies idle EC2 instances using CloudWatch CPU metrics
- 🗃️ Finds unattached (unused) EBS volumes
- 📬 Sends daily email alerts via Amazon SNS
- 🗂️ Logs reports daily to S3 for auditability
- ⏰ Automatically runs via EventBridge schedule

---

## 🧰 Services Used
- AWS Lambda (Python 3.12)
- Amazon SNS
- Amazon S3 (for logging)
- Amazon EventBridge
- AWS Cost Explorer API
- Amazon EC2 & EBS APIs
- Amazon CloudWatch
- IAM (with least-privilege roles)

---

## 📂 Files Included
| File | Description |
|------|-------------|
| `cost-optimization-advisor.yaml` | CloudFormation template to deploy the full solution |
| `README.md` | Project overview and deployment instructions |
| `docs/roadmap.md` | Future enhancements and plans |
| `docs/sample-alert-email.txt` | Example email notification output |

---

## 📦 Deployment Instructions

### ✅ Prerequisites
- AWS account with Cost Explorer enabled
- Verified email to receive alerts
- IAM permissions to deploy CloudFormation stacks

### 🚀 Launch With CloudFormation
1. Go to AWS Console > CloudFormation > **Create Stack**
2. Upload the `cost-optimization-advisor.yaml` template
3. Provide your email when prompted
4. After creation, confirm the subscription from your inbox

### ✅ Manual Test (Optional)
- Go to the deployed Lambda function in AWS Console
- Click **Test** → Configure a test event (empty JSON `{}`) → Click **Test** again
- Check your inbox for a cost alert message
- Check your S3 bucket for a `report-YYYY-MM-DD.json` log

---

## 📧 Sample Alert Email Output
```
[Cost] Amazon EC2 - $2.44 on 2025-07-05
[Idle EC2] i-0123456789abcdef - Avg CPU 1.52% (last 3 days)
[Unused EBS] vol-0abcd12345678 - 30 GB (unattached)
```

---

## 🧠 Why Not Just Use AWS Budgets?
AWS Budgets only alerts when a threshold is passed — it doesn’t explain why you’re overspending.

This solution gives you **actionable insights**:
- It **detects** idle infrastructure
- It **details** resource IDs
- It logs to S3 and emails you daily

> Precision over panic. Insight over summary.

---

## 🔐 IAM Permissions
This solution follows least-privilege principles and uses a scoped inline policy to allow only the necessary actions:

```json
"Action": [
  "logs:*",
  "ce:GetCostAndUsage",
  "ec2:DescribeInstances",
  "ec2:DescribeVolumes",
  "cloudwatch:GetMetricStatistics",
  "sns:Publish",
  "s3:PutObject"
]
```

---

## 🧩 Architecture Diagram
![AWS Cost Optimization Architecture](architecture.png)

---

## 📈 Future Enhancements
- Detect unused Elastic IPs or AMIs
- Auto-tag and notify resource owners
- Store reports to S3 for history (✅ Done ✅)
- Visualize trends in QuickSight or Athena
- Integrate with Slack or Microsoft Teams

---

## 🤝 Let’s Work Together
Whether you're just adopting AWS and want to build smart from day one — or you're already there and tired of silent cost leaks — this project is for you.

Let’s deploy it where it matters.

💬 If you're hiring for cloud architecture, DevOps, or IAM roles — let’s connect. I'm open to collaboration, feedback, and opportunities.

---

## 🧑‍💻 Maintainer
**Ifekiiku Phillips** – AWS Certified Solutions Architect passionate about turning cloud complexity into business clarity.

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
