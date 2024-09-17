import json
import requests
from api_handlers import BaseHandler

class PerplexityHandler(BaseHandler):
    def __init__(self, api_key, model):
        super().__init__()
        self.api_key = api_key
        self.model = model

    def _clean_messages(self, messages):
        # Clean and consolidate messages for the Perplexity API
        cleaned_messages = []
        last_role = None
        for message in messages:
            if message["role"] == "system":
                cleaned_messages.append(message)
            elif message["role"] != last_role:
                cleaned_messages.append(message)
                last_role = message["role"]
            elif message["role"] == "user":
                cleaned_messages[-1]["content"] += "\n" + message["content"]
        # Remove the last assistant message if present
        if cleaned_messages and cleaned_messages[-1]["role"] == "assistant":
            cleaned_messages.pop()  
        return cleaned_messages

    def _make_request(self, messages, max_tokens):
        # Make a request to the Perplexity API
        cleaned_messages = self._clean_messages(messages)

        url = "https://api.perplexity.ai/chat/completions"
        payload = {"model": self.model, "messages": cleaned_messages}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 400:
                error_message = response.json().get("error", {}).get("message", "Unknown error")
                raise ValueError(f"Bad request (400): {error_message}")
            raise  # Re-raise the exception if it's not a 400 error

    def _process_response(self, response, is_final_answer):
        # Process the Perplexity API response
        try:
            return super()._process_response(response, is_final_answer)
        except json.JSONDecodeError:
            print("Warning: content is not a valid JSON, returning raw response")
            forced_final_answer = '"next_action": "final_answer"' in response.lower().strip()
            return {
                "title": "Raw Response",
                "content": response,
                "next_action": "final_answer" if (is_final_answer or forced_final_answer) else "continue"
            }