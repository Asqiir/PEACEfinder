# -*- coding: utf-8 -*-
""" simple fact sample app """

from __future__ import print_function

import random

data = [
    "A year on Mercury is just 88 days long.",
    ("Despite being farther from the Sun, Venus experiences higher "
     "temperatures than Mercury."),
    ("Venus rotates counter-clockwise, possibly because of a collision"
     " in the past with an asteroid."),
    "On Mars, the Sun appears about half the size as it does on Earth.",
    "Earth is the only planet not named after a god.",
    "Jupiter has the shortest day of all the planets.",
    ("The Milky Way galaxy will collide with the Andromeda Galaxy in about"
     " 5 billion years."),
    "The Sun contains 99.86% of the mass in the Solar System.",
    "The Sun is an almost perfect sphere.",
    ("A total solar eclipse can happen once every 1 to 2 years."
     " This makes them a rare event."),
    ("Saturn radiates two and a half times more energy into space"
     " than it receives from the sun."),
    "The temperature inside the Sun can reach 15 million degrees Celsius.",
    "The Moon is moving approximately 3.8 cm away from our planet every year."
]


SKILL_NAME = "PeaceFinder"
GET_FACT_MESSAGE = "Die schönsten Plätze sind: "
HELP_MESSAGE = "Du kannst mich nach schönen Orten fragen, oder du sagst exit... Wie kann ich dir helfen?"
HELP_REPROMPT = "Wie kann ich dir helfen?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "Der Peace Finder kann dir damit nicht helfen.  It can help you discover facts about space if you say tell me a space fact. Wie kann ich dir helfen?"
FALLBACK_REPROMPT = 'Wie kann ich dir helfen?'


zuordnung = {
"südstadt":["der Kringelgraben", "Biestow", "die Mensa"],
"kröpeliner tor vorstadt":["der Lindenpark", "der Ulmencampus"],
"komponistenviertel":["der Botanische Garten", "der Schwanenteich"],
"warnemünde":["der Kurpark", "der Stephan-Jantzen-Park", "die Seepromenade", "der Strand"]
}

def berechne_ort(stadtteil):
    orte = zuordnung.get(stadtteil)
    if orte == None:
        return "Leider habe ich deinen Ort nicht gefunden, probiere es doch mit einem anderen."
    else:
        auflistung = ""
        for i in range (0,len(orte)):
            ist_erster_ort = (i==0)
            ist_letzter_ort = (i==len(orte)-1)
            if ist_erster_ort:
                auflistung = auflistung + ""
            if not ist_erster_ort  and not ist_letzter_ort:
                auflistung = auflistung + ", "
            if ist_letzter_ort:
                auflistung = auflistung + " und "
                
            auflistung = auflistung + orte[i]
        
        return "Die schönsten Orte im Stadtteil "+ stadtteil +" sind " + auflistung + "."


# --------------- App entry point -----------------

def lambda_handler(event, context):
    """  App entry point  """

    #print(event)

    if event['session']['new']:
        on_session_started()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended()

# --------------- Response handlers -----------------

def on_intent(request, session):
    """ called on receipt of an Intent  """

    intent_name = request['intent']['name']
    intent_slot = request['intent']['slots']['district']['value']

    # process the intents
    if intent_name == "GetNewFactIntent":
        return get_fact_response(intent_slot)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    else:
        print("invalid Intent reply with help")
        return get_help_response()

def get_fact_response(district):
    """ get and return a random fact """
    # randomFact = random.choice(data)
 
    
    cardcontent = district
    district = cardcontent
    speechOutput = berechne_ort(district)

    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, True))


def get_help_response():
    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message,
                                                       speech_message, False))
def get_launch_response():
    """ get and return the help string  """

    return get_fact_response()

def get_stop_response():
    """ end the session, user wants to quit the game """

    speech_output = STOP_MESSAGE
    return response(speech_response(speech_output, True))

def get_fallback_response():
    """ end the session, user wants to quit the game """

    speech_output = FALLBACK_MESSAGE
    return response(speech_response(speech_output, False))

def on_session_started():
    """" called when the session starts  """
    #print("on_session_started")

def on_session_ended():
    """ called on session ends """
    #print("on_session_ended")

def on_launch(request):
    """ called on Launch, we reply with a launch message  """

    return get_launch_response()


# --------------- Speech response handlers -----------------

def speech_response(output, endsession):
    """  create a simple json response  """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def dialog_response(endsession):
    """  create a simple json response with card """

    return {
        'version': '1.0',
        'response':{
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ],
            'shouldEndSession': endsession
        }
    }

def speech_response_with_card(title, output, cardcontent, endsession):
    """  create a simple json response with card """

    return {
        'card': {
            'type': 'Simple',
            'title': title,
            'content': cardcontent
        },
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def response_ssml_text_and_prompt(output, endsession, reprompt_text):
    """ create a Ssml response with prompt  """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" +output +"</speak>"
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" +reprompt_text +"</speak>"
            }
        },
        'shouldEndSession': endsession
    }

def speech_response_prompt(output, reprompt_text, endsession):
    """ create a simple json response with a prompt """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': endsession
    }

def response(speech_message):
    """ create a simple json response  """
    return {
        'version': '1.0',
        'response': speech_message
    }

