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

from pyrogram import Client, types
from .. import loader, utils


@loader.module("Spam", "sh1tn3t")
class SpamMod(loader.Module):
    """Спам"""

    async def spam_cmd(self, app: Client, message: types.Message, args: str):
        """Обычный спам. Использование: spam <кол-во сообщений> <аргументы или реплай>"""
        reply = message.reply_to_message

        if not reply:
            if not args:
                return await utils.answer(
                    message, "Нет аргументов и реплая")

            args_ = args.split(maxsplit=1)
            if len(args_) == 1:
                if args_[0].isdigit():
                    return await utils.answer(
                        message, "Не указан текст для спама")

                return await utils.answer(
                    message, "Не указано кол-во сообщений первым аргументом")

            if not args_[0].isdigit():
                return await utils.answer(
                    message, "Кол-во сообщений должно быть целым числом")

            await message.delete()
            for _ in range(int(args_[0])):
                await message.reply(args_[1], quote=False)

            return

        if not args:
            return await utils.answer(
                message, "Не указано кол-во сообщений")

        if not args.isdigit():
            return await utils.answer(
                message, "Кол-во сообщений должно быть целым числом")

        await message.delete()
        for _ in range(int(args)):
            await reply.copy(
                message.chat.id,
                reply_to_message_id=reply.message_id
            )

        return

    async def cspam_cmd(self, app: Client, message: types.Message, args: str):
        """Спам символами. Использование: cspam <аргументы или реплай>"""
        reply = message.reply_to_message
        text = (
            args
            if args
            else reply.text
            if reply and reply.text
            else reply.caption
            if reply and reply.caption
            else ""
        )

        if not text:
            return await utils.answer(
                message, "Нет аргументов или реплая")

        await message.delete()
        for char in text.replace(" ", ""):
            await message.reply(char, quote=False)

        return

    async def wspam_cmd(self, app: Client, message: types.Message, args: str):
        """Спам словами. Использование: wspam <аргументы или реплай>"""
        reply = message.reply_to_message
        text = (
            args
            if args
            else reply.text
            if reply and reply.text
            else reply.caption
            if reply and reply.caption
            else ""
        )

        if not text:
            return await utils.answer(
                message, "Нет аргументов или реплая")

        await message.delete()
        for word in text.split():
            await message.reply(word, quote=False)

        return

    async def delayspam_cmd(self, app: Client, message: types.Message, args: str):
        """Спам с задержкой. Использование: delayspam <кол-во сообщений> <задержка в секундах> <аргументы или реплай>"""
        reply = message.reply_to_message

        if not reply:
            if not args:
                return await utils.answer(
                    message, "Нет аргументов и реплая")
            
            args_ = args.split(maxsplit=2)
            if not args_[0].isdigit():
                return await utils.answer(
                    message, "Не указано кол-во сообщений первым аргументом")

            if len(args_) == 1:
                return await utils.answer(
                    message, "Не указана задержка вторым аргументом и текст для спама")

            if not args_[1].isdigit():
                return await utils.answer(
                    message, "Задержка должна быть целым числом")

            if len(args_) == 2:
                return await utils.answer(
                    message, "Не указан текст для спама")

            await message.delete()
            for _ in range(int(args_[0])):
                await message.reply(args_[2], quote=False)
                await asyncio.sleep(int(args_[1]))

            return

        if not args:
            return await utils.answer(
                message, "Не указано кол-во сообщений и задержка")

        args_ = args.split()
        if not args_[0].isdigit():
            return await utils.answer(
                message, "Кол-во сообщений должно быть целым числом")
        
        if len(args_) == 1:
            return await utils.answer(
                message, "Не указана задержка")

        if not args_[1].isdigit():
            return await utils.answer(
                message, "Задержка должна быть целым числом")

        await message.delete()
        for _ in range(int(args_[0])):
            await reply.copy(
                message.chat.id,
                reply_to_message_id=reply.message_id
            )
            await asyncio.sleep(int(args_[1]))

        return
