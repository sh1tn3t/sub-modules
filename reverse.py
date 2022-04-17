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

from pyrogram import Client, types
from .. import loader, utils


@loader.module("Reverse", "sh1tn3t")
class ReverseMod(loader.Module):
    """Реверс текста"""

    async def reverse_cmd(self, app: Client, message: types.Message, args: str):
        """Реверс текста. Использование: reverse <текст или реплай>"""
        reply = message.reply_to_message
        if not (args or reply):
            return await utils.answer(
                message, "Нет аргументов или реплая")

        return await utils.answer(
            message, (
                args
                if args
                else reply.text
                if reply and reply.text
                else "тскет ен отЭ"
            )
        )
