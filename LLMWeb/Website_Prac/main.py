from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.memory import ConversationBufferMemory


from operator import itemgetter

import chainlit as cl


async def count_token(runnable, query):
    async for result in runnable.astream(query):
        yield result

@cl.cache
def create_memory():
    return ConversationBufferMemory(return_messages = True, input_key = 'question')


@cl.on_chat_start
async def on_chat_start():

    model  = ChatOpenAI(streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.
                But you don't like to give long responses since you're lazy. You usually gives responses that are 1 paragraph long.""",
            ),
            ('system', 'Current conversation'),
            MessagesPlaceholder('history'),
            ("human", '{question}'),
        ]
    )
    memory = create_memory()
    runnable = (
        RunnablePassthrough.assign(
            history = RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt 
        | model
    )
    
    cl.user_session.set("runnable", runnable)
    cl.user_session.set("memory", memory)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable    
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory
    
    msg = cl.Message(content="")

    async for chunk in count_token(runnable, {"question": message.content}):
        await msg.stream_token(chunk.content)

    await msg.send()
    print("Hello")

    memory.save_context({"question": message.content}, {"output": msg.content})
    print(memory.load_memory_variables({}))

    print("Yes")



