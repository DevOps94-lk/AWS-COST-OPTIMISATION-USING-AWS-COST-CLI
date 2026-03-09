# AWS Cost Optimization Using AWS-COST-CLI

A comprehensive guide to monitor and optimize your AWS costs using the AWS-COST-CLI tool with Slack integration for automated reporting.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [AWS IAM Permissions](#aws-iam-permissions)
- [Installation](#installation)
- [Usage](#usage)
- [Slack Configuration](#slack-configuration)
- [Python Slack Integration](#python-slack-integration)
- [Docker Usage](#docker-usage)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Node.js** (v14 or higher)
- **AWS Account** with configured credentials
- **Slack Workspace** (for notifications)

---

## AWS IAM Permissions

You need to create an IAM policy with the following permissions to use the CLI:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "iam:ListAccountAliases",
        "ce:GetCostAndUsage"
      ],
      "Resource": "*"
    }
  ]
}
```

> **Note:** This tool uses AWS Cost Explorer under the hood which costs **$0.01 per request**.

---

## Installation

### 1. Install Node.js

Download and install Node.js from the official website:

🔗 [https://nodejs.org/en/download](https://nodejs.org/en/download)

![Node.js Download Page](./images/Node_js_download_place.png)

### 2. Install AWS-COST-CLI

```bash
npm install -g aws-cost-cli
```

### 3. Verify Installation

```bash
aws-cost --version
```

---

## Usage

### 1. Default Usage - Cost Breakdown by Service

```bash
aws-cost
```

Retrieves total cost breakdown by service.

![Cost Breakdown](./images/aws-cost.png)

### 2. Cost Summary (No Service Breakdown)

```bash
aws-cost --summary
```

Displays total cost only, without service breakdown.

![Cost Summary](./images/aws-cost%20--summary.png)

### 3. Plain Text Output (No colors/tables)

```bash
aws-cost --text
```

Outputs the cost report in plain text format.

![Plain Text Output](./images/aws-cost%20--text.png)

### 4. JSON Output (For Automation)

```bash
aws-cost --json
```

Outputs the cost report in JSON format - useful for CI/CD pipelines.

### 5. Use Specific AWS Credentials

```bash
aws-cost -k <AWS_ACCESS_KEY> -s <AWS_SECRET_KEY> -r <AWS_REGION>
```

Pass AWS credentials directly in the CLI.

| Flag | Description |
|------|-------------|
| `-k` | AWS Access Key ID |
| `-s` | AWS Secret Access Key |
| `-r` | AWS Region |

### 6. Use AWS Profile

```bash
aws-cost -p <profile_name>
```

Use configured AWS CLI profiles.

### 7. Send Report to Slack

```bash
aws-cost --slack-token <SLACK_TOKEN> --slack-channel <CHANNEL_ID>
```

Sends the cost report directly to a Slack channel.

![Slack Report](./images/slack-report.png)

### 8. Help and Version Info

```bash
aws-cost --help        # Shows help info
aws-cost --version     # Displays CLI version
```

---

## Slack Configuration

### Step 1: Create a Slack App

1. Go to: [Slack API: Create App](https://api.slack.com/apps)
2. Click **Create New App**
3. Choose **From scratch**
4. Enter App Name: `AWS Cost Notifier`
5. Select your Slack workspace

### Step 2: Set Slack App Permissions

1. In your app dashboard, go to **OAuth & Permissions**
2. Scroll to **Scopes**
3. Under **Bot Token Scopes**, add the following:

| Scope | Description |
|-------|-------------|
| `chat:write` | Allows the bot to post messages |
| `chat:write.public` | Allows posting in public channels without being invited |
| `files:write` | Allows uploading files to Slack channels |

![Slack Permissions](./images/slack-permissions.png)

### Step 3: Install the App in Your Workspace

1. Still in **OAuth & Permissions**, click **Install App to Workspace**
2. Approve the permissions
3. Copy the **Bot User OAuth Token** (starts with `xoxb-...`)

![OAuth Token](./images/slack-oauth-token.png)

> ⚠️ **Important:** Keep your token secure! Never commit it to version control.

### Step 4: Find Your Slack Channel ID

1. Open Slack
2. Go to the channel you want to post in
3. Click on the channel name at the top → **View channel details**
4. Copy the **Channel ID** (starts with `C...`)

![Channel ID](./images/slack-channel-id.png)

### Step 5: Test Slack Integration

```bash
aws-cost --slack-token xoxb-your-token --slack-channel C08XXXXXXXX
```

### Step 6: Invite the Bot to Your Channel

In your Slack channel, run:

```
/invite @AWS-Cost-Notifier
```

---

## Python Slack Integration

For more advanced reporting, you can use Python to upload cost reports as files.

### 1. Install Python & pip

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Slack SDK

```bash
pip install slack-sdk
```

### 4. Create Python Script

Create a file named `upload_cost_report.py`:

```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Use environment variables for security
slack_token = os.environ.get("SLACK_TOKEN", "xoxb-your-token-here")
channel_id = os.environ.get("SLACK_CHANNEL", "C08XXXXXXXX")

client = WebClient(token=slack_token)

try:
    # Use files_upload_v2 (latest method)
    response = client.files_upload_v2(
        channel=channel_id,
        initial_comment="📊 AWS Cost Report",
        file="cost-report.txt"
    )
    print("✅ File uploaded successfully!")
except SlackApiError as e:
    print(f"❌ Error uploading file: {e.response['error']}")
```

### 5. Run the Complete Workflow

```bash
# Generate cost report
aws-cost --text > cost-report.txt

# Upload to Slack
python3 upload_cost_report.py
```

---

## Docker Usage

### Build the Docker Image

```bash
docker build -t aws-cost-cli .
```

### Run the Container

```bash
docker run aws-cost-cli
```

### With AWS Credentials

```bash
docker run -e AWS_ACCESS_KEY_ID=<key> \
           -e AWS_SECRET_ACCESS_KEY=<secret> \
           -e AWS_REGION=<region> \
           aws-cost-cli
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `command not found: aws-cost` | Ensure Node.js is installed and run `npm install -g aws-cost-cli` |
| `Invalid credentials` | Check your AWS credentials or profile configuration |
| `Slack posting failed` | Verify token permissions and channel ID |
| `Bot not in channel` | Run `/invite @AWS-Cost-Notifier` in the channel |

---

## Project Structure

```
AWS-COST-OPTIMISATION-USING-AWS-COST-CLI/
├── README.md
├── images/
│   ├── aws-cost.png
│   ├── aws-cost --summary.png
│   ├── aws-cost --text.png
│   ├── Node_js_download_place.png
│   ├── slack-channel-id.png
│   ├── slack-oauth-token.png
│   ├── slack-permissions.png
│   └── slack-report.png
├── upload_cost_report.py
├── Dockerfile
└── cost-report.txt
```

---

## Contributing

Feel free to submit issues and pull requests!

---

## License

MIT License

---

## Resources

- [AWS Cost CLI GitHub](https://github.com/kamranahmedse/aws-cost-cli)
- [Slack API Documentation](https://api.slack.com/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
