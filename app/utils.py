import json
import time
import os

def generate_response(prompt, api_handler):# Get the absolute path to the system_prompt.txt file
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    system_prompt_path = os.path.join(current_dir, 'system_prompt.txt')

    # Load the system prompt from an external file
    try:
        with open(system_prompt_path, 'r') as file:
            SYSTEM_PROMPT = file.read()
    except FileNotFoundError:
        print(f"Error: system_prompt.txt not found at {system_prompt_path}")
        os._exit(-1)

    
    # Initialize the conversation with system prompt, user input, and an initial assistant response
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "Understood. I will now create a detailed reasoning chain following the given instructions, starting with a thorough problem decomposition."},
    ]

    steps = []
    step_count = 1
    total_thinking_time = 0

    # Main loop for generating reasoning steps
    while True:
        # Measure time taken for each API call
        start_time = time.time()
        step_data = api_handler.make_api_call(messages, 300)
        end_time = time.time()
        thinking_time = end_time - start_time
        total_thinking_time += thinking_time

        # Store each step's information
        steps.append((f"Step {step_count}: {step_data['title']}", step_data["content"], thinking_time))

        # Add the assistant's response to the conversation
        messages.append({"role": "assistant", "content": json.dumps(step_data)})
        print("Next reasoning step: ", step_data["next_action"])
        
        # Break the loop if it's the final answer or if step count exceeds 10
        if step_data["next_action"].lower().strip() == "final_answer" or step_count > 10:
            break

        step_count += 1

        # Yield intermediate results
        yield steps, None

    # Request final answer
    messages.append({
        "role": "user",
        "content": "Please provide the final answer based on your reasoning above.",
    })

    # Generate and time the final answer
    start_time = time.time()
    final_data = api_handler.make_api_call(messages, 200, is_final_answer=True)
    end_time = time.time()
    thinking_time = end_time - start_time
    total_thinking_time += thinking_time

    # Add final answer to steps
    steps.append(("Final Answer", final_data["content"], thinking_time))

    # Yield final results
    yield steps, total_thinking_time


def load_env_vars():
    # Load environment variables with default values
    return {
        "OLLAMA_URL": os.getenv("OLLAMA_URL", "http://localhost:11434"),
        "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "llama3.1:70b"),
        "PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY"),
        "PERPLEXITY_MODEL": os.getenv("PERPLEXITY_MODEL", "llama-3.1-sonar-small-128k-online"),
    }
