# This script describes a class which keeps the currency rates in the memory

import requests
from datetime import datetime, timedelta
import time


class RateMemory(object):

    def __init__(self):
        self.rates = {}
        self.records_lifespan = 2  # in hours

    def download_rates_by_date(self, date):

        """
        Function download_rates_by_date(date) will check whether the currency rates belonging to given date are already
        in the memory. If not, given day records are added to memory.

        :return:
            None
        """

        if not(date in list(self.rates.keys())):

            url = 'https://api.exchangerate.host/' + date

            try:
                response = requests.get(url, timeout=1)
                data = response.json()
                if data['success'] is False:
                    error_msg = 'Receiving rates for ' + date + ' from server ' + url + ' wasn\'t successful'
                    raise Exception(error_msg)

                else:
                    create_date = datetime.now()
                    self.rates.setdefault(date, [{'created': create_date}, data['rates']])
                    print(date + ' was added to currency rates memory')

            except Exception as error:
                # logging.error(error)
                raise Exception(error)

        else:

            print(date + ' is already in memory')

    def get_rates(self, date, currency):
        """
        Function get_rates(date, currency) will return currency <> EUR rate to given date and currency.
        If given date is not it the memory, than it is automatically downloaded from https://api.exchangerate.host/.

        :return:
            float:
            Currency conversion rates currency -> EUR for given date
        """
        if not(date in list(self.rates.keys())):
            try:
                self.download_rates_by_date(date)
            except Exception as error:
                # logging.error(error)
                raise Exception(error)
                # print('Current rates cannot be downloaded. Error text: %s' % e)

        try:

            rates = self.rates[date][1][currency]

        except Exception as error:
            error_msg = 'Given currency %s is not in the currency rates list' % str(error)
            raise Exception(error_msg)

        return rates

    def clean_mem(self):
        """
        Function clean_mem() clears the records older than x hours from the memory.
        x is set by parameter self.records_lifespan.

        :return:
            None
        """

        list_of_dates = list(self.rates.keys())

        # removes expired currency records
        if (list_of_dates != []) and (self.rates[list_of_dates[0]][0]['created'] +
                                      timedelta(hours=self.records_lifespan) <= datetime.now()):
            self.rates.pop(list_of_dates[0])
            # if any record is expired, function is called again
            self.clean_mem()
            print(list_of_dates[0] + ' was removed from memory')


if __name__ == '__main__':

    # debug session
    cur_rates = RateMemory()
    # cur_rates.records_lifespan = 1/3600
    # cur_rates.download_rates_by_date('2020-04-04')
    time.sleep(2)
    # cur_rates.download_rates_by_date('2019-04-04')
    cur_rates.clean_mem()
    # cur_rates.download_rates_by_date('2020-04-04')
    time.sleep(0.5)
    print(cur_rates.download_rates_by_date('1885-04-04'))
    cur_rates.clean_mem()
    time.sleep(0.7)
    cur_rates.clean_mem()

    print(cur_rates.get_rates('2022-01-13', 'UAH'))
