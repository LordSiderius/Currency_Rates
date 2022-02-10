# This script contains function message_handler(message, rates_mem), which evaluate the message received from heartbeat
# script.
# returns a message with currency transferred to EUR or an error message

import copy
import json
import random
from currency_rate_memory import RateMemory
import time

def message_handler(message, rates_mem):
    """
    The function message_handler(message, rates_mem) takes message of "type" == "message" and returns value of stake
    converted to EUR if possible.
    Otherwise exception will be risen.
    """

    #check message structure

    if message['type'] == 'message':


        keys = ['type', 'id', 'payload']
        payload_keys = ['marketId', 'selectionId', 'odds', 'stake', 'currency', 'date']

        if not(set(message.keys()).issubset(keys)):
            print('error 1')
            raise Exception('Message structure is not correct. One or more keys are missing')

        elif not(set(payload_keys).issubset(message['payload'])):
            print('error 1')
            raise Exception('Message[\'payload\'] structure is not correct. One or more keys are missing')   #


        try:
            rate = rates_mem.get_rates(message['payload']['date'][:10], message['payload']['currency'])
            out_message = copy.copy(message)
            out_message['payload']['stake'] = round(float(out_message['payload']['stake']) / rate, 5)
            out_message['payload']['currency'] = "EUR"


        except Exception as error:
            out_message = None
            # error_handler(e)
            print('error5: ')
            raise Exception(error)
            # print('Currency rate wasn\'t transferred. Error : %s' % e)

    else:
        out_message = None


    return out_message

def error_handler(error):
    """
        The function error_handler(error) is called, when error message should be send as an output.
        Structure of error mesage is:
        out_error = {
        "type": "error",
        "id": 456,
        "message": "Unable to convert stake. Error: error_string
                    }
        """

    out_error = {
        "type": "error",
        "id": 456,
        "message": "Unable to convert stake. Error: %s" % error
    }

    return out_error


if __name__ == '__main__':
    # DEBUG session for this function
    rates_mem = RateMemory()

    while True:

        path = 'test_messages/mixed_messages.txt'
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

                out_message = error_handler(error)

            print('out message: ' + json.dumps(out_message))
            time.sleep(2)




