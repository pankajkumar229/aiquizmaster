from flask import Flask, jsonify
import requests
import openai
import os

app = Flask(__name__)

# Set up OpenAI API credentials 
openai.api_key = os.getenv('OPENAI_API_KEY')

# Read the parsed text 
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

# Use ChatGPT API to generate quiz questions (and answers)
# Generate quiz question and answer using OpenAI ChatGPT API
def generate_quiz():
    try:
        text_file_path = 'path/to/your/text/file.txt'
        text = read_text_file(text_file_path)

        response = openai.Completion.create(
            engine='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are an educational quiz bot. Given the following context, come up with a question \
                 concerning core themes, central ideas, or specific details included in the text. Ensure that the question is directly \
                 relevant and answerable based solely on information provided in the text.'},
                {'role': 'user', 'content': 'Generate a quiz question and answer.'},
                {'role': 'assistant', 'content': text}  # Add the text file content as context
            ],
            max_tokens=50
        )

        choices = response['choices']
        question = choices[0]['message']['content']
        answer = choices[1]['message']['content'] if choices[0]['message']['role'] == 'assistant' else choices[0]['message']['content']

        return {'question': question, 'answer': answer}
    except openai.Error as e:
        print('Failed to generate quiz:', str(e))
        raise e

@app.route('/api/generate-quiz', methods=['POST'])
def handle_generate_quiz():
    try:
        quiz = generate_quiz()
        return jsonify(quiz)
    except requests.Exception as e:
        return jsonify({'error': 'Failed to generate quiz.'}), 500

@app.route('/api/collect-feedback', methods=['POST'])
def handle_collect_feedback():
    # TODO: handle user feedback (just text?)
    return jsonify({'message': 'Feedback received.'})

if __name__ == '__main__':
    app.run(port=3000)
