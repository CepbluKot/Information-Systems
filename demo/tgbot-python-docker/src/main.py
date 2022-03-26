import asyncio
import bot_elements.raspisanie.raspisanie as raspisanie
from aiogram import Bot, Dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot_elements.register.prepod_register import register_handlers_register_prepod
from bot_elements.register.student_register import register_handlers_register_student
from bot_elements.register.admin_register import register_handlers_register_admin

from bot_elements.forms.forms import register_handlers_forms
from bot_elements.forms.forms_menu import register_handlers_forms_menu
from bot_elements.status.status import register_handlers_status
from bot_elements.forms.forms_editor import register_handlers_forms_editor
from bot_elements.cancel import register_handlers_cancel

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

async def prepod_commands(bot: Bot):
    prepod_commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/multi_form", description="Создать форму"),
        BotCommand(command="/saved_forms",
                   description="Посмотреть сохраненные формы"),
        BotCommand(command="/status", description="Отобразить статус"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]

    await bot.set_my_commands(prepod_commands)


async def student_commands(bot: Bot):
    student_commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/status", description="Полученные формы"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(student_commands)


async def main():
    prepod_bot = Bot(token=config['DEFAULT']['prepodBotToken'])
    student_bot = Bot(token=config['DEFAULT']['studentBotToken'])
    admin_bot = Bot(token=config['DEFAULT']['adminBotToken'])
    
    prepod_bot_dispatcher = Dispatcher(prepod_bot, storage=MemoryStorage(),
                    loop=asyncio.get_event_loop())
    
    student_bot_dispatcher = Dispatcher(student_bot, storage=MemoryStorage(),
                    loop=asyncio.get_event_loop())

    admin_bot_dispatcher = Dispatcher(admin_bot, storage=MemoryStorage(),
                    loop=asyncio.get_event_loop())

    prepod_bot_dispatcher.loop.create_task(prepod_commands(prepod_bot))
    student_bot_dispatcher.loop.create_task(student_commands(student_bot))
    
    # dp.loop.create_task(raspisanie.rasp_notification('М3О-221Б-20'))
    
    register_handlers_cancel(prepod_bot_dispatcher)
    register_handlers_forms_editor(prepod_bot_dispatcher)
    register_handlers_forms(prepod_bot_dispatcher)
    register_handlers_forms_menu(prepod_bot_dispatcher)
    register_handlers_status(prepod_bot_dispatcher)
    register_handlers_register_prepod(prepod_bot_dispatcher)


    register_handlers_cancel(student_bot_dispatcher)
    register_handlers_forms_editor(student_bot_dispatcher)
    register_handlers_forms(student_bot_dispatcher)
    register_handlers_forms_menu(student_bot_dispatcher)
    register_handlers_status(student_bot_dispatcher)
    register_handlers_register_student(student_bot_dispatcher)

    register_handlers_register_admin(admin_bot_dispatcher)

    await asyncio.gather(prepod_bot_dispatcher.start_polling(), student_bot_dispatcher.start_polling(), admin_bot_dispatcher.start_polling())
    
    # executor.start_polling(prepod_bot_dispatcher)
    # executor.start_polling(student_bot_dispatcher)

asyncio.run(main())