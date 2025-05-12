from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain the following vehicle event in simple terms: {topic}"
)

chain = LLMChain(llm=llm, prompt=prompt)
output = chain.run("Emergency braking after pedestrian detection at 10:05")
print(output)
