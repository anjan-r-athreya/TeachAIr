# base_agent.py
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)


class BaseAgent:
    """
    Base agent class for LectureLens project.
    Provides basic interface to send prompts to Gemini API.
    """

    def __init__(self, model: str = "gemini-2.0-flash"):
        self.model = model
        self.client = client

    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the response text.
        """
        try:
            chat = self.client.chats.create(model=self.model)
            response = chat.send_message(prompt)
            return response.text
        except Exception as e:
            print(f"[Error] Failed to get response from Gemini: {e}")
            return ""

    def run_task(self, task_description: str):
        """
        Placeholder for subclasses to implement specific tasks.
        """
        raise NotImplementedError("Subclasses must implement run_task() method.")


# Example usage
if __name__ == "__main__":
    agent = BaseAgent()
    prompt = "Explain how AI can help generate lecture slides efficiently."
    response = agent.send_prompt(prompt)
    print("Gemini response:\n", response)
