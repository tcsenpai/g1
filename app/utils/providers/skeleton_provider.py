from api_handlers import BaseHandler

class SkeletonProviderHandler(BaseHandler):
    def __init__(self, api_key, model):
        super().__init__()
        self.api_key = api_key
        self.model = model

    def _make_request(self, messages, max_tokens):
        # Implement the API request to your provider here
        # Return the raw response from the API
        pass

    def _process_response(self, response, is_final_answer):
        # Process the API response and return a formatted dictionary
        # The dictionary should have 'title', 'content', and 'next_action' keys
        pass