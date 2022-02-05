import copy
import json
from currency_rate_memory import RateMemory

def message_handler(message, rates_mem):

    if message['type'] == 'message':

        # here I will cal function to found currency !!!
        rate = rates_mem.get_rates(message['payload']['date'][:10], message['payload']['currency'])

        out_message = copy.copy(message)
        out_message['payload']['stake'] = round(float(out_message['payload']['stake']) / rate, 5)
        out_message['payload']['currency'] = "EUR"

    elif message['type'] == 'heartbeat':

        out_message = None

    else:

        try:
            error_string = message['message']
        except:
            error_string = "Unknown error"

        out_message = {
                    "type": "error",
                    "id": 456,
                    "message": "Unable to convert stake. Error: %s" % error_string
                    }

    rates_mem.clean_mem()
    return out_message


if __name__ == '__main__':
    rates_mem = RateMemory()

    with open('one_line.txt', 'r') as f:
        message = json.load(f)

    print(message)
    out_message = message_handler(message, rates_mem)

    print(out_message)
