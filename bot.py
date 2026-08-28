import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
Application,
CommandHandler,
CallbackQueryHandler,
ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

JOBS = {
"usa": {
"title": "Warehouse Associate 🇺🇸",
"location": "New York, USA",
"salary": "$20/hour",
"type": "Full-time",
"requirements": "18+ years old, valid work authorization, basic English.",
"apply_url": "https://example.com/apply"
},
"uk": {
"title": "Care Assistant 🇬🇧",
"location": "London, UK",
"salary": "£13/hour",
"type": "Full-time",
"requirements": "18+ years old, relevant experience preferred.",
"apply_url": "https://example.com/apply"
},
"canada": {
"title": "General Worker 🇨🇦",
"location": "Toronto, Canada",
"salary": "C$22/hour",
"type": "Full-time",
"requirements": "18+ years old, physically fit, basic communication skills.",
"apply_url": "https://example.com/apply"
}
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
keyboard = [
[InlineKeyboardButton("🇺🇸 USA Jobs", callback_data="usa")],
[InlineKeyboardButton("🇬🇧 UK Jobs", callback_data="uk")],
[InlineKeyboardButton("🇨🇦 Canada Jobs", callback_data="canada")],
]

reply_markup = InlineKeyboardMarkup(keyboard)

await update.message.reply_text(
"👋 Welcome to Global Job Finder!\n\n"
"💼 Find available job opportunities below.\n\n"
"Please select a job category:",
reply_markup=reply_markup
)


async def job_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

job = JOBS.get(query.data)

if not job:
await query.edit_message_text("❌ Job not found.")
return

keyboard = [
[InlineKeyboardButton("📝 Apply Now", url=job["apply_url"])],
[InlineKeyboardButton("🔙 Back to Categories", callback_data="back")]
]

reply_markup = InlineKeyboardMarkup(keyboard)

message = (
f"💼 {job['title']}\n\n"
f"📍 Location: {job['location']}\n"
f"💰 Salary: {job['salary']}\n"
f"🕒 Job Type: {job['type']}\n\n"
f"📋 Requirements:\n{job['requirements']}\n\n"
"👇 Click below to apply:"
)

await query.edit_message_text(
message,
reply_markup=reply_markup
)


async def back_to_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

keyboard = [
[InlineKeyboardButton("🇺🇸 USA Jobs", callback_data="usa")],
[InlineKeyboardButton("🇬🇧 UK Jobs", callback_data="uk")],
[InlineKeyboardButton("🇨🇦 Canada Jobs", callback_data="canada")],
]

await query.edit_message_text(
"💼 Select a job category:",
reply_markup=InlineKeyboardMarkup(keyboard)
)


def main():
if not BOT_TOKEN:
raise ValueError("BOT_TOKEN is not configured.")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(back_to_categories, pattern="^back$"))
app.add_handler(CallbackQueryHandler(job_details))

print("Bot is running...")
app.run_polling()


if name == "main":
main()
