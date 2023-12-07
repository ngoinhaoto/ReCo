import chainlit as cl
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from dotenv import load_dotenv
from questions.ask_questions import ask_users_questions
from api_setup import setup_api
from utils import *

import aiohttp

load_dotenv()


@cl.on_chat_start
async def main():
    client, prompt_template, image_model = setup_api()
    responses_array = await ask_users_questions()
    await cl.Message('Please Upload your image of your item').send()

    cl.user_session.set("model", client)
    cl.user_session.set("prompt_template", prompt_template)
    cl.user_session.set("image_model", image_model)
    cl.user_session.set("responses", responses_array)


@cl.on_message
async def on_message(msg: cl.Message):

    responses = cl.user_session.get("responses")
    model = cl.user_session.get("model")
    prompt_template = cl.user_session.get("prompt_template")
    image_model = cl.user_session.get("image_model")

    new_prompt = f"""Create an image of a stylish {responses['item']} made from {responses['materials']} with a {responses['aesthetics']} look. The {responses['item']} should have a {responses['gender']} design. I am {responses['age']} years old, with the height of ({responses['height']}m) tall, and weight of ({responses['weight']}kg).\n\nThis is bonus note from the user: {responses['bonus']}. The detailed of the material is shown below:"""


    # msg_streaming = cl.Message(content="")
    stream_message = cl.Message(content="")

    total_message = new_prompt

    if not msg.elements:
        await cl.Message(content="No file attached").send()
        return
    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    for chunk in total_message.split(" "):
        messg = chunk + " "
        await stream_message.stream_token(messg)

    for img in images:  
        stream_message.content += "\n\n"

        img_based64 = decode_image(img.content)
        prompt = replace_in_prompt(prompt_template, img_based64)
        prompt = ChatPromptTemplate.from_messages(prompt)
        chain_total = prompt | model | StrOutputParser()

        async for chunk in chain_total.astream({"image_base64" : img_based64}):
            await stream_message.stream_token(chunk)

        await stream_message.send()

    
    elements_images = await generate_images(stream_message.content, image_model)

    await cl.Message(content = "The generated design!", 
                    elements = elements_images).send()

    # await cl.Message(content=).send()