# YouTube Script Assistant with Streamlit

This Streamlit web application helps users generate YouTube video titles and scripts based on provided prompts. It utilizes an LLM (Large Language Model) from the LangChain library and integrates with Wikipedia for additional research.

![YouTube Script Assistant](./Youtube.png)

## Features

- **Title Generation**: Generates YouTube video titles based on user-provided topics.
- **Script Generation**: Generates video scripts based on previously generated titles and relevant Wikipedia research.
- **History Tracking**: Keeps track of generated titles, scripts, and Wikipedia research across sessions.

## Setup

To run this application locally, follow these steps:

### Prerequisites

- Python 3.7 or higher installed on your system.
- Dependencies installed:
  ```bash
  pip install streamlit langchain langchain-community
  ```

### Running the Application

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

4. Access the application in your web browser at `http://localhost:8501`.

## Usage

1. **Input Prompt**: Enter a topic or subject into the text input field.
2. **Title Generation**: Click on "Generate Title" to generate a YouTube video title based on the entered topic.
3. **Wikipedia Research**: The application automatically performs Wikipedia research based on the entered topic.
4. **Script Generation**: Once a title and relevant Wikipedia research are generated, click on "Generate Script" to produce a YouTube video script.
5. **History**: View generated titles, scripts, and Wikipedia research history using the expandable sections.

## Examples

- **Example 1**: Entering "Artificial Intelligence" generates a title like "Exploring the Future of Artificial Intelligence."
- **Example 2**: Based on the above title, the application may generate a script discussing various AI technologies and their impact on society.

## Limitations

- **Rate Limits**: Ensure API calls (like Wikipedia) do not exceed rate limits, which may temporarily limit functionality.

## Contributing

Contributions are welcome! Fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This application uses LangChain and LangChain Community libraries for natural language processing tasks.
- Special thanks to the developers of Streamlit for providing an excellent framework for building interactive web applications.

---

Shaaz Daud