from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config, database, keyboards, functions, generator, quiz_engine, os

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    waiting_for_name = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    database.init_db()
    await message.answer("Assalomu alaykum! Testni boshlash uchun tugmani bosing.", reply_markup=keyboards.main_menu)

@dp.message_handler(lambda m: m.text == "Onlayn Test")
async def show_type(message: types.Message):
    await message.answer("Yo'nalishni tanlang:", reply_markup=keyboards.test_types)

@dp.callback_query_handler(lambda c: c.data.startswith('type_'))
async def start_test(call: types.CallbackQuery):
    subject = "Attestatsiya"
    qs = database.get_questions(subject)
    if not qs: return await call.answer("Hozircha savollar yo'q", show_alert=True)
    
    quiz_engine.quiz_engine.start_session(call.from_user.id, qs)
    q = quiz_engine.quiz_engine.get_current_q(call.from_user.id)
    await call.message.edit_text(f"1-savol:\n\n{q['question']}", reply_markup=keyboards.get_options_kb(q['options']))

@dp.callback_query_handler(lambda c: c.data.startswith('ans_'))
async def handle_ans(call: types.CallbackQuery, state: FSMContext):
    u_id = call.from_user.id
    ans = call.data.replace('ans_', '')
    quiz_engine.quiz_engine.save_answer(u_id, ans)
    
    q = quiz_engine.quiz_engine.get_current_q(u_id)
    if q:
        idx = quiz_engine.quiz_engine.user_data[u_id]['idx']
        await call.message.edit_text(f"{idx+1}-savol:\n\n{q['question']}", reply_markup=keyboards.get_options_kb(q['options']))
    else:
        # Test tugashi
        u_data = quiz_engine.quiz_engine.user_data[u_id]
        percent = (u_data['score'] / len(u_data['qs'])) * 100
        text = f"Natija: {u_data['score']}/{len(u_data['qs'])} ({percent}%)\n"
        
        if percent >= 80:
            await call.message.answer(text + "Tabriklaymiz! Sertifikat uchun Ism-Familiyangizni yozing:")
            await Form.waiting_for_name.set()
        else:
            pdf = functions.create_pdf(call.from_user.first_name, u_data['history'])
            with open(pdf, 'rb') as f:
                await call.message.answer_document(f, caption=text + "Sizga xatolar tahlili yuborildi.")

@dp.message_handler(state=Form.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    cert = generator.make_cert(message.text)
    with open(cert, 'rb') as f:
        await message.answer_photo(f, caption="Sertifikatingiz tayyor!")
    await state.finish()

@dp.message_handler(content_types=['document'])
async def admin_upload(message: types.Message):
    if message.from_user.id == config.ADMIN_ID:
        path = f"uploads/{message.document.file_name}"
        await message.document.download(destination_file=path)
        functions.process_docx(path)
        await message.answer("Savollar yuklandi!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
