
# @copyright (c) 2024 Composabl & Sami Mian. All Rights Reserved
# 
# @project CSTR Teaching Agent Example
# @file    scenarios.py
# @brief   In this file, we define the different scenarios for the teaching agent to use in training loops


#=== Imports ===========================================================================================================
from composabl import Scenario

###################################################################################
#  Scenario Definitions
###################################################################################
#Scenario definitions are stored in a Python dicitonary. For each definition, you enter the variables as key:value pairs.
#There are 3 types of variables: Discreet, Continous, and continuous range.
#
#The format used is as folows:
#
# <Scenarios_Variable_Name> = [
#                               { <Configuration_Variable_name> : <Scenario_name> }
#                             ]
#
#Where the content in <> is replaced with your chosen variable names

#Each of these scenarios below is based on the setpoint signals used to control the system found in the CSTR simulator  
#For this example, the Cref_signal is a configuration variable for Concentration and Temperature setpoints
#Please visit this github page for more details: https://docs.composabl.io/building-agents/defining-scenarios.html


ss1_scenarios = [
    {
        "Cref_signal": "ss1"
    }
]

ss2_scenarios = [
    {
        "Cref_signal": "ss2"
    }
]

transition_scenarios = [
    {
        "Cref_signal": "transition"
    }
]

selector_scenarios = [
    {
        "Cref_signal": "complete"
    }
]

#Print a confirmation of scenarios loaded in after this file is run, for debugging use and sanity check
print("Scenarios's have been loaded into your agent")