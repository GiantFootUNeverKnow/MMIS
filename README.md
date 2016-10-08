# Multi-Machine Interval Scheduling


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

### Installing

### Instructions

Run ./jobs_generator.py to generate a job sequence

Run ./main to start the scheduling program in interactive mode

Run ./main --help should show you all available usages 

Run ./main --experiment [Config File] --jb [JobBase directore] to start scheduling on all job sequences within JobBase directory with configurations in Config File 

There are available job sequences in ./job_base and available configuration file in ./TestConfig

## Running the tests

Run ./scheduler_tester.py

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


