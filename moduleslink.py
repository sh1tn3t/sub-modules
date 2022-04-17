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
import os

import inspect

from pyrogram import Client, types
from .. import loader, utils


@loader.module("ModulesLink", "sh1tn3t")
class ModulesLinkMod(loader.Module):
    """Ссылка или файл установленного модуля"""

    async def ml_cmd(self, app: Client, message: types.Message, args: str):
        """Получить ссылку или файл модуля. Использование: ml <название модуля или команда>"""
        if not args:
            return await utils.answer(
                message, "Не указаны аргументы (название модуля или команда)")

        msg = await utils.answer(
            message, "Ищем модуль...")

        if not (module := self.all_modules.get_module(args, True)):
            return await utils.answer(
                message, "Не удалось найти модуль")

        get_module = inspect.getmodule(module)
        origin = get_module.__spec__.origin

        try:
            source = get_module.__loader__.data
        except AttributeError:
            source = inspect.getsource(get_module).encode("utf-8")

        source_code = io.BytesIO(source)
        source_code.name = module.name + ".py"
        source_code.seek(0)

        caption = (
            f"<a href=\"{origin}\">Ссылка</a> модуля \"{module.name}\":\n"
            f"<code>{origin}</code>"
            if origin != "<string>" and not os.path.exists(origin)
            else f"Файл модуля \"{module.name}\":\n"
        )

        await msg[-1].delete()
        return await utils.answer(
            message, source_code, doc=True, caption=caption)
