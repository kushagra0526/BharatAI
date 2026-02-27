# AWS Lambda Functions for CodeFlow AI

This directory contains serverless backend functions for the CodeFlow AI hackathon project. These Lambda functions demonstrate core AWS integrations including DynamoDB and Amazon Bedrock AI.

## 🎯 Project Overview

CodeFlow AI transforms unstructured LeetCode practice into personalized, AI-guided learning experiences. These Lambda functions form the backend foundation:

1. **Task 1**: DynamoDB User Profile Manager - Store and retrieve skill profiles
2. **Task 2**: Bedrock AI Learning Roadmap Generator - Generate personalized 7-day learning plans

## 📁 Project Structure

```
lambda-functions/
├── task1-dynamodb-lambda/
│   ├── lambda_function.py       # DynamoDB operations
│   ├── iam-policy.json          # IAM permissions
│   ├── test-events.json         # Test payloads
│   └── README.md                # Detailed documentation
│
├── task2-bedrock-ai-lambda/
│   ├── lambda_function.py       # Bedrock AI integration
│   ├── iam-policy.json          # IAM permissions
│   ├── test-events.json         # Test payloads
│   └── README.md                # Detailed documentation
│
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- Python 3.10+
- Basic understanding of Lambda, DynamoDB, and Bedrock

### Task 1: DynamoDB Lambda (45 mins)

```bash
cd task1-dynamodb-lambda

# 1. Create DynamoDB table
aws dynamodb create-table \
    --table-name UserSkillProfiles \
    --attribute-definitions AttributeName=user_id,AttributeType=S \
    --key-schema AttributeName=user_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

# 2. Package and deploy
zip function.zip lambda_function.py
aws lambda create-function \
    --function-name UserSkillProfileManager \
    --runtime python3.10 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/LambdaDynamoDBRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip

# 3. Test
aws lambda invoke \
    --function-name UserSkillProfileManager \
    --payload file://test-events.json \
    response.json
```

### Task 2: Bedrock AI Lambda (1 hour)

```bash
cd task2-bedrock-ai-lambda

# 1. Enable Bedrock model access (AWS Console)
# Go to Bedrock → Model access → Enable Claude 3 Sonnet

# 2. Package and deploy
zip function.zip lambda_function.py
aws lambda create-function \
    --function-name BedrockLearningRoadmap \
    --runtime python3.10 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/LambdaBedrockRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 60 \
    --memory-size 512

# 3. Test
aws lambda invoke \
    --function-name BedrockLearningRoadmap \
    --payload file://test-events.json \
    response.json
```

## 🎨 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT APPLICATION                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY (Future)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│  Task 1: Profile Manager │  │ Task 2: AI Roadmap Gen   │
│  - store_profile()       │  │ - generate_roadmap()     │
│  - get_profile()         │  │ - invoke_bedrock()       │
└──────────────────────────┘  └──────────────────────────┘
                │                           │
                ▼                           ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│       DynamoDB           │  │    Amazon Bedrock        │
│  UserSkillProfiles Table │  │  Claude 3 Sonnet Model   │
└──────────────────────────┘  └──────────────────────────┘
```

## 🔑 Key Features

### Task 1: DynamoDB Lambda

- ✅ Store user skill profiles (weak/strong topics, problems solved)
- ✅ Retrieve profiles by user_id
- ✅ Automatic timestamps (created_at, updated_at)
- ✅ Comprehensive error handling
- ✅ CloudWatch logging

### Task 2: Bedrock AI Lambda

- ✅ AI-powered learning roadmap generation
- ✅ Adaptive difficulty based on skill level
- ✅ 7-day structured learning plans
- ✅ Topic-wise recommendations
- ✅ No code spoilers (conceptual guidance only)
- ✅ JSON-formatted responses

## 📊 Testing

Each function includes comprehensive test events:

### Task 1 Test Events

```json
{
  "store_profile_event": {
    "operation": "store_profile",
    "user_id": "user_12345",
    "profile_data": {
      "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
      "strong_topics": ["Array", "Hash Table"],
      "total_solved": 150
    }
  },
  "get_profile_event": {
    "operation": "get_profile",
    "user_id": "user_12345"
  }
}
```

### Task 2 Test Events

```json
{
  "beginner_profile": {
    "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
    "total_solved": 35
  },
  "intermediate_profile": {
    "weak_topics": ["Backtracking", "Tree Traversal"],
    "total_solved": 120
  }
}
```

## 💰 Cost Estimation

### Task 1 (DynamoDB)

- Lambda: ~$0.20 per 1M requests
- DynamoDB: ~$1.25 per 1M writes, $0.25 per 1M reads
- **Monthly (1000 users)**: ~$2-5

### Task 2 (Bedrock AI)

- Lambda: ~$0.20 per 1M requests
- Bedrock Claude 3 Sonnet: ~$0.075 per request
- **Monthly (1000 users, 1 roadmap/week)**: ~$300

## 🔒 Security

Both functions implement:

- IAM role-based access control
- Least privilege permissions
- Input validation
- Error sanitization
- CloudWatch logging (no sensitive data)

## 📈 Monitoring

### CloudWatch Metrics

- Invocation count
- Error rate
- Duration
- Throttles

### Custom Logs

```bash
# Task 1 logs
aws logs tail /aws/lambda/UserSkillProfileManager --follow

# Task 2 logs
aws logs tail /aws/lambda/BedrockLearningRoadmap --follow
```

## 🎯 Hackathon Validation

These functions demonstrate:

✅ **Real AWS Integration**: Not mocked, uses actual AWS services  
✅ **AI Capability**: Bedrock Claude 3 Sonnet for intelligent recommendations  
✅ **Database Operations**: DynamoDB for persistent storage  
✅ **Production-Ready**: Error handling, logging, monitoring  
✅ **Scalable**: Serverless architecture, auto-scaling  
✅ **Verifiable**: CloudWatch logs prove execution  

## 🔧 Troubleshooting

### Common Issues

**DynamoDB Access Denied**

```bash
# Verify IAM role has correct permissions
aws iam get-role-policy --role-name LambdaDynamoDBRole --policy-name DynamoDBAccess
```

**Bedrock Model Access Denied**

```bash
# Check model access in Bedrock console
aws bedrock list-foundation-models --region us-east-1
```

**Lambda Timeout**

```bash
# Increase timeout for Bedrock function
aws lambda update-function-configuration \
    --function-name BedrockLearningRoadmap \
    --timeout 90
```

## 🚀 Next Steps

1. **API Gateway Integration**: Add HTTP endpoints
2. **Authentication**: Implement JWT/Cognito
3. **Caching**: Add ElastiCache for frequent queries
4. **Batch Processing**: Handle multiple users
5. **Frontend Integration**: Connect to React app

## 📚 Additional Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [Claude 3 Model Documentation](https://docs.anthropic.com/claude/docs)

## 🤝 Contributing

This is a hackathon project. For improvements:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

---

**Built for CodeFlow AI Hackathon** | Demonstrating AWS Lambda + DynamoDB + Bedrock AI Integration
