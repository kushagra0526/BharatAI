# Task 1: DynamoDB User Skill Profile Manager

## Overview

This Lambda function manages LeetCode user skill profiles in DynamoDB. It provides two core operations:

- **store_profile**: Save user skill profiles with weak/strong topics and problem counts
- **get_profile**: Retrieve stored user profiles

## Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Client    │─────▶│  Lambda Function │─────▶│    DynamoDB     │
│  (API Call) │      │  (Python 3.10)   │      │ UserSkillProfiles│
└─────────────┘      └──────────────────┘      └─────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   CloudWatch     │
                     │      Logs        │
                     └──────────────────┘
```

## DynamoDB Table Schema

**Table Name**: `UserSkillProfiles`

| Attribute      | Type   | Description                          |
|----------------|--------|--------------------------------------|
| user_id        | String | Partition Key - Unique user ID       |
| weak_topics    | List   | Topics user struggles with           |
| strong_topics  | List   | Topics user excels at                |
| total_solved   | Number | Total problems solved                |
| created_at     | String | ISO timestamp of profile creation    |
| updated_at     | String | ISO timestamp of last update         |

## Setup Instructions

### 1. Create DynamoDB Table

```bash
aws dynamodb create-table \
    --table-name UserSkillProfiles \
    --attribute-definitions AttributeName=user_id,AttributeType=S \
    --key-schema AttributeName=user_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

### 2. Create IAM Role

Create an IAM role with the policy from `iam-policy.json`:

```bash
aws iam create-role \
    --role-name LambdaDynamoDBRole \
    --assume-role-policy-document file://trust-policy.json

aws iam put-role-policy \
    --role-name LambdaDynamoDBRole \
    --policy-name DynamoDBAccess \
    --policy-document file://iam-policy.json
```

### 3. Deploy Lambda Function

```bash
# Package the function
zip function.zip lambda_function.py

# Create Lambda function
aws lambda create-function \
    --function-name UserSkillProfileManager \
    --runtime python3.10 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/LambdaDynamoDBRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 30 \
    --memory-size 256 \
    --environment Variables={TABLE_NAME=UserSkillProfiles}
```

## Usage Examples

### Store Profile

**Request:**

```json
{
  "operation": "store_profile",
  "user_id": "user_12345",
  "profile_data": {
    "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
    "strong_topics": ["Array", "Hash Table", "String"],
    "total_solved": 150
  }
}
```

**Response:**

```json
{
  "statusCode": 200,
  "body": {
    "message": "Profile stored successfully",
    "user_id": "user_12345",
    "profile": {
      "user_id": "user_12345",
      "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
      "strong_topics": ["Array", "Hash Table", "String"],
      "total_solved": 150,
      "created_at": "2026-02-27T10:30:00.000Z",
      "updated_at": "2026-02-27T10:30:00.000Z"
    }
  }
}
```

### Get Profile

**Request:**

```json
{
  "operation": "get_profile",
  "user_id": "user_12345"
}
```

**Response:**

```json
{
  "statusCode": 200,
  "body": {
    "message": "Profile retrieved successfully",
    "user_id": "user_12345",
    "profile": {
      "user_id": "user_12345",
      "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
      "strong_topics": ["Array", "Hash Table", "String"],
      "total_solved": 150,
      "created_at": "2026-02-27T10:30:00.000Z",
      "updated_at": "2026-02-27T10:30:00.000Z"
    }
  }
}
```

## Testing

Use the AWS Lambda console or CLI to test with events from `test-events.json`:

```bash
aws lambda invoke \
    --function-name UserSkillProfileManager \
    --payload file://test-events.json \
    --cli-binary-format raw-in-base64-out \
    response.json
```

## Error Handling

The function includes comprehensive error handling:

- **400**: Invalid input (missing fields, wrong types)
- **404**: Profile not found
- **500**: Internal server errors (DynamoDB issues, etc.)

All errors are logged to CloudWatch for debugging.

## Monitoring

View logs in CloudWatch:

```bash
aws logs tail /aws/lambda/UserSkillProfileManager --follow
```

## Cost Estimation

- **Lambda**: ~$0.20 per 1M requests (256MB, 100ms avg)
- **DynamoDB**: Pay-per-request pricing (~$1.25 per 1M writes, $0.25 per 1M reads)
- **CloudWatch Logs**: ~$0.50 per GB

## Next Steps

- Add batch operations for multiple profiles
- Implement profile update with merge logic
- Add GSI for querying by topic
- Integrate with API Gateway for HTTP endpoints
