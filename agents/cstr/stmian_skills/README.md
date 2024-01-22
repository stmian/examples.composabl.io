# CSTR Teaching Agent Example
 

## Overview
This repository contains an example agent to get you started with the CSTR (Continuous Stirred Tank Reactor) example.
To learn more about the CSTR, please view the Github [README and introduction to CSTR](https://github.com/Composabl/examples.composabl.io/tree/main/simulators/cstr). Alternatively, you can visit our [official CSTR documentation](https://docs.composabl.io/sample-agents/CSTR.html). 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [References](#references)


## Installation
In order to get your environment setup to use Composable, please review our documentation for [Getting Started](https://docs.composabl.io/getting-started/)

Once you have a proper environment setup, please confirm the Composabl SDK has been installed. 
```bash
composabl version print
```
If you plan on creating a custom simulator, you will need to install the Poetry Python package. 
Poetry can be installed using the following commands:
```bash
# Installing Poetry
curl -sSL https://install.python-poetry.org | python3 -

#You will need to add Poetry to the environment PATH variable
#Detailed instructions can be found [here](https://python-poetry.org/docs/#installing-with-the-official-installer)

# Creating a new poetry project
poetry new my_simulator
cd my_simulator

# Adapt the version of Python to match ~3.8
sed -i.bak 's/\^3.8/~3.8/' pyproject.toml && rm pyproject.toml.bak

# Add the Composabl SDK
poetry add composabl
```


## Usage

Before you can get started using your agent, there are a few setup steps that need to be completed.

First, you need to obtain a Composabl License. Please visit https://composabl.io/ to obtain a license.
Once you have obtained your unique license, you need to export it as a local variable
Alternatively, you can enter the license file directly into yout Agent.py file, if security is not a concern.
```bash
export COMPOSABL_LICENSE="<YOUR_KEY>"
```

### Historian 

The Composabl Agent Historian is a useful tool that logs agent behavior in near real time. It can be used to check the progress of an ongoing training session, and provides useful metrics for training sessions that can be used to audit or debug your agent.

The Historian logs the following information after each agent decision:

- Episode: number that tracks the instance of practicing a scenario
- Iteration: number that counts the agent decisions within an episode
- Skill: skill that was activated to make the agent decision
- Scenario: the scenario being trained
- Sensors: the value of each sensor variable including new sensors created by perceptors
- Actions: each decision action taken by the agent
- Rewards: the reward signal provided to the agent.

Here are the main commands for the historian:
```bash
# Start the historian
composabl historian start

# View the current status of the historian
composabl historian status

# Get the connection string
composabl historian status --moniker-timescaledb

# Clean up th shistorian
composabl historian clean

# Stop the historian
composabl historian stop

```

### Training your Agent

In order to train your agent, you must run the agent.py script

```bash
python main.py
```

There are several optional arguments you can add when you run the agent.py script

The `--local` argument is used to switch the agent to train using a local simulator.
By default the training agednt uses Docker to spin up a simulator instance for training.
```bash
python main.py --local
```

The `--iterations` argument is used to provide a custom number of trainign iterations for each skill
The default value is `10` iterations. The input must be a positive integer value. If a negative number is provided, the default value will be used. If anything other than an Int is passed as the argument, the program will throw an error. 
```bash
python main.py --iterations 100
```
### Benchmarking

In order to benchmark the performance of your agent, a simple benchmarking script has been provided - `agent_inference.py`

```bash
# Run the inference script
python agent_inference.py
```

A Jupyter notebook has also been included that can be used to analyze the training history
`train_history_analytics.ipynb`

## Example Overview

Here is a quick overview of each of the files in this repository, and how they can be used to built your own custom agent.
These exmaple files are built for the CSTR agent example, but can be adapted for use with other use cases and simulators.

### Main.py

This is the main python file used to create and train your teaching agent. 

### Sensors.py

This file is used to define all of the Sensors used by the teaching agent. 

### Scenarios.py

This file is used to define the different scenarios for the teaching agent to use in training loops

### Skills.py

This file is where we define the individual skills our agent will train. 
This file uses the Scenarios generated in `Scenarios.py` to add training scenarios for each skill.

### Teacher.py

This file is where we define how the agent will learn each of the skills.
This includes defining the Goals and Rules for the teaching agent, as well as individual teaching objects for each unique Skill that must be learned. There are also funcitons to store teaching progress and plot metrics, in order to track continuos improvements.


## References

[Composabl Documentation](https://docs.composabl.io/)




