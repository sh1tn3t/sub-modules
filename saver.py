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

import asyncio
import time
import datetime

from pyrogram import Client, types
from .. import loader, utils


@loader.module("Saver", "sh1tn3t")
class SaverMod(loader.Module):
    """Сохраняет самоуничтожающиеся фотографии или видео"""

    async def download_and_send(self, message: types.Message):
        """Скачивает файл на диск и отправляет в избранное"""
        if not utils.get_message_media(message):
            return False

        file_path = await message.download(
            f"save_"
            f"{message.chat.id}_"
            f"{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')}"
            f"{utils.get_media_ext(message)}"
        )
        return await message._client.send_document("me", file_path)

    async def rsave_cmd(self, app: Client, message: types.Message, delete: bool = True):
        """Сохранить медиа в избранное. Использование: rsave <реплай>"""
        reply = message.reply_to_message
        if utils.get_message_media(reply):
            await self.download_and_send(reply)
            if delete:
                await message.delete()

        return True

    async def swsaver_cmd(self, app: Client, message: types.Message):
        """Включить/выключить режим автоматического сохранения медиа. Использование: swsaver"""
        status = self.db.get("Saver", "status", True)
        self.db.set("Saver", "status", not status)
        return await utils.answer(
            message, "<b>[Saver]</b> " + (
                "Включено" if not status
                else "Выключено"
            )
        )

    @loader.on(lambda _, __, m: m.outgoing and (media := utils.get_message_media(m)) and getattr(media, "ttl_seconds", None))
    async def watcher(self, app: Client, message: types.Message):
        if not self.db.get("Saver", "status"):
            return

        return await self.download_and_send(message)

    @loader.on(lambda _, __, m: m.outgoing and m.text == "блч")
    async def watcher_(self, app: Client, message: types.Message):
        await self.rsave_cmd(app, message, False)
        await asyncio.sleep(1.5)
        return await utils.answer(message, "бля")
