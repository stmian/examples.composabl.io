# @copyright (c) 2024 Composabl & Sami Mian. All Rights Reserved
# 
# @project CSTR Teaching Agent Example
# @file    skills.py
# @brief   In this file, we create the individual skills for our agent to train        
#
 


#=== Imports ===========================================================================================================
from composabl import Skill, Scenario
from scenarios import ss1_scenarios, ss2_scenarios, transition_scenarios, selector_scenarios    #Here we will import the scenarios we created in the scenarios.py file
from teacher import CSTRTeacher, SS1Teacher, SS2Teacher, TransitionTeacher                      #Here we will import the teacher classses we made in the teacher.py file

###################################################################################
#  Skill Definitions
###################################################################################
#Each skill is created using the Skill() function call from the Composabl SDK
#After the skill object is instantiated, each scenario is added to the skill using a for loop
#
#The format used for Skill Instantiation is as folows:
#
# <Skill_Variable_Name> = Skill(<Skill_Name>, <Skill_Teacher_Name>)
#
#Where the content in <> is replaced with your chosen variable names

#Each of the skills below is based on the control approach used for the CSTR simulator  
#There is 1 skill made for each state of the system (steady state), there is 1 skill for the transition state, and 1 skill for selection which state to focus on
#Please visit this github page for more details: https://docs.composabl.io/building-agents/adding-skills/defining-skills.html

ss1_skill = Skill("ss1", SS1Teacher)
for scenario_dict in ss1_scenarios:
    ss1_skill.add_scenario(Scenario(scenario_dict))

ss2_skill = Skill("ss2", SS2Teacher)
for scenario_dict in ss2_scenarios:
    ss2_skill.add_scenario(Scenario(scenario_dict))

transition_skill = Skill("transition", TransitionTeacher)
for scenario_dict in transition_scenarios:
    transition_skill.add_scenario(Scenario(scenario_dict))

selector_skill = Skill("selector", CSTRTeacher)
for scenario_dict in selector_scenarios:
    selector_skill.add_scenario(Scenario(scenario_dict))

print("Skills have beeen created")