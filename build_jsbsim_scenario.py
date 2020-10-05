#!/usr/bin/env python3

import os
import xml.etree.ElementTree as eT
import sys


# Updates jsbsim scenario xml at build / run time to reduce duplicates and simplify build targets.

def create_scenario_xml(src_path, scenario_template_name, jsb_aircraft_name, scene_name):
    scenario_template_path = str(src_path + '/Tools/jsbsim_bridge/scenario/' + scenario_template_name + '.xml')
    scenario_name = os.path.basename(scenario_template_path).split('.')[-2]
    new_scenario_file = str(os.path.dirname(scenario_template_path) + '/' + jsb_aircraft_name + '.' + scenario_name +
                            '.' + scene_name + '.xml')

    tree = eT.parse(scenario_template_path)
    root = tree.getroot()

    for child in root.iter():
        if child.tag =='runscript':
            child.set('name', str(jsb_aircraft_name + " Testing"))
        if child.tag == 'description':
            child.text = 'THIS IS AN AUTOMATICALLY GENERATED SCRIPT'
        if child.tag == 'use':
            child.set('aircraft', jsb_aircraft_name)
            child.set('initialize', scene_name)
        if child.tag == 'description':
            child.text = 'THIS IS AN AUTOMATICALLY GENERATED SCRIPT'
    tree.write(new_scenario_file)
    print('Created scenario XML ' + new_scenario_file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR, insufficient arguments")
        print("build_jsbsim_scenario.py script generates airframe and scenario specific JSBSim scripts")
        print("Usage <scenario template file> <jsbsim aircraft name> <scene name>")

    elif not os.path.exists(sys.argv[0]):
        print("ERROR, scenario template file does not exist.\n")

    else:
        create_scenario_xml(str(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4])
