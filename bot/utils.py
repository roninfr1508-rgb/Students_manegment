import re

def log_command(func):
    def wrapper(message, *args, **kwargs):
        print(f"Command '{message.text}' called by User ID: {message.from_user.id}")
        return func(message, *args, **kwargs)
    return wrapper

def fact_generator():
    facts = [
        "Python was named after Monty Python's Flying Circus.",
        "The first version of Flask was created as an April Fool's joke.",
        "Telegram has over 800 million active users."
    ]
    for fact in facts:
        yield fact

def validate_group(group_str):
    pattern = r"^[A-Z]{2}-\d{4}$"
    return bool(re.match(pattern, group_str))