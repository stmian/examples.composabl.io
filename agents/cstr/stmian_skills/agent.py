# @copyright (c) 2024 Composabl & Sami Mian. All Rights Reserved
# 
# @project CSTR Teaching Agent Example
# @file    agent.py
# @brief   This file is the main file used to create the Teaching Agent for our training example.
#          The structure of this file is broken down into 5 parts: Imports, Settings/configs, 
#         
#
# @info    


#=== Imports ===========================================================================================================
import os, argparse

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from skills import ss1_skill, ss2_skill, transition_skill, selector_skill

###################################################################################
#  Initial Setup
###################################################################################

#Grab your unique license key from the environment variable
license_key = os.environ["COMPOSABL_LICENSE"] 

#Determine local path files for the History and Checkpoint folders
PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

#Initial Variables for Training
WORKERS = 8                 #Default numbers of workers used for SIM training
TRAINING_ITERATIONS =  10   #Default number of training iterations for the agent
SIMULATOR_CHOICE = "docker" #Default simulator choice is to use Docker for CSTR sim. Change this if you always want to use the local sim

###################################################################################
#  Configuration Information
###################################################################################
config = {
    "license": license_key,
    "target": {                 #Default SIM choice is docker. Using the "--local" flag when launching agent.py will change this to the local sim settings
            "docker": {
                "image": "composabl/sim-cstr:latest"
            }
        },
    "env": {
        "name": "sim-cstr",
    },
    "runtime": {
        "ray": {
            "workers": WORKERS      #Number of workers used for training (Default = 8)
        }
    }
}

#Config entry for using local sim
target_local = {
    "target": {
            "local": {
            "address": "localhost:1337"
            }
        }

}

#Config entry for using the docker package (this is used by default)
# target_docker = {
#     "target": {
#             "docker": {
#                 "image": "composabl/sim-cstr:latest"
#             }
#         }
# }

###################################################################################
#  Start Function
###################################################################################

def start():
    #Its important to delete old history files, so we can make space for new ones for this training segment
    #The code below checks the "HISTORY" directory for relevant files, and deletes them if found
    #If this section of code throws issues during runtime, you can comment it out and manually remove any History files
    try:
        files = os.listdir(PATH_HISTORY)

        pkl_files = [file for file in files if file.endswith('.pkl')]
        for file in pkl_files:
            file_path = os.path.join(dir, file)
            os.remove(file_path)
    except:
        pass

    #If user wants to use Local SIM, this will change simulator information in config dict
    if SIMULATOR_CHOICE == "local":
        config.update(target_local)

###################################################################################
#  Agent Creation & Training
###################################################################################

    #First we create a Runtime and Agent object using the Composabl SDK
    runtime = Runtime(config)  
    agent = Agent()             

    #Next we add sensors to the agent. Its best practice to add all sensors at once in a list 
    agent.add_sensors(sensors)

    #Next we add the skills to the agent. Each skill is added as a seperate line.
    agent.add_skill(ss1_skill)
    agent.add_skill(ss2_skill)
    agent.add_skill(transition_skill)
    agent.add_selector_skill(selector_skill, [ss1_skill, transition_skill, ss2_skill], fixed_order=False, fixed_order_repeat=False)

    #Lastly, we train the agent using the .train() call. TRAINING_ITERATIONS is the number of iterations used by the training agent, and defaults to 10
    runtime.train(agent, train_iters=TRAINING_ITERATIONS)
    agent.export(PATH_CHECKPOINTS)

###################################################################################
#  Main Function 
###################################################################################

if __name__ == "__main__":
    #We use argparser in order to catch inputs from the user
    #Currently, the only input is "--local" which is used to set the simulator choice
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--iterations", type=int, default=10)   #Number of iterations, must be an int, default is 10 iterations
    args = parser.parse_args()

    #Check to see if simulator variable needs to be updated based on inputs
    if(args.local):
        SIMULATOR_CHOICE = "local"
        print("Using local sim on port 1337")

    #Check to see if user has provided a custom # of training iterations    
    if(args.iterations):    #This will always be true since a default value is set
                            #Try/Except has been removed due to redundancy
        user_iters = int(args.iterations)          
        if(user_iters) > 0:
            TRAINING_ITERATIONS = user_iters
        else:
            raise ValueError("The number of iterations must be a positive integer value!")      

    #Run the Teaching Agent script
    start()
