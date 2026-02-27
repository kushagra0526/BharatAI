# Task 2: Bedrock Claude 3 Sonnet Learning Roadmap Generator

## Overview

This Lambda function leverages **Amazon Bedrock** with **Anthropic Claude 3 Sonnet** to generate personalized 7-day learning roadmaps for competitive programmers. It analyzes weak topics and skill level to create structured, progressive learning plans.

## Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Client    │─────▶│  Lambda Function │─────▶│  Amazon Bedrock │
│  (API Call) │      │  (Python 3.10)   │      │  Claude 3 Sonnet│
└─────────────┘      └──────────────────┘      └─────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   CloudWatch     │
                     │      Logs        │
                     └──────────────────┘
```

## Key Features

✅ **AI-Powered Recommendations**: Uses Claude 3 Sonnet for intelligent problem selection  
✅ **Adaptive Difficulty**: Adjusts based on user's total problems solved  
✅ **Structured Output**: Returns JSON-formatted 7-day roadmap  
✅ **Progressive Learning**: Builds from easier to harder concepts  
✅ **No Code Spoilers**: Provides conceptual guidance only  

## Model Configuration

- **Model**: `anthropic.claude-3-sonnet-20240229-v1:0`
- **Temperature**: `0.3` (balanced creativity and consistency)
- **Max Tokens**: `4096`
- **Region**: `us-east-1`

## Setup Instructions

### 1. Enable Bedrock Model Access

1. Go to AWS Bedrock Console
2. Navigate to "Model access"
3. Request access to **Anthropic Claude 3 Sonnet**
4. Wait for approval (usually instant)

### 2. Create IAM Role

Create an IAM role with the policy from `iam-policy.json`:

```bash
aws iam create-role \
    --role-name LambdaBedrockRole \
    --assume-role-policy-document file://trust-policy.json

aws iam put-role-policy \
    --role-name LambdaBedrockRole \
    --policy-name BedrockAccess \
    --policy-document file://iam-policy.json
```

### 3. Deploy Lambda Function

```bash
# Package the function
zip function.zip lambda_function.py

# Create Lambda function
aws lambda create-function \
    --function-name BedrockLearningRoadmap \
    --runtime python3.10 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/LambdaBedrockRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 60 \
    --memory-size 512 \
    --region us-east-1
```

## Usage Examples

### Beginner User

**Request:**

```json
{
  "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
  "total_solved": 35
}
```

**Response:**

```json
{
  "statusCode": 200,
  "body": {
    "message": "Learning roadmap generated successfully",
    "user_level": "Beginner",
    "total_solved": 35,
    "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
    "roadmap": {
      "roadmap": [
        {
          "day": 1,
          "focus_topic": "Dynamic Programming Basics",
          "daily_goal": "Understand memoization and basic DP patterns",
          "problems": [
            {
              "title": "Climbing Stairs",
              "difficulty": "Easy",
              "key_concept": "Basic recursion with memoization",
              "approach_hint": "Think about how many ways to reach step n from n-1 and n-2"
            }
          ],
          "study_resources": [
            "Watch: Introduction to Dynamic Programming",
            "Read: Top-down vs Bottom-up DP"
          ]
        }
      ],
      "overall_strategy": "Start with simple DP problems, then move to graph fundamentals",
      "success_metrics": "Complete 2-3 problems daily, understand core concepts"
    },
    "generated_at": "2026-02-27T10:30:00.000Z"
  }
}
```

### Intermediate User

**Request:**

```json
{
  "weak_topics": ["Backtracking", "Tree Traversal", "Binary Search"],
  "total_solved": 120
}
```

**Response:**

```json
{
  "statusCode": 200,
  "body": {
    "message": "Learning roadmap generated successfully",
    "user_level": "Intermediate",
    "total_solved": 120,
    "weak_topics": ["Backtracking", "Tree Traversal", "Binary Search"],
    "roadmap": {
      "roadmap": [
        {
          "day": 1,
          "focus_topic": "Backtracking Fundamentals",
          "daily_goal": "Master the backtracking template",
          "problems": [
            {
              "title": "Subsets",
              "difficulty": "Medium",
              "key_concept": "Decision tree exploration",
              "approach_hint": "For each element, decide to include or exclude it"
            }
          ],
          "study_resources": [
            "Study: Backtracking template pattern",
            "Practice: Drawing decision trees"
          ]
        }
      ],
      "overall_strategy": "Focus on pattern recognition across different problem types",
      "success_metrics": "Solve 2 medium problems per day independently"
    },
    "generated_at": "2026-02-27T10:30:00.000Z"
  }
}
```

## Testing

Use the AWS Lambda console or CLI to test with events from `test-events.json`:

```bash
# Test with beginner profile
aws lambda invoke \
    --function-name BedrockLearningRoadmap \
    --payload file://test-events.json \
    --cli-binary-format raw-in-base64-out \
    response.json

