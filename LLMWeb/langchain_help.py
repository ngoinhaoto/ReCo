from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage, AIMessage, SystemMessage
from langchain.schema import StrOutputParser
from copy import deepcopy

import base64
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")


client = ChatOpenAI(model = 'gpt-4-vision-preview', max_tokens = 1024)


prompt_template = [
    SystemMessage(
        content=(
            "You are a useful bot that is especially good at OCR from images"
        )
    ),
    HumanMessage(
        content=[
            {"type": "text", "text": "Identify all items on the this image which are fashion related and describe it in maximum4 sentences"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/jpeg;base64,{image_base64}", 
                },
            },
        ]
    )]

image_base64 = encode_image("./lol.jpg")

prompt = deepcopy(prompt_template)
for message in prompt:
    if isinstance(message, HumanMessage):
        for content in message.content:
            if 'type' in content and content['type'] == 'image_url':
                content['image_url']['url'] = content['image_url']['url'].format(image_base64=image_base64)


prompt = ChatPromptTemplate.from_messages(prompt)
# print(prompt)

chain_total = prompt | client | StrOutputParser()

print(chain_total.invoke({"image_base64": image_base64}))
# print(chain_total.invoke({"image_base64": image_base64}))
