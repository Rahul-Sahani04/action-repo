# GitHub Activity Monitor - Action Repository

This repository triggers GitHub webhook events for the GitHub Activity Monitor system. It contains GitHub Actions workflows that automatically send webhook payloads when repository events occur.

## Purpose

This repository serves as the source repository where GitHub actions (pushes, pull requests, merges) trigger webhook events that are sent to a Flask webhook receiver for monitoring and display.

## Events That Trigger Webhooks

### Push Events
- Triggered when code is pushed to main, develop, or staging branches
- Sends commit information, author details, and branch data

### Pull Request Events
- **Opened**: When a new pull request is created
- **Closed**: When a pull request is closed (merged or rejected)
- **Synchronized**: When new commits are pushed to an existing pull request

### Merge Events
- Specifically detected when a pull request is merged (closed with merged=true)
- Includes merge author and branch information

## Webhook Configuration

1. Go to **Settings → Secrets and variables → Actions**
2. Add a new repository secret: `WEBHOOK_URL`
3. Set the value to your Flask webhook receiver URL (e.g., `http://localhost:5000/webhook`)

## Testing Events

### Push Event Test
```bash
git add .
git commit -m "Test push event"
git push origin main
```

### Pull Request Test
1. Create a new branch: `git checkout -b feature/test`
2. Make changes and commit
3. Push the branch: `git push origin feature/test`
4. Create a pull request on GitHub

### Merge Event Test
1. Merge the pull request on GitHub
2. The workflow will detect the merge and send the webhook

## Repository Structure

```
action-repo/
├── .github/
│   └── workflows/
│       └── webhook-trigger.yml
└── README.md
```

## Workflow Configuration

The workflow file (`.github/workflows/webhook-trigger.yml`) handles:
- Event detection for pushes and pull requests
- Webhook payload construction matching GitHub's format
- HTTP POST requests to the configured webhook endpoint
- Error handling and logging

## Expected Webhook Payloads

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

## Activity Monitor Display

The webhook receiver processes these events and displays them as:
- **Push**: `{author} pushed to {branch} on {timestamp}`
- **Pull Request**: `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`
- **Merge**: `{author} merged branch {from_branch} to {to_branch} on {timestamp}`