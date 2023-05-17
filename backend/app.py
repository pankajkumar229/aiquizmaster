from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Use ChatGPT API to generate quiz questions (and answers)
def generate_quiz():
    try:
        headers = {
            'Authorization': 'Bearer INSERT_OPENAI_KEY_HERE', # TODO secrets management - github will close repo if we accidentally send openai api key
            'Content-Type': 'application/json'
        }
        data = {
            'messages': [
                {'role': 'system', 'content': 'You are an educational quiz bot. Given the following context, come up with a question concerning core ideas or details included in the text. Ensure that the question is directly relevant and answerable based solely on information provided in the text'},
                {'role': 'user', 'content': 'Generate a quiz question and answer.'}
            ],
            'max_tokens': 50
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
        response.raise_for_status()

        choices = response.json()['choices']
        question = choices[0]['message']['content']
        answer = choices[1]['message']['content'] if choices[0]['message']['role'] == 'assistant' else choices[0]['message']['content']

        return {'question': question, 'answer': answer}
    except requests.exceptions.RequestException as e:
        print('Failed to generate quiz:', str(e))
        raise e

@app.route('/api/generate-quiz', methods=['POST'])
def handle_generate_quiz():
    try:
        quiz = generate_quiz()
        return jsonify(quiz)
    except Exception as e:
        return jsonify({'error': 'Failed to generate quiz.'}), 500

@app.route('/api/collect-feedback', methods=['POST'])
def handle_collect_feedback():
    # TODO: handle user feedback (just text?)
    return jsonify({'message': 'Feedback received.'})

if __name__ == '__main__':
    app.run(port=3000)
