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
import asyncio

import html
import time

from typing import Union
from pyrogram import Client, types, errors

from .. import loader, utils


async def get_user(app: Client, args: str, reply: types.Message):
    """Обработка аргументов"""
    args_ = args.split()
    extras = None

    if reply:
        user = await app.get_chat(reply.from_user.id)
        extras = args
    else:
        user = await app.get_chat(
            args_[0] if not args_[0].isdigit()
            else int(args_[0])
        )
        if len(args_) < 2:
            user = await app.get_chat(
                args if not args.isdigit()
                else int(args)
            )
        else:
            extras = args.split(maxsplit=1)[1]

    return user, extras


def process_time_args(args: str):
    """Обработка аргументов времени"""
    n = t = ''
    for char in args.replace(" ", ""):
        if char.isdigit():
            n += char
        else:
            t += char

    text = n
    minutes = ["m", "min", "mins", "minute", "minutes", "м", "мин", "минут", "минута", "минуты"]
    hours = ["h", "hour", "hours", "ч", "час", "часа", "часов"]
    days = ["d", "day", "days", "д", "дн", "день", "дня", "дней"]

    if t not in minutes + hours + days:
        return args, None

    n = (
        int(n) * (
            60
            if t in minutes
            else 3600
            if t in hours
            else 86400
            if t in days
            else ""
        )
    )
    text += (
        " мин."
        if t in minutes
        else " час."
        if t in hours
        else " дн."
        if t in days
        else ""
    )
    return text, n


