# NL2SQL Chatbot

## Project Overview

This project implements a Natural Language to SQL (NL2SQL) chatbot that allows users to query a MySQL database using plain English. The chatbot leverages Large Language Models (LLMs) via Langchain to translate natural language questions into SQL queries, execute them against the database, and then provide the results back to the user in a conversational, natural language format. It also maintains a limited chat history to understand contextual follow-up questions.

## Features

  * **Natural Language to SQL Conversion**: Translate user questions into executable SQL queries.
  * **SQL Query Execution**: Execute the generated SQL queries against a MySQL database.
  * **Natural Language Response Generation**: Convert SQL query results into human-readable answers.
  * **Conversational History**: Maintain context for follow-up questions by remembering the last few turns of the conversation.
  * **Modular Design**: Organized into distinct Python modules for better maintainability and separation of concerns.
  * **Environment Variable Management**: Securely handle sensitive credentials (database, API keys) using `.env` files.
  * **Streamlit UI**: A simple, interactive web interface for the chatbot.

## Technologies Used

  * **Python 3.x**
  * **Streamlit**: For building the interactive web UI.
  * **Langchain**: Framework for building LLM-powered applications.
      * `langchain-community`
      * `langchain-core`
      * `langchain-openai`
  * **SQLAlchemy**: Python SQL Toolkit and Object Relational Mapper (ORM) for database interactions.
  * **PyMySQL**: MySQL database connector for Python (used by SQLAlchemy).
  * **python-dotenv**: For loading environment variables.
  * **OpenAI API**: For the Large Language Model (LLM) capabilities (GPT-3.5 Turbo).

## Project Structure

```
nl2sql_project/
├── .env                  # Environment variables (DB credentials, OpenAI API Key)
├── requirements.txt      # Python dependencies
├── app.py                # Streamlit application for the UI
├── database_utils.py     # Module for database connection and Langchain SQLDatabase setup
├── llm_chain.py          # Module for defining the Langchain NL2SQL chain (query generation, execution, answer generation)
├── logger_config.py      # Module for configuring application logging
├── README.md             # Project description and setup instructions
├── logs/                 # Directory for application logs (created automatically)
│   └── nl2sql_app.log    # Example log file
└── mysql_db/             # Optional: Directory for MySQL database dump files
    └── your_database.sql # Example SQL dump file
```

## Setup and Installation

1.  **Clone the repository (if applicable):**

    ```bash
    git clone <your-repo-url>
    cd nl2sql_project
    ```

2.  **Create a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage dependencies.

    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**

      * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
      * **On Windows:**
        ```bash
        venv\Scripts\activate
        ```

4.  **Install Dependencies:**
    Install all required Python packages using `pip`.

    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables (`.env` file):**
    Create a file named `.env` in the root of your `nl2sql_project` directory and add your MySQL database credentials and OpenAI API Key. Replace the placeholder values with your actual information.

    ```dotenv
    # .env
    DB_USER="root" # Or your MySQL username
    DB_PASSWORD="your_mysql_root_password" # Your actual MySQL password
    DB_HOST="localhost"
    DB_PORT="3306"
    DB_NAME="classicmodels" # Your specific database name

    OPENAI_API_KEY="sk-your_openai_api_key_here" # Your actual OpenAI API Key
    ```

6.  **Ensure MySQL Database is Running:**
    Make sure your MySQL server is running and the specified `DB_NAME` database exists and is accessible with the provided credentials.

7.  **Load Database from `mysql_db` Folder (if applicable):**
    If your database schema and data are provided as a SQL dump file (e.g., `your_database.sql`) in a `mysql_db` folder, you can load it into your MySQL instance using the `mysql` command-line client.

      * **Navigate to your project's root directory.**
      * **Execute the SQL dump:**
        ```bash
        mysql -u your_mysql_username -p your_database_name < mysql_db/your_database.sql
        ```
        (Replace `your_mysql_username` and `your_database_name` with your actual MySQL username and the database name you configured in `.env`. You will be prompted for your MySQL password.)

## Usage

1.  **Run the Streamlit Application:**
    With your virtual environment activated, run the `app.py` file:

    ```bash
    streamlit run app.py
    ```

