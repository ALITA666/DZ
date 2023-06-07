from vkbottle.bot import Blueprint
from vkbottle.bot import Message
from datetime import datetime

from utils.database import Database
from utils.bot import UserBot
from data.config import Tokens, Main

bp = Blueprint()
db = Database('data/db.db')
user = UserBot(token=Tokens.user)

users_pairs: dict[int, list] = {}


@bp.on.private_message(text=['Начать', 'начать'])
async def start_handler_def(message: Message):
    result = db.get_user_or_none(message.from_id)

    if result is None:
        user_info = await user.api.users.get(user_ids=[message.from_id], fields=["relation", "sex", "bdate", "city"])
        user_info = user_info[0]

        # bdate = True if user_info.bdate else False
        bdate = False
        sex = True if user_info.sex else False

        city = True if user_info.city else False

        try:
            bdate_datetime = datetime.strptime(user_info.bdate, "%d.%m.%Y")
            age = (datetime.now() - bdate_datetime).days // 365

        except ValueError as ex:
            bdate = False

        if bdate and sex and city:
            sex = user_info.sex
            city = user_info.city.id

            db.register(
                uid=message.from_id,
                sex=sex,
                age=age,
                city=city
            )

            await message.answer(
                message="Успешно Вас зарегистрировали. Напишите мне 'Поиск', чтобы начать подбор кандидатов"
            )

        else:
            message_text = f'''Ваш профиль не полностью заполнено

Дата рождения - {"не заполнено или не виден год. Напишите «Дата рождение: день.месяц.год». Пример - «Дата рождения: 01.11.2003»" if not bdate else "заполнено"}
Пол - {"не заполнено. Напишите «Пол: ваш пол (м/ж)». Пример - «Пол: м»" if not sex else "заполнено"}
Город - {"не заполнено. Напишите «Город: страна(RU, BY), город». Пример - «Город: RU, Москва»" if not city else "заполнено"}

Заполните профиль и напишите мне "Начать"'''

            await message.answer(
                message=message_text
            )

            db.register(
                uid=message.from_id,
                sex=user_info.sex if sex else None,
                age=age if bdate else None,
                city=user_info.city.id if city else None
            )
    else:
        await message.answer(
            message="Напишите мне 'Поиск', чтобы начать подбор кандидатов"
        )


@bp.on.private_message(text=["Город: <country>, <city>"])
async def update_city_handler_def(message: Message, country: str, city: str):
    data = db.get_user_or_none(message.from_id)

    if data[-1] is None:
        if country in ('RU', 'BY'):
            city_id = await user.get_city_id(
                country_query=country,
                city_query=city
            )

            if city_id:
                query = 'UPDATE users SET city = ? WHERE uid = ?'
                db.execute(
                    query=query,
                    params=(city_id, message.from_id)
                )
                db.commit()

                await message.answer(
                    message='Город успешно заполнен. Напишите "Поиск"'
                )
            else:
                await message.answer(
                    message='Проблема с поиском города. Проверьте данные!'
                )
        else:
            await message.answer('Допущена ошибка в стране!')
    else:
        await message.answer('Город не требуется заполнять')


@bp.on.private_message(text=["Пол: <sex>"])
async def update_sex_handler_def(message: Message, sex: str):
    data = db.get_user_or_none(message.from_id)

    if data[1] is None:
        if sex.lower() in ('м', 'ж'):
            sex_id = 1 if sex.lower() == 'м' else 'ж'

            query = 'UPDATE users SET sex = ? WHERE uid = ?'
            db.execute(
                query=query,
                params=(sex_id, message.from_id)
            )
            db.commit()

            await message.answer(
                message='Пол успешно заполнен. Напишите "Поиск"'
            )
        else:
            await message.answer(
                message='Допущена ошибка в поле!'
            )
    else:
        await message.answer(
            message='Пол не требуется заполнять'
        )


@bp.on.private_message(text=["Дата рождения: <date>"])
async def update_age_handler_def(message: Message, date: str):
    data = db.get_user_or_none(message.from_id)

    if data[2] is None:
        try:
            bdate = datetime.strptime(date, '%d.%m.%Y')
            age = (datetime.now() - bdate).days // 365
        except ValueError:
            await message.answer(
                message='Неверный формат даты!'
            )
            return

        print(age)

        query = 'UPDATE users SET age = ? WHERE uid = ?'
        db.execute(
            query=query,
            params=(age, message.from_id)
        )
        db.commit()

        await message.answer(
            message='Возраст успешно заполнен. Напишите "Поиск"'
        )


    else:
        await message.answer(
            message='Возраст не требуется заполнять'
        )


@bp.on.private_message(text=['Поиск', 'поиск'])
async def search_handler_def(message: Message):
    data: list = db.get_user_or_none(message.from_id)

    if data is None or None in data:
        await message.answer(
            message="Вы не зарегистрированы, напишите 'Начать' и попробуйте потом снова"
        )

    else:

        await message.answer(
            message='Начинаю поиск. Ожидайте'
        )

        if users_pairs.get(message.from_id) is None:
            users_pairs[message.from_id] = []

        if len(users_pairs[message.from_id]) == 0:
            result = await user.find_pair(
                count=Main.count,
                offset=Main.offset,
                city=data[3],
                sex=data[1],
                age=data[2],
                uid=message.from_id
            )

            Main.offset += Main.count + 1

            while len(result) == 0:
                result = await user.find_pair(
                    count=Main.count,
                    offset=Main.offset,
                    city=data[3],
                    sex=data[1],
                    age=data[2],
                    uid=message.from_id
                )

                Main.offset += Main.count + 1

            users_pairs[message.from_id] = result

        person = users_pairs[message.from_id][0]
        photos = await user.get_photo(
            uid=person.get('uid')
        )

        photo_string = ''

        for photo in photos:
            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'

        await message.answer(
            message=f'''Имя - {person['name']}
                
ссылка - vk.com/id{person["uid"]}''',
            attachment=photo_string
        )

        db.add_seen(
            uid=message.from_id,
            person=person.get('uid')
        )

        users_pairs[message.from_id].pop(0)
        print(users_pairs)


@bp.on.private_message()
async def default_handler_def(message: Message):
    await message.answer(
        message="Неизвестная команда, напишите мне 'Начать'"
    )
