from datetime import datetime

from fastapi import Depends, HTTPException

import application
from application import schemas
from application.auth import get_current_user

# Dictionary to keep track of user request counts and timestamps
user_request_count = {}

# Maximum allowed requests per minute per user
MAX_REQUESTS_PER_MINUTE = 3


def rate_limiting(
        current_user: application.schemas.UserInDB = Depends(application.auth.get_current_user)
):
    # Get the username of the current user
    username = current_user.username

    # Check rate limit for the user
    if not is_rate_limited(username):
        raise HTTPException(
            status_code=429,  # Too Many Requests
            detail=f"Rate limit exceeded. You can only make {MAX_REQUESTS_PER_MINUTE} requests per minute.",
        )


def is_rate_limited(username: str) -> bool:
    # Get the current time
    current_time = datetime.now()

    # Check if the user's request count is within the limit
    if username not in user_request_count:
        # Initialize request count for the user
        user_request_count[username] = {
            "count": 1,
            "timestamp": current_time
        }
        return True
    else:
        # Check if the user's request count exceeds the limit
        user_info = user_request_count[username]
        if user_info["count"] >= MAX_REQUESTS_PER_MINUTE:
            # Check if a minute has passed since the first request
            if (current_time - user_info["timestamp"]).total_seconds() >= 60:
                # Reset the count and timestamp
                user_info["count"] = 1
                user_info["timestamp"] = current_time
                return True
            else:
                return False
        else:
            # Increment the request count
            user_info["count"] += 1
            return True
