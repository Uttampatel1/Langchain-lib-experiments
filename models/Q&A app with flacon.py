import os
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
# from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import SequentialChain
import streamlit as st


# --------------------------------------------------------------
# Load the HuggingFaceHub API token from the .env file
# --------------------------------------------------------------

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
# os.environ["OPENAI_API_KEY"]=openai_key

# streamlit framework

st.title('Search Results')
input_text=st.text_input("Search the topic u want")

# Prompt Templates

first_input_prompt=PromptTemplate(
    input_variables=['name'],
    template="Tell me about celebrity {name}"
)

# Memory

person_memory = ConversationBufferMemory(input_key='name', memory_key='chat_history')
dob_memory = ConversationBufferMemory(input_key='person', memory_key='chat_history')
descr_memory = ConversationBufferMemory(input_key='dob', memory_key='description_history')


# --------------------------------------------------------------
# Load the LLM model from the HuggingFaceHub
# --------------------------------------------------------------

repo_id = "tiiuae/falcon-7b-instruct"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
# repo_id ="bigscience/bloom-560m"
llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.1, "max_new_tokens": 500}
)
## OPENAI LLMS
# llm=OpenAI(temperature=0.8)
chain=LLMChain(
    llm=llm,prompt=first_input_prompt,verbose=True,output_key='person',memory=person_memory)

# Prompt Templates

second_input_prompt=PromptTemplate(
    input_variables=['person'],
    template="when was {person} born"
)

chain2=LLMChain(
    llm=llm,prompt=second_input_prompt,verbose=True,output_key='dob',memory=dob_memory)
# Prompt Templates

third_input_prompt=PromptTemplate(
    input_variables=['dob'],
    template="Mention 5 major events happened around {dob} in the world"
)
chain3=LLMChain(llm=llm,prompt=third_input_prompt,verbose=True,output_key='description',memory=descr_memory)
parent_chain=SequentialChain(
    chains=[chain,chain2,chain3],input_variables=['name'],output_variables=['person','dob','description'],verbose=True)



if input_text:
    st.write(parent_chain({'name':input_text}))

    with st.expander('Person Name'): 
        st.info(person_memory.buffer)

    with st.expander('Major Events'): 
        st.info(descr_memory.buffer)