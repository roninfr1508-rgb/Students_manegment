import re
import random

def log_command(func):
    def wrapper(message, *args, **kwargs):
        print(f"Command '{message.text}' called by User ID: {message.from_user.id}")
        return func(message, *args, **kwargs)
    return wrapper

def fact_generator():
    facts = [
        "I love skibidi toilet",
        "67 is super prime number",
        "Generation z is cooked"
        "All people deserve 100 points"
    ]
    for fact in facts:
        yield fact

def validate_group(group_str):
    pattern = r"^[A-Z]{2}-\d{4}$"
    return bool(re.match(pattern, group_str))

import random

def remove_random_student(students_dict, user_id):
    if user_id in students_dict and students_dict[user_id]:
        student = random.choice(students_dict[user_id])
        students_dict[user_id].remove(student)
        return student
    return None