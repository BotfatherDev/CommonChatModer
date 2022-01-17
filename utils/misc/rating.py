
import typing
from loader import db, cache_rating


def get_rating(user_id: int, rating: int):
    total_rating = rating
    if rating_user := db.get_rating_by_user_id(user_id):
        total_rating: int = rating_user[1] + rating
        db.update_rating_by_user_id(user_id, total_rating)
    else:
        db.add_user_for_rating(user_id)
    return total_rating

def caching_rating(helper_id, user_id, message_id) -> typing.Union[str, bool]:
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
