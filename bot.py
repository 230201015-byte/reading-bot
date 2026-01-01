from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from google_sheets import add_record
import os

# ================== CONFIG ==================
BOT_TOKEN = os.environ.get("8526431505:AAGiKgpTBqjUjoxsUCcwTOucC7lzj1D4gtE")
if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN не задан!")

SELECT_ACTION, SELECT_PERSON, SELECT_DATE, ENTER_PAGES = range(4)

# ================== KEYBOARDS ==================
main_keyboard = ReplyKeyboardMarkup(
    [["📘 Бет енгізу"], ["📊 Google Sheets-ті қарау"]],
    resize_keyboard=True
)

person_keyboard = ReplyKeyboardMarkup(
    [["Әлішер", "Нұрхасан", "Жаһид"],
     ["Айша", "Гүлайна", "Әсем"],
     ["⬅️ Бас менюге қайту"]],
    resize_keyboard=True
)

def january_keyboard():
    days = [str(i) for i in range(1, 32)]
    rows = [days[i:i + 5] for i in range(0, len(days), 5)]
    rows.append(["⬅️ Бас менюге қайту"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

# ================== HANDLERS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 *2026 ОҚУ МАРАФОНЫНА ҚОШ КЕЛДІҢ!*\n\n"
        "Күн сайын оқыған бет саны осы бот арқылы енгізіледі.\n"
        "Барлық деректер автоматты түрде Google Sheets-ке жазылады.\n\n"
        "👇 Төменнен әрекетті таңда:"
    )
    await update.message.reply_markdown(text, reply_markup=main_keyboard)
    return SELECT_ACTION

async def choose_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📘 Бет енгізу":
        await update.message.reply_text("👤 Кім оқыды?", reply_markup=person_keyboard)
        return SELECT_PERSON
    if text == "📊 Google Sheets-ті қарау":
        sheet_keyboard = ReplyKeyboardMarkup(
            [["🔗 Google Sheets-ке өту"], ["⬅️ Бас менюге қайту"]],
            resize_keyboard=True
        )
        await update.message.reply_markdown(
            "📊 *Статистика кестесі:*\n\nБағандар:\n• name — қатысушы\n• gender — ұл / қыз\n• date — күн\n• pages — бет саны",
            reply_markup=sheet_keyboard
        )
        return SELECT_ACTION
    if text == "🔗 Google Sheets-ке өту":
        await update.message.reply_text("📎 Сілтеме: https://docs.google.com/spreadsheets/d/1joO33x2UdcGWJTk8F--GCpPpmP-MnyB0YfJpatlcu2k/edit")
        return SELECT_ACTION
    if text == "⬅️ Бас менюге қайту":
        await update.message.reply_text("🏠 Басты меню", reply_markup=main_keyboard)
        return SELECT_ACTION
    await update.message.reply_text("❓ Төмендегі батырмалардың бірін таңда.")
    return SELECT_ACTION

async def choose_person(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    if name == "⬅️ Бас менюге қайту":
        await update.message.reply_text("🏠 Басты меню", reply_markup=main_keyboard)
        return SELECT_ACTION
    context.user_data["name"] = name
    await update.message.reply_text("📅 Қай күн? (Қаңтар 2026)", reply_markup=january_keyboard())
    return SELECT_DATE

async def choose_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "⬅️ Бас менюге қайту":
        await update.message.reply_text("🏠 Басты меню", reply_markup=main_keyboard)
        return SELECT_ACTION
    if not text.isdigit() or not (1 <= int(text) <= 31):
        await update.message.reply_text("❌ Күнді 1 мен 31 аралығында таңда.")
        return SELECT_DATE
    context.user_data["date"] = f"2026-01-{text.zfill(2)}"
    await update.message.reply_text("📖 Қанша бет оқыдың?")
    return ENTER_PAGES

async def enter_pages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pages = update.message.text.strip()
    if not pages.isdigit():
        await update.message.reply_text("❌ Бет саны тек сан болуы керек.\nҚайта енгіз:")
        return ENTER_PAGES
    add_record(
        name=context.user_data["name"],
        date_str=context.user_data["date"],
        pages=int(pages)
    )
    await update.message.reply_text("✅ Мәлімет сәтті сақталды!", reply_markup=main_keyboard)
    return SELECT_ACTION

# ================== MAIN ==================
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_action)],
            SELECT_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_person)],
            SELECT_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_date)],
            ENTER_PAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_pages)],
        },
        fallbacks=[],
    )
    app.add_handler(conv)
    print("🤖 BOT STARTED")
    app.run_polling()

if __name__ == "__main__":
    main()
