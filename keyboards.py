from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Onlayn Test"))

test_types = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Quiz Test (Tezkor)", callback_data="type_quiz"),
    InlineKeyboardButton("Attestatsiyaga tayyorgarlik", callback_data="type_attest"),
    InlineKeyboardButton("Reyting", callback_data="show_rating")
)

def get_options_kb(options):
    kb = InlineKeyboardMarkup(row_width=1)
    opts = options.split(',')
    for opt in opts:
        clean_opt = opt.strip()
        kb.insert(InlineKeyboardButton(clean_opt, callback_data=f"ans_{clean_opt}"))
    return kb
