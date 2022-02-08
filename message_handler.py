# This script contains function message_handler(message, rates_mem), which evaluate the message received from heartbeat
# script.
# returns a message with currency tranfered to EUR or an error message

import copy
import json
from currency_rate_memory import RateMemory

def message_handler(message, rates_mem):
    """
    The function message_handler(message, rates_mem)
    """
    if message['type'] == 'message':

        # here I will call function to found currency !!!
        try:
            rate = rates_mem.get_rates(message['payload']['date'][:10], message['payload']['currency'])
            out_message = copy.copy(message)
            out_message['payload']['stake'] = round(float(out_message['payload']['stake']) / rate, 5)
            out_message['payload']['currency'] = "EUR"

        except Exception as e:
            print('Currency rate wasn\'t transfered. Error : %s' % e)
            out_message = None

    else:
        out_message = None


    rates_mem.clean_mem()
    return out_message

def error_handler(error):

    out_error = {
        "type": "error",
        "id": 456,
        "message": "Unable to convert stake. Error: %s" % error
    }

    return out_error

if __name__ == '__main__':
    rates_mem = RateMemory()

    with open('one_line.txt', 'r') as f:
        message = json.load(f)

    print(message)
    out_message = message_handler(message, rates_mem)

    print(out_message)

    print(error_handler('Timeout Error'))
