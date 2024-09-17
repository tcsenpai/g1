import json
import time
from abc import ABC, abstractmethod

# Abstract base class for API handlers
class BaseHandler(ABC):
    def __init__(self):
        self.max_attempts = 3  # Maximum number of retry attempts
        self.retry_delay = 1   # Delay between retry attempts in seconds

    @abstractmethod
    def _make_request(self, messages, max_tokens):
        # Abstract method to be implemented by subclasses
        pass

    def make_api_call(self, messages, max_tokens, is_final_answer=False):
        # Attempt to make an API call with retry logic
        for attempt in range(self.max_attempts):
            try:
                response = self._make_request(messages, max_tokens)
                return self._process_response(response, is_final_answer)
            except Exception as e:
                if attempt == self.max_attempts - 1:
                    return self._error_response(str(e), is_final_answer)
                time.sleep(self.retry_delay)

    def _process_response(self, response, is_final_answer):
        # Default response processing (can be overridden by subclasses)
        return json.loads(response)

    def _error_response(self, error_msg, is_final_answer):
        # Generate an error response
        return {
            "title": "Error",
            "content": f"Failed to generate {'final answer' if is_final_answer else 'step'} after {self.max_attempts} attempts. Error: {error_msg}",
            "next_action": "final_answer" if is_final_answer else "continue"
        }

# Import derived handlers
from handlers.ollama_handler import OllamaHandler
from handlers.perplexity_handler import PerplexityHandler
from handlers.groq_handler import GroqHandler