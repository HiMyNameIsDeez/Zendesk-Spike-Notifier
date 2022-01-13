# support_volume.py
## This script is designed to be run once an hour
## it counts the Zendesk tickets created over the past hour
## and saves the information to a database
## in the event of a "spike" (abnormally high ticket volume)
## an email is sent to <reporters> 
from datetime import datetime, timedelta
from tqdm import tqdm
import configparser
import logging
import json

print('Before the fall')
config = configparser.ConfigParser()
config.read('../src/auth.ini')
print(config)
print('HHHHHHHHHHHHHHHHHHHHHHHHHH'*5)
print(config['DEFAULT']['Test'])
OUTPUT_FILE = config['DEFAULT']['SpikeDB'].strip('"')
SERVICE_FILE = config['email']['ServiceFile'].strip('"')
DOMAIN = config['zendesk']['Domain'].strip('"')
AUTH = config['zendesk']['Credentials'].strip('"')
SENDER = config['email']['Sender'].strip('"')
RECIPIENT = config['email']['Recipient'].strip('"')

print(OUTPUT_FILE)
exit()


## NOTE: May be a better endpoint than the search API: 
## https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/#count-tickets
def main(logger):
    # load up the database for reading and writing to
    db = None
    # get the current time
    now = None
    # subtract one hour into a second variable
    start = None
    try:
        # perform zendesk search of all tickets between those times
        logger.info('Searching tickets created over the past hour...')
        tickets = timed_search(DOMAIN, AUTH, start, now)
        # return the 'count' of the result and store it in the database
        count = tickets['count']
        logger.info('{} New Tickets.'.format(count))
        # update the database
        db_update(OUTPUT_FILE, db, count)
    except Exception as e:
        logger.exception('{}\nError trying to call the Zendesk search API! '.format(str(e)))
        exit()
    # calculate whether the past hour was a spike
    if calc_spike(db, count):
        logger.warning(' SPIKE DETECTED! ')
        try:
            # if so, get a list of the 10 most frequent tags 
            tags = frequent_tags(tickets)
            # and send out an email notification to the recipient
            send_report(RECIPIENT, tags)
            logger.info('Spike report emailed to <{}>.'.format(RECIPIENT))
        except Exception as e:
            logger.exception('{}\nError trying to send an email report! '.format(str(e)))
            exit()
    return count

# takes a domain, start time, and end time as arguments
# returns a json object
def timed_search(dom, auth, start, finish):
    return tickets

# takes the output filename, database, and count of past hour as arguments
# saves out the updated db to the file
def db_update(file, db, count):
    pass

# takes the database, as well as count of the past hour as arguments
# returns a boolean of whether it qualifies as a spike
def calc_spike(db, count):
    return True

# takes the json output of tickets as an argument
# returns a list of the top 10 tags over the past hour
def frequent_tags(tickets):
    for ticket in tickets:
        for tag in tqdm(ticket['tags']):
            pass
    return tags

# takes the recipient email and frequent tags as arguments
# builds a message and sends it to the recipient
def send_report(to, tags, auth=None):
    pass


if __name__=="__main__":
    # TODO: set logging level based on input
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    main(logger)