# CodeFlow AI - AWS Lambda Backend Functions

[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws)](https://aws.amazon.com/lambda/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-blue?logo=amazon-dynamodb)](https://aws.amazon.com/dynamodb/)
[![Bedrock](https://img.shields.io/badge/AWS-Bedrock-purple?logo=amazon-aws)](https://aws.amazon.com/bedrock/)
[![Claude 3](https://img.shields.io/badge/Anthropic-Claude%203-black)](https://www.anthropic.com/)

> Transform unstructured LeetCode practice into personalized, AI-guided learning experiences

## 🎯 Project Overview

CodeFlow AI is a serverless backend system that leverages AWS services to provide intelligent learning recommendations for competitive programmers. This repository contains two production-ready Lambda functions demonstrating real AWS integrations.

### What This Project Does

1. **Stores User Skill Profiles** - Manages LeetCode user data in DynamoDB
2. **Generates AI Learning Roadmaps** - Creates personalized 7-day learning plans using Claude 3 Sonnet

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/codeflow-AI.git
cd codeflow-AI/lambda-functions

# Deploy Task 1 (DynamoDB)
cd task1-dynamodb-lambda
zip function.zip lambda_function.py
aws lambda create-function --function-name UserSkillProfileManager ...

# Deploy Task 2 (Bedrock AI)
cd ../task2-bedrock-ai-lambda
zip function.zip lambda_function.py
aws lambda create-function --function-name BedrockLearningRoadmap ...
```

See [DEPLOYMENT.md](lambda-functions/DEPLOYMENT.md) for complete instructions.

## 📁 Repository Structure

```
codeflow-AI/
├── lambda-functions/
│   ├── task1-dynamodb-lambda/          # DynamoDB Profile Manager
│   │   ├── lambda_function.py          # Main Lambda code
│   │   ├── iam-policy.json             # IAM permissions
│   │   ├── test-events.json            # Test payloads
│   │   └── README.md                   # Task 1 documentation
│   │
│   ├── task2-bedrock-ai-lambda/        # Bedrock AI Roadmap Generator
│   │   ├── lambda_function.py          # Main Lambda code
│   │   ├── iam-policy.json             # IAM permissions
│   │   ├── test-events.json            # Test payloads
│   │   └── README.md                   # Task 2 documentation
│   │
│   ├── trust-policy.json               # Lambda execution role
│   ├── DEPLOYMENT.md                   # Complete deployment guide
│   ├── .gitignore                      # Git ignore rules
│   └── README.md                       # Lambda functions overview
│
├── design.md                           # Full system design document
└── README.md                           # This file
```

## 🎨 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT APPLICATION                       │
│                  (Future: React Frontend)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   AWS API GATEWAY (Future)                   │
│              REST API with JWT Authentication                │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│  TASK 1: Profile Manager │  │ TASK 2: AI Roadmap Gen   │
│  ┌────────────────────┐  │  │  ┌────────────────────┐  │
│  │ Lambda Function    │  │  │  │ Lambda Function    │  │
│  │ Python 3.10        │  │  │  │ Python 3.10        │  │
│  │ - store_profile()  │  │  │  │ - generate_path()  │  │
│  │ - get_profile()    │  │  │  │ - invoke_bedrock() │  │
│  └────────────────────┘  │  │  └────────────────────┘  │
└──────────────────────────┘  └──────────────────────────┘
                │                           │
                ▼                           ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│     Amazon DynamoDB      │  │    Amazon Bedrock        │
│  ┌────────────────────┐  │  │  ┌────────────────────┐  │
│  │ UserSkillProfiles  │  │  │  │ Claude 3 Sonnet    │  │
│  │ - user_id (PK)     │  │  │  │ - Model ID: v1:0   │  │
│  │ - weak_topics      │  │  │  │ - Temperature: 0.3 │  │
│  │ - strong_topics    │  │  │  │ - Max Tokens: 4096 │  │
│  │ - total_solved     │  │  │  └────────────────────┘  │
│  └────────────────────┘  │  └──────────────────────────┘
└──────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│                    AWS CloudWatch Logs                        │
│              Monitoring, Metrics, and Alerting                │
└──────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

### Task 1: DynamoDB Profile Manager

- ✅ Store user skill profiles with weak/strong topics
- ✅ Retrieve profiles by user_id
- ✅ Automatic timestamps (created_at, updated_at)
- ✅ Input validation and error handling
- ✅ CloudWatch logging

### Task 2: Bedrock AI Roadmap Generator

- ✅ AI-powered learning roadmap generation
- ✅ Adaptive difficulty (Beginner/Intermediate/Advanced)
- ✅ 7-day structured learning plans
- ✅ Topic-wise recommendations
- ✅ No code spoilers (conceptual guidance only)
- ✅ JSON-formatted responses

## 🔧 Technologies Used

- **AWS Lambda** - Serverless compute
- **Amazon DynamoDB** - NoSQL database
- **Amazon Bedrock** - Managed AI service
- **Anthropic Claude 3 Sonnet** - Large language model
- **Python 3.10** - Runtime environment
- **AWS CloudWatch** - Logging and monitoring
- **AWS IAM** - Security and permissions

## 📊 Example Usage

### Task 1: Store and Retrieve Profile

```python
# Store profile
{
  "operation": "store_profile",
  "user_id": "user_12345",
  "profile_data": {
    "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
    "strong_topics": ["Array", "Hash Table"],
    "total_solved": 150
  }
}

# Response
{
  "statusCode": 200,
  "body": {
    "message": "Profile stored successfully",
    "user_id": "user_12345",
    "profile": { ... }
  }
}
```

### Task 2: Generate Learning Roadmap

```python
# Request
{
  "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
  "total_solved": 35
}

# Response
{
  "statusCode": 200,
  "body": {
    "message": "Learning roadmap generated successfully",
    "user_level": "Beginner",
    "roadmap": {
      "roadmap": [
        {
          "day": 1,
          "focus_topic": "Dynamic Programming Basics",
          "daily_goal": "Understand memoization",
          "problems": [ ... ],
          "study_resources": [ ... ]
        }
      ],
      "overall_strategy": "...",
      "success_metrics": "..."
    }
  }
}
```

## 💰 Cost Estimation

### Monthly Cost (1000 users, moderate usage)

| Service | Usage | Cost |
|---------|-------|------|
| Lambda (Task 1) | 10K invocations | $0.20 |
| Lambda (Task 2) | 4K invocations | $0.20 |
| DynamoDB | 10K writes, 50K reads | $15 |
| Bedrock (Claude 3) | 4K requests | $300 |
| CloudWatch Logs | 5GB | $2.50 |
| **Total** | | **~$318/month** |

## 🔒 Security

- IAM role-based access control
- Least privilege permissions
- Input validation on all endpoints
- Error sanitization (no sensitive data in logs)
- HTTPS/TLS for all communications

## 📈 Monitoring & Logging

All functions log to CloudWatch:

```bash
# View Task 1 logs
aws logs tail /aws/lambda/UserSkillProfileManager --follow

# View Task 2 logs
aws logs tail /aws/lambda/BedrockLearningRoadmap --follow
```

## 🎯 Hackathon Validation

This project demonstrates:

✅ **Real AWS Integration** - Not mocked, uses actual services  
✅ **AI Capability** - Bedrock Claude 3 Sonnet for intelligent recommendations  
✅ **Database Operations** - DynamoDB for persistent storage  
✅ **Production-Ready** - Error handling, logging, monitoring  
✅ **Scalable** - Serverless architecture, auto-scaling  
✅ **Verifiable** - CloudWatch logs prove execution  

## 🚀 Deployment

See [DEPLOYMENT.md](lambda-functions/DEPLOYMENT.md) for step-by-step instructions.

Quick deploy:

```bash
cd lambda-functions
./deploy.sh  # Coming soon
```

## 🧪 Testing

Each function includes comprehensive test events:

```bash
# Test Task 1
aws lambda invoke \
    --function-name UserSkillProfileManager \
    --payload file://task1-dynamodb-lambda/test-events.json \
    response.json

# Test Task 2
aws lambda invoke \
    --function-name BedrockLearningRoadmap \
    --payload file://task2-bedrock-ai-lambda/test-events.json \
    response.json
```

## 🔧 Troubleshooting

### Common Issues

**DynamoDB Access Denied**

```bash
aws iam get-role-policy --role-name LambdaDynamoDBRole --policy-name DynamoDBAccess
```

**Bedrock Model Access Denied**

- Go to AWS Console → Bedrock → Model access
- Enable Claude 3 Sonnet

**Lambda Timeout**

```bash
aws lambda update-function-configuration \
    --function-name BedrockLearningRoadmap \
    --timeout 90
```

## 📚 Documentation

- [Task 1 README](lambda-functions/task1-dynamodb-lambda/README.md) - DynamoDB Lambda details
- [Task 2 README](lambda-functions/task2-bedrock-ai-lambda/README.md) - Bedrock Lambda details
- [DEPLOYMENT.md](lambda-functions/DEPLOYMENT.md) - Complete deployment guide
- [design.md](design.md) - Full system design document

## 🛣️ Roadmap

- [ ] Add API Gateway integration
- [ ] Implement JWT authentication
- [ ] Add caching layer (ElastiCache)
- [ ] Build React frontend
- [ ] Add batch processing
- [ ] Implement CI/CD pipeline
- [ ] Add integration tests
- [ ] Create Terraform/CloudFormation templates

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👥 Authors

-Leher Joshi(leader)
-Kushagra Pratap Singh
-Harshita Devnani



