from vkbottle.user import User
from vkbottle.bot import Bot
from data.config import Main
from utils.database import Database

db = Database('data/db.db')

class UserBot(User):
    def __init__(self, token: str):
        super().__init__(token=token)

    async def find_pair(self, count: int, offset: int, city: int, sex: int, age: int, uid: int):
        sex_pair = int(sex) ^ 3

        result = await self.api.users.search(
            count=count,
            offset=offset,
            city=city,
            sex=sex_pair,
            has_photo=True,
            age_from=age - Main.delta,
            age_to=age + Main.delta,
            status=6
        )

        result = [
            {
                "name": item.first_name + " " + item.last_name,
                "uid": item.id,
            }
            for item in result.items if item.is_closed is False and db.get_seen(
                uid=uid,
                person=item.id
            ) is None
        ]

        return result

    async def get_photo(self, uid: int):
        photos = await self.api.photos.get(
            owner_id=uid,
            album_id='profile',
            extended=True
        )

        result = [
            {
                'owner_id': item.owner_id,
                'id': item.id,
                'likes': item.likes.count,
                'comments': item.comments.count
            } for item in photos.items
        ]

        result = sorted(result, key=lambda x: (x['likes'], x['comments']), reverse=True)

        return result[:3]

    async def get_city_id(self, country_query: str, city_query: str):
        country_data = await self.api.database.get_countries(
            code=country_query,
        )

        country_id = country_data.items[0].id

        data = await self.api.database.get_cities(
            country_id=country_id,
            q=city_query
        )

        if data.count:
            return data.items[0].id
        return None


class GroupBot(Bot):
    def __init__(self, token: str):
        super().__init__(token=token)
