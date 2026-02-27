# GitHub Activity Monitor - Action Repository

This repository is designed to trigger GitHub webhooks for the GitHub Activity Monitor project. It contains workflows that automatically send webhook events when specific GitHub actions occur.

## 🎯 Purpose

This repository serves as a **trigger repository** that generates GitHub events (pushes, pull requests, merges) which are then sent to a Flask webhook receiver for monitoring and display.

## 🚀 How It Works

1. **GitHub Actions Workflows** automatically trigger on specific events
2. **Webhook payloads** are constructed to match GitHub's webhook format
3. **HTTP requests** are sent to the configured webhook endpoint
4. **Flask backend** receives and processes the events
5. **Activity Monitor UI** displays the events in real-time

## 🔗 Webhook Configuration

The webhook endpoint should be configured in the repository secrets:

1. Go to **Settings → Secrets and variables → Actions**
2. Add a new secret: `WEBHOOK_URL`
3. Set the value to your Flask webhook receiver URL (e.g., `http://localhost:5001/webhook`)

## 📋 Supported Events

### ✅ Push Events
- Triggered when code is pushed to any branch
- Sends commit information, author details, and branch info

### ✅ Pull Request Events
- **Opened**: When a new PR is created
- **Closed**: When a PR is closed (merged or rejected)
- **Synchronized**: When new commits are pushed to an existing PR

### ✅ Merge Events
- Specifically detected when a PR is merged (not just closed)
- Includes merge author and branch information

## 🛠️ Testing the Integration

### 1. Push Event Test
```bash
git add .
git commit -m "Test push event"
git push origin main
```

### 2. Pull Request Test
1. Create a new branch: `git checkout -b feature/test-pr`
2. Make changes and commit
3. Push the branch: `git push origin feature/test-pr`
4. Create a pull request on GitHub
5. The webhook will trigger automatically

### 3. Merge Event Test
1. Merge the pull request on GitHub
2. The workflow will detect the merge and send the webhook

## 📊 Expected Webhook Payloads

### Push Event
```json
{
  "ref": "refs/heads/main",
  "after": "commit-hash",
  "pusher": {
    "name": "username",
    "email": "user@example.com"
  },
  "repository": {
    "name": "action-repo",
    "full_name": "username/action-repo"
  }
}
```

### Pull Request Event
```json
{
  "action": "opened",
  "number": 123,
  "pull_request": {
    "number": 123,
    "user": {"login": "username"},
    "head": {"ref": "feature-branch"},
    "base": {"ref": "main"},
    "merged": false
  }
}
```

### Merge Event
```json
{
  "action": "closed",
  "number": 123,
  "pull_request": {
    "number": 123,
    "user": {"login": "username"},
    "merged_by": {"login": "merger-username"},
    "head": {"ref": "feature-branch"},
    "base": {"ref": "main"},
    "merged": true
  }
}
```

## 🔧 Configuration

### Environment Variables
Set these in your GitHub repository secrets:
- `WEBHOOK_URL`: Your Flask webhook receiver endpoint

### Workflow Files
- `.github/workflows/webhook-trigger.yml`: Main webhook trigger workflow

## 🎨 Activity Monitor Display

The webhook receiver will process these events and display them as:

- **Push**: `{author} pushed to {branch} on {timestamp}`
- **Pull Request**: `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`
- **Merge**: `{author} merged branch {from_branch} to {to_branch} on {timestamp}`

## 🚀 Getting Started

1. **Fork or clone this repository**
2. **Set up the webhook URL secret**
3. **Start your Flask webhook receiver**
4. **Make some changes and push them**
5. **Watch the activity monitor update in real-time!**

## 📈 Monitoring

Check the GitHub Actions logs to see:
- Webhook payload details
- HTTP response status
- Any errors or issues

## 🔗 Related Repositories

- **webhook-repo**: Contains the Flask webhook receiver and Next.js frontend
- **Main project**: The complete GitHub Activity Monitor system

---

**Happy monitoring!** 🎉