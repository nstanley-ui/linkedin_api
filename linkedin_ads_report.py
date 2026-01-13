#!/usr/bin/env python3
"""
LinkedIn Ads Performance Report Generator
Fetches campaigns, creatives, landing pages, and click data from LinkedIn Ads API
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import csv


class LinkedInAdsClient:
    """Client for LinkedIn Ads API"""
    
    def __init__(self, access_token: str, account_id: str):
        self.access_token = access_token
        self.account_id = account_id
        self.base_url = "https://api.linkedin.com"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": "202411"
        }
    
    def test_connection(self) -> bool:
        """Test if the access token is valid"""
        url = f"{self.base_url}/v2/me"
        try:
            print("Testing API connection...")
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Connected as: {data.get('localizedFirstName', '')} {data.get('localizedLastName', '')}")
                return True
            else:
                print(f"✗ Connection failed: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def get_campaigns(self) -> List[Dict]:
        """Fetch all campaigns for the account"""
        # Try multiple endpoint formats
        endpoints = [
            (f"{self.base_url}/v2/adCampaignsV2", {
                "q": "search",
                "search.account.values[0]": f"urn:li:sponsoredAccount:{self.account_id}"
            }),
            (f"{self.base_url}/rest/adCampaigns", {
                "q": "account",
                "account": f"urn:li:sponsoredAccount:{self.account_id}"
            })
        ]
        
        for url, params in endpoints:
            try:
                print(f"  Trying: {url}")
                response = requests.get(url, headers=self.headers, params=params)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    elements = data.get("elements", [])
                    if elements:
                        print(f"  ✓ Success! Found {len(elements)} campaigns")
                        return elements
                else:
                    print(f"  Response: {response.text[:200]}")
                    
            except requests.exceptions.RequestException as e:
                print(f"  Error: {e}")
                continue
        
        print("  ✗ All campaign endpoints failed")
        return []
    
    def get_creatives(self) -> List[Dict]:
        """Fetch all creatives (ads) for the account"""
        # Try multiple endpoint formats
        endpoints = [
            (f"{self.base_url}/v2/adCreativesV2", {
                "q": "search",
                "search.account.values[0]": f"urn:li:sponsoredAccount:{self.account_id}"
            }),
            (f"{self.base_url}/rest/creatives", {
                "q": "account",
                "account": f"urn:li:sponsoredAccount:{self.account_id}"
            })
        ]
        
        for url, params in endpoints:
            try:
                print(f"  Trying: {url}")
                response = requests.get(url, headers=self.headers, params=params)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    elements = data.get("elements", [])
                    if elements:
                        print(f"  ✓ Success! Found {len(elements)} creatives")
                        return elements
                else:
                    print(f"  Response: {response.text[:200]}")
                    
            except requests.exceptions.RequestException as e:
                print(f"  Error: {e}")
                continue
        
        print("  ✗ All creative endpoints failed")
        return []
    
    def get_analytics(self, days: int = 7) -> List[Dict]:
        """Fetch analytics data for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Try multiple endpoint formats
        endpoints = [
            # v2 format
            (f"{self.base_url}/v2/adAnalyticsV2", {
                "q": "analytics",
                "pivot": "CAMPAIGN,CREATIVE",
                "dateRange.start.day": start_date.day,
                "dateRange.start.month": start_date.month,
                "dateRange.start.year": start_date.year,
                "dateRange.end.day": end_date.day,
                "dateRange.end.month": end_date.month,
                "dateRange.end.year": end_date.year,
                "accounts[0]": f"urn:li:sponsoredAccount:{self.account_id}",
                "fields": "clicks,impressions,landingPageClicks,pivotValues"
            }),
            # REST format
            (f"{self.base_url}/rest/adAnalytics", {
                "q": "analytics",
                "pivot": "CAMPAIGN,CREATIVE",
                "dateRange": f"(start:(day:{start_date.day},month:{start_date.month},year:{start_date.year}),"
                            f"end:(day:{end_date.day},month:{end_date.month},year:{end_date.year}))",
                "accounts": f"List(urn:li:sponsoredAccount:{self.account_id})",
                "fields": "clicks,impressions,landingPageClicks,pivotValues"
            })
        ]
        
        for url, params in endpoints:
            try:
                print(f"  Trying: {url}")
                response = requests.get(url, headers=self.headers, params=params)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    elements = data.get("elements", [])
                    if elements:
                        print(f"  ✓ Success! Found {len(elements)} analytics records")
                        return elements
                else:
                    print(f"  Response: {response.text[:200]}")
                    
            except requests.exceptions.RequestException as e:
                print(f"  Error: {e}")
                continue
        
        print("  ✗ All analytics endpoints failed")
        return []
    
    def extract_landing_page(self, creative: Dict) -> Optional[str]:
        """Extract landing page URL from creative content"""
        content = creative.get("content", {})
        
        # Try different ad format structures
        for ad_type in ["sponsoredContent", "textAd", "spotlight", "sponsoredVideo", "carousel"]:
            if ad_type in content:
                landing_page = content[ad_type].get("landingPage")
                if landing_page:
                    return landing_page
        
        return None


