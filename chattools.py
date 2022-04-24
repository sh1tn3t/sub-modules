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

import io
import html

from pyrogram import Client, types, errors
from .. import loader, utils


@loader.module("ChatTools", "sh1tn3t")
class ChatToolsMod(loader.Module):
    """Инструменты для чата"""

    async def who_cmd(self, app: Client, message: types.Message, args: str):
        """Вывести имя и айди пользователя/чата. Использование: who <@ или ID или реплай>"""
        entity = message.from_user
        reply = message.reply_to_message

        if (args or reply):
            try:
                entity = await app.get_chat(
                    (int(args) if args.isdigit() else args) if args
                    else reply.from_user.id
                )
            except Exception:
                pass

        return await utils.answer(
            message, f"Имя: <code>{html.escape(utils.get_display_name(entity))}</code>\n"
                     f"ID: <code>{entity.id}</code>"
        )

    async def invite_cmd(self, app: Client, message: types.Message, args: str):
        """Пригласить пользователя. Использование: invite <@ или ID или реплай>"""
        if chat.type == "private":
            return await utils.answer(
                message, "<b>[ChatTools]</b> Это не чат!")

        reply = message.reply_to_message
        
        if not (args or reply):
            return await utils.answer(
                message, "<b>[ChatTools]</b> Нет аргументов или реплая")

        try:
            await chat.add_members(
                args.split() if args else reply.from_user.id)
        except errors.UserNotMutualContact:
            return await utils.answer(
                message, "<b>[ChatTools]</b> Невзаимный контакт")
        except (errors.RPCError, Exception) as error:
            return await utils.answer(
                message, f"<b>[ChatTools]</b> Не удалось пригласить. Ошибка: {error}")

        return await utils.answer(
            message, "<b>[ChatTools]</b> Пользователь приглашен успешно")

    async def users_cmd(self, app: Client, message: types.Message, args: str):
        """Показать список пользователей. Использование: users [имя] [!doc]>"""
        chat = message.chat
        if chat.type == "private":
            return await utils.answer(
                message, "<b>[ChatTools]</b> Это не чат!")

        m = await utils.answer(
            message, "<b>[ChatTools]</b> Загружаю...")

        msg = [
            (
                "Удалённый аккаунт" if member.user.is_deleted
                else member.user.mention
            ) + f" | <code>{member.user.id}</code>"
            async for member in chat.iter_members(query=args.replace("!doc", ""))
        ]
        text = (
            f"<b>[ChatTools]</b> Пользователи в \"{chat.title}\"" + (
                f" по запросу \"{args.replace('!doc', '')}\"" if args
                else ""
            ) + f": {len(msg)}"
        )

        msg = "\n".join(msg)
        if len(msg) < 4096 and "!doc" not in args:
            return await utils.answer(
                m, text + f"\n\n{msg}")

        m = await utils.answer(
            m, "<b>[ChatTools]</b> Слишком много пользователей. Загружаю в файл...")

        file = io.BytesIO(bytes(f"{text}\n\n{msg}"))
        file.name = f"users-{chat.id}.html"
        file.seek(0)

        await utils.answer(
            message, file, caption = text)
        return await m[-1].delete()

    async def admins_cmd(self, app: Client, message: types.Message, args: str):
        """Показать список админов. Использование: admins [имя] [!doc]"""
        chat = message.chat
        if chat.type == "private":
            return await utils.answer(
                message, "<b>[ChatTools]</b> Это не чат!")

        m = await utils.answer(
            message, "<b>[ChatTools]</b> Загружаю...")

        msg = [
            (
                "Удалённый аккаунт" if member.user.is_deleted
                else member.user.mention
            ) + f" | {member.title or 'admin'} | <code>{member.user.id}</code>"
            async for member in chat.iter_members(
                query=args.replace("!doc", ""), filter="administrators")
        ]
        text = (
            f"<b>[ChatTools]</b> Админы в \"{chat.title}\"" + (
                f" по запросу \"{args.replace('!doc', '')}\"" if args
                else ""
            ) + f": {len(msg)}"
        )

        msg = "\n".join(msg)
        if "!doc" not in args:
            return await utils.answer(
                m, text + f"\n\n{msg}")

        m = await utils.answer(
            m, "<b>[ChatTools]</b> Загружаю в файл...")

        file = io.BytesIO(bytes(f"{text}\n\n{msg}"))
        file.name = f"admins-{chat.id}.html"
        file.seek(0)

        await utils.answer(
            message, file, caption=text)
        return await m[-1].delete()

    async def bots_cmd(self, app: Client, message: types.Message, args: str):
        """Показать список ботов. Использование: bots [имя] [!doc]"""
        chat = message.chat
        if chat.type == "private":
            return await utils.answer(
                message, "<b>[ChatTools]</b> Это не чат!")

        m = await utils.answer(
            message, "<b>[ChatTools]</b> Загружаю...")

        msg = [
            (
                "Удалённый аккаунт" if member.user.is_deleted
                else member.user.mention
            ) + f" | <code>{member.user.id}</code>"
            async for member in chat.iter_members(
                query = args.replace("!doc", ""), filter = "bots")
        ]
        text = (
            f"<b>[ChatTools]</b> Боты в \"{chat.title}\"" + (
                f" по запросу \"{args.replace('!doc', '')}\"" if args
                else ""
            ) + f": {len(msg)}"
        )

        msg = "\n".join(msg)
        if "!doc" not in args:
            return await utils.answer(
                m, text + f"\n\n{msg}")

        m = await utils.answer(
            m, "<b>[ChatTools]</b> Загружаю в файл...")

        file = io.BytesIO(bytes(f"{text}\n\n{msg}"))
        file.name = f"bots-{chat.id}.html"
        file.seek(0)

        await utils.answer(
            message, file, caption=text)
        return await m[-1].delete()
