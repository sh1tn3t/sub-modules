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


@loader.module("Purge", "sh1tn3t")
class PurgeMod(loader.Module):
    """Удаление сообщений"""

    async def purge_cmd(self, app: Client, message: types.Message, args: str):
        """Удалить сообщения до реплая или кол-во сообщений. Использование: purge <реплай или кол-во>"""
        chat = message.chat
        reply = message.reply_to_message

        if not reply:
            if not args:
                return await utils.answer(
                    message, "<b>[Purge]</b> Нет реплая или не указаны кол-во сообщений числом")

            if not args.isdigit():
                return await utils.answer(
                    message, "<b>[Purge]</b> Кол-во сообщений должно быть числом")

            msgs = [
                msg for msg in await app.get_messages(
                    chat.id, range(message.message_id - int(args), message.message_id))
            ]

        else:
            msgs = [
                msg for msg in await app.get_messages(
                    chat.id, range(reply.message_id, message.message_id))
            ]

        await message.delete()
        for msg in msgs:
            await msg.delete()

        return True

    async def del_cmd(self, app: Client, message: types.Message):
        """Удалить реплай. Использование: del <реплай>"""
        reply = message.reply_to_message
        if not reply:
            return await utils.answer(
                message, "<b>[Del]</b> Нет реплая")

        await reply.delete()
        return await message.delete()
