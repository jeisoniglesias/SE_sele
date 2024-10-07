import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
chat_history = [
    {
        "role": "system",
        "content": "You are a helpful assistant and respond in Spanish.",
    }
]
while True:
    prompt = input("Enter a prompt: ")
    if prompt == "exit":
        break
    else:

        chat_history.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            stream=True,
        )
        collected_responses = []
        for chunk in response:
            chunk_message = chunk.choices[0].delta
            if chunk_message.content is not None:
                collected_responses.append(chunk_message)
                full_reply_content = "".join(
                    [
                        message.content
                        for message in collected_responses
                        if message.content
                    ]
                )
                print(full_reply_content)
                print("\033[H\033[J", end="")

        chat_history.append({"role": "system", "content": full_reply_content})
        full_reply_content = full_reply_content = "".join(
            [message.content for message in collected_responses if message.content]
        )
        print(f"GPT: {full_reply_content}")

print("Goodbye!")
print(chat_history)
