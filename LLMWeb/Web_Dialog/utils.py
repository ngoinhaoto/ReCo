from PIL import Image
import base64
import io
from langchain.schema.messages import HumanMessage
from copy import deepcopy
import aiohttp
import os
from collections import OrderedDict

import chainlit as cl


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


async def generate_images(prompt, image_model):
    response = image_model.images.generate(
            model = "dall-e-3",
            prompt = prompt,
            size = "1024x1024",
            n = 1
        )

    image_url = response.data[0].url

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            image_content = await resp.read()
            image2 = cl.Image(name="image2", display="inline", content=image_content)
            
            elements = [image2]
            
            return elements
        
