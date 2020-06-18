def get_exception(func):
    def catch_execption_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
    return catch_execption_func


