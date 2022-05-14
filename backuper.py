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

from pyrogram import Client, types
from .. import loader, utils


@loader.module("Backuper", "sh1tn3t")
class BackuperMod(loader.Module):
    """Создание бекапов базы данных"""

    async def backupdb_cmd(self, app: Client, message: types.Message):
        """Создать бекап всей базы данных. Использование: backupdb"""
        if not os.path.exists(self.db.location):
            return await utils.answer(
                message, "Ошибка! Файл с локальной базой данных не найден")

        await app.send_document(
            "me", self.db.location, caption="Бекап базы данных"
        )

        return await utils.answer(
            message, "Бекап базы данных успешно создан и отправлен в избранное")

    async def restoredb_cmd(self, app: Client, message: types.Message):
        """Восстановить базу данных из файла с реплая. Использование: restoredb <реплай на файл с названием db.json>"""
        reply = message.reply_to_message
        if (
            not reply
            or not reply.document
            or reply.document.file_name != "db.json"
        ):
            return await utils.answer(
                message, "Ошибка! Нет реплая на файл с названием db.json")

        await reply.download("." + self.db.location)
        return await utils.answer(
            message, "База данных успешно восстановлена.\n"
                     "Пропиши команду <code>restart</code>, чтобы изменения вступили в силу"
        )
