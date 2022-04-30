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

from typing import List

from pyrogram import Client, types, filters
from .. import loader, utils


@loader.module("MegaMozg", "sh1tn3t")
class MegaMozgMod(loader.Module):
    """Подобие ИИ"""

    async def mozg_cmd(self, app: Client, message: types.Message):
        """Включить/выключить мозг. Использование: mozg"""
        chat = message.chat
        if chat.type == "private":
            return await utils.answer(
                message, "<b>[MegaMozg]</b> Это не чат.")

        chats = self.db.get("MegaMozg", "chats", {})
        if not chats.get(str(chat.id)):
            chats[str(chat.id)] = 30
            self.db.set("MegaMozg", "chats", chats)
            return await utils.answer(
                message, "<b>[MegaMozg]</b> Режим в этом чате был включён. Шанс: <b>30</b>%.")

        del chats[str(chat.id)]
        self.db.set("MegaMozg", "chats", chats)
        return await utils.answer(
                message, "<b>[MegaMozg]</b> Режим в этом чате был выключен.")

    async def mozgchance_cmd(self, app: Client, message: types.Message, args: str):
        """Установить шанс для мозга. Использование: mozgchance [шанс (в %, от 1 до 100]>"""
        chat = message.chat
        if chat.type == "private":
            return await utils.answer(
                message, "<b>[MegaMozg]</b> Это не чат.")

        chats = self.db.get("MegaMozg", "chats", {})
        if not chats.get(str(chat.id)):
            return await utils.answer(
                message, "<b>[MegaMozg]</b> В этом чате режим выключен.")

        if not args:
            return await utils.answer(
                message, f"<b>[MegaMozg]</b> Шанс в этом чате: <b>{chats[str(chat.id)]}</b>%.")

        if not (
            args
            and args.isdigit()
            and 0 < int(args) <= 100
        ):
            return await utils.answer(
                message, "<b>[MegaMozg]</b> Шанс должно быть числом, и быть от <b>1</b> до <b>100</b>%.")

        chats[str(chat.id)] = int(args)
        self.db.set("MegaMozg", "chats", chats)
        return await utils.answer(
                message, f"<b>[MegaMozg]</b> Шанс в этом чате был установлен на <b>{args}</b>%.")

    @loader.on(filters.text & ~filters.me & filters.group)
    async def watcher(self, app: Client, message: types.Message):
        """Отправка сообщений"""
        chat = message.chat

        chats = self.db.get("MegaMozg", "chats", {})
        if not (chance := chats.get(str(chat.id))):
            return

        if random.randint(0, 100) >= chance:
            return

        words = list(
            filter(
                lambda word: len(word) >= 3, message.text.split())
        )
        if not words:
            return

        sorted_words = {
            random.choice(words)
            for _ in ".."
        }

        msgs: List[types.Message] = []
        for word in sorted_words:
            async for msg in app.search_messages(chat.id, word):
                if msg.message_id != message.message_id:
                    msgs.append(msg)

        if not msgs:
            return

        msg = random.choice(msgs)
        return await utils.answer(
            message, msg.text)
