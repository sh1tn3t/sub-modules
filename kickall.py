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

from pyrogram import Client, types, errors
from .. import loader, utils


@loader.module("KickAll", "sh1tn3t")
class KickAllMod(loader.Module):
    """Кикает всех с группы"""

    async def kickall_cmd(self, app: Client, message: types.Message, args: str):
        """Кикнуть всех с группы. Использование: kickall [*любой аргумент* - скрытный режим]"""
        chat = message.chat
        if chat.type == "private":
            return await utils.answer(
                message, "<b>[KickAll]</b> Это не чат")

        check_me = await chat.get_member(user.id)
        if not check_me.can_restrict_members:
            return await utils.answer(
                message,
                "<b>[KickAll]</b> У меня нет прав на кик",
                chat_id="me" if args else None
            )

        if args:
            await message.delete()

        count = 0

        async for user in chat.iter_members():
            if user.user.is_self or user.user.is_deleted:
                pass

            try:
                await chat.ban_member(user.user.id)
                await chat.unban_member(user.user.id)
                count += 1
            except errors.RPCError:
                pass

        if args:
            return await utils.answer(
                message,
                f"<b>[KickAll]</b> В чате \"{utils.get_display_name(chat)}\" было кикнуто <b>{count}</b> участников",
                chat_id="me"
            )

        return await utils.answer(
            message, f"<b>[KickAll]</b> Было кикнуто <b>{count}</b> участников")
