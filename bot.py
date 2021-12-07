# -*- coding: utf-8 -*-

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from config import ACCESS_ID

import exceptions
import expenses
from categories import Categories
# from middlewares import AccessMiddleware


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\n"
                        "Я Бот для учёта финансов! Напиши мне свои затраты и добавлю их в базу.\n"
                        "Например: Добавить расход: 250 такси\n")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("Вот что я умею\n"
                         "Добавить расход: 250 такси\n"
                         "Сегодняшняя статистика: /today\n"
                         "За текущий месяц: /month\n"
                         "Последние внесённые расходы: /expenses\n"
                         "Категории трат: /categories")


# просмотр расходов
@dp.message_handler(commands=['expenses'])
async def process_expenses_command(message: types.Message):
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses
    ]
    answer_message = "Последние сохранённые траты: ".join(last_expenses_rows)
    await message.answer(answer_message)


# удаление статьи расхода по ее id
@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expenses_command(message: types.Message):
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    await message.answer("Удалил")


# получение категорий расходов
@dp.message_handler(commands=['categories'])
async def get_categories_command(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " + ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


# добавление новых расходы
@dp.message_handler()
async def add_expenses_command(message: types.Message):
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp)
