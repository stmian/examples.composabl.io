
# @copyright (c) 2024 Composabl & Sami Mian. All Rights Reserved
# 
# @project CSTR Teaching Agent Example
# @file    sensors.py
# @brief   In this file, we define all of the Sensors used by the CSTR teaching agent. 


#=== Imports ===========================================================================================================
from composabl import Sensor

###################################################################################
#  Sensor Definitions
###################################################################################

#Each sensor is created by calling the Sensor() command from the Composabl SDK.
#The format used is as folows:
#
#  <Sensor_Variable_Name> = Sensor("<Sensor_Name>", "")
#
#Where the content in <> is replaced with your chosen variable names

#Each of these sensors is based on the state variables found in the CSTR simulator  
#Please visit this github page for more details: https://github.com/Composabl/examples.composabl.io/tree/main/simulators/cstr

T_StateVariable = Sensor("T", "")
Tc_StateVariable = Sensor("Tc", "")
Ca_StateVariable = Sensor("Ca", "")
Cref_StateVariable = Sensor("Cref", "")
Tref_StateVariable = Sensor("Tref", "")

sensors = [T_StateVariable, Tc_StateVariable, Ca_StateVariable, Cref_StateVariable, Tref_StateVariable] #This is the array of sensors that will be imported into your Agent.py file 

#Print a confirmation of sensors loaded in after this file is run, for debugging use and sanity check
print("Sensor's have been loaded into your agent")