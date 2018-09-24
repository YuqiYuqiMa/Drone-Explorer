# Drone Explorer

UAV machine will explore a map and discover objects. 

## Getting Started

### Prerequisites
Install SITL
Preferably use on Linux 
Install QGroundControl 

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

### Start simulator without map
Go to ArduCopter
sim_vehicle.py
### Start QC
cd to Downloads (or wherever your QC locates at)
./QGroundControl.AppImage
### Run our script file
Go to the mission folder
./DroneExplorer.sh

Graph.py 
Change directory that has reports of drone's explorations 

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## File Descriptions
### Arena.py
This file contains Arena class, which contains the map that our agent(UAV) is going to explore
### Board.py
This file contains Threading class, and this file will initiate the board to be explored
### Distribution.py
Contains distribution: exponential, random
### Drone.py
This file controls the drone action
### Graph.py
This file generates corresponding graphs
### Main.py
This file contains main function for the board running in the background
### Parameter.py
get parameters from user
### Policy.py
Contains policies drone will fly including: random, roomba
### Stats.py
This file conmpute and analyze the result that drone collected


## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
