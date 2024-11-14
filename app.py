from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Hugging Face API Token 
HF_API_TOKEN = "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"

# Inference API endpoint
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

@app.route('/')
def index():
    return render_template('index.html')

# Generate Question
@app.route('/generate_question', methods=['POST'])
def generate_question():
    topic = request.json.get("topic")
    prompt = f"Generate a simple, factual question about {topic}. Provide a clear and concise question."
    response = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        question = response.json()[0]["generated_text"].replace(prompt, "").strip()
        return jsonify({"question": question})
    else:
        return jsonify({"error": "Failed to generate question"}), 500

# Validate Answer
@app.route('/validate_answer', methods=['POST'])
def validate_answer():
    question = request.json.get("question")
    user_answer = request.json.get("user_answer")
    
    prompt = (f"Question: {question}\n"
              f"User's Answer: {user_answer}\n"
              "Evaluate the answer strictly. If it is correct, respond only with 'Correct.' "
              "If it is incorrect, respond only with 'Incorrect.'")

    response = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        feedback = response.json()[0]["generated_text"].strip()
        if feedback.lower() not in ["correct", "incorrect"]:
            # Replace with actual keywords
            correct_keywords = ["expected_keyword1", "expected_keyword2"]  
            if any(keyword.lower() in user_answer.lower() for keyword in correct_keywords):
                feedback = "Correct"
            else:
                feedback = "Incorrect"
        return jsonify({"feedback": feedback})
    else:
        return jsonify({"error": "Failed to validate answer"}), 500

if __name__ == '__main__':
    app.run(debug=True)

    