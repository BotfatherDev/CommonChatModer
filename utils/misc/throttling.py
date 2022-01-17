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
