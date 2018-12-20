import json
import requests
from lxml import html
from collections import OrderedDict
import argparse
import datetime


def parse(source, destination, date):
    lists = []
    for j in range(30):
        date1 = (datetime.datetime.today() + datetime.timedelta(days=j)).strftime("%m/%d/%Y")
        print (date1)
        try:
            url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(
                source, destination, date1)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
            response = requests.get(url, headers=headers, verify=False)
            parser = html.fromstring(response.text)
            json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
            raw_json = json.loads(json_data_xpath[0] if json_data_xpath else '')
            flight_data = json.loads(raw_json["content"])

            for i in flight_data['legs'].keys():
                exact_price = flight_data['legs'][i].get('price', {}).get('totalPriceAsDecimal', '')
                no_of_stops = flight_data['legs'][i].get("stops", "")
                if no_of_stops == 0:
                    stop = "Nonstop"
                else:
                    continue
                formatted_price = "{0:.2f}".format(exact_price)
                flight_info = {
                    'ticket price': formatted_price,
                    'date': date1,
                    'day': (datetime.datetime.today() + datetime.timedelta(days=j)).strftime("%A")
                }
                lists.append(flight_info)
                break
            sortedlist = sorted(lists, key=lambda k: k['date'], reverse=False)
            if j >= 29:
                print sortedlist
                return sortedlist

        except ValueError:
            print ("Rerying...")

    # print sortedlist
    # return sortedlist


if __name__ == "__main__":
    source = "sea"
    destination = "mia"
    # Todo change dates
    date = "04/01/2019"
    print ("Fetching flight details")
    scraped_data = parse(source, destination, date)
    print ("Writing data to output file")
    with open('%s-%s-flight-results.json' % (source, destination), 'w') as fp:
        json.dump(scraped_data, fp, indent=4)
