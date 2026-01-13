# LinkedIn Ads Performance Reporter

A Python script to fetch and analyze LinkedIn Ads performance data including campaigns, creatives, landing pages, and click metrics.

## Features

- ✅ Fetches all campaigns and creatives from your LinkedIn Ads account
- ✅ Retrieves performance metrics (clicks, impressions, landing page clicks)
- ✅ Extracts landing page URLs from all ad formats
- ✅ Generates CSV reports sorted by performance
- ✅ Displays summary statistics and top performers

## Prerequisites

- Python 3.7+
- LinkedIn Ads API access with the following scopes:
  - `r_ads` (read advertising data)
  - `r_ads_reporting` (read analytics data)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/linkedin-ads-reporter.git
cd linkedin-ads-reporter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Getting Your LinkedIn Access Token

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Select your app (or create a new one)
3. Add the "Advertising API" product to your app
4. Go to the **Auth** tab
5. Under "OAuth 2.0 settings", generate an access token
6. Make sure the token has these scopes:
   - `r_ads`
   - `r_ads_reporting`

**Note:** Access tokens expire after 60 days. You'll need to regenerate them periodically.

## Usage

Basic usage (last 7 days):
```bash
python linkedin_ads_report.py YOUR_ACCESS_TOKEN YOUR_ACCOUNT_ID
```

Custom date range (e.g., last 30 days):
```bash
python linkedin_ads_report.py YOUR_ACCESS_TOKEN YOUR_ACCOUNT_ID 30
```

### Finding Your Account ID

Your LinkedIn Ads account ID can be found:
1. In the URL when viewing your campaigns: `ads.linkedin.com/accounts/XXXXXXXX`
2. Or use the number from your account URN: `urn:li:sponsoredAccount:507539077` → `507539077`

## Output

The script generates:

1. **Console Summary** - Quick overview with top performers
2. **CSV Report** (`linkedin_ads_report.csv`) - Complete data export with columns:
   - Campaign ID & Name
   - Creative ID & Name  
   - Landing Page URL
   - Clicks, Impressions, Landing Page Clicks
   - Campaign Status

## Example Output

```
==============================================================================
SUMMARY
==============================================================================
Total Campaigns: 8
Total Creatives: 28
Total Clicks: 294
Total Impressions: 42,516
Average CTR: 0.69%

==============================================================================
TOP 10 PERFORMING ADS (by clicks)
==============================================================================
Campaign                       Creative ID     Clicks     Landing Page
------------------------------------------------------------------------------
Q4 Product Launch              1080836164      62         https://example.com/product
Spring Campaign 2026           1073834074      41         https://example.com/spring
...
```

## Supported Ad Formats

The script extracts landing pages from:
- Sponsored Content (Single Image Ads)
- Text Ads
- Spotlight Ads
- Video Ads
- Carousel Ads

## Troubleshooting

**"Error fetching campaigns: 401"**
- Your access token is invalid or expired. Generate a new one.

**"Error fetching campaigns: 403"**  
- Your token doesn't have the required scopes (`r_ads`, `r_ads_reporting`)
- Or your user account doesn't have permission to access this ad account

**"No data retrieved"**
- Verify your account ID is correct
- Check that you have active campaigns in the specified date range
- Ensure your API permissions are properly configured

## License

MIT License - feel free to use and modify as needed.

## Contributing

Pull requests welcome! Please ensure your code follows the existing style.

## Support

For issues related to:
- **This script**: Open a GitHub issue
- **LinkedIn API**: Visit [LinkedIn Developer Support](https://developer.linkedin.com/support)
