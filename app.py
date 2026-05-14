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
    help_text = "/start\n/help\n/echo\n/save\n/list\n/fact\n/validate\n/about\n/update\n/del_student"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['echo'])
def echo(message):
    text = message.text.replace("/echo", "").strip()
    bot.reply_to(message, text if text else "Nothing to echo")


@bot.message_handler(commands=['save'])
def save(message):
    parts = message.text.split()[1:]
    if len(parts) == 4:
        try:
            name, age_str, group, gpa_str = parts
            age = int(age_str)
            gpa = float(gpa_str)

            if age < 15 or age > 35:
                bot.reply_to(message, f"Error! age must be between 15 and 25.")
                return

            if gpa > 4.0:
                bot.reply_to(message, f"Error! GPA {gpa} cant be more than 4.0.")
                return
            if gpa < 0.0:
                bot.reply_to(message, "Error GPA cant be bellow 0.")
                return

            student = Student(name, age, group, gpa)
            user_id = message.from_user.id

            if user_id not in saved_students:
                saved_students[user_id] = []

            saved_students[user_id].append(student)
            bot.reply_to(message, "Student saved")

        except ValueError:
            bot.reply_to(message, "Error GPA must be float number.")
    else:
        bot.reply_to(message, "Format /save name age group GPA")

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
    bot.reply_to(message, "I am a bot that manages student and their groups")

@bot.message_handler(commands=['del_student'])
def delete(message):
    parts = message.text.split()
    if len(parts) == 2:
        try:
            student_id = int(parts[1])
            user_id = message.from_user.id

            if user_id in saved_students:
                for student in saved_students[user_id]:
                    if student.id == student_id:
                        saved_students[user_id].remove(student)
                        bot.reply_to(message, "Student deleted")
                        return
                bot.reply_to(message, "Student not found")
            else:
                bot.reply_to(message, "No saved students")
        except ValueError:
            bot.reply_to(message, "ID must be a number")
    else:
        bot.reply_to(message, "Usage: /del_student ID")

@bot.message_handler(commands=['update'])
def update_student(message):
    parts = message.text.split()[1:]
    if len(parts) == 5:
        try:
            student_id = int(parts[0])
            name = parts[1]
            age = int(parts[2])
            group = parts[3]
            gpa = float(parts[4])

            if age < 15 or age > 35:
                bot.reply_to(message, "Error! age must be between 15 and 35.")
                return

            if gpa > 4.0 or gpa < 0.0:
                bot.reply_to(message, "Error! GPA must be between 0.0 and 4.0.")
                return

            user_id = message.from_user.id

            if user_id in saved_students:
                for student in saved_students[user_id]:
                    if student.id == student_id:
                        student.name = name
                        student.age = age
                        student.group = group
                        student.gpa = gpa
                        bot.reply_to(message, "Student updated")
                        return
                bot.reply_to(message, "Student not found")
            else:
                bot.reply_to(message, "No saved students")
        except ValueError:
            bot.reply_to(message, "Error! Invalid ID, age or GPA format.")
    else:
        bot.reply_to(message, "Format: /update ID name age group GPA")


if __name__ == '__main__':
    app.run(port=5000)