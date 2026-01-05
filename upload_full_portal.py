"""
Full portal with Q Business chat AND QuickSight dashboard embedded.
"""
import os
import boto3
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
Q_WEBEXP_URL = "https://hfadflfi.chat.qbusiness.us-east-1.on.aws/"
QS_DASHBOARD_URL = "https://us-east-1.quicksight.aws.amazon.com/sn/embed/share/accounts/572990652154/dashboards/import86596ebd-a1aa-4598-ae5d-2cd8dfbba9d6"
CLOUDFRONT_BUCKET = os.environ.get("QBIZ_CLOUDFRONT_BUCKET_NAME", "")

if not CLOUDFRONT_BUCKET:
    print("ERROR: Set QBIZ_CLOUDFRONT_BUCKET_NAME environment variable first!")
    print("Run: set QBIZ_CLOUDFRONT_BUCKET_NAME=retail-XXXXXXXXXX")
    exit(1)

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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }}
        .header {{
            background: rgba(255,255,255,0.1);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .header h1 {{
            font-size: 22px;
            font-weight: 600;
        }}
        .header span {{
            color: #00d4ff;
        }}
        .tabs {{
            display: flex;
            gap: 10px;
        }}
        .tab {{
            padding: 8px 20px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            color: #fff;
            font-size: 14px;
        }}
        .tab:hover, .tab.active {{
            background: #00d4ff;
            color: #1a1a2e;
        }}
        .main-container {{
            display: flex;
            height: calc(100vh - 60px);
        }}
        .panel {{
            flex: 1;
            display: none;
            height: 100%;
        }}
        .panel.active {{
            display: flex;
        }}
        
        /* Dashboard Panel */
        .dashboard-panel {{
            flex-direction: column;
            padding: 20px;
        }}
        .dashboard-frame {{
            flex: 1;
            border: none;
            border-radius: 12px;
            background: #fff;
        }}
        
        /* Chat Panel */
        .chat-panel {{
            padding: 20px;
            gap: 20px;
        }}
        .chat-section {{
            flex: 1;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
            display: flex;
            flex-direction: column;
        }}
        .chat-header {{
            padding: 15px 20px;
            background: rgba(0,212,255,0.1);
            font-size: 16px;
            font-weight: 500;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .chat-frame {{
            flex: 1;
            border: none;
        }}
        .info-sidebar {{
            width: 280px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        .info-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .info-card h3 {{
            color: #00d4ff;
            margin-bottom: 10px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .info-card ul {{
            list-style: none;
        }}
        .info-card li {{
            padding: 6px 0;
            color: rgba(255,255,255,0.8);
            font-size: 13px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .info-card li:last-child {{
            border-bottom: none;
        }}
        .status {{
            display: inline-block;
            width: 6px;
            height: 6px;
            background: #00ff88;
            border-radius: 50%;
            margin-right: 8px;
        }}
        
        /* Split View */
        .split-panel {{
            display: flex;
            gap: 15px;
            padding: 15px;
        }}
        .split-left, .split-right {{
            flex: 1;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .split-left {{
            background: #fff;
        }}
        .split-right {{
            background: rgba(255,255,255,0.05);
            display: flex;
            flex-direction: column;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Retail <span>Intelligence</span> Portal</h1>
        <div class="tabs">
            <div class="tab active" id="tab-split" onclick="showPanel('split', this)">Dashboard + Chat</div>
            <div class="tab" id="tab-dashboard" onclick="showPanel('dashboard', this)">Dashboard Only</div>
            <div class="tab" id="tab-chat" onclick="showPanel('chat', this)">Chat Only</div>
        </div>
    </div>
    
    <div class="main-container">
        <!-- Split View (Default) -->
        <div id="split" class="panel split-panel active">
            <div class="split-left">
                <iframe class="dashboard-frame" style="width:100%;height:100%;" src="{QS_DASHBOARD_URL}"></iframe>
            </div>
            <div class="split-right">
                <div class="chat-header">Ask Q Business</div>
                <iframe class="chat-frame" src="{Q_WEBEXP_URL}" allow="clipboard-write"></iframe>
            </div>
        </div>
        
        <!-- Dashboard Only -->
        <div id="dashboard" class="panel dashboard-panel">
            <iframe class="dashboard-frame" src="{QS_DASHBOARD_URL}"></iframe>
        </div>
        
        <!-- Chat Only -->
        <div id="chat" class="panel chat-panel">
            <div class="chat-section">
                <div class="chat-header">Ask Questions About Your Retail Data</div>
                <iframe class="chat-frame" src="{Q_WEBEXP_URL}" allow="clipboard-write"></iframe>
            </div>
            <div class="info-sidebar">
                <div class="info-card">
                    <h3>Sample Questions</h3>
                    <ul>
                        <li>"What are our top products?"</li>
                        <li>"Show sales by region"</li>
                        <li>"Which items are low stock?"</li>
                        <li>"List platinum customers"</li>
                    </ul>
                </div>
                <div class="info-card">
                    <h3>Data Sources</h3>
                    <ul>
                        <li><span class="status"></span>Sales Data</li>
                        <li><span class="status"></span>Products</li>
                        <li><span class="status"></span>Customers</li>
                        <li><span class="status"></span>Inventory</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function showPanel(panelId, clickedTab) {{
            // Hide all panels
            var panels = document.querySelectorAll('.panel');
            for (var i = 0; i < panels.length; i++) {{
                panels[i].classList.remove('active');
            }}
            // Show selected panel
            document.getElementById(panelId).classList.add('active');
            // Update tabs
            var tabs = document.querySelectorAll('.tab');
            for (var j = 0; j < tabs.length; j++) {{
                tabs[j].classList.remove('active');
            }}
            clickedTab.classList.add('active');
        }}
    </script>
</body>
</html>
'''

def main():
    os.makedirs("static", exist_ok=True)
    html_file = "static/retail-qbizapp.html"
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    logger.info(f"Created: {html_file}")
    
    s3_client = boto3.client('s3')
    with open(html_file, "rb") as f:
        s3_client.upload_fileobj(f, CLOUDFRONT_BUCKET, "retail-qbizapp.html", 
                                  ExtraArgs={'ContentType': 'text/html'})
    logger.info(f"Uploaded to S3: s3://{CLOUDFRONT_BUCKET}/retail-qbizapp.html")
    
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
        logger.info("CloudFront cache invalidated")
        logger.info("")
        logger.info("SUCCESS! Your full portal is ready at:")
        logger.info(f"https://{cf_fqdn}/retail-qbizapp.html")
    else:
        logger.warning("No CloudFront distribution found")

if __name__ == "__main__":
    main()
