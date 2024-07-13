import openai
import json
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Set up logging
logging.basicConfig(filename='byte_architect.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def generate_random_project_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def load_knowledge_base():
    knowledge_base = {}
    base_dir = 'knowledge_base'
    for filename in os.listdir(base_dir):
        if filename.endswith('.json'):
            with open(os.path.join(base_dir, filename), 'r') as file:
                service_config = json.load(file)
                knowledge_base[service_config['name']] = service_config
    return knowledge_base

class BYTE:
    def __init__(self, openai_api_key, configurator_url):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key
        self.configurator_url = configurator_url
        self.chat_log = []
        self.knowledge_base = load_knowledge_base()

    def chat_with_user(self, message):
        logging.info(f"User message: {message}")
        self.chat_log.append({"user": message})
        response = openai.Completion.create(
            engine="davinci",
            prompt=message,
            max_tokens=150
        )
        response_text = response.choices[0].text.strip()
        self.chat_log.append({"architect": response_text})
        logging.info(f"AI response: {response_text}")
        return response_text

    def forward_to_configurator(self, requirements):
        project_name = generate_random_project_name()
        services = [self.knowledge_base[req] for req in requirements if req in self.knowledge_base]
        data = {
            "project_name": project_name,
            "services": services,
            "chat_log": self.chat_log
        }
        response = requests.post(f"{self.configurator_url}/configure", json=data)
        return response.json()

app = Flask(__name__)
CORS(app)
byte = BYTE(openai_api_key="your-openai-api-key", configurator_url="http://configurator-service")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = byte.chat_with_user(user_message)
    return jsonify({"response": response})

@app.route('/configure', methods=['POST'])
def configure():
    requirements = request.json.get('requirements')
    result = byte.forward_to_configurator(requirements)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
