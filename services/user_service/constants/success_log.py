def reponse_success_log(success_code: int, message: str):
    return {
        'code': success_code,
        'status': True,
        'msg': message
    }
