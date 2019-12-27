
responses = {"hello":"hey!"}

def messenger(message_text):
    if message_text.lower() in responses.keys():
        return responses[message_text]
    else:
        return "Command not recognized."