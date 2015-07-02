#!/usr/bin/python3

import json
import jsonschema
import trolly
import os.path
import urllib
from optparse import OptionParser

#log helper function
def log(logLevel, message):
    if logLevel <= 3:
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
