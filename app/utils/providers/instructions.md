# Creating a New Provider

To add a new provider to the multi1 application, follow these steps:

1. Create a new file in the `app/handlers/` directory named `your_provider_handler.py`.

2. Copy the contents of the `skeleton_provider.py` file into your new handler file.

3. Rename the class to match your provider (e.g., `YourProviderHandler`).

4. Implement the `__init__`, `_make_request`, and `_process_response` methods according to your provider's API requirements.

5. Import your new handler in `app/handlers/__init__.py`.

6. Update the `get_api_handler` function in `app/main.py` to include your new provider.

7. Add the necessary configuration options in `app/config_menu.py`.

8. Update the `README.md` file to include information about the new provider.

Remember to handle API keys, rate limiting, and error responses appropriately for your provider.