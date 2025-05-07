# Topics for generating code-switching scripts
TOPICS = ["Business", "Everyday Conversation", "Language Education", "Entertainment", "Slang/Neologisms",
          "Travel", "Software Development", "Health & Wellness", "Academic", "Traditional Culture"]

# Level of code-switching (word/phrase/sentence level)
CS_LEVEL = ["word", "phrase", "sentence"]

# Primary language for word/phrase level code-switching
MAJOR_LANG = ["English", "Korean"]

def generate_prompt(topic, cs_level, major_lang):
    """Generate prompt for LLM to create code-switching scripts"""
    if cs_level in ["word", "phrase"]:
        examples = {
            "English": {
                "word": "His favorite food is 김치.",
                "phrase": "I need to 열심히 공부하다 for the exam."
            },
            "Korean": {
                "word": "그의 favorite 음식은 김치예요.",
                "phrase": "시험을 위해 study hard 해야 해요."
            }
        }
        
        prompt = f"""Generate a 1-2 sentence script with {major_lang} as the primary language, 
        incorporating {cs_level}-level code-switching with {"Korean" if major_lang == "English" else "English"}.
        
        Topic: {topic}
        Code-switching level: {cs_level}
        Primary language: {major_lang}
        
        Requirements:
        1. The script should be 1-2 sentences long
        2. The main content should be in {major_lang}
        3. Include {cs_level}-level code-switching from {"Korean" if major_lang == "English" else "English"}
        4. Focus on the {topic} domain
        5. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages
        6. The code-switching should feel organic and commonly used, not forced or artificial
        7. Only use English and Korean - do not mix in other languages like Chinese or Spanish
        
        Example:
        {examples[major_lang][cs_level]}
        """
    else:  # sentence level
        prompt = f"""Generate a 2-sentence script that alternates between English and Korean.
        
        Topic: {topic}
        Code-switching level: sentence
        
        Requirements:
        1. Generate exactly 2 sentences - one in English, one in Korean
        2. The sentences should be related and make sense together
        3. Focus on the {topic} domain
        4. Try to create natural and realistic code-switching that reflects how bilingual speakers actually mix languages
        5. The code-switching should feel organic and commonly used, not forced or artificial
        6. Only use English and Korean - do not mix in other languages like Chinese or Spanish
        
        Example:
        I really want to learn Korean cooking.
        특히 김치찌개 만드는 법을 배우고 싶어요.
        """
    return prompt

import os
import requests

def send_llm_request(prompt):
    """Send request to LiteLLM server and get response"""
    api_key = os.getenv("LITELLM_API_KEY")
    if not api_key:
        raise ValueError("LITELLM_API_KEY environment variable is not set")
        
    try:
        response = requests.post(
            "https://litellm-dev.thetaone-ai.com/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error making request to LiteLLM server: {e}")
        return None

_prompt = generate_prompt(TOPICS[1], CS_LEVEL[0], MAJOR_LANG[1])
response = send_llm_request(_prompt)

import pdb;pdb.set_trace()