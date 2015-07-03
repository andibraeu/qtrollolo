#!/usr/bin/python3

import json
import jsonschema
from trolly.client import Client
from trolly.organisation import Organisation
from trolly.board import Board
from trolly.list import List
from trolly.card import Card
from trolly.checklist import Checklist
from trolly.member import Member
from trolly import ResourceUnavailable
import os.path
import urllib
from optparse import OptionParser

#log helper function
def log(logLevel, message):
    if logLevel <= options.logLevel:
        print("Message from engine room (level " + str(logLevel) + "): " + message)

def validate_options(specs, instance):
  validation_result = {}
  status_text = ''
  status = ''
  text_result = ''
  try:
    validator = jsonschema.validators.validator_for(specs) 
    validator.check_schema(specs)
    v = validator(specs)
    result = v.iter_errors(instance)
    has_error = False
    for error in sorted(result,key=str):
      if not has_error:
        text_result = '<ul>'
      has_error = True
      text_result = '%s<li>Error in %s: %s</li>' % (text_result, '->'.join(str(path) for path in error.path), error.message)
    if has_error:
      text_result = '%s</ul>' % (text_result)
      status = 'invalid'
      status_text = 'Invalid'
    else:
      status = 'valid'
      status_text = 'Valid'
    validation_result['status_text'] = status_text
    validation_result['status'] = status
    validation_result['result'] = text_result
    return validation_result

  except KeyError as e:
    print('Invalid or unknown API version %s: %s' % (api_content['api'], url))


#read some command line arguments
usage = "usage: %prog -c <config file> -o <output file>"
parser = OptionParser(usage = usage)
parser.add_option("-l", "--loglevel", dest="logLevel", default=1, type=int, help="define loglevel")
parser.add_option("-c", "--config", dest="config", action="store", help="path to your config json file")
parser.add_option("-o", "--output", dest="output", default="results.json", action="store", help="where the result is saved")
(options, args) = parser.parse_args()

if not options.config:
    parser.error("config option is missing")

try:
    configFile = open(options.config, "r").read()
    configSpecs = open("options.schema.json").read()
    specs = json.loads(configSpecs)
    config = json.loads(configFile)
    configstatus = validate_options(specs, config)
except IOError as e:
    log(0, "error opening config file " +str(e))
    exit(1)

if not configstatus['status'] == "valid":
    log(0, "error, config not valid: " + str(configstatus))

defaultCardFields = config['fields']
lists = config['lists']

trello = Client(config['apikey'], config['token'])

result = {}

for list in lists:
    if 'cardFields' in list:
        cardFields = list['cardFields']
    else:
        cardFields = defaultCardFields

    cardParams = {}
    listResult = {}
    myList = trello.get_list(list['id'])
    myListInfo = myList.get_list_information()
    listResult['id'] = list['id']
    listResult['cards'] = []
    cardParams['fields'] = ",".join(cardFields)
    cards = myList.get_cards()
    for card in cards:
        cardInfo = card.get_card_information(cardParams)
        listResult['cards'].append(cardInfo)
    result[myListInfo['name']] = listResult

log(3, "our result: " + json.dumps(result,indent=4,ensure_ascii=False))
#write summary to bin directory
try:
    f = open(options.output, "w")
    try:
        f.write(str(json.dumps(result, indent=4, ensure_ascii=False)))
    finally:
        f.close()
except IOError:
    pass
