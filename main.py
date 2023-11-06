import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Function to extract content within curly braces
def extract_content(data):
    contents = []
    start_index = data.find('{')
    while start_index != -1:
        end_index = data.find('}', start_index)
        if end_index != -1:
            content = data[start_index + 1:end_index].strip()
            contents.append(content)
            start_index = data.find('{', end_index)
        else:
            break
    return contents

# Function to handle the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi, I'm a bot that checks the content within braces.")

# Function to handle incoming messages
def handle_message(update: Update, context: CallbackContext):
    input_str = update.message.text

    # Extract content within curly braces from a file
    contents_in_brackets = extract_content(open('help.txt', 'r', encoding='utf-8').read())

    # Check if the input value is found within the contents of curly braces
    found_contents = []
    for content in contents_in_brackets:
        if input_str in content:
            found_contents.append(content)

    if found_contents:
        result = f"There's an error for value ({input_str}):"
        for found_content in found_contents:
            result += f"\n- {found_content}"
    else:
        result = f"The value ({input_str}) was not found within the braces."

    update.message.reply_text(result)

def main():
    # Replace 'YOUR_BOT_TOKEN' with your bot's token
    updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
    dispatcher = updater.dispatcher

    # Handle the /start command
    dispatcher.add_handler(CommandHandler('start', start))
    # Handle incoming text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
