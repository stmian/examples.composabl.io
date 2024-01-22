import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller
from teacher import CSTRTeacher, SS1Teacher, SS2Teacher, TransitionTeacher
from sensors import sensors
from skills import ss1_skill, ss2_skill, transition_skill, selector_skill
from cstr.external_sim.sim import CSTREnv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###################################################################################
#  Initial Setup
###################################################################################

#Grab your unique license key from the environment variable
license_key = os.environ["COMPOSABL_LICENSE"] 

#Determine local path files for the History and Checkpoint folders
PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

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
        "name": "sim-cstr:latest",
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

###################################################################################
#  Inference Controller
###################################################################################
class ProgrammedSelector(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        if self.counter < 22:
            action = [0]
        elif self.counter < 74 : #transition
            action = [1]
        else:
            action = [2]

        self.counter += 1

        return action

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    def compute_success_criteria(self, transformed_obs, action):
        if self.counter > 100:
            return True

    def compute_termination(self, transformed_obs, action):
        return False



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
    agent.add_selector_skill(selector_skill, [ss2_skill, transition_skill, ss1_skill], fixed_order=False, fixed_order_repeat=False)

    #load agent
    agent.load(PATH_CHECKPOINTS)

    #save agent
    trained_agent = runtime.package(agent)

    # Inference
    noise = 0.05
    sim = CSTREnv()
    sim.scenario = Scenario({
            "Cref_signal": "complete",
            "noise_percentage": noise
        })
    df = pd.DataFrame()
    obs, info= sim.reset()
    for i in range(90):
        action = trained_agent.execute(obs)
        #action = np.array((action[0]+10)/20)
        obs, reward, done, truncated, info = sim.step(action)
        df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        if done:
            break

    # save inference data
    df.to_pickle(f"{PATH}/checkpoints/inference_data.pkl")

    # plot the results
    plt.figure(figsize=(10,5))
    plt.subplot(3,1,1)
    plt.plot(df.reset_index()['time'],df.reset_index()['Tc'])
    plt.ylabel('Tc')
    plt.legend(['reward'],loc='best')
    plt.title('Agent Inference Multi Skill Program Selector' + f" - Noise: {noise}")

    plt.subplot(3,1,2)
    #plt.plot(self.rms_history, 'r.-')
    plt.plot(df.reset_index()['time'],df.reset_index()['T'])
    plt.plot(df.reset_index()['time'],df.reset_index()['Tref'],'r--')
    plt.ylabel('Temp')
    plt.legend(['T', 'Tref'],loc='best')

    plt.subplot(3,1,3)
    plt.plot(df.reset_index()['time'],df.reset_index()['Ca'])
    plt.plot(df.reset_index()['time'],df.reset_index()['Cref'],'r--')
    plt.legend(['Ca', 'Cref'],loc='best')
    plt.ylabel('Concentration')
    plt.xlabel('iteration')

    plt.savefig(f"{PATH}/checkpoints/inference_figure.png")


if __name__ == "__main__":
    start()
