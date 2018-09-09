#!/usr/local/bin/python3
import asyncio
import logging
import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from telegramcalendar import create_calendar

API_TOKEN = 'BOT TOKEN HERE'

logging.basicConfig(level=logging.DEBUG)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop)
dp = Dispatcher(bot)

current_shown_dates={}

@dp.message_handler(commands=['calendar'])
async def calendar_handler(message: types.Message):
    now = datetime.datetime.now()
    current_shown_dates[message.chat.id] = (now.year, now.month)
    markup = create_calendar(now.year,now.month)
    await bot.send_message(message.chat.id, "Please, choose a date", reply_markup=markup)

@dp.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
async def get_day(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        day = call.data[13:]
        day = call.data[13:]
        date = datetime.datetime(int(saved_date[0]),int(saved_date[1]),int(day),0,0,0)
        await bot.send_message(chat_id, str(date))
        await bot.answer_callback_query(call.id, text="")
    else:
        pass

@dp.callback_query_handler(func=lambda call: call.data == 'next-month')
async def next_month(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month += 1
        if month > 12:
            month = 1
            year += 1
        date = (year, month)
        current_shown_dates[chat_id] = date
        markup = create_calendar(year,month)
        await bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)                                                     
        await bot.answer_callback_query(call.id, text="")
    else:
        pass

@dp.callback_query_handler(func=lambda call: call.data == 'previous-month')
async def previous_month(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        date = (year, month)
        current_shown_dates[chat_id] = date
        markup = create_calendar(year,month)
        await bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)                                                     
        await bot.answer_callback_query(call.id, text="")
    else:
        pass

@dp.callback_query_handler(func=lambda call: call.data == 'ignore')
async def ignore(call: types.CallbackQuery):
    bot.answer_callback_query(call.id, text="")

if __name__ == '__main__':
    start_polling(dp, loop=loop, skip_updates=True)
