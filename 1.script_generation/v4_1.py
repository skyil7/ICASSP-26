import json
import os
import requests # Import requests for the actual API call
import itertools
import tqdm
import time

# --- Actual send_llm_request function provided by the user ---
def send_llm_request(prompt, temp=0.7, model="gpt-4o-mini"):
    """Send request to LiteLLM server and get response"""
    api_key = os.getenv("LITELLM_API_KEY", "sk-gj7YUNiW7EHVmjoWNwn7")
    if not api_key:
        print("LITELLM_API_KEY environment variable is not set")
        return None

    try:
        print(f"Sending LLM request to LiteLLM server...\nModel: {model}, Temp: {temp}")
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
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except KeyError as e:
        print(f"Key error in response: {e}")
        return None

# Topics for generating code-switching scripts
TOPICS = [
    "Business",
    "Everyday Conversation",
    "Language Education",
    "Entertainment",
    "Slang/Neologisms",
    "Travel",
    "Software Development",
    "Health & Wellness",
    "Academic",
    "Traditional Culture",
]
# Primary language for word/phrase level code-switching
LANGUAGE_SET = [("English", "Korean"), ("Korean", "English")]

MODELS = [
    "gpt-4o-mini",
    "gpt-4.1-nano",
    "gpt-4.1-mini",
    "claude-3.7-sonnet",
]

PROMPT = """
[Role Assignment]
You are an expert scriptwriter tasked with creating a natural {main_language} dialogue script that reflects authentic conversation. 
The dialogue should flow naturally and avoid any awkward or artificial phrasing, while incorporating relevant vocabulary and expressions for the given topic.

[Requirements]
1. **Language:** {main_language}
2. **Topic:** {topic}
3. **Dialogue Length:** Approximately 10-12 turns.
4 **Format:** Please use the speaker's name followed by a colon (:) before their line. (e.g., Sarah: Hi Mark!)

[Output Example]
Sarah: [Dialogue]
Mark: [Dialogue]
...

[Important Notes]
* Use spoken language, not written language.
* Maintain a natural conversational flow.
* Vary sentence length; avoid only short or only long sentences.
* Use natural-sounding expressions and vocabulary that native {main_language} speakers would use.
""".strip()

def generate_dialogue_examples():
    """Generate dialogue examples for each combination of topic, language set, and model"""
    results = []
    
    # Create all possible combinations
    combinations = list(itertools.product(TOPICS, LANGUAGE_SET, MODELS))
    
    # Process each combination
    for topic, language_pair, model in tqdm.tqdm(combinations):
        main_language = language_pair[0]
        
        # Format the prompt with the current combination
        formatted_prompt = PROMPT.format(
            main_language=main_language,
            topic=topic
        )
        
        # Send the request to the LLM
        dialogue = send_llm_request(prompt=formatted_prompt, model=model)
        
        if dialogue:
            # Store the result with metadata
            result = {
                "topic": topic,
                "language_pair": {
                    "main": language_pair[0],
                    "secondary": language_pair[1]
                },
                "model": model,
                "dialogue": dialogue
            }
            results.append(result)
            
            # Add a short delay to avoid rate limiting
            time.sleep(1)
    
    return results

def save_to_json(data, filename="v4_dialogue.json"):
    """Save the generated examples to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} dialogue examples to {filename}")

if __name__ == "__main__":
    print("Generating dialogue examples...")
    examples = generate_dialogue_examples()
    save_to_json(examples)
    print("Done!")

