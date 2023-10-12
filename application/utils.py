from datetime import datetime

from fastapi import Depends, HTTPException

import application
from application import schemas
from application.auth import get_current_user

user_request_count = {}

MAX_REQUESTS_PER_MINUTE = 3


def rate_limiting(
        current_user: application.schemas.UserInDB = Depends(application.auth.get_current_user)
):
    username = current_user.username

    if is_rate_limit_exceeded(username):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. You can only make {MAX_REQUESTS_PER_MINUTE} requests per minute.",
        )


def is_rate_limit_exceeded(username: str) -> bool:
    current_time = datetime.now()

    if username not in user_request_count:
        user_request_count[username] = {
            "count": 1,
            "timestamp": current_time
        }
        return False
    else:
        user_info = user_request_count[username]
        if user_info["count"] >= MAX_REQUESTS_PER_MINUTE:
            if (current_time - user_info["timestamp"]).total_seconds() >= 60:
                user_info["count"] = 1
                user_info["timestamp"] = current_time
                return False
            else:
                return True
        else:
            user_info["count"] += 1
            return False
