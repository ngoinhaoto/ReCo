from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import load_tools
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from dotenv import load_dotenv


load_dotenv()


def generate_pet_name(animal_type, pet_color):
    llm = OpenAI(temperature=0.6)

    prompt_template_name = PromptTemplate(
        input_variables = ['animal_type', 'pet_color'],
        template = """I have a {animal_type} pet and I want a cool name for it,
         it is {pet_color}. Suggest me five cool names for my pet.""",
    )

    name = LLMChain(llm = llm, prompt = prompt_template_name,
                    output_key = "pet_name")
    
    response = name({'animal_type': animal_type, 'pet_color': pet_color})
    return response


def langchain_agent():
    llm = OpenAI(temperature=0.5)
    
    tools = load_tools(['wikipedia', 'llm-math'], llm = llm)
    agent = initialize_agent(
        tools, llm, agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose = True
    )

    result = agent.run(
        "What is the average age of a dog? Multiply the age by 3"
    )
    print(result)

if __name__ == '__main__':
    # print(generate_pet_name("cow", "black"))
    print(langchain_agent())