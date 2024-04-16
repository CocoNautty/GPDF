from openai import OpenAI

client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

class ollm(object):
    def __init__(self, api_key, proxy, base_url, model, temperature):
        self.api_key = api_key
        self.proxy = proxy
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.messages = []
    
    def request_llm(self):
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature
        )
        response = response.choices[0].message.content
        return response

    def send(self, prompt, material, system_message=None):
        if system_message is None:
            system_message = "You are a profession in the field of global engineering ethics. Try your best to answer my questions or help with my problems. Note that the materials may not be complete. Try your best."
        self.messages.append({"role":"system","content":system_message})
        self.messages.append({"role":"user","content":prompt + "The following materials may be helpful: " + material})
        self.messages.append({"role":"assistant","content":"keep it short"})
        # self.messages.append({"role":"user","content":prompt})
        # self.messages.append({"role":"assistant","content":material})
        response = self.request_llm()
        self.messages = []

        return response

# def send(prompt, material, system_message=None):
#     if system_message is None:
#         system_message = "You are a profession in the field of global engineering ethics. Try your best to answer my questions or help with my problems. Note that the materials may not be complete. Try your best."
#     messages = [
#         {"role":"system","content":system_message},
#         {"role":"user","content":prompt + "The following materials may be helpful: " + material},
#         {"role":"assistant","content":"keep it short"}
#     ]
#     response = client.chat.completions.create(
#         model="gemma",
#         messages=messages
#     )
#     return response.choices[0].message.content

# response = client.chat.completions.create(
#   model="gemma",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Who won the world series in 2020?"},
#     {"role": "assistant", "content": "The LA Dodgers won in 2020."},
#     {"role": "user", "content": "Where was it played?"}
#   ]
# )
# print(response.choices[0].message.content)