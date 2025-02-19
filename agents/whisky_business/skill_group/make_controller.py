from composabl import Controller

import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO
from sensors import sensors


class MakeController(Controller):
    def __init__(self):
        self.total_time = 0 
        self.obs_history = []
 
    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return [s.name for s in sensors]
    
    def compute_action(self, obs):
        self.total_time += 1

        #obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.obs_history.append(obs)
        
        # input: [0,1,2,3]
        step_action_dict = {
            0:"wait",
            1:"Chip_mix_cookies",
            2:"Chip_mix_cupcakes",
            3:"Chip_mix_cakes",
            4:"Coco_mix_cookies",
            5:"Coco_mix_cupcakes",
            6:"Coco_mix_cakes",
            7:"Eclair_mix_cookies",
            8:"Eclair_mix_cupcakes",
            9:"Eclair_mix_cakes",
            10:"Chip_bake_from_Mixer_1",
            11:"Chip_bake_from_Mixer_2",
            12:"Coco_bake_from_Mixer_1",
            13:"Coco_bake_from_Mixer_2",
            14:"Eclair_bake_from_Mixer_1",
            15:"Eclair_bake_from_Mixer_2",
            16:"Chip_decorate_from_Oven_1",
            17:"Chip_decorate_from_Oven_2",
            18:"Chip_decorate_from_Oven_3",
            19:"Eclair_decorate_from_Oven_1",
            20:"Eclair_decorate_from_Oven_2",
            21:"Eclair_decorate_from_Oven_3",
            22:"Reese_decorate_from_Oven_1",
            23:"Reese_decorate_from_Oven_2",
            24:"Reese_decorate_from_Oven_3"
        }
        action = 0 
        # WAIT
        if obs['order_skill'] == 0:
            action = 0
        
        elif obs['order_skill'] == 1:  #cookies
            # MIX
            if obs['baker_1_time_remaining'] == 0: #chip
                action = 1
            elif obs['baker_2_time_remaining'] == 0: #coco
                action = 4
            elif obs['baker_3_time_remaining'] == 0: #eclair
                action = 7

            # BAKE
            if obs['baker_1_time_remaining'] == 0: #chip
                if obs['mixer_1_recipe'] == 1:
                    action = 10
                elif obs['mixer_2_recipe'] == 1:
                    action = 11

            elif obs['baker_2_time_remaining'] == 0: #coco
                if obs['mixer_1_recipe'] == 1:
                    action = 12
                elif obs['mixer_2_recipe'] == 1:
                    action = 13
                    
            elif obs['baker_3_time_remaining'] == 0: #eclair
                if obs['mixer_1_recipe'] == 1:
                    action = 14
                elif obs['mixer_2_recipe'] == 1:
                    action = 15

            # DECORATE
            if obs['baker_1_time_remaining'] == 0: #chip
                if obs['oven_1_recipe'] == 1:
                    action = 16
                elif obs['oven_2_recipe'] == 1:
                    action = 17
                elif obs['oven_3_recipe'] == 1:
                    action = 18
                    
            elif obs['baker_3_time_remaining'] == 0: #eclair
                if obs['oven_1_recipe'] == 1:
                    action = 19
                elif obs['oven_2_recipe'] == 1:
                    action = 20
                elif obs['oven_3_recipe'] == 1:
                    action = 21

            elif obs['baker_4_time_remaining'] == 0: #reesee
                if obs['oven_1_recipe'] == 1:
                    action = 22
                elif obs['oven_2_recipe'] == 1:
                    action = 23
                elif obs['oven_3_recipe'] == 1:
                    action = 24

        return action
    
    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False
    