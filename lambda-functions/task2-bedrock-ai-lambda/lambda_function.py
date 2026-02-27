"""
AWS Lambda Function: Bedrock Claude 3 Sonnet Learning Path Generator
Task 2: Generate personalized 7-day learning roadmap using AI

This Lambda function invokes Anthropic Claude 3 Sonnet via Amazon Bedrock
to generate structured learning recommendations based on user skill profile.
"""

import json
import boto3
from datetime import datetime
from typing import Dict, Any, List
import os

# Initialize Bedrock Runtime client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

# Model configuration
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
TEMPERATURE = 0.3
MAX_TOKENS = 4096


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler function
    
    Expected event structure:
    {
        "weak_topics": ["Dynamic Programming", "Graph Algorithms"],
        "total_solved": 150
    }
    """
    try:
        # Extract input parameters
        weak_topics = event.get('weak_topics', [])
        total_solved = event.get('total_solved', 0)
        
        # Validation
        if not weak_topics:
            return error_response(400, "weak_topics is required and cannot be empty")
        
        if not isinstance(weak_topics, list):
            return error_response(400, "weak_topics must be a list")
        
        if not isinstance(total_solved, (int, float)):
            return error_response(400, "total_solved must be a number")
        
        # Determine user level based on problems solved
        user_level = determine_user_level(total_solved)
        
        # Generate learning roadmap using Bedrock
        roadmap = generate_learning_roadmap(weak_topics, user_level)
        
        print(f"Successfully generated roadmap for user with {total_solved} problems solved")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Learning roadmap generated successfully',
                'user_level': user_level,
                'total_solved': total_solved,
                'weak_topics': weak_topics,
                'roadmap': roadmap,
                'generated_at': datetime.utcnow().isoformat()
            })
        }
        
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return error_response(500, f"Internal server error: {str(e)}")


def determine_user_level(total_solved: int) -> str:
    """
    Determine user skill level based on problems solved
    
    Args:
        total_solved: Total number of problems solved
        
    Returns:
        User level: Beginner, Intermediate, or Advanced
    """
    if total_solved < 50:
        return "Beginner"
    elif total_solved < 200:
        return "Intermediate"
    else:
        return "Advanced"


def generate_learning_roadmap(weak_topics: List[str], user_level: str) -> Dict[str, Any]:
    """
    Generate personalized learning roadmap using Claude 3 Sonnet
    
    Args:
        weak_topics: List of topics user struggles with
        user_level: User's skill level (Beginner/Intermediate/Advanced)
        
    Returns:
        Structured learning roadmap
    """
    try:
        # Construct the prompt
        prompt = build_prompt(weak_topics, user_level)
        
        # Prepare request body for Bedrock
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        print(f"Invoking Bedrock model: {MODEL_ID}")
        
        # Invoke Bedrock model
        response = bedrock_runtime.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_body)
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        ai_response = response_body['content'][0]['text']
        
        # Parse JSON from AI response
        roadmap = parse_ai_response(ai_response)
        
        return roadmap
        
    except Exception as e:
        print(f"Error in generate_learning_roadmap: {str(e)}")
        raise


def build_prompt(weak_topics: List[str], user_level: str) -> str:
    """
    Build structured prompt for Claude 3 Sonnet
    
    Args:
        weak_topics: List of weak topics
        user_level: User's skill level
        
    Returns:
        Formatted prompt string
    """
    topics_str = ", ".join(weak_topics)
    
    prompt = f"""You are an expert competitive programming mentor specializing in LeetCode preparation.

User Profile:
- Skill Level: {user_level}
- Weak Topics: {topics_str}

Task: Generate a structured 7-day learning roadmap to help this user improve their weak topics.

Requirements:
1. Focus on the weak topics provided
2. Provide 2-3 specific problem recommendations per day
3. Include topic-wise recommendations (which concepts to study)
4. Provide learning resources (no full solutions, only conceptual guidance)
5. Ensure progressive difficulty (start easier, build up)
6. Include daily goals and milestones

Return your response in the following JSON format:
{{
  "roadmap": [
    {{
      "day": 1,
      "focus_topic": "Topic name",
      "daily_goal": "What to achieve today",
      "problems": [
        {{
          "title": "Problem name",
          "difficulty": "Easy/Medium/Hard",
          "key_concept": "Main concept to learn",
          "approach_hint": "High-level approach (no code)"
        }}
      ],
      "study_resources": [
        "Resource 1: Brief description",
        "Resource 2: Brief description"
      ]
    }}
  ],
  "overall_strategy": "Brief overview of the 7-day plan",
  "success_metrics": "How to measure progress"
}}

Important: Return ONLY valid JSON, no additional text or markdown formatting."""
    
    return prompt


def parse_ai_response(ai_response: str) -> Dict[str, Any]:
    """
    Parse and validate AI response
    
    Args:
        ai_response: Raw response from Claude
        
    Returns:
        Parsed roadmap dictionary
    """
    try:
        # Try to extract JSON from response
        # Sometimes Claude wraps JSON in markdown code blocks
        if "```json" in ai_response:
            start = ai_response.find("```json") + 7
            end = ai_response.find("```", start)
            json_str = ai_response[start:end].strip()
        elif "```" in ai_response:
            start = ai_response.find("```") + 3
            end = ai_response.find("```", start)
            json_str = ai_response[start:end].strip()
        else:
            json_str = ai_response.strip()
        
        roadmap = json.loads(json_str)
        
        # Validate structure
        if 'roadmap' not in roadmap:
            raise ValueError("Response missing 'roadmap' field")
        
        return roadmap
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse AI response as JSON: {str(e)}")
        print(f"Raw response: {ai_response}")
        raise ValueError(f"Invalid JSON response from AI: {str(e)}")


def error_response(status_code: int, message: str) -> Dict[str, Any]:
    """
    Generate standardized error response
    
    Args:
        status_code: HTTP status code
        message: Error message
        
    Returns:
        Formatted error response
    """
    return {
        'statusCode': status_code,
        'body': json.dumps({
            'error': message,
            'timestamp': datetime.utcnow().isoformat()
        })
    }
