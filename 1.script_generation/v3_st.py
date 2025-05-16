import streamlit as st
import json
import os
import requests # Import requests for the actual API call

# Define the path to the prompts file
PROMPTS_FILE = "prompts.json"

# --- Functions for loading and saving prompts ---
def load_prompts(filepath):
    """Loads prompts from a JSON file."""
    if not os.path.exists(filepath):
        st.warning(f"'{filepath}' not found. Creating a new file with default data.")
        # Use the hardcoded data as default if the file doesn't exist
        default_data = {
            "Business": {
                "word": {
                    "English": "Generate a 1-2 sentence script with English as the primary language, \nincorporating word-level code-switching with Korean.\n\nTopic: Business\nCode-switching level: word\nPrimary language: English\n\nRequirements:\n1. The script should be 1-2 sentences long\n2. The main content should be in English\n3. Include word-level code-switching from Korean\n4. Focus on the Business domain\n5. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n6. The code-switching should feel organic and commonly used, not forced or artificial\n7. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\nHis favorite food is 김치.",
                    "Korean": "Generate a 1-2 sentence script with Korean as the primary language, \nincorporating word-level code-switching with English.\n\nTopic: Business\nCode-switching level: word\nPrimary language: Korean\n\nRequirements:\n1. The script should be 1-2 sentences long\n2. The main content should be in Korean\n3. Include word-level code-switching from English\n4. Focus on the Business domain\n5. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n6. The code-switching should feel organic and commonly used, not forced or artificial\n7. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\n그의 favorite 음식은 김치예요."
                },
                "phrase": {
                    "English": "Generate a 1-2 sentence script with English as the primary language, \nincorporating phrase-level code-switching with Korean.\n\nTopic: Business\nCode-switching level: phrase\nPrimary language: English\n\nRequirements:\n1. The script should be 1-2 sentences long\n2. The main content should be in English\n3. Include phrase-level code-switching from Korean\n4. Focus on the Business domain\n5. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n6. The code-switching should feel organic and commonly used, not forced or artificial\n7. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\nI need to 열심히 공부하다 for the exam.",
                    "Korean": "Generate a 1-2 sentence script with Korean as the primary language, \nincorporating phrase-level code-switching with English.\n\nTopic: Business\nCode-switching level: phrase\nPrimary language: Korean\n\nRequirements:\n1. The script should be 1-2 sentences long\n2. The main content should be in Korean\n3. Include phrase-level code-switching from English\n4. Focus on the Business domain\n5. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n6. The code-switching should feel organic and commonly used, not forced or artificial\n7. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\n시험을 위해 study hard 해야 해요."
                },
                "sentence": {
                    "English": "Generate a 2-sentence script that alternates between English and Korean.\n\nTopic: Business\nCode-switching level: sentence\n\nRequirements:\n1. Generate exactly 2 sentences - one in English, one in Korean\n2. The sentences should be related and make sense together\n3. Focus on the Business domain\n4. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n5. The code-switching should feel organic and commonly used, not forced or artificial\n6. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\nI really want to learn Korean cooking.\n특히 김치찌개 만드는 법을 배우고 싶어요.",
                    "Korean": "Generate a 2-sentence script that alternates between English and Korean.\n\nTopic: Business\nCode-switching level: sentence\n\nRequirements:\n1. Generate exactly 2 sentences - one in English, one in Korean\n2. The sentences should be related and make sense together\n3. Focus on the Business domain\n4. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n5. The code-switching should feel organic and commonly used, not forced or artificial\n6. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\nI really want to learn Korean cooking.\n특히 김치찌개 만드는 법을 배우고 싶어요."
                }
            },
            "Everyday Conversation": {
                "word": {
                    "English": "Generate a 1-2 sentence script with English as the primary language, \nincorporating word-level code-switching with Korean.\n\nTopic: Everyday Conversation\nCode-switching level: word\nPrimary language: English\n\nRequirements:\n1. The script should be 1-2 sentences long\n2. The main content should be in English\n3. Include word-level code-switching from Korean\n4. Focus on the Everyday Conversation domain\n5. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n6. The code-switching should feel organic and commonly used, not forced or artificial\n7. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\nHis favorite food is 김치.",
                    "Korean": "Generate a 1-2 sentence script with Korean as the primary language, \nincorporating word-level code-switching with English.\n\nTopic: Everyday Conversation\nCode-switching level: word\nPrimary language: Korean\n\nRequirements:\n1. The script should be 1-2 sentences long\n2. The main content should be in Korean\n3. Include word-level code-switching from English\n4. Focus on the Everyday Conversation domain\n5. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n6. The code-switching should feel organic and commonly used, not forced or artificial\n7. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\n그의 favorite 음식은 김치예요."
                },
                "phrase": {
                    "English": "Generate a 1-2 sentence script with English as the primary language, \nincorporating phrase-level code-switching with Korean.\n\nTopic: Everyday Conversation\nCode-switching level: phrase\nPrimary language: English\n\nRequirements:\n1. The script should be 1-2 sentences long\n2. The main content should be in English\n3. Include phrase-level code-switching from Korean\n4. Focus on the Everyday Conversation domain\n5. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n6. The code-switching should feel organic and commonly used, not forced or artificial\n7. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\nI need to 열심히 공부하다 for the exam.",
                    "Korean": "Generate a 1-2 sentence script with Korean as the primary language, \nincorporating phrase-level code-switching with English.\n\nTopic: Everyday Conversation\nCode-switching level: phrase\nPrimary language: Korean\n\nRequirements:\n1. The script should be 1-2 sentences long\n2. The main content should be in Korean\n3. Include phrase-level code-switching from English\n4. Focus on the Everyday Conversation domain\n5. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n6. The code-switching should feel organic and commonly used, not forced or artificial\n7. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\n시험을 위해 study hard 해야 해요."
                },
                "sentence": {
                    "English": "Generate a 2-sentence script that alternates between English and Korean.\n\nTopic: Everyday Conversation\nCode-switching level: sentence\n\nRequirements:\n1. Generate exactly 2 sentences - one in English, one in Korean\n2. The sentences should be related and make sense together\n3. Focus on the Everyday Conversation domain\n4. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n5. The code-switching should feel organic and commonly used, not forced or artificial\n6. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\nI really want to learn Korean cooking.\n특히 김치찌개 만드는 법을 배우고 싶어요.",
                    "Korean": "Generate a 2-sentence script that alternates between English and Korean.\n\nTopic: Everyday Conversation\nCode-switching level: sentence\n\nRequirements:\n1. Generate exactly 2 sentences - one in English, one in Korean\n2. The sentences should be related and make sense together\n3. Focus on the Everyday Conversation domain\n4. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages\n6. The code-switching should feel organic and commonly used, not forced or artificial\n7. Only use English and Korean - do not mix in other languages like Chinese or Spanish\n\nExample:\nI really want to learn Korean cooking.\n특히 김치찌개 만드는 법을 배우고 싶어요."
                }
            }
        }
        save_prompts(default_data, filepath) # Save the default data to the new file
        return default_data
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from '{filepath}'. Please check the file format.")
        return {}
    except Exception as e:
        st.error(f"Error loading prompts from '{filepath}': {e}")
        return {}

