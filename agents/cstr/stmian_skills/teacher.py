# @copyright (c) 2024 Composabl & Sami Mian. All Rights Reserved
# 
# @project CSTR Teaching Agent Example
# @file    teacher.py
# @brief   In this file, we create a Teaching class that will be used by the agent.
#          This teaching class allows you to define your goals for the teaching agent,
#          as well as add "Action Masks" in order to set rules that the agent must follow.
#          Teaching objects are generated for each specific skill that the Agent will train and learn.
#          In addition, several plotting functions have been included for metrics & performance tracking.
# @info    https://docs.composabl.io/building-agents/adding-skills/teaching-skills.html


#=== Imports ===========================================================================================================

import os
from composabl import Teacher
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd

#Determine path for History folder for storing training pickle files
PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"

###################################################################################
#  Base Class Definiiton
###################################################################################

class BaseCSTR(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []
        self.rms_history = []
        self.last_reward = 0
        self.count = 0
        self.title = 'CSTR Live Control'
        self.history_path = f"{PATH_HISTORY}/history.pkl"
        self.metrics = 'none' #standard, fast, none

        # Create history folder if it doesn't exist
        if not os.path.exists(PATH_HISTORY):
            os.mkdir(PATH_HISTORY)

        # create metrics db
        try:
            self.df = pd.read_pickle(self.history_path)

            if self.metrics == 'fast':
                self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()



###################################################################################
#  Rules
###################################################################################

# The action mask provides rules at each step about which actions the agent is allowed to take.

    def compute_action_mask(self, transformed_obs, action):
        return None

###################################################################################
#  Goals
###################################################################################
#
#Goals are how the agent improves its performance over a span of training cycles
#Goals are made of three components: the Reward Function, the Termination Function, and the Success Criteria Function
#

    #The reward funciton is the primary feedback mechanism for the agent.
    #Just like in reinforcement learning, the function returns a numerical value that represents the reward signal for the agents most recent performance.
    #Crafting the reward function is an imporant part of designing the teacher. Below is a simple example using the inverse of RMS error as the main reward value.
    #More info can be found here: https://docs.composabl.io/building-agents/adding-skills/teaching-skills.html#compute-reward-function
    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)


        error = (transformed_obs['Cref'] - transformed_obs['Ca'])**2
        self.error_history.append(error)
        rms = math.sqrt(np.mean(self.error_history))    #Calculate the RMS error
        self.rms_history.append(rms)                    
        # minimize rms error
        reward = 1 / rms                                #The larger the error, the smaller the reward. Using a linear reward like this keeps the range of values simple         
        self.reward_history.append(reward)

        self.count += 1

        # history metrics
        df_temp = pd.DataFrame(columns=['time','Ca','Cref','reward','rms'],data=[[self.count,transformed_obs['Ca'], transformed_obs['Cref'], reward, rms]])
        self.df = pd.concat([self.df, df_temp])
        self.df.to_pickle(self.history_path)

        return reward


    #The computer_termination function is used to tell the agent when to terminate the current practrice episode, and start a new one.
    #Usually, this is based on the action of the agent (such as success, failure, or incorrect actions). An example is ending the episode if you drone crashes into the ground.
    #More info can be found here: https://docs.composabl.io/building-agents/adding-skills/teaching-skills.html#compute-termination-function
    def compute_termination(self, transformed_obs, action):
        return False


    #The success criteria function is used to measure skill success, and determine how completely the agent has learned the skill.
    #The output of this function isused to determine when the skill has been fully trained, and the platform can move on to the next skill.
    #For fixed order sequences, this function is used to determine when to move from one skill to the next in the order. 
    #More info can be found here: https://docs.composabl.io/building-agents/adding-skills/teaching-skills.html#compute-success-criteria-function
    def compute_success_criteria(self, transformed_obs, action):
        success = False
        if self.obs_history is None:        #This ensures there is some history of training/observations
            success = False
        else:
            if self.metrics == 'standard':
                try:
                    self.plot_obs()
                    self.plot_metrics()
                except Exception as e:
                    print('Error: ', e)

        return success


###################################################################################
#  Managing Information
###################################################################################

    #This function is used to transform sensor variables, such as conversion or normalization
    #See more: https://docs.composabl.io/building-agents/adding-skills/teaching-skills.html#transforming-sensor-variables
    def transform_obs(self, obs, action):
        return obs

    #This function is used to transform the actions taken by the agent.
    def transform_action(self, transformed_obs, action):
        return action

    #This function is used to filter/minimize the sensor information needed for specific skills 
    def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

