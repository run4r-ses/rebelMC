# Installing rebelMC

## Packaging notice
Most Python projects are packed by using tools to "freeze" the project *(e.g. PyInstaller, Nuitka, cx_freeze)*.

However, rebelMC is *incompatible* with any of these methods due to the way it handles methods and UAC elevation.

A fix is being worked on to ensure that users don't have to install anything to run rebelMC, however an ETA is not available at this time.

## Getting started
To install rebelMC, you need the following:
- Latest Python runtime *(Python 3.8 or higher is required)*, download [here](https://www.python.org/downloads/windows/)
- Git SCM, download [here](https://git-scm.com/download/win)

After installing both, make sure that they're accesible from the command line by running `python --version` and `git --version` respectively.

## Installing package
rebelMC is distributed as a Python package. To install, run this command:

`pip install git+https://github.com/run4r-ses/rebelMC`

Now, rebelMC should be available from the command line as `rebelMC.exe`.
