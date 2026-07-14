'''
A script to generate a config.json file, appening landlord details for relevant vocabs
Your config file should already support the vocab, e.g. be in prefixes + have filter: true.
The vocab fields themselves should be empty, this will be filled in by this script.
Takes in two arguments, csv_destination, config_destination, outputs them in the same place.
This script will also happily change addresses as required.
TODO BOROUGHS ARE HARDCODED IN THE JSON, UNLIKE THE OTHERS, CONFIRM WHETHER I SHOULD CHANGE BOROUGHS TO BE CONSISTENT WITH THIS
'''

import csv
import json
import os
import sys
import re


def editConfigJson(csv_destination, config_destination):
    '''
    Reads landlord csv and edits the config file to have landlord support
    '''

    csv_details = os.path.splitext(csv_destination)
    config_details = os.path.splitext(config_destination)
    NEW_CSV_NAME = csv_details[0] + "_edited" + csv_details[1]
    NEW_CONFIG_NAME = config_details[0] + "_edited" + config_details[1]

    with open(csv_destination, newline='') as licence_data, open(config_destination) as config, open(NEW_CSV_NAME, 'w') as new_csv, open(NEW_CONFIG_NAME, 'w') as new_json:
        licence_data_reader = csv.reader(
            licence_data)
        licence_data_writer = csv.writer(
            new_csv)
        unique_licence_holders = {}
        unique_managing_agents = {}

        header = next(licence_data_reader)
        licence_data_writer.writerow(header)

        # A simple vocab mapping from fields to mappings since iterating gives a list
        # TODO Simplify? Probably iterate over a list of filterables.
        LICENCE_HOLDER_INDEX = header.index('licence_holder_name')
        MANAGING_AGENT_INDEX = header.index('managing_agent_name')
        BOROUGH_INDEX = header.index('borough')
        LICENCE_TYPE_INDEX = header.index('licence_type')

        def repl(matchobj):
            if matchobj.group(0).isdigit() and matchobj.start(0) == 0:
                return '_' + matchobj.group(0)
            if matchobj.string == '':  # Vocabs can't be empty
                return 'NA'
            else:
                return '_'

        for address in licence_data_reader:
            address_licence_holder = address[LICENCE_HOLDER_INDEX]
            address_managing_agent = address[MANAGING_AGENT_INDEX]
            address_borough = address[BOROUGH_INDEX]
            address_licence_type = address[LICENCE_TYPE_INDEX]

            wspace_fixed_licence_holder = re.sub(
                r"([\W+\s+])|(^$)|(?=^\d)", repl, address_licence_holder)
            wspace_fixed_managing_agent = re.sub(
                r"([\W+\s+])|(^$)|(?=^\d)", repl, address_managing_agent)
            wspace_fixed_borough = re.sub(
                r"([\W+\s+])|(^$)|(?=^\d)", repl, address_borough)
            wspace_fixed_licence_type = re.sub(
                # HMOs must be replaced
                r"([\W+\s+])|(^$)|(?=^\d)", repl, address_licence_type)

            if address_licence_holder not in unique_licence_holders.values():
                unique_licence_holders[wspace_fixed_licence_holder] = address_licence_holder
            if address_managing_agent not in unique_managing_agents.values():
                unique_managing_agents[wspace_fixed_managing_agent] = address_managing_agent

            # TODO CLEAN THIS
            # We still edit the .csv to make it vocab compatible by replacing spaces with _s
            address[LICENCE_HOLDER_INDEX] = wspace_fixed_licence_holder
            address[MANAGING_AGENT_INDEX] = wspace_fixed_managing_agent
            address[BOROUGH_INDEX] = wspace_fixed_borough
            address[LICENCE_TYPE_INDEX] = wspace_fixed_licence_type
            licence_data_writer.writerow(address)

        config = json.load(config)

        # TODO Probably a cleaner way to do this?
        lic_holder_dict = {"lic_holder": {
            "en": {"title": "Licence Holder"}}}
        lic_holder_dict['lic_holder']['en']['terms'] = unique_licence_holders
        man_agent_dict = {"man_agent": {
            "en": {"title": "Managing Agent"}}}
        man_agent_dict['man_agent']['en']['terms'] = unique_managing_agents
        config['vocabs'].update(lic_holder_dict)
        config['vocabs'].update(man_agent_dict)

        json.dump(config, new_json)


args = sys.argv[1:]
editConfigJson(args[0], args[1])
