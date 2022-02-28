from backend.db.helper import get_api_run_count


def is_api_run_limit_exceeded(user_id: str):
    """
    Check if API run limit is exceeded by user
    """
    count, limit = get_api_run_count(user_id)

    if count >= limit:
        return True

    return False
