# This script contains function message_handler(message, rates_mem), which evaluate the message received from heartbeat
# script.
# returns a message with currency transferred to EUR or an error message

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


        except Exception as error:
            out_message = None
            # error_handler(e)
            raise Exception(error)
            # print('Currency rate wasn\'t transferred. Error : %s' % e)

    else:
        out_message = None


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

    with open('input.txt', 'r') as f:
        for i in range(25):
            line = f.readline()
            message = json.loads(line)
            print(message)

            try:

                out_message = message_handler(message, rates_mem)

            except Exception as error:

                out_message = error_handler(error)

            print(out_message)




