def reponse_success_log(success_code: int, message: str):
    return {
        'code': success_code,
        'status': True,
        'msg': message
    }


def reponse_success_log_object(success_code: int, key: str, message: str):
    message_convert = {
        key: message
    }
    return {
        'code': success_code,
        'status': True,
        'msg': message_convert
    }
