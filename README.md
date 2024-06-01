# YouTube Script Assistant

YouTube Script Assistant is a web application that helps you generate YouTube video titles and scripts based on a given topic. It utilizes OpenAI's GPT-3.5 model via the LangChain library to generate content and fetches additional research information from Wikipedia.

## Features

- Generate YouTube video titles based on user-provided topics.
- Generate detailed YouTube video scripts leveraging Wikipedia research.
- View history of generated titles and scripts.
- Handles API rate limits with an exponential backoff retry mechanism.

## Prerequisites

- Python 3.7 or higher
- Streamlit
- LangChain
- OpenAI API key

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/youtube-script-assistant.git
   cd youtube-script-assistant
   ```

2. **Install the required packages:**

   ```bash
   pip install streamlit langchain openai pandas
   ```

3. **Set up your OpenAI API key:**

   Create a file named `apikey.py` in the project directory and add your OpenAI API key:

   ```python
   apikey = 'your_openai_api_key'
   ```

## Usage

1. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

2. **Open the app in your web browser:**

   After running the above command, Streamlit will provide a URL (typically `http://localhost:8501`). Open this URL in your web browser to access the app.

3. **Generate content:**

   - Enter a topic for your YouTube video in the provided input box.
   - The app will generate a video title and script based on the topic.
   - You can view the generated content and check the history of generated titles and scripts.

## Code Explanation

### Main Components

- **Prompt Templates:** Define how prompts are structured for title and script generation.
- **Memory:** Stores the conversation history for both title and script generation.
- **Language Model Chains:** Manage the interaction with the OpenAI model using the defined prompts and memory.
- **Wikipedia API Wrapper:** Fetches research information from Wikipedia.

### Key Functions

- **call_api_with_retry:** Handles API calls with retry logic to manage rate limits.
- **generate_content:** Generates the title and script, displays the results, and handles errors.
- **main:** Sets up the Streamlit interface and handles user input.

### Handling API Rate Limits

The `call_api_with_retry` function implements an exponential backoff mechanism to handle API rate limits gracefully. It retries the API call several times with increasing wait times in case of a rate limit error.

## Code Details

```python
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
```

## Further Improvements

Adding a download_link which creates a download link for the generated script.

## Contributing

Contributions are welcome! Please create an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [LangChain](https://langchain.io/)
- [OpenAI](https://openai.com/)