import os
import telebot
import chess

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Store games by chat id
games = {}

def get_board_text(board):
    return f"<pre>{board}</pre>"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "♟️ Welcome to Chess Bot!\nType /newgame to start.")

@bot.message_handler(commands=['newgame'])
def new_game(message):
    games[message.chat.id] = chess.Board()
    board = games[message.chat.id]
    bot.send_message(message.chat.id, "New game started!\n" + get_board_text(board), parse_mode="HTML")

@bot.message_handler(func=lambda message: True)
def handle_move(message):
    chat_id = message.chat.id

    if chat_id not in games:
        bot.reply_to(message, "Start a game first with /newgame")
        return

    board = games[chat_id]
    move_text = message.text.strip()

    try:
        move = chess.Move.from_uci(move_text)

        if move in board.legal_moves:
            board.push(move)

            if board.is_checkmate():
                bot.send_message(chat_id, "Checkmate! Game over.\n" + get_board_text(board), parse_mode="HTML")
                del games[chat_id]
                return

            bot.send_message(chat_id, get_board_text(board), parse_mode="HTML")
        else:
            bot.reply_to(message, "Illegal move!")

    except:
        bot.reply_to(message, "Invalid format! Use moves like e2e4")

bot.infinity_polling()