@loader.module("AdminTools", "sh1tn3t", 1.0)
class AdminToolsMod(loader.Module):
    """Администрирование чата"""
 
    strings = {
        string: "<b>[AdminTools]</b> " + description
        for string, description in {
            "no_args_or_reply": "Нет аргументов или реплая.",
            "no_reply": "Нет реплая.",
            "this_is_not_a_chat": "Это не чат.",
            "cant_find_the_user": "Не удалось найти пользователя.",
            "no_rights": "Нет определённых прав для этого.",
            "unknown_error": "Произошла неизвестная ошибка. Подробности смотри в логах.",
            "promoted": "{name} был повышен в правах администратора.\nПрефикс: {prefix}",
            "demoted": "{name} был понижен в правах администратора.",
            "the_user_is_an_admin": "Ошибка! Пользователь является администратором.",
            "kicked": "{name} был кикнут.",
            "banned": "{name} был забанен.",
            "unbanned": "{name} был разбанен.",
            "muted": "{name} был замучен",
            "unmuted": "{name} был размучен.",
            "pinned": "Сообщение было закреплено.",
            "unpinned": "Сообщение было откреплено.",
            "unpinned_all": "Все сообщения были откреплены.",
            "no_pin": "Нет закрепленных сообщений.",
        }.items()
    }

    async def check_all(self, app: Client, message: types.Message, args: str, action: str):
        """Обработка всего"""
        chat = message.chat
        if chat.type == "private":
            return await utils.answer(
                message, self.strings["this_is_not_a_chat"])

        reply = message.reply_to_message
        if not (args or reply):
            return await utils.answer(
                message, self.strings["no_args_or_reply"])

        check_me = await chat.get_member("me")
        if not check_me[
            "can_promote_members" if action in ["promote", "demote"]
            else "can_restrict_members"
        ]:
            return await utils.answer(
                message, self.strings["no_rights"])

        try:
            return await get_user(app, args, reply)
        except errors.RPCError:
            return await utils.answer(
                message, self.strings["cant_find_the_user"])

    async def process_mute_args(self, user: types.User, args: str = None):
        """Обработка аргументов мута"""
        if not args:
            return self.strings["muted"].format(
                name=html.escape(utils.get_display_name(user)),
            ) + ".", None

        args_ = args.split("\n", maxsplit=1)
        args = args_[0]
        reason_text = args_[1] if len(args_) > 1 else None

        text, n = process_time_args(args.replace(" ", ""))
        if not n:
            return self.strings["muted"].format(
                name=html.escape(utils.get_display_name(user))
            ) + f".\nПричина: {args}", None

        return self.strings["muted"].format(
            name=html.escape(utils.get_display_name(user)),
        ) + f" на {text}" + (
            f"\nПричина: {reason_text}" if reason_text
            else ""
        ), n

    async def promote_cmd(self, app: Client, message: types.Message, args: str):
        """Повысить пользователя. Использование: promote <@ или ID или реплай> [ранг]"""
        result = await self.check_all(app, message, args, "promote")
        if isinstance(result, list):
            return

        chat = message.chat
        check_me = await chat.get_member("me")

        promote_rights = {
            "can_delete_messages": check_me.can_delete_messages,
            "can_restrict_members": check_me.can_restrict_members,
            "can_invite_users": check_me.can_invite_users,
            "can_pin_messages": check_me.can_pin_messages
        }

        user, prefix = result
        try:
            await chat.promote_member(user.id, **promote_rights)
        except (errors.ChatAdminRequired, errors.UserCreator):
            return await utils.answer(
                message, self.strings["the_user_is_an_admin"])
        except errors.RPCError as error:
            logging.exception(error)
            return await utils.answer(
                message, self.strings["unknown_error"])

        prefix = prefix[:16] or "одмэн"

        await utils.answer(
            message, self.strings["promoted"].format(
                name=html.escape(utils.get_display_name(user)),
                prefix=prefix
            )
        )

        await asyncio.sleep(1)
        return await app.set_administrator_title(chat.id, user.id, prefix)

    async def demote_cmd(self, app: Client, message: types.Message, args: str):
        """Понизить пользователя. Использование: demote <@ или ID или реплай> [причина]"""
        result = await self.check_all(app, message, args, "demote")
        if isinstance(result, list):
            return

        chat = message.chat
        demote_rights = {
            "can_manage_chat": False,
            "can_change_info": False,
            "can_post_messages": False,
            "can_edit_messages": False,
            "can_delete_messages": False,
            "can_restrict_members": False,
            "can_invite_users": False,
            "can_pin_messages": False,
            "can_promote_members": False,
            "can_manage_voice_chats": False
        }

        user, reason = result
        try:
            await chat.promote_member(user.id, **demote_rights)
        except (errors.ChatAdminRequired, errors.UserCreator):
            return await utils.answer(
                message, self.strings["the_user_is_an_admin"])
        except errors.RPCError as error:
            logging.exception(error)
            return await utils.answer(
                message, self.strings["unknown_error"])

        return await utils.answer(
            message, self.strings["demoted"].format(
                name=html.escape(utils.get_display_name(user))
            ) + (
                f"\nПричина: {reason}" if reason
                else ""
            )
        )

    async def kick_cmd(self, app: Client, message: types.Message, args: str):
        """Кикнуть пользователя. Использование: kick <@ или ID или реплай> [причина]"""
        result = await self.check_all(app, message, args, "kick")
        if isinstance(result, list):
            return

        chat = message.chat

        user, reason = result
        try:
            await chat.ban_member(user.id)
            await chat.unban_member(user.id)
        except errors.UserAdminInvalid:
            return await utils.answer(
                message, self.strings["the_user_is_an_admin"])
        except errors.RPCError as error:
            logging.exception(error)
            return await utils.answer(
                message, self.strings["unknown_error"])

        return await utils.answer(
            message, self.strings["kicked"].format(
                name=html.escape(utils.get_display_name(user))
            ) + (
                f"\nПричина: {reason}" if reason
                else ""
            )
        )

    async def ban_cmd(self, app: Client, message: types.Message, args: str):
        """Забанить пользователя. Использование: ban <@ или ID или реплай> [причина]"""
        result = await self.check_all(app, message, args, "ban")
        if isinstance(result, list):
            return

        chat = message.chat

        user, reason = result
        try:
            await chat.ban_member(user.id)
        except errors.UserAdminInvalid:
            return await utils.answer(
                message, self.strings["the_user_is_an_admin"])
        except errors.RPCError as error:
            logging.exception(error)
            return await utils.answer(
                message, self.strings["unknown_error"])

        return await utils.answer(
            message, self.strings["banned"].format(
                name=html.escape(utils.get_display_name(user))
            ) + (
                f"\nПричина: {reason}" if reason
                else ""
            )
        )

    async def unban_cmd(self, app: Client, message: types.Message, args: str):
        """Разбанить пользователя. Использование: unban <@ или ID или реплай> [причина]"""
        result = await self.check_all(app, message, args, "unban")
        if isinstance(result, list):
            return

        chat = message.chat

        user, reason = result
        try:
            await chat.unban_member(user.id)
        except errors.RPCError as error:
            logging.exception(error)
            return await utils.answer(
                message, self.strings["unknown_error"])

        return await utils.answer(
            message, self.strings["unbanned"].format(
                name=html.escape(utils.get_display_name(user))
            ) + (
                f"\nПричина: {reason}" if reason
                else ""
            )
        )

    async def mute_cmd(self, app: Client, message: types.Message, args: str):
        """Замутить пользователя. Использование: mute <@ или ID или реплай> [время (1м, 2 часа, 7 days, так далее)] [*перенос строки* + причина]"""
        result = await self.check_all(app, message, args, "mute")
        if isinstance(result, list):
            return

        chat = message.chat

        user, args = result
        text, n = await self.process_mute_args(user, args)

        try:
            if not n:
                await chat.restrict_member(
                    user.id, types.ChatPermissions(
                        can_send_messages=False)
                )
            else:
                await chat.restrict_member(
                    user.id, types.ChatPermissions(
                        can_send_messages=False), until_date=int(time.time()) + int(n)
                )
        except errors.UserAdminInvalid:
            return await utils.answer(
                message, self.strings["the_user_is_an_admin"])
        except errors.RPCError as error:
            logging.exception(error)
            return await utils.answer(
                message, self.strings["unknown_error"])

        return await utils.answer(
            message, text)

    async def unmute_cmd(self, app: Client, message: types.Message, args: str):
        """Размутить пользователя. Использование: unmute <@ или ID или реплай> [причина]"""
        result = await self.check_all(app, message, args, "unmute")
        if isinstance(result, list):
            return

        chat = message.chat

        user, reason = result
        try:
            await chat.restrict_member(
                user.id, types.ChatPermissions(
                    can_send_messages=True))
        except errors.RPCError as error:
            logging.exception(error)
            return await utils.answer(
                message, self.strings["unknown_error"])

        return await utils.answer(
            message, self.strings["unmuted"].format(
                name=html.escape(utils.get_display_name(user))
            ) + (
                f"\nПричина: {reason}" if reason
                else ""
            )
        )

    async def pin_cmd(self, app: Client, message: types.Message):
        """Закрепить сообщение. Использование: pin <реплай>"""
        chat = message.chat

        if chat.type != "private":
            check_me = await chat.get_member("me")
            if not check_me.can_pin_messages:
                return await utils.answer(
                    message, self.strings["no_rights"])

        reply = message.reply_to_message
        if not reply:
            return await utils.answer(
                message, self.strings["no_reply"])

        try:
            await reply.pin(True, True)
        except errors.RPCError as error:
            logging.exception(error)
            return await utils.answer(
                message, self.strings["unknown_error"])

        return await utils.answer(
            message, self.strings["pinned"])

    async def unpin_cmd(self, app: Client, message: types.Message, args: str):
        """Открепить сообщение. Использование: unpin <реплай> [all - открепить все сообщения]"""
        chat = message.chat

        if chat.type != "private":
            check_me = await chat.get_member("me")
            if not check_me.can_pin_messages:
                return await utils.answer(
                    message, self.strings["no_rights"])

        chat = await app.get_chat(chat.id)
        pinned_message: Union[types.Message, None] = chat.pinned_message
        if not pinned_message:
            return await utils.answer(
                message, self.strings["no_pin"])

        try:
            if args == "all":
                await app.unpin_all_chat_messages(chat.id)
            else:
                await pinned_message.unpin()
        except errors.RPCError as error:
            logging.exception(error)
            return await utils.answer(
                message, self.strings["unknown_error"])

        return await utils.answer(
            message, self.strings["unpinned" if args != "all" else "unpinned all"])
