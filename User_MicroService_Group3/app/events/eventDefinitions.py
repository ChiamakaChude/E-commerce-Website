def updated_username(user_id, new_username):

    return {"event_type": "profile_updated",
        "user_id": user_id,
        "new_username": new_username}