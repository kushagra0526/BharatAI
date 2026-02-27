# Complete Deployment Guide

## Prerequisites

- AWS Account with admin access
- AWS CLI installed and configured
- Python 3.10 or higher
- Basic understanding of Lambda, DynamoDB, and Bedrock

## Step-by-Step Deployment

### Part 1: Task 1 - DynamoDB Lambda (45 minutes)

#### Step 1: Create DynamoDB Table

```bash
aws dynamodb create-table \
    --table-name UserSkillProfiles \
    --attribute-definitions AttributeName=user_id,AttributeType=S \
    --key-schema AttributeName=user_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

Verify table creation:

```bash
aws dynamodb describe-table --table-name UserSkillProfiles --region us-east-1
```

#### Step 2: Create IAM Role for Task 1

```bash
# Create the role
aws iam create-role \
    --role-name LambdaDynamoDBRole \
    --assume-role-policy-document file://trust-policy.json

# Attach the policy
aws iam put-role-policy \
    --role-name LambdaDynamoDBRole \
    --policy-name DynamoDBAccess \
    --policy-document file://task1-dynamodb-lambda/iam-policy.json

# Wait for role to propagate (10 seconds)
sleep 10
```

#### Step 3: Deploy Task 1 Lambda

```bash
cd task1-dynamodb-lambda

# Package the function
zip function.zip lambda_function.py

# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create Lambda function
aws lambda create-function \
    --function-name UserSkillProfileManager \
    --runtime python3.10 \
    --role arn:aws:iam::${ACCOUNT_ID}:role/LambdaDynamoDBRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 30 \
    --memory-size 256 \
    --environment Variables={TABLE_NAME=UserSkillProfiles} \
    --region us-east-1

cd ..
```

#### Step 4: Test Task 1

```bash
# Test store operation
aws lambda invoke \
    --function-name UserSkillProfileManager \
    --payload '{"operation":"store_profile","user_id":"test_user_001","profile_data":{"weak_topics":["Dynamic Programming","Graph Algorithms"],"strong_topics":["Array","Hash Table"],"total_solved":150}}' \
    --cli-binary-format raw-in-base64-out \
    response1.json

cat response1.json

# Test get operation
aws lambda invoke \
    --function-name UserSkillProfileManager \
    --payload '{"operation":"get_profile","user_id":"test_user_001"}' \
    --cli-binary-format raw-in-base64-out \
    response2.json

cat response2.json
```

### Part 2: Task 2 - Bedrock AI Lambda (1 hour)

#### Step 1: Enable Bedrock Model Access

**Via AWS Console:**

1. Go to AWS Console → Amazon Bedrock
2. Click "Model access" in left sidebar
3. Click "Manage model access"
4. Find "Anthropic Claude 3 Sonnet"
5. Check the box and click "Request model access"
6. Wait for approval (usually instant)

**Verify access:**

```bash
aws bedrock list-foundation-models --region us-east-1 | grep claude-3-sonnet
```

#### Step 2: Create IAM Role for Task 2

```bash
# Create the role
aws iam create-role \
    --role-name LambdaBedrockRole \
    --assume-role-policy-document file://trust-policy.json

# Attach the policy
aws iam put-role-policy \
    --role-name LambdaBedrockRole \
    --policy-name BedrockAccess \
    --policy-document file://task2-bedrock-ai-lambda/iam-policy.json

# Wait for role to propagate
sleep 10
```

#### Step 3: Deploy Task 2 Lambda

```bash
cd task2-bedrock-ai-lambda

# Package the function
zip function.zip lambda_function.py

# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create Lambda function
aws lambda create-function \
    --function-name BedrockLearningRoadmap \
    --runtime python3.10 \
    --role arn:aws:iam::${ACCOUNT_ID}:role/LambdaBedrockRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 60 \
    --memory-size 512 \
    --region us-east-1

cd ..
```

#### Step 4: Test Task 2

```bash
# Test with beginner profile
aws lambda invoke \
    --function-name BedrockLearningRoadmap \
    --payload '{"weak_topics":["Dynamic Programming","Graph Algorithms"],"total_solved":35}' \
    --cli-binary-format raw-in-base64-out \
    response3.json

