import telebot
from flask import Flask, request
import config
from bot.models import Student
from bot.utils import log_command, fact_generator, validate_group

app = Flask(__name__)
bot = telebot.TeleBot(config.BOT_TOKEN)

saved_students = {}
facts = fact_generator()

@app.route(config.WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return '', 403

@bot.message_handler(commands=['start'])
@log_command
def send_welcome(message):
    bot.reply_to(message, "Welcome! Type /help for commands.")

@bot.message_handler(commands=['help'])
@log_command
def send_help(message):
    help_text = "/start\n/help\n/echo\n/save\n/list\n/fact\n/validate\n/about"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['echo'])
def echo(message):
    text = message.text.replace("/echo", "").strip()
    bot.reply_to(message, text if text else "Nothing to echo")

@bot.message_handler(commands=['save'])
def save(message):
    parts = message.text.split()[1:]
    if len(parts) == 4:
        name, age, group, gpa = parts
        student = Student(name, int(age), group, float(gpa))
        user_id = message.from_user.id
        if user_id not in saved_students:
            saved_students[user_id] = []
        saved_students[user_id].append(student)
        bot.reply_to(message, "Student saved.")
    else:
        bot.reply_to(message, "Format: /save Name Age Group GPA")

@bot.message_handler(commands=['list'])
def list_saved(message):
    user_id = message.from_user.id
    if user_id in saved_students and saved_students[user_id]:
        response = "\n".join(str(s) for s in saved_students[user_id])
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "No saved students.")

@bot.message_handler(commands=['fact'])
def fact(message):
    global facts
    try:
        bot.reply_to(message, next(facts))
    except StopIteration:
        facts = fact_generator()
        bot.reply_to(message, next(facts))

@bot.message_handler(commands=['validate'])
def validate(message):
    text = message.text.replace("/validate", "").strip()
    if validate_group(text):
        bot.reply_to(message, "Valid group format.")
    else:
        bot.reply_to(message, "Invalid format. Expected XX-0000.")

@bot.message_handler(commands=['about'])
def about(message):
    dummy = Student("BotAdmin", 20, "BOT-1010", 4.0)
    bot.reply_to(message, f"I am a bot managing:\n{dummy}")

if __name__ == '__main__':
    app.run(port=5000)