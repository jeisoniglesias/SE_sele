import os
from openai import OpenAI
import requests


class Asisitente:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def chat(self, messages):

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        return response.choices[0].message.content

    def chatApi(self, messages):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json={"model": "gpt-4o-mini", "messages": messages},
        )
        data = response.json()
        print({"model": "gpt-4o-mini", "messages": messages})
        print(data)
        return data["choices"][0]["message"]["content"]
