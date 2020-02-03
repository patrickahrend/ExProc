
responses = {"hello":"hey!"}

def messenger(message_text):
    #Higher Level Functions first?

    the_msg = message_text.lower()
    if message_text.lower() == "reboot raspi":
        reboot_raspi()
        return "Rebooting Raspberry Pi Now."
    if the_msg in responses.keys():
        return responses[the_msg]
    else:
        return "Command not recognized."

def reboot_raspi():
    import os
    #os.system('sudo shutdown -r now')
