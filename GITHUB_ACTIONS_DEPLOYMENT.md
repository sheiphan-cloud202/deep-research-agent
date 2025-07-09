# GitHub Actions Lambda Deployment Guide

This guide explains how to deploy your Deep Research Agent API to AWS Lambda using GitHub Actions.

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **GitHub Repository** with your code
3. **Lambda Execution Role** created in AWS (see below)

## GitHub Secrets Configuration

You need to configure these secrets in your GitHub repository:

### Go to: Repository → Settings → Secrets and variables → Actions

## Option 1: AWS Access Keys (Simpler Setup)

### Required GitHub Secrets:
- `AWS_ACCESS_KEY_ID` - Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret access key
- `LAMBDA_EXECUTION_ROLE_ARN` - ARN of the Lambda execution role

### Steps to get AWS Access Keys:

1. **Create IAM User for GitHub Actions:**
   ```bash
   aws iam create-user --user-name github-actions-lambda-deploy
   ```

2. **Create and attach policy for deployment permissions:**

   Create a file `lambda-deploy-policy.json`:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "lambda:CreateFunction",
           "lambda:UpdateFunctionCode",
           "lambda:UpdateFunctionConfiguration",
           "lambda:GetFunction",
           "lambda:CreateFunctionUrlConfig",
           "lambda:GetFunctionUrlConfig",
           "lambda:UpdateFunctionUrlConfig",
           "iam:PassRole"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

   ```bash
   aws iam create-policy --policy-name GitHubActionsLambdaDeploy --policy-document file://lambda-deploy-policy.json
   aws iam attach-user-policy --user-name github-actions-lambda-deploy --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/GitHubActionsLambdaDeploy
   ```

3. **Create access keys:**
   ```bash
   aws iam create-access-key --user-name github-actions-lambda-deploy
   ```

## Option 2: OIDC with IAM Roles (Recommended - More Secure)

### Required GitHub Secrets:
- `AWS_ROLE_ARN` - ARN of the role to assume
- `LAMBDA_EXECUTION_ROLE_ARN` - ARN of the Lambda execution role

### Steps to setup OIDC:

1. **Create OIDC Identity Provider in AWS:**
   ```bash
   aws iam create-open-id-connect-provider \
     --url https://token.actions.githubusercontent.com \
     --client-id-list sts.amazonaws.com \
     --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
   ```

2. **Create role for GitHub Actions:**

   Create `github-actions-trust-policy.json`:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
           },
           "StringLike": {
             "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USERNAME/YOUR_REPO_NAME:*"
           }
         }
       }
     ]
   }
   ```

   ```bash
   aws iam create-role --role-name GitHubActionsLambdaRole --assume-role-policy-document file://github-actions-trust-policy.json
   aws iam attach-role-policy --role-name GitHubActionsLambdaRole --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/GitHubActionsLambdaDeploy
   ```

3. **Update GitHub Actions workflow:**
   In `.github/workflows/deploy-lambda.yml`, comment out the access key lines and uncomment the OIDC lines:
   ```yaml
   - name: Configure AWS credentials
     uses: aws-actions/configure-aws-credentials@v4
     with:
       role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
       role-session-name: GitHubActions-DeployLambda
       aws-region: ${{ env.AWS_REGION }}
   ```

## Lambda Execution Role Setup

Your Lambda function needs an execution role with proper permissions:

### 1. Create Lambda Execution Role:

Create `lambda-execution-trust-policy.json`:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

```bash
aws iam create-role \
  --role-name DeepResearchAgentLambdaRole \
  --assume-role-policy-document file://lambda-execution-trust-policy.json
```

### 2. Attach Required Policies:

```bash
# Basic Lambda execution permissions
aws iam attach-role-policy \
  --role-name DeepResearchAgentLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Bedrock permissions for AI models
aws iam create-policy --policy-name BedrockInvokePolicy --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0",
        "arn:aws:bedrock:*::foundation-model/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
      ]
    }
  ]
}'

