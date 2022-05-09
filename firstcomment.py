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

import logging

from pyrogram import Client, types, filters, errors
from .. import loader, utils


@loader.module("FirstComment", "sh1tn3t")
class FirstCommentMod(loader.Module):
    """Первый комментарий на канале"""

    async def fcsw_cmd(self, app: Client, message: types.Message):
        """Включить/выключить режим. Использование: fcsw"""
        status = not self.db.get("FirstComment", "status")
        self.db.set("FirstComment", "status", status)

        return await utils.answer(
            message, "<b>[FirstComment]</b> Теперь статус: " + (
                "Включен" if status
                else"Выключен"
            )
        )

    async def fctext_cmd(self, app: Client, message: types.Message, args: str):
        """Изменить текст комментария. Использование: fctext <текст>"""
        if not args:
            return await utils.answer(
                message, "<b>[FirstComment]</b> Текст комментария: " + self.db.get("FirstComment", "text"))

        self.db.set("FirstComment", "text", args)
        return await utils.answer(
            message, "<b>[FirstComment]</b> Текст был изменён успешно")

    async def fcadd_cmd(self, app: Client, message: types.Message, args: str):
        """Добавить канал(-ы) в базу. Использование: fcadd <@ или ID> (через пробел)"""
        if not (args := args.split()):
            return await utils.answer(
                message, "<b>[FirstComment - Error]</b> Нет аргументов")

        channels = self.db.get("FirstComment", "channels", [])
        for arg in args:
            try:
                chat = await app.get_chat(
                    int(arg) if arg.isdigit() or arg.startswith("-")
                    else arg
                )
                if chat.type != "channel":
                    raise errors.RPCError("Это не канал")
            except errors.RPCError as error:
                logging.exception(error)
                await message.reply(
                    f"<b>[FirstComment - Error]</b> \"{arg}\" не был добавлен в базу. Подробности в логах")
            else:
                if chat.id not in channels:
                    channels.append(chat.id)

        self.db.set("FirstComment", "channels", channels)
        return await utils.answer(
            message, "<b>[FirstComment]</b> Канал(-ы) были добавлены в базу")

    async def fcdel_cmd(self, app: Client, message: types.Message, args: str):
        """Удалить канал(-ы) из базы. Использование: fcdel <@ или ID> (через пробел)"""
        channels = self.db.get("FirstComment", "channels", [])
        if not channels:
            return await utils.answer(
                message, "<b>[FirstComment - Error]</b> База и так пуста")

        if not (args := args.split()):
            return await utils.answer(
                message, "<b>[FirstComment - Error]</b> Нет аргументов")

        if len(args) == 1 and args[0] == "all":
            self.db.set("FirstComment", "channels", [])
            return await utils.answer(
                message, "<b>[FirstComment]</b> Теперь база пуста")

        for arg in args:
            arg = int(arg) if arg.isdigit() or arg.startswith("-") else arg
            if arg not in channels:
                await message.reply(
                    f"<b>[FirstComment - Error]</b> \"{arg}\" нет в базе")
                continue

            channels.remove(arg) 

        self.db.set("FirstComment", "channels", channels)
        return await utils.answer(
            message, "<b>[FirstComment]</b> Канал(-ы) был(-и) удален(-ы) из базы")

    async def fcs_cmd(self, app: Client, message: types.Message):
        """Вывести список каналов в базе. Использование: fcs"""
        if not (channels := self.db.get("FirstComment", "channels", [])):
            return await utils.answer(
                message, "<b>[FirstComment - Error]</b> База пуста")

        text = "<b>[FirstComment]</b> Каналы в базе:\n"
        for channel in channels.copy():
            try:
                chat = await app.get_chat(channel)
            except errors.RPCError as error:
                channels.remove(channel)
                self.db.set("FirstComment", "channels", channels)

                logging.exception(error)
                await message.reply(
                    f"<b>[FirstComment - Error]</b> \"{channel}\" не найден. Подробности в логах")
            else:
                text += f"\n• {chat.title} | <code>{chat.id}</code>"

        return await utils.answer(
            message, text)

    @loader.on(filters.channel)
    async def watcher(self, app: Client, message: types.Message):
        if (
            not self.db.get("FirstComment", "status")
            or (chat := message.chat).id not in self.db.get("FirstComment", "channels", [])
        ):
            return

        try:
            msg = await app.get_discussion_message(chat.id, message.message_id)
            await msg.reply(self.db.get("FirstComment", "text", "Я первый!"))
        except errors.RPCError as error:
            logging.exception(error)
