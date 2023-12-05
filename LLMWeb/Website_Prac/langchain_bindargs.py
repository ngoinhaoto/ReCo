from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from dotenv import load_dotenv
import json

load_dotenv()

# Attaching OpenAI Functions
function = {
    "name": "solver",
    "description": "Formulates and solves an equation",
    "parameters": {
        "type": "object",
        "properties": {
            "equation": {
                "type": "string",
                "description": "The algebraic expression of the equation",
            },
            "solution": {
                "type": "string",
                "description": "The solution to the equation",
            },
        },
        "required": ["equation", "solution"],
    },
}


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Gets the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },

                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location", "unit"]
            }
        }
    }
]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Write out the following equation using algebraic symbols and then solve it"
        ),

        ("human", "{equation_statement}")
    ]

)
model = ChatOpenAI(model = "gpt-3.5-turbo-1106").bind(
    tools = tools
)

runnable = (
    {"equation_statement": RunnablePassthrough()} | prompt | model
    
)

# runnable.invoke("x raised to the third plus seven equals 12")
print(model.invoke("What's the weather in SF, NYC and LA?"))