"""
Simplified script to upload web portal files to CloudFront S3 bucket.
Skips Q Apps (which require special Identity Center credentials).
"""
import os
import boto3
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration - UPDATE THESE VALUES
Q_WEBEXP_URL = "https://hfadflfi.chat.qbusiness.us-east-1.on.aws/"
CLOUDFRONT_BUCKET = os.environ.get("QBIZ_CLOUDFRONT_BUCKET_NAME", "")

if not CLOUDFRONT_BUCKET:
    print("ERROR: Set QBIZ_CLOUDFRONT_BUCKET_NAME environment variable first!")
    print("Example: set QBIZ_CLOUDFRONT_BUCKET_NAME=retail-XXXXXXXXXX")
    exit(1)

# Create a simple HTML file that embeds Q Business
HTML_CONTENT = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Intelligence Portal</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }}
        .header {{
            background: rgba(255,255,255,0.1);
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(10px);
        }}
        .header h1 {{
            font-size: 24px;
            font-weight: 600;
        }}
        .header span {{
            color: #00d4ff;
        }}
        .main-container {{
            display: flex;
            height: calc(100vh - 80px);
            padding: 20px;
            gap: 20px;
        }}
        .chat-section {{
            flex: 1;
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .chat-section h2 {{
            padding: 20px;
            background: rgba(0,212,255,0.1);
            font-size: 18px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .chat-frame {{
            width: 100%;
            height: calc(100% - 60px);
            border: none;
        }}
        .info-section {{
            width: 300px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .info-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .info-card h3 {{
            color: #00d4ff;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .info-card p {{
            color: rgba(255,255,255,0.7);
            font-size: 14px;
            line-height: 1.6;
        }}
        .info-card ul {{
            list-style: none;
            margin-top: 10px;
        }}
        .info-card li {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            color: rgba(255,255,255,0.8);
            font-size: 13px;
        }}
        .info-card li:last-child {{
            border-bottom: none;
        }}
        .status {{
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #00ff88;
            border-radius: 50%;
            margin-right: 8px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Retail <span>Intelligence</span> Portal</h1>
        <div><span class="status"></span> Connected to Q Business</div>
    </div>
    
    <div class="main-container">
        <div class="chat-section">
            <h2>Ask Questions About Your Retail Data</h2>
            <iframe 
                class="chat-frame" 
                src="{Q_WEBEXP_URL}"
                allow="clipboard-write"
            ></iframe>
        </div>
        
        <div class="info-section">
            <div class="info-card">
                <h3>Quick Start</h3>
                <p>Ask natural language questions about your retail data:</p>
                <ul>
                    <li>"What were our top selling products?"</li>
                    <li>"Show me sales trends"</li>
                    <li>"Which region has highest revenue?"</li>
                    <li>"Analyze customer segments"</li>
                </ul>
            </div>
            
            <div class="info-card">
                <h3>Data Sources</h3>
                <ul>
                    <li><span class="status"></span> Sales Data</li>
                    <li><span class="status"></span> Inventory</li>
                    <li><span class="status"></span> Customer Segments</li>
                    <li><span class="status"></span> Marketing Performance</li>
                </ul>
            </div>
            
            <div class="info-card">
                <h3>Powered By</h3>
                <p>Amazon Q Business + QuickSight</p>
            </div>
        </div>
    </div>
</body>
</html>
'''

def main():
    # Save HTML locally
    os.makedirs("static", exist_ok=True)
    html_file = "static/retail-qbizapp.html"
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    logger.info(f"Created: {html_file}")
    
    # Upload to S3
    s3_client = boto3.client('s3')
    
    with open(html_file, "rb") as f:
        s3_client.upload_fileobj(f, CLOUDFRONT_BUCKET, "retail-qbizapp.html", 
                                  ExtraArgs={'ContentType': 'text/html'})
    logger.info(f"Uploaded to S3: s3://{CLOUDFRONT_BUCKET}/retail-qbizapp.html")
    
    # Invalidate CloudFront cache
    cf_client = boto3.client('cloudfront')
    response = cf_client.list_distributions()
    
    if response['DistributionList']['Quantity'] > 0:
        cf_dist_id = response['DistributionList']['Items'][0]['Id']
        cf_fqdn = response['DistributionList']['Items'][0]['DomainName']
        
        cf_client.create_invalidation(
            DistributionId=cf_dist_id,
            InvalidationBatch={
                'Paths': {'Quantity': 1, 'Items': ["/*"]},
                'CallerReference': f"inv-{random.randrange(1,1000000)}"
            }
        )
        logger.info(f"CloudFront cache invalidated")
        logger.info(f"")
        logger.info(f"SUCCESS! Your portal is ready at:")
        logger.info(f"https://{cf_fqdn}/retail-qbizapp.html")
    else:
        logger.warning("No CloudFront distribution found")

if __name__ == "__main__":
    main()
