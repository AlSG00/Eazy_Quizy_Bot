from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F

import database_requests as dbr
from quiz_data import quiz_data

dp = Dispatcher()

right_answer_count = 0
current_record = 0

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    global right_answer_count
    right_answer_count = 0
    global current_record
    current_record = await dbr.get_record(message.from_user.id)
    await message.answer(f"Давайте начнем квиз!")
    await dbr.new_quiz(message)

@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await dbr.get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    
    await callback.message.answer(f"Верно! {quiz_data[current_question_index]['options'][correct_option]}")
    global right_answer_count
    right_answer_count += 1
    #current_question_index = await dbr.get_quiz_index(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await dbr.update_quiz_index(callback.from_user.id, current_question_index)


    if current_question_index < len(quiz_data):
        await dbr.get_question(callback.message, callback.from_user.id)
    else:
        #record_count = await dbr.get_record(callback.from_user.id)
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВерных ответов: {right_answer_count}. Ваш рекорд: {current_record}")
        if right_answer_count > current_record:
            await dbr.update_record(callback.from_user.id, right_answer_count)


@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await dbr.get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await dbr.update_quiz_index(callback.from_user.id, current_question_index)


    if current_question_index < len(quiz_data):
        await dbr.get_question(callback.message, callback.from_user.id)
    else:
        #record_count = await dbr.get_record(callback.from_user.id)
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВерных ответов: {right_answer_count}. Ваш рекорд: {current_record}")
        if right_answer_count > current_record:
            await dbr.update_record(callback.from_user.id, right_answer_count)

# @dp.callback_query(F.data == "wrong_answer")
# @dp.callback_query(F.data == "right_answer")
# async def wrong_answer(callback: types.CallbackQuery):
#     await callback.bot.edit_message_reply_markup(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         reply_markup=None
#     )

#     # Получение текущего вопроса из словаря состояний пользователя
#     current_question_index = await dbr.get_quiz_index(callback.from_user.id)
#     correct_option = quiz_data[current_question_index]['correct_option']

#     if F.text.contains("wrong_answer"):
#         await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
#     elif F.data == "right_answer":
#         await callback.message.answer(f"Верно! {quiz_data[current_question_index]['options'][correct_option]}")

#     # Обновление номера текущего вопроса в базе данных
#     current_question_index += 1
#     await dbr.update_quiz_index(callback.from_user.id, current_question_index)


#     if current_question_index < len(quiz_data):
#         await dbr.get_question(callback.message, callback.from_user.id)
#     else:
#         await callback.message.answer("Это был последний вопрос. Квиз завершен!")