aws iam attach-role-policy \
  --role-name DeepResearchAgentLambdaRole \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/BedrockInvokePolicy
```

### 3. Get the Role ARN:
```bash
aws iam get-role --role-name DeepResearchAgentLambdaRole --query 'Role.Arn' --output text
```

Add this ARN to your GitHub Secrets as `LAMBDA_EXECUTION_ROLE_ARN`.

## Quick Setup Commands

### For Access Keys Method:
```bash
# Replace YOUR_ACCOUNT_ID with your actual AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# 1. Create deployment policy
cat > lambda-deploy-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:CreateFunction",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:GetFunction",
        "lambda:CreateFunctionUrlConfig",
        "lambda:GetFunctionUrlConfig",
        "lambda:UpdateFunctionUrlConfig",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
EOF

# 2. Create Lambda execution role
cat > lambda-execution-trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

cat > bedrock-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0",
        "arn:aws:bedrock:*::foundation-model/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
      ]
    }
  ]
}
EOF

# 3. Create all resources
aws iam create-user --user-name github-actions-lambda-deploy
aws iam create-policy --policy-name GitHubActionsLambdaDeploy --policy-document file://lambda-deploy-policy.json
aws iam create-policy --policy-name BedrockInvokePolicy --policy-document file://bedrock-policy.json
aws iam create-role --role-name DeepResearchAgentLambdaRole --assume-role-policy-document file://lambda-execution-trust-policy.json

# 4. Attach policies
aws iam attach-user-policy --user-name github-actions-lambda-deploy --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/GitHubActionsLambdaDeploy
aws iam attach-role-policy --role-name DeepResearchAgentLambdaRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name DeepResearchAgentLambdaRole --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/BedrockInvokePolicy

# 5. Create access keys
aws iam create-access-key --user-name github-actions-lambda-deploy

# 6. Get role ARN
echo "Lambda Execution Role ARN:"
aws iam get-role --role-name DeepResearchAgentLambdaRole --query 'Role.Arn' --output text
```

## GitHub Secrets Setup

Add these to your GitHub repository secrets:

### For Access Keys Method:
- `AWS_ACCESS_KEY_ID`: From the access key creation output
- `AWS_SECRET_ACCESS_KEY`: From the access key creation output
- `LAMBDA_EXECUTION_ROLE_ARN`: The ARN from step 6 above

### For OIDC Method:
- `AWS_ROLE_ARN`: The GitHub Actions role ARN
- `LAMBDA_EXECUTION_ROLE_ARN`: The Lambda execution role ARN

## Deployment

Once everything is configured:

1. **Push to main branch** or **manually trigger** the workflow
2. The workflow will:
   - Package your code with dependencies
   - Create/update the Lambda function
   - Set up a Function URL for HTTP access
   - Test the deployment

3. **Access your API** using the Function URL provided in the workflow output

## Environment Variables

The workflow automatically sets these environment variables in your Lambda:
- `AWS_REGION`: us-east-1 (configurable in workflow)
- `DEFAULT_MODEL_ID`: us.anthropic.claude-3-7-sonnet-20250219-v1:0
- `CLAUDE_SONNET_MODEL_ID`: anthropic.claude-3-5-sonnet-20240620-v1:0

## Troubleshooting

### Common Issues:

1. **ZIP file too large**: Lambda direct upload limit is 50MB. Use S3 if needed.
2. **Permission denied**: Check IAM policies and role attachments
3. **Function not found**: The workflow handles creation automatically
4. **Import errors**: Ensure all dependencies are in requirements.txt

### Monitoring:
- Check CloudWatch Logs for function execution logs
- Use AWS X-Ray for request tracing
- Monitor function metrics in Lambda console

## Security Best Practices

1. **Use OIDC** instead of access keys when possible
2. **Limit IAM permissions** to minimum required
3. **Enable CloudTrail** for audit logging
4. **Use environment-specific secrets** for different stages
5. **Rotate access keys** regularly if using them

This setup provides a complete CI/CD pipeline for your Lambda function with proper security and monitoring.
