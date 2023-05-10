import openai
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Set up OpenAI API key
openai.api_key = "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"
model_engine = "text-davinci-003"

# Set up Telegram bot
bot = Bot(token= '6150621356:AAHnWvtS3G_cGG5s7kAAXMU1xZsvcV1LD7s')
dp = Dispatcher(bot)

# Dictionary to keep track of sender IDs and their current dialogues
dialogues = {}

# Define the welcome message
welcome_message = "Hello! I'm Ziniukas, a helpful assistant. How can I assist you today?"

# Define a function to generate responses using GPT-3
async def generate_response(message):
    # Get the sender's ID
    sender_id = message.from_user.id

    # Get the sender's current dialogue (if any)
    current_dialogue = dialogues.get(sender_id, [])

    # Add the current message to the sender's dialogue
    current_dialogue.append(message.text)

    # Keep only the last 3 messages in the sender's dialogue
    if len(current_dialogue) > 3:
        current_dialogue = current_dialogue[-3:]

    dialogues[sender_id] = current_dialogue

    # Concatenate all messages in the sender's dialogue into a single string
    dialogue_str = "\n".join(current_dialogue)

    # Generate a response from GPT-3
    response = openai.Completion.create(
        model=model_engine,
        prompt=dialogue_str,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the generated text from the response
    generated_text = response.choices[0].text.strip()

    # Add the generated text to the sender's dialogue
    current_dialogue.append(generated_text)

    # Keep only the last 3 messages in the sender's dialogue
    if len(current_dialogue) > 3:
        current_dialogue = current_dialogue[-3:]

    dialogues[sender_id] = current_dialogue

    # Return the generated text
    return generated_text

# Define the handler for the /start command
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    # Get the sender's ID
    sender_id = message.from_user.id

    # Clear the sender's dialogue history
    dialogues[sender_id] = []

    # Send the welcome message
    await message.answer(welcome_message)

# Define the handler for all other messages
@dp.message_handler()
async def message_handler(message: types.Message):
    # Generate a response using GPT-3
    response_text = await generate_response(message)

    # Send the response back to the user
    await message.answer(response_text)

# Start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)




