import os
from composabl import Teacher
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from sensors import sensors

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"


class BaseTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []
        self.action_history = []
        self.colors = []
        self.last_reward = 0
        self.count = 0
        self.metrics = 'none' # standard, fast, none

        # Read metrics db
        try:
            self.df = pd.read_pickle(f"{PATH_HISTORY}/db.pkl")

            if self.metrics == 'fast':
                self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return [s.name for s in sensors]

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)
        
        reward = (float(transformed_obs['completed_cookies'])*(float(transformed_obs['cookies_price'])) \
                  + float(transformed_obs['completed_cupcakes'])*(float(transformed_obs['cupcake_price'])) \
                  + float(transformed_obs['completed_cake'])*(float(transformed_obs['cake_price'])))
        
        reward = sim_reward
    
        self.reward_history.append(reward)
        self.action_history.append(action)

        allowed = float(action * list(transformed_obs.values())[action])

        if allowed == 0:
            allowed = 'NOT ALLOWED'
            color = 'red'
        else:
            allowed = 'ALLOWED'
            color = 'green'

        self.colors.append(color)

        self.count += 1

        # history metrics
        if self.metrics != 'none':
            df_temp = pd.DataFrame(columns=['time', "completed_cookies", "completed_cupcakes","completed_cake" ,'reward'], 
                                   data=[[self.count,float(transformed_obs["completed_cookies"]), float(transformed_obs["completed_cupcakes"]),
                                          float(transformed_obs["completed_cake"]),
                                           reward]])
            self.df = pd.concat([self.df, df_temp])
            self.df.to_pickle(f"{PATH_HISTORY}/db.pkl")

        return reward

    def compute_action_mask(self, transformed_obs, action):
        action_mask = [float(x) for x in list(transformed_obs.values())[:25]]
        return action_mask

    def compute_success_criteria(self, transformed_obs, action):
        if self.obs_history is None:
            success = False
        else:
            success = False
            if self.metrics == 'standard':
                try:
                    self.plot_obs()
                    self.plot_metrics()
                except Exception as e:
                    print('Error: ', e)

        return success

    def compute_termination(self, transformed_obs, action):
        return False

    def plot_metrics(self):
        plt.figure(1, figsize=(7, 5))
        plt.clf()
        plt.subplot(2, 1, 1)
        plt.plot(self.reward_history, 'r.-')
        plt.scatter(self.df.reset_index()['time'], self.df.reset_index()['reward'], s=0.5, alpha=0.2)
        plt.ylabel('Reward')
        plt.legend(['reward'],loc='best')
        plt.title('Metrics')

        plt.subplot(2, 1, 2)
        plt.plot(self.df.reset_index()['time'],self.df.reset_index()["completed_cookies"])
        plt.plot(self.df.reset_index()['time'],self.df.reset_index()["completed_cupcakes"])
        plt.plot(self.df.reset_index()['time'],self.df.reset_index()["completed_cake"])
        plt.ylabel('Completed')
        plt.legend(['cookies','cupcakes','cake'],loc='best')
        plt.xlabel('iteration')

        plt.draw()
        plt.pause(0.001)

    def plot_obs(self):
        plt.figure(2,figsize=(7,5))
        plt.clf()
        plt.subplot(6,1,1)
        plt.plot([ x["completed_cookies"] for x in self.obs_history],'k.-',lw=2)
        plt.plot([ x["completed_cupcakes"] for x in self.obs_history],'b.-',lw=2)
        plt.plot([ x["completed_cake"] for x in self.obs_history],'r.-',lw=2)
        plt.ylabel('Completed')
        plt.legend(['cookies','cupcakes','cake'],loc='best')
        plt.title('Live Control')

        plt.subplot(6,1,2)
        plt.bar(['cookies','cupcakes', 'cakes'], [float(self.obs_history[-1]["completed_cookies"]), 
                                                  float(self.obs_history[-1]["completed_cupcakes"]), 
                                                  float(self.obs_history[-1]["completed_cake"]) 
                                                  ])
        plt.plot([ float(self.obs_history[-1]["cookies_demand"])] * 3,'b--',lw=1)
        plt.plot([ float(self.obs_history[-1]["cupcake_demand"])] * 3,'r--',lw=1)
        plt.plot([ float(self.obs_history[-1]["cake_demand"])] * 3,'g--',lw=1)
        plt.ylabel('Completed')
        plt.legend(['cookies','cupcakes','cake', 'completed'],loc='best')

        plt.subplot(6,1,3)
        plt.bar(['cookies','cupcakes', 'cakes'], [float(self.obs_history[-1]["completed_cookies"]) * float(self.obs_history[-1]["cookies_price"]), 
                                                  float(self.obs_history[-1]["completed_cupcakes"])  * float(self.obs_history[-1]["cupcake_price"]), 
                                                  float(self.obs_history[-1]["completed_cake"])  * float(self.obs_history[-1]["cake_price"]) 
                                                  ])
        plt.ylabel('Income')
        plt.legend(['cookie','cupcake','cake'],loc='best')

        plt.subplot(6,1,4)
        plt.plot(self.reward_history,'k--',lw=2,label=r'$T_{sp}$')
        plt.ylabel('Reward')
        plt.legend(['Reward'],loc='best')

        plt.subplot(6,1,5)
        plt.bar([i for i in range(len(self.action_history))], self.action_history, color=self.colors)
        plt.ylabel('Action')
        plt.legend(['Action'],loc='best')

        plt.subplot(6,1,6)
        plt.plot([ x["baker_1_time_remaining"] for x in self.obs_history],'k.-',lw=2)
        plt.plot([ x["baker_2_time_remaining"] for x in self.obs_history],'b.-',lw=2)
        plt.plot([ x["baker_3_time_remaining"] for x in self.obs_history],'r.-',lw=2)
        plt.plot([ x["baker_4_time_remaining"] for x in self.obs_history],'g.-',lw=2)
        plt.ylabel('Completed')
        plt.legend(['baker1','baker2','baker3', 'baker4'],loc='best')

        plt.xlabel('Time (min)')
        

        plt.draw()
        plt.pause(0.001)




class CookiesTeacher(BaseTeacher):
    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        reward = float(transformed_obs['completed_cookies'])
        self.reward_history.append(reward)

        self.count += 1

        # history metrics
        df_temp = pd.DataFrame(columns=['time', "completed_cookies", "completed_cupcakes","completed_cake" ,'reward'], 
                               data=[[self.count,float(transformed_obs["completed_cookies"]), float(transformed_obs["completed_cupcakes"]),
                                      float(transformed_obs["completed_cake"]),
                                       reward]])
        self.df = pd.concat([self.df, df_temp])
        self.df.to_pickle(f"{PATH_HISTORY}/db.pkl")

        return reward

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        reward = float(transformed_obs['completed_cake'])
        self.reward_history.append(reward)

        self.count += 1

        # history metrics
        df_temp = pd.DataFrame(columns=['time', "completed_cookies", "completed_cupcakes","completed_cake" ,'reward'], 
                               data=[[self.count,float(transformed_obs["completed_cookies"]), float(transformed_obs["completed_cupcakes"]),
                                      float(transformed_obs["completed_cake"]),
                                       reward]])
        self.df = pd.concat([self.df, df_temp])
        self.df.to_pickle(f"{PATH_HISTORY}/db.pkl")

        return reward