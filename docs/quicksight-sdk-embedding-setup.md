# Quick Suite Chat Agent SDK Embedding Setup Guide

This guide walks you through setting up SDK-based embedding for Quick Suite Chat Agents to enable full visual generation capabilities.

## Why SDK Embedding?

The simple iframe "one-click embed" share link method has limitations:
- Visual generation shows blank space instead of charts
- Limited customization options
- No programmatic control

SDK embedding with `GenerateEmbedUrlForRegisteredUser` API provides:
- **Full visual generation support**
- Proper authentication handling
- Customizable UI options
- Event callbacks for integration

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   API Gateway   │────▶│     Lambda      │
│   (HTML/JS)     │     │   /embed-url    │     │  Generate URL   │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   Quick Suite   │
                                                │   Embed API     │
                                                │  (QuickChat)    │
                                                └─────────────────┘
```

## Prerequisites

1. AWS Account with Quick Suite (QuickSight Enterprise Edition)
2. Chat Agents created in Quick Suite
3. AWS CLI configured with appropriate permissions
4. Your CloudFront domain added to Quick Suite's allowed domains
5. QuickSight Embedding SDK version **2.11.0 or higher**

## Step 1: Deploy the Backend API

Deploy the CloudFormation template to create the Lambda + API Gateway:

```bash
aws cloudformation deploy \
  --template-file cfn-templates/quicksight-embed-api.yaml \
  --stack-name quicksuite-embed-api \
  --parameter-overrides \
    AllowedDomain=https://d2jqqf54ibg5b0.cloudfront.net \
  --capabilities CAPABILITY_NAMED_IAM
```

Get the API endpoint:

```bash
aws cloudformation describe-stacks \
  --stack-name quicksuite-embed-api \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
  --output text
```

## Step 2: Get Your Chat Agent ARNs

For each chat agent, you need the Agent ARN:

1. Go to Quick Suite Console → **Explore** → **Chat agents**
2. Click the **Action menu** (⋮) next to your agent
3. Choose **View chat agent details**
4. Click **Copy link** next to the chat agent name
5. The URL looks like: `https://...quicksight.aws.amazon.com/.../view=AGENT_ID`
6. Extract the agent ID and format as ARN:
   ```
   arn:aws:quicksight:us-east-1:YOUR_ACCOUNT_ID:agent/AGENT_ID
   ```

Your current agent ARNs (based on existing URLs):
- Main Chat: `arn:aws:quicksight:us-east-1:572990652154:agent/a8305c40-62d9-4173-92a3-0353994989e0`
- Sales Agent: `arn:aws:quicksight:us-east-1:572990652154:agent/230809cd-c2ac-4455-85fe-a5968a29980b`
- Inventory Agent: `arn:aws:quicksight:us-east-1:572990652154:agent/9eb08ace-ab20-4a9a-ba23-52344a345f2f`
- Marketing Agent: `arn:aws:quicksight:us-east-1:572990652154:agent/9926d31d-aea7-4e3f-ac6e-ea2eb36ab748`
- Forecast Agent: `arn:aws:quicksight:us-east-1:572990652154:agent/9b8f0d26-16c2-4b0f-8da5-4af1ffd903e1`
- Customer Agent: `arn:aws:quicksight:us-east-1:572990652154:agent/b4f53f86-be25-420e-b698-251d5c677d8d`

## Step 3: Get Your QuickSight User ARN

You need a registered QuickSight user ARN for embedding:

```bash
aws quicksight list-users \
  --aws-account-id 572990652154 \
  --namespace default \
  --query 'UserList[*].Arn'
```

The ARN format is:
```
arn:aws:quicksight:us-east-1:572990652154:user/default/USERNAME
```

## Step 4: Configure the HTML Template

Update `html_templates/retail-qbizapp-sdk.html.j2`:

```javascript
const CONFIG = {
  // API endpoint from Step 1
  apiEndpoint: 'https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/embed-url',
  
  // Your AWS Account ID
  accountId: '572990652154',
  
  // QuickSight User ARN from Step 3
  userArn: 'arn:aws:quicksight:us-east-1:572990652154:user/default/YOUR_USERNAME',
  
  // Agent ARNs from Step 2
  agents: {
    mainChat: {
      containerId: 'main-chat-agent',
      agentArn: 'arn:aws:quicksight:us-east-1:572990652154:agent/a8305c40-62d9-4173-92a3-0353994989e0'
    },
    // ... other agents
  }
};
```

## Step 5: Add Domain to Quick Suite

1. Go to Quick Suite Console → **Manage QuickSight** (top right)
2. Click **Domains and Embedding**
3. Add your CloudFront domain: `https://d2jqqf54ibg5b0.cloudfront.net`
4. Save

## Step 6: Deploy and Test

1. Process the template with your values (using Jinja2 or manually replace placeholders)
2. Upload to S3/CloudFront
3. Test the embedded agents

## API Reference

### Generate Embed URL Request

```json
POST /embed-url
{
  "userArn": "arn:aws:quicksight:us-east-1:ACCOUNT:user/default/USERNAME",
  "agentArn": "arn:aws:quicksight:us-east-1:ACCOUNT:agent/AGENT_ID"
}
```

### Response

```json
{
  "embedUrl": "https://us-east-1.quicksight.aws.amazon.com/embed/..."
}
```

## SDK Usage

The SDK uses `embedQuickChat` for chat agent embedding:

```javascript
const { createEmbeddingContext } = QuickSightEmbedding;
const embeddingContext = await createEmbeddingContext();

const frameOptions = {
  url: embedUrl,  // From API
  container: document.getElementById('container'),
  height: '900px',
  width: '100%'
};

const contentOptions = {
  onMessage: (messageEvent) => {
    console.log('Event:', messageEvent.eventName);
  }
};

const embeddedChat = await embeddingContext.embedQuickChat(frameOptions, contentOptions);
```

## Troubleshooting

### "Access Denied" Error
- Verify the Lambda role has QuickSight permissions
- Check that the user ARN is valid and has access to the chat agent
- Ensure the domain is in Quick Suite's allowed list

### "Invalid Agent" Error
- Verify the Agent ARN is correct
- Ensure the agent exists and is published
- Check that the agent is in the correct region (us-east-1)

### Visual Generation Still Failing
- Ensure you're using SDK version **2.11.0 or higher**
- Verify the embed URL is generated fresh (URLs expire after 5 minutes)
- Check browser console for specific error messages
- Confirm the chat agent works in the Quick Suite console

### CORS Errors
- Verify the `AllowedDomain` parameter matches your hosting domain exactly
- Include the protocol (https://)
- Check API Gateway CORS configuration

## References

- [Announcing embedded chat in Amazon Quick Suite](https://aws.amazon.com/blogs/business-intelligence/announcing-embedded-chat-in-amazon-quick-suite/)
- [QuickSight Embedding SDK GitHub](https://github.com/awslabs/amazon-quicksight-embedding-sdk)
- [GenerateEmbedUrlForRegisteredUser API](https://docs.aws.amazon.com/quicksight/latest/APIReference/API_GenerateEmbedUrlForRegisteredUser.html)
