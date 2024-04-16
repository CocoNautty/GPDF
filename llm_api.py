import os; os.environ['no_proxy'] = '*'
import requests

class llm_api(object):
    def __init__(self, api_key, proxy, base_url, model, temperature):
        self.api_key = api_key
        self.proxy = proxy
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.messages = []
    
    def request_llm(self):
        response = requests.post(self.base_url, 
                                proxies = self.proxy, 
                                headers={'Authorization': 'Bearer ' + self.api_key}, 
                                json={"model": self.model, 
                                    "messages": self.messages, 
                                    "temperature": self.temperature,
                                    "stream": False})
        if response is None:
            for retries in range(0, 3):
                print("Didn't get response, retrying...[" + retries + "/3]")
                response = requests.post(self.base_url, 
                                        proxies = self.proxy, 
                                        headers={'Authorization': 'Bearer ' + self.api_key}, 
                                        json={"model": self.model, 
                                            "messages": self.messages, 
                                            "temperature": self.temperature,
                                            "stream": False})
                if response is not None:
                    break
        if 'choices' in response.json():
            response = response.json().get('choices')[0]["message"]["content"]
        else:
            response = response.json()["message"]["content"]
        return response

    def send(self, prompt, material, system_message=None):
        if system_message is None:
            system_message = "You are a profession in the field of global engineering ethics. Try your best to answer my questions or help with my problems. Note that the materials may not be complete. Try your best."
        self.messages.append({"role":"system","content":system_message})
        self.messages.append({"role":"user","content":prompt + "The following materials may be helpful: " + material})
        self.messages.append({"role":"assistant","content":"keep it short"})
        response = self.request_llm()
        self.messages = []

        return response


if __name__ == '__main__':
    api_key='sk-8m4SzjD6Nobff6l6pGN6KFsoD2xfx6pKsWjyLTqfjPp69vzh'
    proxy = None
    base_url = 'https://api.chatanywhere.com.cn/v1/chat/completions'
    model = "gpt-3.5-turbo"
    temperature = 0.7

    api_obj = llm_api(api_key, proxy, base_url, model, temperature)

    prompt = "what is the definition of ethics?"
    material = "6  Global Engineering Ethics\n1.2 WHAT IS ETHICS?\nHere the terms “ethics” and “morality” will be used interchangeably. A variety \nof different ways of defining these terms are in common use, but many of them rely on technical differences in interpretations. The definition proposed for use in this text is that ethics is about actions that have the potential to seriously im -\npact the lives of others.  The meaning of the word “serious” is, of course, vague \nbut will be clarified in subject matter analysis.\nIt should be noted that, for the purposes of this text, ethics concerns human \nbeings, although significant discussion exists about whether or not that should be its limit. For example, some people have argued that animals should have moral rights, based on their capacity to suffer. Our limitation does not mean, of course, that either animals or the environment should not be discussed ethically, since our actions toward other beings and things often have consequences for the lives of human beings. Here global warming as such, for instance, would not be of ethical interest, but considering that what people do to the environment can seri -\nously harm human beings, it becomes a matter of ethical concern. Many discus -\nsions in ethics also take place regarding who is to be defined as a “person,” but the theoretical ramifications of that issue will not be explored here.\n4\nIt should also be noted that, according to this definition, ethics is concerned \nwith potential effects on others. Some ethical theories have proposed that ethics is about the furtherance of self-interest. As people do not require encourage -\nment to seek out and further their own self-interests, the position here is that there is no need to develop rules about behaviors of this sort—human beings do so quite naturally.\n5 Much of ethics is ultimately about setting restrictions on or \nlimits to behaviors.\nEspecially in the context of a global ethics, it must also be noted that this \ndefinition of ethics is framed in terms of actions. Questions regarding the char -\nacter of individuals, for example, are thus left unresolved. There exist a number of ethical traditions that stress character development or spiritual state of per -\nsons. Neglecting this issue in framing an ethics for engineers is not to indicate that this is an unimportant dimension of ethics but, rather, that it is often not suitably assessed by an outsider.\n6\n4. For discussions of such issues, see Smith (2010). Regarding animal rights and ethics, see Singer \n(1975), Rowlands (2002), and Carruthers (1992). Concerning environmental ethics, see Naess \n(1973), O'Neill (1992), and Jamieson (2001). This issue is taken up further in Chapter\xa011, regarding \nthe nature of rights.\n5. The position that ethics is about the furtherance of self-interest is known as “descriptive” egoism. \nThe position that ethics should be about the furtherance of self-interest is known as “normative” \negoism. For more on descriptive egoism, see Feinberg (1999), Mercer (2001), and Rachels (2003). \nFor an overview of normative egoism, see Shaver (2015).\n6. Stemming from the thought of ancient Greek philosopher Aristotle, ethical questions regarding \nthe character of individuals are included under the broad purview of “virtue” ethics. Concerning re -\ncent psychological and philosophical criticisms of the understanding of moral psychology on which this ethical position is based, see Wilson (2004) and Doris (2005)."

    response = api_obj.send(prompt=prompt, material=material)

    print(response)