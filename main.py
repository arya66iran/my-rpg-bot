from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import json
import os


TOKEN = "8983609353:AAFzvwfsTRVV_lSaYCGucNGuXgbdP_cLODQ"

FILE = "players.json"


def load_players():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def save_players(players):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=4)





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_id = str(user.id)

    players = load_players()

    if user_id not in players:
        players[user_id] = {
            "name": user.first_name,
            "level": 1,
            "xp": 0,
            "hp": 100,
            "gold": 50
        }

        save_players(players)

        text = """
⚔️ شخصیت جدید ساخته شد!

نام: {}
سطح: 1
❤️ جان: 100
💰 طلا: 50

ماجراجویی تو شروع شد!
        """.format(user.first_name)

    else:
        text = "⚔️ دوباره خوش آمدی ماجراجو!"





    await update.message.reply_text(text)
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    players = load_players()

    if user_id not in players:
        await update.message.reply_text(
            "❌ هنوز شخصیت نساختی!\nاول /start را بزن."
        )
        return


    player = players[user_id]

    text = f"""
⚔️ شخصیت تو

👤 نام: {player['name']}
⭐ سطح: {player['level']}
❤️ جان: {player['hp']}
✨ تجربه: {player['xp']}
💰 طلا: {player['gold']}
"""

    await update.message.reply_text(text)




def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()