import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors

from composabl_core.grpc.client.client import make
import numpy as np
import math
from gymnasium import spaces
import matplotlib.pyplot as plt

license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"


def start():
    # Define the right configuration
    config = {
        "license": license_key,
        "target": {
            #"docker": {
            #    "image": "composabl/sim-cstr:latest"
            #},
            "local": {
               "address": "localhost:1337"
            }
        },
        "env": {
            "name": "sim-whisky",
        },
        "runtime": {
            "workers": 1
        }
    }

    # Remove unused files from path (mac only)
    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    # Start Runtime
    runtime = Runtime(config)
    directory = PATH_CHECKPOINTS

    # Load the pre trained agent
    agent = Agent.load(directory)

    # Prepare the loaded agent for inference
    trained_agent = runtime.package(agent)
    
    # Create a new Simulation Environment
    print("Creating Environment")
    sim = make(
        "run-benchmark",
        "sim-benchmark",
        "",
        "localhost:1337",
        {
            "render_mode": "rgb_array",
            #"observation_space": _create_observation_space(),
            #"action_space": _create_action_space()
        },
    )

    print("Initializing Environment")
    sim.init()
    print("Resetting Environment")
    obs, info = sim.reset()
    print("Initialized")
    # Get a sim action sample if needed (debug)
    #a = sim.action_space_sample()
    obs_history = []
    action_history = []
    reward_history = []
    sensors_name = [s.name for s in sensors]
    obs_base = {}
    
    for s in sensors_name:
        obs_base[s] = None
    
    for i in range(480):
        # Extract agent actions - Here you can pass the obs (observation state), call the agent.execute() and get the action back
        action = trained_agent.execute(obs)
        #action_history.append(list(action.values()))
        #action = [action]
        #action = sim.action_space_sample()[0]
        print(action)

        obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        obs_history.append(obs)
        #ccok = obs[sensor_names.index('completed_cookies')] if obs[sensor_names.index('completed_cookies')] > 0 else 0
        #ccup = obs[sensor_names.index('completed_cupcakes')] if obs[sensor_names.index('completed_cupcakes')] > 0 else 0
        #ccak = obs[sensor_names.index('completed_cake')] if obs[sensor_names.index('completed_cake')] > 0 else 0
        ccok = obs['completed_cookies']
        ccup = obs['completed_cupcakes']
        ccak = obs['completed_cake']

        observation_dict = {
            0:'sim_time',
            1:'baker_1_time_remaining',
            2:'baker_2_time_remaining',
            3:'baker_3_time_remaining',
            4:'baker_4_time_remaining',
            # EQUIPMENT
            5:'mixer_1_recipe',
            6:'mixer_1_time_remaining',
            7:'mixer_2_recipe',
            8:'mixer_2_time_remaining',
            9:'oven_1_recipe',
            10:'oven_1_time_remaining',
            11:'oven_2_recipe',
            12:'oven_2_time_remaining',
            13:'oven_3_recipe',
            14:'oven_3_time_remaining',
            15:'decorating_station_1_recipe',
            16:'decorating_station_1_time_remaining',
            17:'decorating_station_2_recipe',
            18:'decorating_station_2_time_remaining',
            # DESSERT CASE
            #19:'completed_cookies',
            #20:'completed_cupcakes',
            #21:'completed_cake',
        }
        print(obs[observation_dict[5]],obs[observation_dict[6]])
        print(obs[observation_dict[7]],obs[observation_dict[8]])

        obs, sim_reward, done, terminated, info =  sim.step(action)
        reward_history.append(sim_reward)
        
        #print(ccok, ccup, ccak)
        

        #if done:
        #    break

    print("Closing")
    sim.close()

    plt.figure(2,figsize=(7,5))
    plt.subplot(4,1,1)
    plt.plot([ x["completed_cookies"] for x in obs_history],'k.-',lw=2)
    plt.plot([ x["completed_cupcakes"] for x in obs_history],'b.-',lw=2)
    plt.plot([ x["completed_cake"] for x in obs_history],'r.-',lw=2)
    plt.ylabel('Completed')
    plt.legend(['cookies','cupcakes','cake'],loc='best')
    plt.title('Live Control')

    plt.subplot(4,1,2)
    '''plt.bar(['cookies','cupcakes', 'cakes'], [float(obs_history[-1]["completed_cookies"]), 
                                                float(obs_history[-1]["completed_cupcakes"]), 
                                                float(obs_history[-1]["completed_cake"]) 
                                                ])'''
    plt.plot([ x[observation_dict[5]] for x in obs_history],'k.-',lw=2)
    plt.plot([ x[observation_dict[6]] for x in obs_history],'k.-',lw=2)
    plt.plot([ x[observation_dict[9]] for x in obs_history],'r.-',lw=2)
    plt.plot([ x[observation_dict[10]] for x in obs_history],'r.-',lw=2)
    plt.plot([ x[observation_dict[15]] for x in obs_history],'g.-',lw=2)
    plt.plot([ x[observation_dict[16]] for x in obs_history],'g.-',lw=2)
    plt.ylabel('Completed')
    plt.legend(['cookies','cupcakes','cake', 'completed'],loc='best')

    plt.subplot(4,1,3)
    '''plt.bar(['cookies','cupcakes', 'cakes'], [float(obs_history[-1]["completed_cookies"]) * float(obs_history[-1]["cookies_price"]), 
                                                float(obs_history[-1]["completed_cupcakes"])  * float(obs_history[-1]["cupcake_price"]), 
                                                float(obs_history[-1]["completed_cake"])  * float(obs_history[-1]["cake_price"]) 
                                                ])'''
    '''plt.plot([ x[observation_dict[7]] for x in obs_history],'k.-',lw=2)
    plt.plot([ x[observation_dict[8]] for x in obs_history],'k.-',lw=2)
    plt.plot([ x[observation_dict[11]] for x in obs_history],'r.-',lw=2)
    plt.plot([ x[observation_dict[12]] for x in obs_history],'r.-',lw=2)
    plt.plot([ x[observation_dict[13]] for x in obs_history],'b.-',lw=2)
    plt.plot([ x[observation_dict[14]] for x in obs_history],'b.-',lw=2)
    plt.plot([ x[observation_dict[17]] for x in obs_history],'g.-',lw=2)
    plt.plot([ x[observation_dict[18]] for x in obs_history],'g.-',lw=2)'''
    plt.plot(action_history)
    plt.ylabel('Income')
    plt.legend(['cookie','cupcake','cake'],loc='best')

    plt.subplot(4,1,4)
    plt.plot(reward_history,'k--',lw=2,label=r'$T_{sp}$')
    plt.ylabel('Reward')
    plt.xlabel('Time (min)')
    plt.legend(['Reward'],loc='best')

    plt.show()
    

if __name__ == "__main__":
    start()

