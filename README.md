# Multi-Machine Interval Scheduling


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

### Installing

### Instructions

Run ./jobs_generator.py to generate a job sequence, which would be stored in the corresponding category in job_base with a timestamp as the identifier

Run ./jobs_generator.py --batch --redir [DIR_NAME] to generate a batch of jobs in job_base/[DIR_NAME]

Run ./main to start the scheduling program in interactive mode

Run ./main --help should show you all available usages of the program

Run ./main --experiment [Config File] --jb [JobBase Directory] to start scheduling on all job sequences within JobBase Directory with configurations in Config File 

There are available job sequences in ./job_base and available configuration file in ./testConfigs

## Running the tests

Run ./scheduler_tester.py to do regression testings

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


