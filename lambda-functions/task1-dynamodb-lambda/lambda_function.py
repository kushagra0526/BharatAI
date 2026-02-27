"""
AWS Lambda Function: DynamoDB User Skill Profile Manager
Task 1: Store and retrieve LeetCode skill profiles from DynamoDB

This Lambda function provides two core operations:
1. store_profile: Save user skill profile to DynamoDB
2. get_profile: Retrieve user skill profile from DynamoDB
"""

import json
import boto3
from datetime import datetime
from typing import Dict, Any, List
import os

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'UserSkillProfiles')


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler function
    
    Expected event structure:
    {
        "operation": "store_profile" | "get_profile",
        "user_id": "string",
        "profile_data": {  # Only for store_profile
            "weak_topics": ["Array", "Dynamic Programming"],
            "strong_topics": ["Hash Table", "String"],
            "total_solved": 150
        }
    }
    """
    try:
        operation = event.get('operation')
        
        if operation == 'store_profile':
            return store_profile(event)
        elif operation == 'get_profile':
            return get_profile(event)
        else:
            return error_response(400, f"Invalid operation: {operation}")
            
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return error_response(500, f"Internal server error: {str(e)}")


def store_profile(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Store user skill profile in DynamoDB
    
    Args:
        event: Contains user_id and profile_data
        
    Returns:
        Success response with stored profile
    """
    try:
        user_id = event.get('user_id')
        profile_data = event.get('profile_data')
        
        # Validation
        if not user_id:
            return error_response(400, "user_id is required")
        
        if not profile_data:
            return error_response(400, "profile_data is required")
        
        if not isinstance(profile_data.get('weak_topics'), list):
            return error_response(400, "weak_topics must be a list")
        
        if not isinstance(profile_data.get('strong_topics'), list):
            return error_response(400, "strong_topics must be a list")
        
        if not isinstance(profile_data.get('total_solved'), (int, float)):
            return error_response(400, "total_solved must be a number")
        
        # Prepare item for DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        timestamp = datetime.utcnow().isoformat()
        
        item = {
            'user_id': user_id,
            'weak_topics': profile_data['weak_topics'],
            'strong_topics': profile_data['strong_topics'],
            'total_solved': int(profile_data['total_solved']),
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        # Store in DynamoDB
        table.put_item(Item=item)
        
        print(f"Successfully stored profile for user: {user_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Profile stored successfully',
                'user_id': user_id,
                'profile': item
            })
        }
        
    except Exception as e:
        print(f"Error in store_profile: {str(e)}")
        return error_response(500, f"Failed to store profile: {str(e)}")


def get_profile(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve user skill profile from DynamoDB
    
    Args:
        event: Contains user_id
        
    Returns:
        User profile data or error
    """
    try:
        user_id = event.get('user_id')
        
        # Validation
        if not user_id:
            return error_response(400, "user_id is required")
        
        # Query DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={'user_id': user_id})
        
        # Check if item exists
        if 'Item' not in response:
            return error_response(404, f"Profile not found for user_id: {user_id}")
        
        profile = response['Item']
        print(f"Successfully retrieved profile for user: {user_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Profile retrieved successfully',
                'user_id': user_id,
                'profile': profile
            })
        }
        
    except Exception as e:
        print(f"Error in get_profile: {str(e)}")
        return error_response(500, f"Failed to retrieve profile: {str(e)}")


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
