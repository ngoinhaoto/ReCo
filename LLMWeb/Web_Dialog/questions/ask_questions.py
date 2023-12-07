import chainlit as cl
from .choice_items import *


def check_valid_age(age):
    if age.isdigit() and int(age) > 0:
        return True
    return False

def check_valid_weight(weight):
    if weight.isdigit() and int(weight) > 0:
        return True
    return False

def check_valid_height(height):
    height = float(height)
    if height > 0:
        return True
    return False


async def ask_users_questions():
    while True:
        res1 = await cl.AskActionMessage(
            content="What item do you want to create?",
            actions=[
                cl.Action(name="Shirt", value="shirt", label="👕 Shirt"),
                cl.Action(name="Pants", value="pants", label="👖 Pants"),
                cl.Action(name="Bag", value="bag", label="🎒 Bag")
                ]
        ).send()
        if res1.get("value") in clothes_items:
            break


    res2 = await cl.AskUserMessage(content = "What materials do you have? ", timeout = 1000).send()
    
    while True:
        res3 = await cl.AskActionMessage(
            content = "What is your desired aesthetic?",
            actions = [
                cl.Action(name="Business", value='business', label='Business'),
                cl.Action(name="Vintage", value='vintage', label='Vintage'),
                cl.Action(name="Minimalist", value='minimalist', label='Minimalist'),
                cl.Action(name="Casual", value='casual', label='Casual')
            ]
        ).send()
    
        if res3.get("value") in asthetics:
            break


    while True:
        res4 = await cl.AskActionMessage(
            content = "What gender do you want your item to be?",
            actions = [
                cl.Action(name="Male", value='male', label='👨 Male'),
                cl.Action(name="Female", value='female', label='👩 Female'),
                cl.Action(name="Unisex", value='unisex', label='🚻 Unisex'),
            ]
        ).send()
        if res4.get("value") in gender:
            break
    
    while True:
        res5 = await cl.AskUserMessage(content = "What is your age? ", timeout = 1000).send()   
        if check_valid_age(res5.get("content")):
            break
    
    while True:
        res6 = await cl.AskUserMessage(content = "What is your weight (in kg)? ", timeout = 1000).send()
        if check_valid_weight(res6.get("content")):
            break
    
    while True:
        res7 = await cl.AskUserMessage(content = "What is your height (in meters)? ", timeout = 1000).send()
        if check_valid_height(res7.get("content")):
            break

    res8 = await cl.AskUserMessage(content = "What are your notes to the designer? ", timeout = 1000).send()
    
    return {
        "item": res1.get("value"),
        "materials": res2.get("content"),
        "aesthetics": res3.get("value"),
        "gender": res4.get("value"),
        "age": res5.get("content"),
        "height": res6.get("content"),
        "weight": res7.get("content"),
        "bonus": res8.get("content")
    }