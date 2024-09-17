import json
import requests
from api_handlers import BaseHandler

class OllamaHandler(BaseHandler):
    def __init__(self, url, model):
        super().__init__()
        self.url = url
        self.model = model

    def _make_request(self, messages, max_tokens):
        # Make a request to the Ollama API
        response = requests.post(
            f"{self.url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "format": "json",
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.2
                }
            }
        )
        response.raise_for_status()
        print(response.json())
        return response.json()["message"]["content"]

    def _process_response(self, response, is_final_answer):
        # Process the Ollama API response
        if isinstance(response, dict) and 'message' in response:
            content = response['message']['content']
        else:
            content = response

        try:
            parsed_content = json.loads(content)
            if 'final_answer' in parsed_content:
                return {
                    "title": "Final Answer",
                    "content": parsed_content['final_answer'],
                    "next_action": "final_answer"
                }
            return parsed_content
        except json.JSONDecodeError:
            return {
                "title": "Raw Response",
                "content": content,
                "next_action": "final_answer" if is_final_answer else "continue"
            }