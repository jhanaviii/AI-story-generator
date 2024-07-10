from flask import Flask, render_template, request, jsonify
import spacy
from transformers import pipeline, set_seed, GPT2LMHeadModel, GPT2Tokenizer
from datasets import load_dataset
import random
import torch

app = Flask(__name__)

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Load the lm1b dataset
lm1b_dataset = load_dataset('lm1b', split='train')

# Initialize Hugging Face's GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
generator = pipeline('text-generation', model=model, tokenizer=tokenizer, device=torch.cuda.current_device() if torch.cuda.is_available() else -1)

def get_random_lm1b_text():
    random_index = random.randint(0, len(lm1b_dataset) - 1)
    return lm1b_dataset[random_index]['text']

def generate_story(prompt, use_lm1b=False):
    if use_lm1b:
        initial_text = get_random_lm1b_text()
    else:
        initial_text = ""

    combined_prompt = initial_text + "\n" + prompt
    set_seed(42)
    response = generator(combined_prompt, max_length=300, num_return_sequences=1, temperature=0.7, top_p=0.9, pad_token_id=tokenizer.eos_token_id, truncation=True)

    story = response[0]['generated_text'].strip()

    # Ensure the story ends with a complete sentence
    if not story.endswith(('.', '!', '?')):
        sentences = story.split('. ')
        story = '. '.join(sentences[:-1]) + '.'

    return story

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')
    use_lm1b = data.get('use_lm1b', False)
    story = generate_story(prompt, use_lm1b)
    return jsonify({'story': story})

if __name__ == "__main__":
    app.run(debug=True)
