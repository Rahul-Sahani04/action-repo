# GitHub Actions Webhook Integration Guide

## 🎯 Overview

This guide explains how to set up the GitHub Actions webhook integration for the GitHub Activity Monitor project. The action-repo contains workflows that automatically trigger webhooks when GitHub events occur.

## 🏗️ Architecture

```
GitHub Repository (action-repo)
    ↓ (GitHub Actions triggers on events)
GitHub Actions Workflow
    ↓ (Constructs webhook payload)
HTTP POST to Flask Webhook Endpoint
    ↓ (Processes and stores data)
Flask Backend (webhook-repo)
    ↓ (Provides API endpoint)
Next.js Frontend (polls every 15s)
    ↓ (Displays activity)
Activity Monitor UI
```

## 🚀 Setup Instructions

### 1. Configure the Action Repository

1. **Create a new GitHub repository** or use the provided action-repo
2. **Add the webhook URL as a secret**:
   - Go to **Settings → Secrets and variables → Actions**
   - Click **New repository secret**
   - Name: `WEBHOOK_URL`
   - Value: Your Flask webhook receiver URL (e.g., `http://your-server:5001/webhook`)

### 2. Repository Structure

Your action-repo should have this structure:
```
action-repo/
├── .github/
│   └── workflows/
│       └── webhook-trigger.yml
├── main.py
├── webhook_test.py
├── test_webhooks.py
├── .gitignore
└── README.md
```

### 3. GitHub Actions Workflow

The workflow file (`.github/workflows/webhook-trigger.yml`) contains:

- **Push event triggers** for main, develop, and staging branches
- **Pull request event triggers** for opened, closed, and synchronized actions
- **Webhook payload construction** that matches GitHub's format
- **HTTP POST requests** to your Flask webhook endpoint

### 4. Event Types and Payloads

#### Push Events
Triggered when code is pushed to any configured branch.

**Payload includes:**
- `ref`: Branch reference (e.g., `refs/heads/main`)
- `after`: New commit hash
- `before`: Previous commit hash
- `pusher`: Author information
- `repository`: Repository details

#### Pull Request Events
Triggered for PR lifecycle events.

**Payload includes:**
- `action`: Event type (`opened`, `closed`, `synchronize`)
- `number`: Pull request number
- `pull_request`: Complete PR object with head/base branches
- `merged`: Boolean indicating if PR was merged
- `merged_by`: User who merged the PR (for merge events)

#### Merge Events
Specifically detected when `action == "closed"` and `merged == true`.

## 🧪 Testing the Integration

### Local Testing

Use the provided `test_webhooks.py` script:

```bash
# Test all webhook types
python3 test_webhooks.py

# Test with custom webhook URL
WEBHOOK_URL=http://your-server:5001/webhook python3 test_webhooks.py
```

### GitHub Testing

#### Test Push Events
```bash
git add .
git commit -m "Test push event"
git push origin main
```

#### Test Pull Request Events
1. Create a feature branch: `git checkout -b feature/test-pr`
2. Make changes and commit: `git commit -m "Add test feature"`
3. Push the branch: `git push origin feature/test-pr`
4. Create a pull request on GitHub
5. The webhook will trigger automatically

#### Test Merge Events
1. Merge the pull request on GitHub
2. The workflow will detect the merge and send the webhook

## 📊 Monitoring and Debugging

### GitHub Actions Logs
- Go to **Actions** tab in your repository
- Click on the workflow run
- Expand the job steps to see:
  - Webhook payload details
  - HTTP response status
  - Any errors or issues

### Flask Backend Logs
- Check your Flask application console
- Look for "Stored event" messages
- Verify MongoDB connection and data storage

### Frontend Verification
- Open the Activity Monitor UI
- Verify events appear in the feed
- Check the 15-second polling updates

## 🔧 Configuration Options

### Webhook URL Configuration
- **Local development**: `http://localhost:5001/webhook`
- **Production**: Use your deployed Flask server URL
- **With ngrok**: `https://your-ngrok-url.ngrok.io/webhook`

### Branch Configuration
Modify the workflow file to trigger on different branches:
```yaml
on:
  push:
    branches: [ main, develop, staging, feature/* ]
  pull_request:
    types: [opened, closed, synchronize]
    branches: [ main, develop ]
```

### Event Type Configuration
Add or remove event types as needed:
```yaml
pull_request:
  types: [opened, closed, synchronize, reopened, ready_for_review]
```

## 🚨 Troubleshooting

### Common Issues

1. **Webhook URL not working**
   - Verify the URL is correct and accessible
   - Check if the Flask server is running
   - Test with curl or the test script

2. **GitHub Actions not triggering**
   - Verify the workflow file syntax
   - Check branch names in the trigger configuration
   - Ensure the workflow is in the `.github/workflows/` directory

3. **Webhook payload format issues**
   - Compare with GitHub's official webhook documentation
   - Use the test script to verify payload structure
   - Check Flask backend logs for parsing errors

4. **MongoDB connection issues**
   - Verify MongoDB URI in Flask backend
   - Check database permissions
   - Test MongoDB connection independently

### Debug Steps

1. **Test locally first** using the test script
2. **Check GitHub Actions logs** for payload details
3. **Monitor Flask backend logs** for processing errors
4. **Verify MongoDB storage** by checking the `/events` endpoint
5. **Test frontend integration** by viewing the Activity Monitor UI

## 🎉 Success Indicators

- ✅ GitHub Actions workflow runs successfully
- ✅ Webhook HTTP requests return 200 status
- ✅ Flask backend logs show "Stored event" messages
- ✅ Events appear in MongoDB (check `/events` endpoint)
- ✅ Activity Monitor UI displays events correctly
- ✅ UI updates every 15 seconds with new events

## 🚀 Next Steps

1. **Deploy the Flask backend** to a cloud service (Heroku, AWS, etc.)
2. **Update the webhook URL** in GitHub repository secrets
3. **Test with real GitHub events** in your repository
4. **Monitor the activity** through the Next.js frontend
5. **Scale as needed** for production use

---

**Your GitHub Activity Monitor is now fully integrated with GitHub Actions!** 🎊