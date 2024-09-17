import json
import requests
import groq
import time
from abc import ABC, abstractmethod

class BaseHandler(ABC):
    def __init__(self):
        self.max_attempts = 3
        self.retry_delay = 1

    @abstractmethod
    def _make_request(self, messages, max_tokens):
        pass

    def make_api_call(self, messages, max_tokens, is_final_answer=False):
        for attempt in range(self.max_attempts):
            try:
                response = self._make_request(messages, max_tokens)
                return self._process_response(response, is_final_answer)
            except Exception as e:
                if attempt == self.max_attempts - 1:
                    return self._error_response(str(e), is_final_answer)
                time.sleep(self.retry_delay)

    def _process_response(self, response, is_final_answer):
        return json.loads(response)

    def _error_response(self, error_msg, is_final_answer):
        return {
            "title": "Error",
            "content": f"Failed to generate {'final answer' if is_final_answer else 'step'} after {self.max_attempts} attempts. Error: {error_msg}",
            "next_action": "final_answer" if is_final_answer else "continue"
        }

class OllamaHandler(BaseHandler):
    def __init__(self, url, model):
        super().__init__()
        self.url = url
        self.model = model

    def _make_request(self, messages, max_tokens):
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

class PerplexityHandler(BaseHandler):
    def __init__(self, api_key, model):
        super().__init__()
        self.api_key = api_key
        self.model = model

    def _clean_messages(self, messages):
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
        # If the last message is an assistant message, delete it
        if cleaned_messages and cleaned_messages[-1]["role"] == "assistant":
            cleaned_messages.pop()  
        return cleaned_messages

    def _make_request(self, messages, max_tokens):
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

class GroqHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.client = groq.Groq()

    def _make_request(self, messages, max_tokens):
        response = self.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content