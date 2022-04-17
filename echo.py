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

from pyrogram import Client, types, filters
from .. import loader, utils


@loader.module("Echo", "sh1tn3t")
class EchoMod(loader.Module):
    """Режим эхо"""

    async def echo_cmd(self, app: Client, message: types.Message, args: str):
        """Включить/выключить режим эхо. Использование: echo"""
        chats = self.db.get("Echo", "chats", [])
        echo_status = message.chat.id in chats

        self.db.set("Echo", "chats", list({*chats} ^ {message.chat.id}))
        return await utils.answer(
            message, "<b>[Echo]</b> " + (
                "Включено" if not echo_status
                else "Выключено"
            ) + " для этого чата"
        )

    @loader.on(~filters.me)
    async def watcher(self, app: Client, message: types.Message):
        """Эхо"""
        if message.chat.id in self.db.get("Echo", "chats", []):
            return await message.copy(
                message.chat.id, reply_to_message_id=message.message_id)
