from api_handlers import BaseHandler
from litellm import completion

class LiteLLMHandler(BaseHandler):
    def __init__(self, model, api_base=None, api_key=None):
        super().__init__()
        self.model = model
        self.api_base = api_base
        self.api_key = api_key

    def _make_request(self, messages, max_tokens):
        response = completion(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2,
            api_base=self.api_base,
            api_key=self.api_key
        )
        return response.choices[0].message.content

    def _process_response(self, response, is_final_answer):
        return super()._process_response(response, is_final_answer)