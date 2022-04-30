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
from pyrogram.raw.types import InputPeerUser
from .. import loader, utils


@loader.module("Permalink", "sh1tn3t")
class PermalinkMod(loader.Module):
    """Постоянная ссылка на пользователя"""

    async def permalink_cmd(self, app: Client, message: types.Message, args: str):
        """Получить пермалинк на пользователя. Использование: permalink <@ или ID или реплай>"""
        reply = message.reply_to_message

        try:
            peer = await app.resolve_peer(
                args
                if args
                else reply.from_user.id
                if reply
                else message.from_user.id
            )
            if not isinstance(peer, InputPeerUser):
                raise errors.PeerIdInvalid
        except errors.PeerIdInvalid:
            return await utils.answer(
                message, "Не удалось найти пользователя")

        return await utils.answer(
            message, f"<a href=\"tg://user?id={peer.user_id}\">Пермалинк на {peer.user_id}</a>")