def generate_report(client: LinkedInAdsClient, days: int = 7):
    """Generate comprehensive ads performance report"""
    
    print(f"Fetching LinkedIn Ads data for the last {days} days...")
    
    # Fetch all data
    print("→ Fetching campaigns...")
    campaigns = client.get_campaigns()
    campaigns_map = {c.get("id"): c for c in campaigns}
    
    print("→ Fetching creatives...")
    creatives = client.get_creatives()
    creatives_map = {c.get("id"): c for c in creatives}
    
    print("→ Fetching analytics...")
    analytics = client.get_analytics(days)
    
    # Build report data
    report_data = []
    
    for item in analytics:
        pivot_values = item.get("pivotValues", [])
        if len(pivot_values) >= 2:
            campaign_urn = pivot_values[0]
            creative_urn = pivot_values[1]
            
            # Extract IDs from URNs
            campaign_id = campaign_urn.split(":")[-1] if campaign_urn else None
            creative_id = creative_urn.split(":")[-1] if creative_urn else None
            
            # Get campaign and creative details
            campaign = campaigns_map.get(campaign_urn, {})
            creative = creatives_map.get(creative_urn, {})
            
            # Extract landing page
            landing_page = client.extract_landing_page(creative)
            
            report_data.append({
                "campaign_id": campaign_id,
                "campaign_name": campaign.get("name", "Unknown"),
                "campaign_status": campaign.get("status", "Unknown"),
                "creative_id": creative_id,
                "creative_name": creative.get("name", "Unknown"),
                "landing_page": landing_page or "N/A",
                "clicks": item.get("clicks", 0),
                "impressions": item.get("impressions", 0),
                "landing_page_clicks": item.get("landingPageClicks", 0)
            })
    
    # Sort by clicks (descending)
    report_data.sort(key=lambda x: x["clicks"], reverse=True)
    
    return report_data


def save_to_csv(data: List[Dict], filename: str = "linkedin_ads_report.csv"):
    """Save report data to CSV file"""
    if not data:
        print("No data to save")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\n✓ Report saved to: {filename}")


def print_summary(data: List[Dict]):
    """Print summary statistics"""
    if not data:
        print("No data available")
        return
    
    total_clicks = sum(item["clicks"] for item in data)
    total_impressions = sum(item["impressions"] for item in data)
    total_campaigns = len(set(item["campaign_id"] for item in data))
    total_creatives = len(set(item["creative_id"] for item in data))
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Campaigns: {total_campaigns}")
    print(f"Total Creatives: {total_creatives}")
    print(f"Total Clicks: {total_clicks:,}")
    print(f"Total Impressions: {total_impressions:,}")
    print(f"Average CTR: {(total_clicks/total_impressions*100):.2f}%" if total_impressions > 0 else "N/A")
    
    print("\n" + "="*80)
    print("TOP 10 PERFORMING ADS (by clicks)")
    print("="*80)
    print(f"{'Campaign':<30} {'Creative ID':<15} {'Clicks':<10} {'Landing Page'}")
    print("-"*80)
    
    for item in data[:10]:
        campaign_name = item["campaign_name"][:28]
        creative_id = str(item["creative_id"])[:13]
        clicks = item["clicks"]
        landing_page = item["landing_page"][:40] if len(item["landing_page"]) > 40 else item["landing_page"]
        
        print(f"{campaign_name:<30} {creative_id:<15} {clicks:<10} {landing_page}")


def main():
    """Main execution function"""
    
    # Check for access token
    if len(sys.argv) < 3:
        print("Usage: python linkedin_ads_report.py <ACCESS_TOKEN> <ACCOUNT_ID> [DAYS]")
        print("\nExample:")
        print("  python linkedin_ads_report.py 'YOUR_TOKEN' '507539077' 7")
        print("\nHow to get your access token:")
        print("  1. Go to https://www.linkedin.com/developers/apps")
        print("  2. Select your app")
        print("  3. Go to 'Auth' tab")
        print("  4. Generate a new access token with r_ads and r_ads_reporting scopes")
        sys.exit(1)
    
    access_token = sys.argv[1]
    account_id = sys.argv[2]
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    
    # Create client and generate report
    client = LinkedInAdsClient(access_token, account_id)
    
    # Test connection first
    if not client.test_connection():
        print("\n✗ Failed to connect to LinkedIn API")
        print("\nPlease check:")
        print("  1. Your access token is valid (tokens expire after 60 days)")
        print("  2. Go to https://www.linkedin.com/developers/apps")
        print("  3. Select your app → Auth tab → Generate new token")
        print("  4. Ensure the token has r_ads and r_ads_reporting scopes")
        sys.exit(1)
    
    print()
    report_data = generate_report(client, days)
    
    if report_data:
        # Print summary
        print_summary(report_data)
        
        # Save to CSV
        save_to_csv(report_data)
        
        print("\n✓ Report generation complete!")
    else:
        print("\n✗ No data retrieved. Please check:")
        print("  - Access token is valid")
        print("  - Token has r_ads and r_ads_reporting scopes")
        print("  - Account ID is correct")


if __name__ == "__main__":
    main()
