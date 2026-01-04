import openai

openai.api_key="your_token"

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=0,
    )

    return response.choices[0].message["content"]

prompt="SQL Optimization Techniques"

response = get_completion(prompt)

print(response)