# View response
cat response.json | jq .
```

## User Level Classification

The function automatically determines user level:

| Total Solved | Level        | Roadmap Focus                    |
|--------------|--------------|----------------------------------|
| < 50         | Beginner     | Fundamentals, easy problems      |
| 50-199       | Intermediate | Pattern recognition, medium      |
| 200+         | Advanced     | Complex algorithms, hard problems|

## Error Handling

The function includes comprehensive error handling:

- **400**: Invalid input (missing/wrong type for weak_topics or total_solved)
- **500**: Bedrock invocation errors, JSON parsing failures

All errors are logged to CloudWatch with full context.

## Monitoring

### CloudWatch Logs

```bash
# Tail logs in real-time
aws logs tail /aws/lambda/BedrockLearningRoadmap --follow

# Filter for errors
aws logs filter-pattern /aws/lambda/BedrockLearningRoadmap --filter-pattern "ERROR"
```

### Bedrock Invocation Metrics

Track in CloudWatch Metrics:

- `bedrock:InvokeModel` - Number of API calls
- `bedrock:ModelInvocationLatency` - Response time
- `bedrock:ModelInvocationErrors` - Error count

## Cost Estimation

### Lambda Costs

- **Compute**: ~$0.20 per 1M requests (512MB, 5s avg)
- **Duration**: ~$0.0000083 per second

### Bedrock Costs (Claude 3 Sonnet)

- **Input tokens**: $0.003 per 1K tokens (~$0.015 per request)
- **Output tokens**: $0.015 per 1K tokens (~$0.060 per request)
- **Total per request**: ~$0.075

### Example Monthly Cost (1000 users, 1 roadmap/week)

- Lambda: ~$0.80
- Bedrock: ~$300
- **Total**: ~$301/month

## Response Format

The AI returns a structured JSON roadmap:

```json
{
  "roadmap": [
    {
      "day": 1,
      "focus_topic": "Topic name",
      "daily_goal": "What to achieve",
      "problems": [
        {
          "title": "Problem name",
          "difficulty": "Easy/Medium/Hard",
          "key_concept": "Main learning point",
          "approach_hint": "High-level strategy"
        }
      ],
      "study_resources": ["Resource 1", "Resource 2"]
    }
  ],
  "overall_strategy": "7-day plan overview",
  "success_metrics": "How to measure progress"
}
```

## Validation & Testing

The function validates:

1. ✅ `weak_topics` is a non-empty list
2. ✅ `total_solved` is a number
3. ✅ Bedrock response is valid JSON
4. ✅ Response contains required `roadmap` field

## Next Steps

- Add caching for common topic combinations
- Implement streaming responses for real-time updates
- Add support for custom difficulty preferences
- Integrate with DynamoDB to store generated roadmaps
- Add A/B testing for different prompt strategies

## Troubleshooting

### "Model access denied"

- Ensure Bedrock model access is enabled in your AWS account
- Verify IAM role has `bedrock:InvokeModel` permission

### "Invalid JSON response"

- Check CloudWatch logs for raw AI response
- Adjust temperature or prompt if responses are inconsistent

### "Timeout errors"

- Increase Lambda timeout (current: 60s)
- Consider using streaming responses for faster feedback
