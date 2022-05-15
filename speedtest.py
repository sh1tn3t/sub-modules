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

# required: speedtest

import speedtest

from pyrogram import Client, types
from .. import loader, utils


def speed_test():
    tester = speedtest.Speedtest()
    tester.get_best_server()
    tester.download()
    tester.upload()
    return tester.results.dict()


@loader.module(name="SpeedTest", author="sh1tn3t")
class SpeedTestMod(loader.Module):
    """Тест интернет-соединения"""

    async def speedtest_cmd(self, app: Client, message: types.Message):
        """Запускает тест скорости. Использование: speedtest"""
        await utils.answer(
            message, "<b>Запускаем тест...</b>")
 
        result = speed_test()
        text = (
            f"<b>Результаты теста:</b>\n\n"
            f"<b>Скачивание:</b> <code>{round(result['download'] / 2 ** 20 / 8, 2)}</code> <b>мб/с</b>\n"
            f"<b>Загрузка:</b> <code>{round(result['upload'] / 2 ** 20 / 8, 2)}</code> <b>мб/c</b>\n"
            f"<b>Задержка:</b> <code>{round(result['ping'], 2)}</code> <b>мc</b>"
        )
        return await utils.answer(
            message, text)
