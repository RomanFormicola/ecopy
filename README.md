# ecopy

As of now ecopy is simply an environment set up to train and test various machine learning algorithms.
Currently the environment is made up of automatically generated terrain and with resources which can be distributed
according to settings defined in a JSON file. There is an example JSON file called config.json. To run ecosim with
my configuration file you will first need to install the packages in package-list.tx using Anaconda. Then you can execute
  
    python ecosim.py config.json -animate
  
  The generated terrain will be displayed and the agents positions animated using matplotlib.