2.  **Interact with the Chatbot:**
    Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`). Type your natural language questions about the database into the chat input and press Enter.

## Interview Focus / Key Learnings

This project demonstrates several key software engineering and AI development concepts that are frequently discussed in technical interviews:

1.  **Modular Design and Separation of Concerns**:

      * **`database_utils.py`**: Handles all database connection logic, abstracting it away from the core application. This promotes reusability and makes it easy to swap database types if needed.
      * **`llm_chain.py`**: Contains the core LLM and Langchain logic, separating it from the UI. This allows for independent testing and evolution of the NL2SQL capabilities.
      * **`logger_config.py`**: Centralizes logging configuration, ensuring consistent logging across the application and easy modification of log levels/destinations.
      * **`app.py`**: Focuses solely on the Streamlit UI and orchestrating calls to the backend modules.

2.  **Dependency Management**:

      * The `requirements.txt` file ensures all project dependencies are clearly listed and can be easily installed, promoting reproducibility.
      * The use of `venv` (virtual environments) isolates project dependencies, preventing conflicts with other Python projects on your system.

3.  **Configuration Management and Security**:

      * Using a `.env` file with `python-dotenv` is a standard practice for managing sensitive information (API keys, database credentials) securely. This keeps secrets out of version control and allows for easy configuration changes across different environments (development, staging, production).

4.  **Langchain Fundamentals**:

      * **`SQLDatabase`**: Understanding how Langchain interfaces with databases via SQLAlchemy.
      * **`create_sql_query_chain`**: Demonstrates the core capability of generating SQL from natural language.
      * **`QuerySQLDataBaseTool`**: Shows how to execute generated SQL queries.
      * **Runnable Interface (`|`, `RunnableParallel`, `RunnablePassthrough`)**: Highlights Langchain's powerful expression language for building complex, composable LLM applications. This is a modern approach to chaining components.
      * **Prompt Engineering**: The `answer_prompt_template` shows a basic example of how to guide the LLM to format its output. (Future: Few-shot prompting for better SQL generation).

5.  **State Management in Streamlit**:

      * The use of `st.session_state` is critical for maintaining the `DatabaseManager`, `NL2SQLChainManager`, and the chat `messages` across Streamlit's reruns. This prevents expensive re-initializations and preserves conversational context.

6.  **Error Handling and Robustness**:

      * `try-except` blocks are implemented in all modules (`database_utils.py`, `llm_chain.py`, `app.py`) to gracefully handle potential issues like database connection failures, missing environment variables, or LLM errors.
      * Logging (`logger_config.py`) provides visibility into the application's runtime behavior, aiding in debugging and monitoring.

7.  **Conversational AI Concepts**:

      * **Chat History Management**: The FIFO (First-In, First-Out) logic for `st.session_state.messages` demonstrates how to manage conversational context efficiently, preventing the context window from growing indefinitely and improving relevance for follow-up questions.
      * **Contextual Understanding**: The LLM's ability to interpret "how many disputed?" after "how many orders are there?" showcases basic contextual understanding.

8.  **Scalability and Extensibility (Future Considerations)**:

      * The current modular design makes it easier to swap out components (e.g., change LLM providers, integrate different database types, or upgrade to Langchain's SQL Agent framework for more complex reasoning) without a complete rewrite.
      * The foundation is laid for adding features like few-shot examples, input validation, or more sophisticated error recovery.

-----

**To "download" this `README.md` file:**

1.  **Select and copy all the text above**, from `# NL2SQL Chatbot` to the very last line of the "Scalability and Extensibility" section.
2.  **Open a plain text editor** on your computer (e.g., Notepad on Windows, TextEdit on macOS, or a code editor like VS Code, Sublime Text, Atom).
3.  **Paste the copied text** into the new, empty file.
4.  Go to **File \> Save As...**
5.  **Navigate to the root directory of your `nl2sql_project`**.
6.  In the "File name" field, type **`README.md`**.
7.  In the "Save as type" or "Format" dropdown, ensure you select **"All Files"** or **"Plain Text"** to prevent the editor from adding a `.txt` extension.
8.  Click **Save**.

This file now contains the raw Markdown syntax. When you open this `README.md` file in an application that understands Markdown (like VS Code's built-in preview, or when you upload it to a platform like GitHub), it will display with the proper formatting.