import typing


def rate_limit(limit: int, key=None, text: typing.Optional[str] = None):
    """
    Decorator for configuring rate limit and key in different functions.

    :param limit:
    :param key:
    :param text:
    :return:
    """

    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        if text:
            setattr(func, "throttling_text", text)

        return func

    return decorator


def override(user_id):
    """
    Decorator for configuring override for user_id in different functions.

    :param user_id:
    :return:
    """

    def decorator(func):
        setattr(func, "override", user_id)

        return func

    return decorator
