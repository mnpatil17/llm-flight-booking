import openai
import json
from typing import Dict
from pathlib import Path


def get_llm_response(prompt: str) -> Dict:
    """
    Gets a JSON response from an LLM as a Python dictionary, given a prompt

    :param prompt: The prompt to send to the LLM. This should be a carefully engineered prompt.
    :return: A dictionary representing the JSON response from the LLM.
    """
    set_openai_api_key()

    # Generate a completion using the OpenAI API
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=128
    )

    # Extract the generated text from the API response
    generated_text = response.choices[0].text.strip()
    return json.loads(generated_text)


def replace_handlebars(filename: str, **kwargs) -> str:
    """
    Replaces the handlebars in the given file and returns the full file contents as a string.
    :param filename: A file with handlebars
    :param kwargs: a key-value mapping of handlebar values to replace.
    """
    file = open(filename, 'r')
    text = file.read()
    file.close()

    for key, value in kwargs.items():
        placeholder = "{{" + key + "}}"
        text = text.replace(placeholder, str(value))

    return text


def set_openai_api_key():
    # Define the path to the API key file
    api_key_file = Path.home() / ".tokens" / "openai.token"

    # Read the API key from the file
    with api_key_file.open() as f:
        api_key = f.read().strip()

    # Set up your OpenAI API credentials
    openai.api_key = api_key
