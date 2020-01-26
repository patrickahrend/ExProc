
responses = {"hello":"hey!"}

def messenger(message_text):
    #Higher Level Functions first?

    if message_text.lower() == "reboot raspi":
        reboot_raspi()
        return "Rebooting Raspberry Pi Now."
    if message_text.lower() in responses.keys():
        return responses[message_text]
    else:
        return "Command not recognized."

def reboot_raspi():
    import os
    os.system('sudo shutdown -r now')
