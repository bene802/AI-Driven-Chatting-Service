import math
import dateutil.parser
import datetime
import time
import os
import logging
import re
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(event, session_attributes, fulfillment_state, message):
    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName="restaurant_sqs")
    queue.send_message(MessageBody=json.dumps(event))
    
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


""" --- Helper Functions --- """


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def validateEmail(email):

    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False


def validate_request(cuisine, email, date):
    cuisine_types = ['mexican', 'italian', 'american', 'burgers', 'chinese', 'indian', 'korean', 'japanese']
    if cuisine is not None and cuisine.lower() not in cuisine_types:
        return build_validation_result(False,
                                       'cuisine',
                                       'We do not have {}, would you like a different type of cuisine?  '
                                       'Our most popular types are American'.format(cuisine))

    if email is not None:
        if not validateEmail(email):
            return build_validation_result(False, 'email', 'Invalid email format, please enter your email again.')

    if date is not None:
        if not isvalid_date(date):
            return build_validation_result(False, 'date', 'Invalid data format, please enter it again.')
        elif datetime.datetime.strptime(date, '%Y-%m-%d').date() < datetime.date.today():
            return build_validation_result(False, 'date', 'You should choose a day from tomorrow onwards.  please enter it again')

    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def chatsuggest(intent_request):
    cuisine = get_slots(intent_request)["cuisine"]
    location = get_slots(intent_request)["location"]
    diningTime = get_slots(intent_request)["diningTime"]
    numberOfPeople = get_slots(intent_request)["numberOfPeople"]
    email = get_slots(intent_request)["email"]
    date = get_slots(intent_request)["date"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        validation_result = validate_request(cuisine, email, date)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

        return delegate(output_session_attributes, get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return close(intent_request, intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Great, you are all set. We will send you an email with 1 minute. '})


""" --- Intents --- """


def dispatch(intent_request):
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'DiningSuggestionsIntent':
        return chatsuggest(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
