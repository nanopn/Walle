__author__ = 'nano'
import wolframalpha
client = wolframalpha.Client('X9LAU5-2TVY285XL2')

def query_wolfram(q):
    res = client.query(q)
    if len(res.pods) > 0:
        texts = ""
        pod = res.pods[1]
        if pod.text:
            texts = pod.text
        else:
            texts = "I have no answer for that"
        # to skip ascii character in case of error
        texts = texts.encode('ascii', 'ignore')
        return texts
    else:
        return "Sorry, I am not sure."


