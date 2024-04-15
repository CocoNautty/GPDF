import os; os.environ['no_proxy'] = '*'
import requests

class gpt_api(object):
    def __init__(self, api_key, proxy, base_url, model, temperature):
        self.api_key = api_key
        self.proxy = proxy
        self.base_url = base_url
        self.model = model
        self.temperature = temperature

    def request_gpt(self, messages):
        response = requests.post(self.base_url, 
                                proxies = self.proxy, 
                                headers={'Authorization': 'Bearer ' + self.api_key}, 
                                json={"model": self.model, 
                                    "messages": messages, 
                                    "temperature": self.temperature})
        if response is None:
            for retries in range(0, 3):
                print("Didn't get response, retrying...[" + retries + "/3]")
                response = requests.post(self.base_url, 
                                        proxies = self.proxy, 
                                        headers={'Authorization': 'Bearer ' + self.api_key}, 
                                        json={"model": self.model, 
                                            "messages": messages, 
                                            "temperature": self.temperature})
                if response is not None:
                    break
        response = response.json().get('choices')[0]["message"]["content"]
        return response

# [{"role": "user", "content": "Say this is a test!"}]
if __name__ == '__main__':
    api_key='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'
    proxy = {
        'http': 'socks5h://127.0.0.1:7897',
        'https': 'socks5h://127.0.0.1:7897'
    }
    base_url = 'https://api.openai.com/v1/chat/completions'
    model = "gpt-3.5-turbo"
    temperature = 0.7

    api_obj = gpt_api(api_key, proxy, base_url, model, temperature)

    while(1):
        messages = []
        system_message = "you are an assistant robot trying to answer my questions"
        messages.append({"role":"system","content":system_message})
        message = input("")
        if message == "exit":
            break
        messages.append({"role":"user","content": message})
        response = api_obj.request_gpt(messages)
        print(response)
