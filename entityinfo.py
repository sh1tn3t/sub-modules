#    Sh1t-UB (telegram userbot by sh1tn3t)
#    Copyright (C) 2021-2022 Sh1tN3t

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

from pyrogram import Client, types, errors
from .. import loader, utils


def yes_no(boolean: bool):
    return "Да" if boolean else "Нет"


@loader.module("EntityInfo", "sh1tn3t")
class EntityInfoMod(loader.Module):
    """Полная информация о пользователе"""

    async def whois_cmd(self, app: Client, message: types.Message, args: str):
        """Получить информацию о пользователе. Использование: whois <@ или реплай или ничего>"""
        reply = message.reply_to_message

        try:
            user = await app.get_users(
                int(args)
                if args.isdigit()
                else reply.from_user.id
                if reply
                else message.from_user.id
            )
        except (errors.RPCError, Exception):
            user = await app.get_users(message.from_user.id)

        bio = (await app.get_chat(user.id)).bio
        text = (
            f"<b>ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ:<b>\n\n"
            f"<b>Имя:</b> {user.first_name or ''}\n"
            f"<b>Фамилия:</b> {user.last_name or 'Пользователь не указал фамилию'}\n"
            f"<b>Юзернейм:</b> {user.username or 'Пользователь не указал юзернейм'}\n"
            f"<b>ID:</b> {user.id}\n"
            f"<b>Бот:</b> {yes_no(user.is_bot)}\n"
            f"<b>Контакт/взаимный:</b> {yes_no(user.is_contact)}/{yes_no(user.is_mutual_contact)}\n"
            f"<b>Верифицирован:</b> {yes_no(user.is_verified)}\n\n"
            f"<b>О себе:</b>\n{bio or ''}\n\n"
            f"<b>Кол-во аватарок:</b> {await app.get_profile_photos_count(user.id)}\n"
            f"<b>Кол-во общих чатов:</b> {len(await user.get_common_chats())}\n\n"
            f"<b>Пермалинк:</b> <a href=\"tg://user?id={user.id}\">тык</a>"
        )

        await message.delete()

        if user.photo:
            file_name = await app.download_media(user.photo.big_file_id, "tempava.png")
            await utils.answer(
                message, file_name, photo=True,
                quote=False, caption=text
            )
            return os.remove(file_name)

        return await utils.answer(
            message, text, quote=False
        )