###################################################################################
#  Plot Settings for Data Analysis
###################################################################################

    def plot_metrics(self):
        plt.figure(1,figsize=(7,5))
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot(self.reward_history, 'r.-')
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['reward'],s=0.5, alpha=0.2)
        plt.ylabel('Reward')
        plt.legend(['reward'],loc='best')
        plt.title('Metrics')

        plt.subplot(3,1,2)
        plt.plot(self.rms_history, 'r.-')
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['rms'],s=0.5, alpha=0.2)
        plt.ylabel('RMS error')
        plt.legend(['RMS'],loc='best')

        plt.subplot(3,1,3)
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['Ca'],s=0.6, alpha=0.2)
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['Cref'],s=0.6, alpha=0.2)
        plt.ylabel('Ca')
        plt.legend(['Ca'],loc='best')
        plt.xlabel('iteration')

        plt.draw()
        plt.pause(0.001)

    def plot_obs(self):
        plt.figure(2,figsize=(7,5))
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot([ x["Tc"] for x in self.obs_history],'k.-',lw=2)
        plt.ylabel('Cooling Tc (K)')
        plt.legend(['Jacket Temperature'],loc='best')
        plt.title(self.title)


        plt.subplot(3,1,2)
        plt.plot([ x["Ca"] for x in self.obs_history],'b.-',lw=3)
        plt.plot([ x["Cref"] for x in self.obs_history],'k--',lw=2,label=r'$C_{sp}$')
        plt.ylabel('Ca (mol/L)')
        plt.legend(['Reactor Concentration','Concentration Setpoint'],loc='best')

        plt.subplot(3,1,3)
        plt.plot([ x["Tref"] for x in self.obs_history],'k--',lw=2,label=r'$T_{sp}$')
        plt.plot([ x["T"] for x in self.obs_history],'b.-',lw=3,label=r'$T_{meas}$')
        plt.ylabel('T (K)')
        plt.xlabel('Time (min)')
        plt.legend(['Temperature Setpoint','Reactor Temperature'],loc='best')

        plt.draw()
        plt.pause(0.001)


###################################################################################
#  Skill Specific Teachers
###################################################################################
#
#Here, we will create a teacher class for each specific skill we want our Teaching Agent to learn
#For each teacher, we want to keep track of the history of the training. So we create a PICKLE file (*.pkl) to store this information.
#A local folder named "HISTORY" is used to store this information 
#We also want to measaure the progress of the teacher, so we analyze and plot the metrics recorded in each pickle file
###

class SS1Teacher(BaseCSTR):
    def __init__(self):
        super().__init__()
        self.title = 'CSTR Live Control - SS1 skill'
        self.history_path = f"{PATH_HISTORY}/ss1_history.pkl"

        # create metrics db
        try:
            self.df = pd.read_pickle(self.history_path)

            if self.metrics == 'fast':
                self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()


class SS2Teacher(BaseCSTR):
    def __init__(self):
        super().__init__()
        self.title = 'CSTR Live Control - SS2 skill'
        self.history_path = f"{PATH_HISTORY}/ss2_history.pkl"

        # create metrics db
        try:
            self.df = pd.read_pickle(self.history_path)

            if self.metrics == 'fast':
                self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()

class TransitionTeacher(BaseCSTR):
    def __init__(self):
        super().__init__()
        self.title = 'CSTR Live Control - Transition skill'
        self.history_path = f"{PATH_HISTORY}/transition_history.pkl"

        # create metrics db
        try:
            self.df = pd.read_pickle(self.history_path)

            if self.metrics == 'fast':
                self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()

class CSTRTeacher(BaseCSTR):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []
        self.rms_history = []
        self.last_reward = 0
        self.count = 0
        self.title = 'CSTR Live Control - Selector skill'
        self.history_path = f"{PATH_HISTORY}/selector_history.pkl"
        self.plot = False
        self.metrics = 'none' #standard, fast, none

        if self.plot:
            plt.close("all")
            plt.figure(figsize=(7,5))
            plt.title(self.title)
            plt.ion()

        # create metrics db
        try:
            self.df = pd.read_pickle(self.history_path)

            if self.metrics == 'fast':
                self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()


print("Teacher has been loaded into your agent")