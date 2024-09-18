from api_handlers import BaseHandler
from litellm import completion, set_verbose
from pydantic import BaseModel, Field
import json

class ResponseSchema(BaseModel):
    title: str = Field(..., description="Title of the reasoning step")
    content: str = Field(..., description="Content demonstrating the thought process")
    confidence: int = Field(..., ge=0, le=100, description="Confidence level (0-100)")
    next_action: str = Field(..., description="Either 'continue' or 'final_answer'")

class LiteLLMHandler(BaseHandler):
    def __init__(self, model, api_base=None, api_key=None):
        super().__init__()
        self.model = model
        self.api_base = api_base
        self.api_key = api_key

    def _make_request(self, messages, max_tokens):
        set_verbose=True
        response = completion(
            model=self.model,
            messages=messages,
            response_format= { "type": "json_schema", "json_schema": ResponseSchema.model_json_schema()  , "strict": True },
            max_tokens=max_tokens,
            temperature=0.2,
            api_base=self.api_base,
            api_key=self.api_key,
            stream=False,
        )
    
        # Parse the JSON content from the response
        content = response.choices[0].message.content
        print("\nResponse from LiteLLM:")
        print(content)
        print("===\n")
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Warning: Response is not valid JSON. Formatting raw content.")
            return {
                "title": "Raw Response",
                "content": "Warning: Response is not valid JSON. Formatting raw content.\n\n" + content,
                "confidence": 50,
                "next_action": "continue"
            }

    def _process_response(self, response, is_final_answer):
        # The response is already validated against the schema
        return response