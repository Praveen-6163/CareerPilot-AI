def format_error_response(error_code, message, user_action=None, status_code=400):
    payload = {
        'success': False,
        'error_code': error_code,
        'message': message,
    }
    if user_action:
        payload['user_action'] = user_action
    return payload, status_code