cat response3.json | jq .

# Test with intermediate profile
aws lambda invoke \
    --function-name BedrockLearningRoadmap \
    --payload '{"weak_topics":["Backtracking","Tree Traversal","Binary Search"],"total_solved":120}' \
    --cli-binary-format raw-in-base64-out \
    response4.json

cat response4.json | jq .
```

## Verification Checklist

### Task 1 Verification

- [ ] DynamoDB table "UserSkillProfiles" exists
- [ ] Lambda function "UserSkillProfileManager" deployed
- [ ] Store operation returns 200 status
- [ ] Get operation retrieves stored profile
- [ ] CloudWatch logs show successful execution

### Task 2 Verification

- [ ] Bedrock Claude 3 Sonnet access enabled
- [ ] Lambda function "BedrockLearningRoadmap" deployed
- [ ] Function returns structured 7-day roadmap
- [ ] Response includes problems, topics, and resources
- [ ] CloudWatch logs show Bedrock invocation

## Monitoring

### View CloudWatch Logs

```bash
# Task 1 logs
aws logs tail /aws/lambda/UserSkillProfileManager --follow

# Task 2 logs
aws logs tail /aws/lambda/BedrockLearningRoadmap --follow
```

### Check Metrics

```bash
# Task 1 invocations
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=UserSkillProfileManager \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 3600 \
    --statistics Sum

# Task 2 invocations
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=BedrockLearningRoadmap \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 3600 \
    --statistics Sum
```

## Cleanup (Optional)

To remove all resources:

```bash
# Delete Lambda functions
aws lambda delete-function --function-name UserSkillProfileManager
aws lambda delete-function --function-name BedrockLearningRoadmap

# Delete DynamoDB table
aws dynamodb delete-table --table-name UserSkillProfiles

# Delete IAM roles
aws iam delete-role-policy --role-name LambdaDynamoDBRole --policy-name DynamoDBAccess
aws iam delete-role --role-name LambdaDynamoDBRole

aws iam delete-role-policy --role-name LambdaBedrockRole --policy-name BedrockAccess
aws iam delete-role --role-name LambdaBedrockRole
```

## Troubleshooting

### Issue: "AccessDeniedException" for DynamoDB

**Solution:**

```bash
# Verify IAM policy is attached
aws iam get-role-policy --role-name LambdaDynamoDBRole --policy-name DynamoDBAccess

# If missing, reattach
aws iam put-role-policy \
    --role-name LambdaDynamoDBRole \
    --policy-name DynamoDBAccess \
    --policy-document file://task1-dynamodb-lambda/iam-policy.json
```

### Issue: "Model access denied" for Bedrock

**Solution:**

1. Go to AWS Console → Bedrock → Model access
2. Ensure Claude 3 Sonnet is enabled
3. Wait 5 minutes for propagation

### Issue: Lambda timeout

**Solution:**

```bash
# Increase timeout for Task 2
aws lambda update-function-configuration \
    --function-name BedrockLearningRoadmap \
    --timeout 90
```

### Issue: "Invalid JSON" from Bedrock

**Solution:**

- Check CloudWatch logs for raw response
- Adjust temperature in lambda_function.py
- Redeploy function

## Cost Monitoring

Set up billing alerts:

```bash
aws cloudwatch put-metric-alarm \
    --alarm-name lambda-cost-alert \
    --alarm-description "Alert when Lambda costs exceed $10" \
    --metric-name EstimatedCharges \
    --namespace AWS/Billing \
    --statistic Maximum \
    --period 86400 \
    --evaluation-periods 1 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold
```

## Next Steps

1. Add API Gateway for HTTP endpoints
2. Implement authentication (Cognito/JWT)
3. Add caching layer (ElastiCache)
4. Set up CI/CD pipeline
5. Connect to frontend application

---

**Deployment Complete!** 🎉

Your Lambda functions are now live and ready for the hackathon demo.
