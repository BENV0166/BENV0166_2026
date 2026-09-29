import os
from pathlib import Path
import subprocess
import time

from src.idf import modifyIDF
from src.processResults import processHourlyResults, processResilienceResults

def run_energyPlus (ep_dir, baseline_idf_path, weather_file_path, inputs, i, deleteResults = False):
    """
    This function modifies a baseline idf file usisng the modifyIDF function.

    This function creates a unique idf file by using the search and replace method.
    
    The simulation is then run in a temporary folder (iterations/iteration_{i})

    Returns a tuple of the returncode, and dictionaries of the hourly results, and thermal resilience results.

    The deleteResults argument is there to delete csv results and mdd/rdd files once they have been read and no longer needed in order to save disk space.

    """

    # Create the folder which the simulation will run in
    output_path = Path("iterations", f"iteration_{i}")
    #output_path = Path("..", "iterations", f"iteration_{i}") # Turn this on if running from a notebook in a sub-directory.
    Path.mkdir(output_path, exist_ok = True)

    # Create new path to save idf file based on iteration number
    new_idf_path = Path(output_path, f"iteration_{i}.idf")

    # Modify the idf file based on the inputs and save a new idf file
    modifyIDF (baseline_idf_path, new_idf_path, inputs)


    # Prepare the EnergyPlus command for Windows (NT) or Mac/Linux (Posix)
    if os.name == "nt": # Command for Windows users
        ep_path = Path (ep_dir, "energyplus.exe")
        ep_cmd = f'"{ep_path}" {new_idf_path} -w {weather_file_path} -d {output_path}'

    elif os.name == "posix": # Generate command for Mac/Linux Users
        ep_path = Path (ep_dir, "energyplus")
        ep_cmd = f"/{ep_path} {new_idf_path} -w {weather_file_path} -d {output_path}"


    # Run the simulation through a command line call.
    print (f"Beginning EnergyPlus simulation of iteration {i}.", flush = True)
    t0 = time.time()
    retcode = subprocess.run(ep_cmd, shell = True, stdout = subprocess.DEVNULL, stderr=subprocess.STDOUT) 
    t1 = time.time()

    # Check if the simulation completed without any major errors and process the results
    if retcode.returncode == 0:
        print (f"Finished EnergyPlus simulation of iteration {i}. Time of simulation = {t1 - t0:.4f} s.", flush = True)
        # Analyse the results
        hourlyResults = processHourlyResults(Path(output_path, "eplusout.csv"))
        resilienceResults = processResilienceResults(Path(output_path, "eplustbl.csv"))

    else:
        print (f"Error in EnergyPlus simulation of iteration {i}", flush = True)
        # if there is an error, return dummy results
        hourlyResults = None
        resilienceResults = None

    # delete files except for the .err file to save space if this option is set to True
    if deleteResults is True:
        if Path(output_path, f"iteration_{i}.idf").exists():
            Path(output_path, f"iteration_{i}.idf").unlink()
        if Path(output_path, "eplusout.csv").exists():
            Path(output_path, "eplusout.csv").unlink()
        if Path(output_path, "eplustbl.csv").exists():
            Path(output_path, "eplustbl.csv").unlink()
        if Path(output_path, "eplusout.rdd").exists():
            Path(output_path, "eplusout.rdd").unlink()
        if Path(output_path, "eplusout.mdd").exists():
            Path(output_path, "eplusout.mdd").unlink()


    return retcode, hourlyResults, resilienceResults