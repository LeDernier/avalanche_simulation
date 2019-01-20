# Avalanche Simulation with YADE DEM

Originally a school project at the INP-ENSEEIHT engineering school. The aim was to study the influence of a few parameters on the flow of an avalanche and its impact on a structure.  

![Picture of a simulation.](https://github.com/LeDernier/avalanche_simulation/img/Avalanche.png)

## Getting Started

Clone or download the project and unzip it. Then move to its location with a terminal to get started.

### Prerequisites

You will need YADE DEM to use the code and run the examples : [https://yade-dem.org/doc/](https://yade-dem.org/doc/)
Follow the instructions at the bottom of the website to install it.

## Running the tests

Make sure you are in the same directory as the example1.py file and run the examples using the following commands in your terminal :

```
yade example1.py
python example1PostProcess.py

yade example2.py
python example2PostProcess.py
```

or

```
yadedaily example1.py
python example1PostProcess.py

yadedaily example2.py
python example2PostProcess.py
```

## Using and Extending

The lib folder contains several python files you may want to extend, especially, utils.py and inSimulationUtils.py.

## License

This project is licensed under the Unlicense - see the [LICENSE.md](LICENSE.md) file for details
