# GT IEEE Robotics: Agent 2020
This repo is how you make the robot accomplish the block stacking task for Southeastcon 2020. Interfaces2020, Planning2020, Vision2020, and Localization2020 are all libraries used in the agent scripts.

## How to Run

If you don't have a conda environment, first install miniconda, then:
```
$ conda create --name southeastcon2020 PYTHON=3.7.1
$ conda activate southeastcon2020
```
Now clone and visit the `Simulator2020`, `Interfaces2020`, `Vision2020`, `Planning2020` repos in that order, and run the following within each repo.
```
$ pip install -e .
```
Then come back here and run it one last time in this repo.

Remember to activate the env with: `conda activate southeastcon2020`. Now visit the `examples\` to run any of the samples.
