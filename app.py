import os
import time
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.llms import Ollama  # Replace with your specific open-source LLM model

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

# Initialize your open-source LLM model
llm = Ollama(model="llama2:7b")  # Replace with your actual initialization method for the LLM model

# Chains using LLM
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper()

# Show stuff to the screen if there's a prompt
if prompt:
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    if title and wiki_research:
        script = script_chain.run(title=title, wikipedia_research=wiki_research)

        st.write(title)
        st.write(script)

        with st.expander('Title History'):
            st.info(title_memory.buffer)

        with st.expander('Script History'):
            st.info(script_memory.buffer)

        with st.expander('Wikipedia Research'):
            st.info(wiki_research)
    else:
        st.error("Failed to generate title or script.")
