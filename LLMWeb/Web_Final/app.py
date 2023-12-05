from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage
from langchain.schema import StrOutputParser
from openai import OpenAI
import aiofiles
import aiohttp

from PIL import Image
import io
from copy import deepcopy

import base64
from dotenv import load_dotenv

import chainlit as cl

load_dotenv()

def decode_image(image_file):
    img = Image.open(io.BytesIO(image_file))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()
    encoded_string = base64.b64encode(img_byte_arr)
    return encoded_string.decode('utf-8')

def replace_in_prompt(prompt, image_base64):
    prompt = deepcopy(prompt)
    for message in prompt:
        if isinstance(message, HumanMessage):
            for content in message.content:
                if 'type' in content and content['type'] == 'image_url':
                    content['image_url']['url'] = content['image_url']['url'].format(image_base64=image_base64)
    return prompt

@cl.on_chat_start
async def on_chat_start():  
    client = ChatOpenAI(model = 'gpt-4-vision-preview', max_tokens = 1024)

    prompt_template = [
        SystemMessage(
            content=(
                """Being a knowledgeable bot with expertise in eco-fashion, I am adept at describing fashion-related items depicted in images. 
                My proficiency extends to providing insights on extracting features for the design of eco-friendly fashion items crafted from 
                recycled materials, particularly old clothes. My goal is to assist in generating prompts that inspire the redesigning process 
                for sustainable and stylish fashion creations."""
            )
        ),
        HumanMessage(
            content=[
                {"type": "text", "text": """Examine the image closely and identify fashion-related features from old clothes. 
                                            Provide a detailed description in a maximum of 3 sentences, emphasizing unique and distinctive elements.
                                             Your goal is to gather insights that will inspire the creation of prompts for DALL-E 3, focusing on generating 
                                            innovative and eco-friendly designs from the identified features in the old clothes"""},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,{image_base64}", 
                    },
                },
            ]
        )]
    
    image_model = OpenAI()
    
    cl.user_session.set('image_model', image_model)
    cl.user_session.set('model', client)
    cl.user_session.set('prompt_template', prompt_template)

@cl.on_message
async def on_message(message: cl.Message):

    model = cl.user_session.get('model')
    prompt_template = cl.user_session.get('prompt_template')
    image_model = cl.user_session.get('image_model')

    msg = cl.Message(content="")
    
    if not message.elements:
        await cl.Message(content="No file attached").send()
        
    else:
        print(message.content)

        images = [file for file in message.elements if "image" in file.mime]
        
        for img in images:

            img_based64 = decode_image(img.content)
            prompt = replace_in_prompt(prompt_template, img_based64)
            prompt = ChatPromptTemplate.from_messages(prompt)

            chain_total = prompt | model | StrOutputParser()

            async for chunk in chain_total.astream({"image_base64" : img_based64}):
                await msg.stream_token(chunk)
        
        await msg.send()

    msg.content = msg.content + "\n\n" + message.content

    response = image_model.images.generate(
        model = "dall-e-3",
        prompt = msg.content,
        size = "1024x1024",
        n = 1
    )

    print(response.data)
    print()
    image_url = response.data[0].url
    # image_url = 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-X9TzN7BYbDqfHIaaAH439fWF/user-OWXpSYqIC3opjQXB1XuCVvJW/img-bxwvIuNitqOtVd48QegeVctY.png?st=2023-12-02T08%3A36%3A55Z&se=2023-12-02T10%3A36%3A55Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-12-01T22%3A35%3A15Z&ske=2023-12-02T22%3A35%3A15Z&sks=b&skv=2021-08-06&sig=mncJGKSlbkr5PcDY2Hgajj6AJuomdzZ%2BIv3G4qUQuOE%3D'
    # image_url = 'https://images.unsplash.com/photo-1682685797439-a05dd915cee9?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    print(image_url)

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            image_content = await resp.read()
            image2 = cl.Image(name="image2", display="inline", content=image_content)
            
            elements = [image2]
            await cl.Message(content="The generated design!", elements=elements).send()
            print(image2)
            

