import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller
from sensors import sensors
from teacher import CookiesTeacher, CupcakesTeacher, CakesTeacher
from perceptors import perceptors


license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

class ProgrammedSelector(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        if obs['cake_demand'] < obs['completed_cake']:
            action = [2]
        elif obs['cupcake_demand'] < obs['completed_cupcakes']:
            action = [1]
        else:
            action = [0]

        return action

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return [s.name for s in sensors]
        
    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False


def start():
    # delete old history files
    try:
        files = os.listdir(PATH_HISTORY)

        pkl_files = [file for file in files if file.endswith('.pkl')]

        for file in pkl_files:
            file_path = PATH_HISTORY + '/' + file
            os.remove(file_path)
    except:
        pass

    # dt=1 minute, we are running for 8hours=480 mins
    bake_scenarios = [
        {
            "cookies_price": 2,
            "cupcake_price": 5,
            "cake_price": 20,

            "cookies_demand": 30,
            "cupcake_demand": 10,
            "cake_demand": 20

        }
    ]

    cookies_skill = Skill("cookies", CookiesTeacher)
    cupcakes_skill = Skill("cupcakes", CupcakesTeacher)
    cakes_skill = Skill("cakes", CakesTeacher)

    selector_skill = Skill("selector", ProgrammedSelector)
    for scenario_dict in bake_scenarios:
        cookies_skill.add_scenario(Scenario(scenario_dict))
        cupcakes_skill.add_scenario(Scenario(scenario_dict))
        cakes_skill.add_scenario(Scenario(scenario_dict))

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

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)
    #agent.add_perceptors(perceptors)

    agent.add_skill(cookies_skill)
    agent.add_skill(cupcakes_skill)
    agent.add_skill(cakes_skill)
    agent.add_selector_skill(selector_skill, [cookies_skill,cupcakes_skill,cakes_skill], fixed_order=False, fixed_order_repeat=False)

    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    try:
        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        os.mkdir(PATH_CHECKPOINTS)

    runtime.train(agent, train_iters=10)
    
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()

