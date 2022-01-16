import asyncio
import datetime
import typing

from aiogram.types import Message

from loader import db, cache_helpers, cache_rating


def get_rating(user_id: int, rating: int):
    total_rating = rating
    if rating_user := db.get_rating_by_user_id(user_id):
        total_rating: int = rating_user[1] + rating
        db.update_rating_by_user_id(user_id, total_rating)
    else:
        db.add_user_for_rating(user_id)
    return total_rating


async def flood_helper(m: Message):
    msg = await m.answer("Вы не можете так часто начислять рейтинг. (<i>Сообщение автоматически удалится</i>")
    await asyncio.sleep(5)
    await msg.delete()


def throttling_rating(**kwargs):
    def decorator(func):

        def wrapper(m: Message, helper_id, user_id, *args):
            datetime_now = datetime.datetime.now()
            flood_wait = datetime_now + datetime.timedelta(**kwargs)
            if not (helper := cache_helpers.get(user_id)):
                cache_helpers.update(
                    {
                        user_id: {
                            "flood_wait": flood_wait
                        }
                    }
                )
            else:
                flood_wait: datetime.datetime = helper['flood_wait']

            if helper:
                if datetime_now < flood_wait:
                    print(flood_wait, datetime_now)
                    asyncio.create_task(flood_helper(m))
                    return "flood"
                else:
                    del cache_helpers[user_id]

            return func(m, helper_id, user_id, *args)

        return wrapper

    return decorator


@throttling_rating(seconds=10)
def caching_rating(m: Message, helper_id, user_id, message_id) -> typing.Union[str, bool]:
    obj_rating = {
        "helper_id": helper_id,
        "user_id": user_id
    }

    if ratings := cache_rating.get(message_id):
        if obj_rating not in ratings:
            cache_rating.update(
                {
                    message_id: ratings.append(obj_rating)
                }
            )
            return True
    else:
        cache_rating.update(
            {
                message_id: [obj_rating]
            }
        )
        return True
