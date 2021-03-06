# This script contains:
# Function message_handler(message, rates_mem), which evaluate the message received from heartbeat script.
# Function message error_handler(error-string), which returns error message.

import copy
import json
import random
from currency_rate_memory import RateMemory
import time
from datetime import datetime
import logging


def message_handler(message, rates_mem):
    """
    The function message_handler(message, rates_mem) takes message of "type" == "message" and returns value of stake
    converted to EUR if possible.
    Otherwise exception will be risen.

    :return:
        If message is of type message, than it returns message with stake value converted into EUR.
        Otherwise returns None
    """

    # checks whether the message can be loaded as json and contains key 'type'
    try:
        message = json.loads(message)
        message_type = message['type']

    except Exception as error_msg:
        return error_handler(error_msg)


    # if heartbeat is returned from server heartbeat is returned to consumer_handler() function
    if message_type == 'heartbeat':

        return 'heartbeat'


    # createsd answer for message of 'type' == 'message'
    elif message_type == 'message':

        # checks message structure
        keys = ['type', 'id', 'payload']
        if not (set(message.keys()).issubset(keys)):
            error_msg = 'Message structure is not correct. One or more keys are missing'
            return error_handler(error_msg)
            # raise Exception(error_msg)

        # checks message['payload'] structure
        payload_keys = ['marketId', 'selectionId', 'odds', 'stake', 'currency', 'date']
        if not(set(payload_keys).issubset(message['payload'])):
            error_msg = 'Message[\'payload\'] structure is not correct. One or more keys are missing'
            return error_handler(error_msg)

        # checks if answer message can be created and other stuff
        try:
            # check date format
            datetime.strptime(message['payload']['date'][:10], '%Y-%m-%d')

            # get currency rate for given date an currency
            rate = rates_mem.get_rates(message['payload']['date'][:10], message['payload']['currency'])

            # create out_message and convert stakes into EUR
            out_message = copy.copy(message)
            out_message['payload']['stake'] = round(float(out_message['payload']['stake']) / rate, 5)
            out_message['payload']['currency'] = "EUR"

            return json.dumps(out_message)

        except Exception as error_msg:
            return error_handler(error_msg)

    else:
        error_msg = "Message doesn't contain valid key-value pair 'type': 'message' or 'heartbeat'"
        return error_handler(error_msg)


def error_handler(error_string):
    """
        The function error_handler(error_string) is called, when error message should be send as an output.

        :return:
        Structured error message:
        {
        "type": "error",
        "id": 456,
        "message": "Unable to convert stake. Error: error_string
        }
        """

    out_error = {
        "type": "error",
        "id": 456,
        "message": "Unable to convert stake. Error: %s" % error_string
    }

    return json.dumps(out_error)


if __name__ == '__main__':
    # DEBUG session for this function
    rates_mem = RateMemory()

    while True:

        path = 'test_space/test_messages/mixed_messages.txt'
        with open(path, 'r') as f:
            text = f.readlines()
            size = len(text)
            i = random.randint(0, size - 1)
            print('----------------------------------------------------------------------------------'
                  '----------------------------------------------------------------------------------')
            print('in message: ' + text[i].replace('\n', ''))

            try:
                message = json.loads(text[i])
                out_message = message_handler(message, rates_mem)

            except Exception as error:
                logging.error(error)

                out_message = error_handler(error)

            print('out message: ' + json.dumps(out_message))
            time.sleep(2)
