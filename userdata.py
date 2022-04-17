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


@loader.module("UserData", "sh1tn3t")
class UserDataMod(loader.Module):
    """Изменение информации аккаунта"""

    async def setname_cmd(self, app: Client, message: types.Message, args: str):
        """Изменить имя и фамилию. Использование: name <имя> // [фамилия]"""
        first_name, last_name = args.split(" // ")
        if not (first_name or last_name):
            return await utils.answer(
                message, "Не указано имя или фамилия")

        if last_name and not first_name:
            return await utils.answer(
                message, "Не указано имя")

        await app.update_profile(first_name[:64], last_name[:64])
        full_name = first_name + (" " + last_name[:64] if last_name[:64] else "")

        return await utils.answer(
            message, f"Имя успешно изменено на <code>{full_name}</code>!")

    async def setbio_cmd(self, app: Client, message: types.Message, args: str):
        """Изменить био. Использование: setbio <текст>"""
        if not args:
            return await utils.answer(
                message, "Нет аргументов")

        await app.update_profile(bio=args[:70])
        return await utils.answer(
            message, "Био успешно изменено!")

    async def setusername_cmd(self, app: Client, message: types.Message, args: str):
        """Изменить юзернейм. Использование: setusername <новый юзернейм> или ничего (будет убран текущий)"""
        await app.update_username(args)
        return await utils.answer(
            message, "Юзернейм успешно изменен!")
