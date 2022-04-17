import re
from ExProcGoogle import epgcon


def process_message(message, response_array, response):
    list_message = re.findall(r"[\w']+|[.,!?;]", message.lower())
    score = 0
    for word in list_message:
        if word in response_array:
            score = score + 1

    return [score, response]


def get_response(message):
    # Sample reponses
    response_list = [
        process_message(message, ["hello", "hi", "hey"], "Hey there!"),
        process_message(message, ["bye", "goodbye"], "Goodbye!"),
        process_message(message, ["how", "are", "you"], "I'm doing fine thanks!"),
        process_message(
            message, ["your", "name"], "My name is Farah's Bot, nice to meet you!"
        ),
        process_message(message, ["help", "me"], "I will do my best to assist you!"),
    ]

    response_scores = []
    for response in response_list:
        response_scores.append(response[0])
    winning_response = max(response_scores)
    matching_response = response_list[response_scores.index(winning_response)]

    if winning_response == 0:
        bot_response = "I didn't understand what you wrote."
    else:
        bot_response = matching_response[1]

    if "soc:lu:" in message:
        name = message.split(":")
        name = name[2]
        note = epgcon.get_contact_info(name)
        bot_response = " " + note
    print("Bot response:", bot_response)
    return bot_response
