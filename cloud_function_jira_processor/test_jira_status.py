#!/usr/bin/env python3
"""
Test script to check JIRA availability and credentials.
Run this to verify JIRA is back online before expecting tickets to be created.
"""

import sys
import requests
from google.cloud import secretmanager


def check_jira_status():
    """Check if JIRA service is available."""
    JIRA_SERVER = "https://sadaadvservices.atlassian.net"
    
    print("=" * 60)
    print("JIRA Service Status Check")
    print("=" * 60)
    print()
    
    # Test 1: Basic connectivity
    print("1️⃣  Testing basic connectivity...")
    try:
        response = requests.get(f"{JIRA_SERVER}", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ JIRA site is reachable (HTTP {response.status_code})")
        elif response.status_code == 404:
            print(f"   ❌ JIRA site unavailable (HTTP {response.status_code})")
            print(f"   ⚠️  Error: Site temporarily unavailable")
            return False
        else:
            print(f"   ⚠️  Unexpected status: HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    print()
    
    # Test 2: API endpoint
    print("2️⃣  Testing API endpoint...")
    try:
        response = requests.get(f"{JIRA_SERVER}/rest/api/2/serverInfo", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ JIRA API is accessible (HTTP {response.status_code})")
            server_info = response.json()
            print(f"   📊 Server: {server_info.get('serverTitle', 'N/A')}")
            print(f"   🔢 Version: {server_info.get('version', 'N/A')}")
            return True
        else:
            print(f"   ❌ JIRA API unavailable (HTTP {response.status_code})")
            if response.status_code == 404:
                print(f"   ⚠️  Error: {response.json().get('errorMessage', 'Unknown')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ API connection failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False


def test_jira_credentials():
    """Test JIRA credentials from Secret Manager."""
    print()
    print("3️⃣  Testing JIRA credentials...")
    
    try:
        # Get API key
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(
            request={"name": "projects/900228280944/secrets/JIRA_API_KEY/versions/latest"}
        )
        api_key = response.payload.data.decode("UTF-8")
        print(f"   ✅ Retrieved API key from Secret Manager")
        print(f"   📏 Key length: {len(api_key)} characters")
        
        # Try to connect (will fail if JIRA is down)
        from jira import JIRA
        JIRA_SERVER = "https://sadaadvservices.atlassian.net"
        USER_EMAIL = "joseph.shorter@sada.com"
        
        jira_options = {'server': JIRA_SERVER}
        jira = JIRA(options=jira_options, basic_auth=(USER_EMAIL, api_key))
        
        myself = jira.myself()
        print(f"   ✅ Successfully authenticated as: {myself['displayName']}")
        print(f"   📧 Email: {myself['emailAddress']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Authentication failed: {type(e).__name__}")
        if "Site temporarily unavailable" in str(e):
            print(f"   ⚠️  JIRA service is down - credentials cannot be tested")
        else:
            print(f"   ℹ️  Error: {str(e)[:100]}")
        return False


def main():
    """Main execution."""
    jira_available = check_jira_status()
    
    if jira_available:
        credentials_valid = test_jira_credentials()
        
        print()
        print("=" * 60)
        if credentials_valid:
            print("✅ JIRA is ONLINE and credentials are VALID")
            print("=" * 60)
            print()
            print("🎯 Next Steps:")
            print("   1. Cloud Function will automatically process queued messages")
            print("   2. Or publish new alerts to trigger ticket creation")
            print("   3. Check Cloud Function logs for execution details")
            print()
            return 0
        else:
            print("⚠️  JIRA is online but credentials failed")
            print("=" * 60)
            return 1
    else:
        print()
        print("=" * 60)
        print("❌ JIRA SERVICE IS CURRENTLY UNAVAILABLE")
        print("=" * 60)
        print()
        print("ℹ️  What this means:")
        print("   • JIRA tickets cannot be created right now")
        print("   • Cloud Function will retry failed messages automatically")
        print("   • Messages will be retried with exponential backoff")
        print("   • Once JIRA is back, tickets will be created automatically")
        print()
        print("🔄 Retry Policy:")
        print("   • Initial retry: 10 seconds")
        print("   • Maximum backoff: 600 seconds (10 minutes)")
        print("   • Message retention: 7 days")
        print()
        print("👀 Monitor JIRA status:")
        print("   Run this script again: python test_jira_status.py")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
