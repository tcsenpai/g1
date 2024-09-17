import json
import time
import os
from api_handlers import BaseHandler


def generate_response(prompt:str, api_handler:BaseHandler, max_steps:int=5, max_tokens:int=512, temperature:float=0.2, timeout:float = 30.0, sleeptime:float=2.0):
    messages = [
        {
            "role": "system",
            "content": """You are an expert AI assistant that explains your reasoning step by step. For each step, provide a title that describes what you're doing in that step, along with the content. Decide if you need another step or if you're ready to give the final answer. Respond in JSON format with 'title', 'content', and 'next_action' (either 'continue' or 'final_answer') keys. USE AS MANY REASONING STEPS AS POSSIBLE. AT LEAST 3. BE AWARE OF YOUR LIMITATIONS AS AN LLM AND WHAT YOU CAN AND CANNOT DO. IN YOUR REASONING, INCLUDE EXPLORATION OF ALTERNATIVE ANSWERS. CONSIDER YOU MAY BE WRONG, AND IF YOU ARE WRONG IN YOUR REASONING, WHERE IT WOULD BE. FULLY TEST ALL OTHER POSSIBILITIES. YOU CAN BE WRONG. WHEN YOU SAY YOU ARE RE-EXAMINING, ACTUALLY RE-EXAMINE, AND USE ANOTHER APPROACH TO DO SO. DO NOT JUST SAY YOU ARE RE-EXAMINING. USE AT LEAST 3 METHODS TO DERIVE THE ANSWER. USE BEST PRACTICES.""",
        },
        {"role": "user", "content": prompt},
        {
            "role": "assistant",
            "content": "Thank you! I will now think step by step following my instructions, starting at the beginning after decomposing the problem.",
        },
    ]

    steps = []
    step_count = 1
    total_thinking_time = 0

    for _ in range(max_steps):
        time.sleep(sleeptime) # to avoid too many requests error
        start_time = time.time()
        step_data = api_handler.make_api_call(messages, max_tokens=max_tokens, temperature=temperature, timeout=timeout)
        print(step_data)
        end_time = time.time()
        thinking_time = end_time - start_time
        total_thinking_time += thinking_time

        steps.append(
            (
                f"Step {step_count}: {step_data['title']}",
                step_data["content"],
                thinking_time,
            )
        )

        messages.append({"role": "assistant", "content": json.dumps(step_data)})
        print("Next reasoning step: ", step_data["next_action"])
        if step_data["next_action"].lower().strip() == "final_answer":
            break

        step_count += 1

        yield steps, None

    messages.append(
        {
            "role": "user",
            "content": "Please provide the final answer based on your reasoning above.",
        }
    )

    start_time = time.time()
    final_data = api_handler.make_api_call(messages, 200, is_final_answer=True)
    end_time = time.time()
    thinking_time = end_time - start_time
    total_thinking_time += thinking_time

    steps.append(("Final Answer", final_data["content"], thinking_time))

    yield steps, total_thinking_time


def load_env_vars():
    return {
        "MODEL": os.getenv("MODEL", "gemini/gemini-1.5-pro"),
        "MODEL_API_KEY": os.getenv("MODEL_API_KEY"),
    }

