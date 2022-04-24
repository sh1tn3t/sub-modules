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

import random

from pyrogram import Client, types
from .. import loader, utils


@loader.module("TagAll", "sh1tn3t")
class TagAllMod(loader.Module):
    """Тегает всех в чате"""

    async def tagall_cmd(self, app: Client, message: types.Message, args: str):
        """Начинает всех тегать. Использование: tagall [текст]"""
        chat = message.chat
        if chat.type == "private":
            return await utils.answer(
                message, "Это не чат")

        args = args or "говно залупное\n                пашет." 

        users = [
            f"<a href=\"tg://user?id={member.user.id}\">\u2060</a>"
            async for member in chat.iter_members()
            if not (member.user.is_bot or member.user.is_deleted)
        ]

        random.shuffle(users)
        await message.delete()

        for output in [
            users[i: i + 5]
            for i in range(0, len(users), 5)
        ]:
            await message.reply(args + "\u2060".join(output))

        return
