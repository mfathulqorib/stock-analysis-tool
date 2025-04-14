from openai import OpenAI
from pydantic import BaseModel


class PromptManager:
    def __init__(self, client=None, messages=None, model="gpt-4o"):
        self.messages = messages or []
        self.model = model
        self.client = client or OpenAI()

    def add_message(self, role=str, content=str):
        self.messages.append({"role": role, "content": content})

    def generate(self):
        response = self.client.chat.completions.create(
            model=self.model, messages=self.messages
        )

        return response.choices[0].message.content

    def generate_structured(self, schema: BaseModel):
        response = self.client.beta.chat.completions.parse(
            model=self.model, messages=self.messages, response_format=schema
        )

        content = response.choices[0].message.parsed
        data = schema.model_dump(content)
        return data
