import os
import time
from apikey import apikey
import streamlit as st
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import WikipediaAPIWrapper

os.environ['OPENAI_API_KEY'] = apikey

# Streamlit App framework
st.title('YouTube Script Assistant')
st.image('./Youtube.png', use_column_width=True)
prompt = st.text_input('Plug in your prompt here')

# Prompt templates
title_template = PromptTemplate(
    input_variables=['topic'],
    template='write me a youtube video title about {topic}'
)

script_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'],
    template='write me a youtube video script based on this title TITLE: {title} while leveraging this wikipedia research: {wikipedia_research}'
)

# Memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

# LLMs
llm = OpenAI(temperature=0.9)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper()

# Function to handle API call with retry mechanism
def call_api_with_retry(api_call, max_retries=5, backoff_factor=1):
    retries = 0
    while retries < max_retries:
        try:
            return api_call()
        except Exception as e:
            if '429' in str(e):  # Check for rate limit error
                wait_time = backoff_factor * (2 ** retries)  # Exponential backoff
                st.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
            else:
                st.error(f"An error occurred: {e}")
                break
    return None

# Show stuff to the screen if there's a prompt
if prompt:
    title = call_api_with_retry(lambda: title_chain.run(prompt))
    wiki_research = call_api_with_retry(lambda: wiki.run(prompt))
    if title and wiki_research:
        script = call_api_with_retry(lambda: script_chain.run(title=title, wikipedia_research=wiki_research))

        st.write(title)
        st.write(script)

        with st.expander('Title History'):
            st.info(title_memory.buffer)

        with st.expander('Script History'):
            st.info(script_memory.buffer)

        with st.expander('Wikipedia Research'):
            st.info(wiki_research)
    else:
        st.error("Failed to generate title or script due to rate limit issues.")
