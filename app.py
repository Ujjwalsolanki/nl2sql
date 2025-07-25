import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

# Import our custom modules
from database_utils import DatabaseManager
from llm_chain import NL2SQLChainManager
from logger_config import setup_logging

# Setup logging for the Streamlit app
logger = setup_logging(log_file="nl2sql_app.log", log_level="INFO", console_output=True)

# --- Streamlit UI Configuration ---
st.set_page_config(
    page_title="NL2SQL Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🤖 NL2SQL Chatbot")
st.markdown("Ask me questions about your database in natural language!")

# --- Initialize Session State ---
# This helps prevent re-initializing heavy objects (like LLM chains) on every rerun.
if "db_manager" not in st.session_state:
    try:
        st.session_state.db_manager = DatabaseManager()
        st.session_state.langchain_sql_db = st.session_state.db_manager.get_langchain_db()
        logger.info("DatabaseManager and Langchain SQLDatabase initialized in session state.")
    except Exception as e:
        st.error(f"Failed to connect to the database: {e}")
        logger.critical(f"Failed to initialize DatabaseManager: {e}", exc_info=True)
        st.stop() # Stop the app if DB connection fails

if "nl2sql_chain" not in st.session_state:
    try:
        st.session_state.nl2sql_chain = NL2SQLChainManager(st.session_state.langchain_sql_db)
        logger.info("NL2SQLChainManager initialized in session state.")
    except Exception as e:
        st.error(f"Failed to initialize the NL2SQL chain: {e}")
        logger.critical(f"Failed to initialize NL2SQLChainManager: {e}", exc_info=True)
        st.stop() # Stop the app if LLM chain fails

if "messages" not in st.session_state:
    st.session_state.messages = []
    logger.info("Chat history initialized in session state.")

# --- Display Chat Messages ---
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# --- User Input and Processing ---
if prompt := st.chat_input("Ask a question about your database..."):
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Pass the current query and the full chat history to the NL2SQLChainManager
                # We slice the history to exclude the *current* user prompt, as it's already handled
                # by the 'question' input to the chain. The chat_history should contain previous turns.
                # Limit chat_history to the last 10 messages (5 user, 5 AI) for context
                context_history = st.session_state.messages[:-1] # Exclude current HumanMessage
                if len(context_history) > 10: # Keep only the last 10 messages (5 pairs)
                    context_history = context_history[-10:]

                response = st.session_state.nl2sql_chain.process_query(
                    natural_language_query=prompt,
                    chat_history=context_history
                )
                st.markdown(response)
                st.session_state.messages.append(AIMessage(content=response))

                # After appending the new AI message, ensure total history length is limited
                # This ensures we always keep the last 5 user messages and their 5 AI responses
                if len(st.session_state.messages) > 10:
                    st.session_state.messages = st.session_state.messages[-10:]
                    logger.info("Chat history truncated to last 10 messages (5 pairs).")

            except Exception as e:
                error_message = f"An error occurred while processing your request. Please try again. Error: {e}"
                st.error(error_message)
                logger.error(f"Error during Streamlit query processing: {e}", exc_info=True)
                st.session_state.messages.append(AIMessage(content="Sorry, I encountered an error. Please check the logs."))
                # Ensure history is still limited even on error
                if len(st.session_state.messages) > 10:
                    st.session_state.messages = st.session_state.messages[-10:]


# --- Clear History Button (Optional) ---
if st.button("Clear Chat History"):
    st.session_state.messages = []
    logger.info("Chat history cleared.")
    st.rerun() # Rerun the app to clear the displayed messages
