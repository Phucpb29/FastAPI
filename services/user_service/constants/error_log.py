def reponse_error_log(error_code: int, message: str):
    return {
        'status': False,
        'error_code': error_code,
        'error_message': message
    }
