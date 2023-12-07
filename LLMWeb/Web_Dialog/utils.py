from PIL import Image
import base64
import io
from langchain.schema.messages import HumanMessage
from copy import deepcopy
import aiohttp
import torchvision.transforms as transforms
import os
import torch
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
        


class Normalize_image(object):
    """Normalize given tensor into given mean and standard dev

    Args:
        mean (float): Desired mean to substract from tensors
        std (float): Desired std to divide from tensors
    """

    def __init__(self, mean, std):
        assert isinstance(mean, (float))
        if isinstance(mean, float):
            self.mean = mean

        if isinstance(std, float):
            self.std = std

        self.normalize_1 = transforms.Normalize(self.mean, self.std)
        self.normalize_3 = transforms.Normalize([self.mean] * 3, [self.std] * 3)
        self.normalize_18 = transforms.Normalize([self.mean] * 18, [self.std] * 18)

    def __call__(self, image_tensor):
        if image_tensor.shape[0] == 1:
            return self.normalize_1(image_tensor)

        elif image_tensor.shape[0] == 3:
            return self.normalize_3(image_tensor)

        elif image_tensor.shape[0] == 18:
            return self.normalize_18(image_tensor)

        else:
            assert "Please set proper channels! Normlization implemented only for 1, 3 and 18"


def load_checkpoint_mgpu(model, checkpoint_path):
    if not os.path.exists(checkpoint_path):
        print("----No checkpoints at given path----")
        return 
    
    model_state_dict = torch.load(checkpoint_path, map_location=torch.device("cpu"))
    new_state_dict = OrderedDict()
    for k, v in model_state_dict.items():
        name = k[7:]  # remove `module.`
        new_state_dict[name] = v

    model.load_state_dict(new_state_dict)
    print("----checkpoints loaded from path: {}----".format(checkpoint_path))
    
    return model