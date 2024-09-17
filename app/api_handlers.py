import json
from socket import timeout
from unittest.mock import Base
import os
import requests
import litellm
import re
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

    def make_api_call(self, messages, max_tokens, is_final_answer=False, **kwargs):
        for attempt in range(self.max_attempts):
            try:
                response = self._make_request(messages, max_tokens, **kwargs)
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

class LitellmHandler(BaseHandler):
    def __init__(self, api_key, model):
        super().__init__()
        self.api_key = api_key
        self.model = model


    def _make_request(self, messages, max_tokens, **kwargs):
        try:
            temperature = kwargs.get("temperature", 0.2)
            max_tokens = kwargs.get("max_tokens", 512)
            timeout = kwargs.get('timeout', 30.0)
            response = litellm.completion(messages=messages, model=self.model, max_tokens=max_tokens, temperature=temperature, api_key=self.api_key, timeout=timeout)
            return response.choices[0].message.content
        except Exception as e: 
            raise  # Re-raise the exception if it's not a 400 error

    def _process_response(self, response, is_final_answer):
        try:
            response = str(response).strip()
            if response.startswith('```'):
                response = self._remove_code_blocks(response)
            return super()._process_response(response, is_final_answer)
        except json.JSONDecodeError:
            print("Warning: content is not a valid JSON, returning raw response")
            forced_final_answer = '"next_action": "final_answer"' in response.lower().strip()
            return {
                "title": "Raw Response",
                "content": response,
                "next_action": "final_answer" if (is_final_answer or forced_final_answer) else "continue"
            }
    def _remove_code_blocks(self, text):
        cleaned_text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        cleaned_text = cleaned_text.strip()
        return cleaned_text