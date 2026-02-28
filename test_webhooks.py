#!/usr/bin/env python3
"""
Local test script to simulate GitHub Actions webhook triggers
This script demonstrates how the GitHub Actions workflow will send webhooks to the Flask receiver.
"""

import requests
import json
import os
from datetime import datetime

def send_push_webhook(webhook_url, author="testuser", branch="main", commit_hash="abc123def456"):
    """Simulate a push event webhook"""
    payload = {
        "ref": f"refs/heads/{branch}",
        "before": "0000000000000000000000000000000000000000",
        "after": commit_hash,
        "pusher": {
            "name": author,
            "email": f"{author}@example.com"
        },
        "repository": {
            "name": "action-repo",
            "full_name": f"{author}/action-repo",
            "owner": {
                "login": author
            }
        },
        "created": True,
        "deleted": False,
        "forced": False,
        "base_ref": None,
        "compare": f"https://github.com/{author}/action-repo/compare/0000000...{commit_hash}",
        "commits": [
            {
                "id": commit_hash,
                "message": f"Test commit by {author}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "author": {
                    "name": author,
                    "email": f"{author}@example.com"
                },
                "committer": {
                    "name": author,
                    "email": f"{author}@example.com"
                }
            }
        ],
        "head_commit": {
            "id": commit_hash,
            "message": f"Test commit by {author}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "author": {
                "name": author,
                "email": f"{author}@example.com"
            },
            "committer": {
                "name": author,
                "email": f"{author}@example.com"
            }
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'push',
        'X-GitHub-Delivery': '12345-67890-abcdef',
        'User-Agent': 'GitHub-Hookshot/abc123'
    }
    
    try:
        response = requests.post(webhook_url, headers=headers, json=payload)
        print(f"✅ Push webhook sent successfully!")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Error sending push webhook: {e}")
        return False

def send_pull_request_webhook(webhook_url, author="testuser", from_branch="feature-branch", to_branch="main", action="opened", pr_number=123):
    """Simulate a pull request event webhook"""
    payload = {
        "action": action,
        "number": pr_number,
        "pull_request": {
            "id": pr_number * 1000,
            "number": pr_number,
            "state": "open" if action in ["opened", "synchronize"] else "closed",
            "title": f"Test PR #{pr_number} by {author}",
            "user": {
                "login": author
            },
            "head": {
                "label": f"{author}:{from_branch}",
                "ref": from_branch,
                "sha": "abc123def456head",
                "user": {
                    "login": author
                }
            },
            "base": {
                "label": f"{author}:{to_branch}",
                "ref": to_branch,
                "sha": "def456abc123base",
                "user": {
                    "login": author
                }
            },
            "merged": action == "closed" and True,  # Simulate merged when closed
            "mergeable": True,
            "merged_at": datetime.utcnow().isoformat() + "Z" if action == "closed" else None,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "closed_at": datetime.utcnow().isoformat() + "Z" if action == "closed" else None
        },
        "repository": {
            "name": "action-repo",
            "full_name": f"{author}/action-repo",
            "owner": {
                "login": author
            }
        },
        "sender": {
            "login": author
        }
    }
    
    # Add merged_by for merge events
    if action == "closed":
        payload["pull_request"]["merged_by"] = {
            "login": author,
            "id": pr_number * 100,
            "type": "User"
        }
    
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'pull_request',
        'X-GitHub-Delivery': f'pr-{pr_number}-{action}',
        'User-Agent': 'GitHub-Hookshot/abc123'
    }
    
    try:
        response = requests.post(webhook_url, headers=headers, json=payload)
        print(f"✅ Pull request webhook sent successfully!")
        print(f"   Action: {action}")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Error sending pull request webhook: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 GitHub Activity Monitor - Webhook Test Script")
    print("=" * 60)
    
    # Get webhook URL from environment or use default
    webhook_url = os.environ.get('WEBHOOK_URL', 'http://localhost:5001/webhook')
    print(f"Using webhook URL: {webhook_url}")
    print()
    
    # Test push event
    print("📤 Testing Push Event...")
    send_push_webhook(webhook_url, author="testuser", branch="main", commit_hash="abc123def456")
    print()
    
    # Test pull request opened
    print("📤 Testing Pull Request Opened...")
    send_pull_request_webhook(webhook_url, author="testuser", from_branch="feature-branch", 
                            to_branch="main", action="opened", pr_number=123)
    print()
    
    # Test pull request merged (closed with merged=true)
    print("📤 Testing Pull Request Merged...")
    send_pull_request_webhook(webhook_url, author="testuser", from_branch="feature-branch", 
                            to_branch="main", action="closed", pr_number=123)
    print()
    
    print("✅ All webhook tests completed!")
    print("\n💡 To test with different parameters, modify the function calls above.")
    print("💡 To test with a different webhook URL, set the WEBHOOK_URL environment variable.")

if __name__ == '__main__':
    main()