def save_prompts(data, filepath):
    """Saves prompts to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        st.success(f"Prompts saved to '{filepath}'")
    except Exception as e:
        st.error(f"Error saving prompts to '{filepath}': {e}")

# --- Actual send_llm_request function provided by the user ---
def send_llm_request(prompt, temp=0.7, model="gpt-4o-mini"):
    """Send request to LiteLLM server and get response"""
    api_key = os.getenv("LITELLM_API_KEY", "sk-gj7YUNiW7EHVmjoWNwn7")
    if not api_key:
        st.error("LITELLM_API_KEY environment variable is not set")
        return None

    try:
        st.info(f"Sending LLM request to LiteLLM server...\nModel: {model}, Temp: {temp}")
        response = requests.post(
            "https://litellm-dev.thetaone-ai.com/chat/completions", # Ensure this URL is correct and accessible
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temp,
            },
        )
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        st.success("LLM request successful!")
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error making request to LiteLLM server: {e}")
        return None
    except KeyError:
        st.error("Unexpected response format from LiteLLM server.")
        return None


# --- Streamlit App Layout ---
st.title("STT Dataset Prompt Designer")

# Load prompts data at the start
if 'prompts' not in st.session_state:
    st.session_state.prompts = load_prompts(PROMPTS_FILE)

# Handle case where loading failed or file was empty
if not st.session_state.prompts:
     st.error("Could not load or initialize prompts data.")
     st.stop() # Stop the app if data is not available

# Initialize session state for selections if data is loaded
if 'selected_topic' not in st.session_state or st.session_state.selected_topic not in st.session_state.prompts:
    st.session_state.selected_topic = list(st.session_state.prompts.keys())[0]
if 'selected_level' not in st.session_state or st.session_state.selected_level not in st.session_state.prompts[st.session_state.selected_topic]:
    st.session_state.selected_level = list(st.session_state.prompts[st.session_state.selected_topic].keys())[0]
if 'selected_language' not in st.session_state or st.session_state.selected_language not in st.session_state.prompts[st.session_state.selected_topic][st.session_state.selected_level]:
    st.session_state.selected_language = list(st.session_state.prompts[st.session_state.selected_topic][st.session_state.selected_level].keys())[0]


# --- Sidebar for Prompt Selection ---
st.sidebar.header("Select Prompt Category")

# Select Topic
selected_topic = st.sidebar.selectbox(
    "Topic",
    list(st.session_state.prompts.keys()),
    index=list(st.session_state.prompts.keys()).index(st.session_state.selected_topic), # Set initial value
    key='sidebar_topic_select' # Use unique keys for selectboxes
)
st.session_state.selected_topic = selected_topic # Update session state on change

# Select Code-switching Level based on selected Topic
selected_level = st.sidebar.selectbox(
    "Code-switching Level",
    list(st.session_state.prompts[selected_topic].keys()),
    index=list(st.session_state.prompts[selected_topic].keys()).index(st.session_state.selected_level), # Set initial value
    key='sidebar_level_select'
)
st.session_state.selected_level = selected_level # Update session state on change

# Select Primary Language based on selected Topic and Level
selected_language = st.sidebar.selectbox(
    "Primary Language",
    list(st.session_state.prompts[selected_topic][selected_level].keys()),
    index=list(st.session_state.prompts[selected_topic][selected_level].keys()).index(st.session_state.selected_language), # Set initial value
    key='sidebar_language_select'
)
st.session_state.selected_language = selected_language # Update session state on change


# --- Main Area for Prompt Editing and Testing ---
st.header("Edit and Test Prompt")

# Get the current prompt based on selections
current_prompt = st.session_state.prompts[selected_topic][selected_level][selected_language]

# Text area for editing the prompt content
# Initialize the text area with the current prompt when selection changes
edited_prompt_content = st.text_area(
    "Prompt Content",
    current_prompt,
    height=400,
    key=f'prompt_editor_{selected_topic}_{selected_level}_{selected_language}' # Unique key based on selection
)

# --- Actions ---
col1, col2 = st.columns(2)

with col1:
    # Button to update the prompt in the in-memory session state AND save to file
    if st.button("Update and Save Prompt"):
        st.session_state.prompts[selected_topic][selected_level][selected_language] = edited_prompt_content
        save_prompts(st.session_state.prompts, PROMPTS_FILE) # Save to file

with col2:
    # Button to test the prompt using the actual LLM function
    if st.button("Test Prompt"):
        st.subheader("LLM Response")
        # Use the content from the text area for testing
        response = send_llm_request(edited_prompt_content, model="claude-3.7-sonnet") # Call the actual function
        if response:
            st.text(response)
        else:
            st.warning("Could not retrieve LLM response. Check the console for errors or ensure your LiteLLM setup is correct.")

# Optional: Display the current state of the prompts dictionary (for debugging)
# st.subheader("Current Prompts Data (in memory)")
# st.json(st.session_state.prompts)
