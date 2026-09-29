import pandas as pd

def processHourlyResults (filePath):
    """
    Opens the given EnergyPlus results file and extracts the results of interest as a dict.
    """

    results = {}

    df = pd.read_csv(filePath)
    # Convert EnergyPlus' timestamps into a standardized datetime object 
    # Need to include the .str.strip() to remove all leading whitespace otherwise an error can occur.
    df["Date/Time"] = pd.to_datetime(df["Date/Time"].str.strip(), format = "%Y-%m-%dT%H:%M:%S")
    df.set_index("Date/Time", inplace=True)

    # Energy related results
    results["heatingSum"] = df["ZONE 1 IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Supply Air Total Heating Energy [J](Hourly)"].sum()          # Annual heating demand [J]
    results["heatingMax"] = df["ZONE 1 IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Supply Air Total Heating Energy [J](Hourly)"].max() / 3600   # Peak heating demand [W] 
    results["coolingSum"] = df["ZONE 1 IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Supply Air Total Cooling Energy [J](Hourly)"].sum()          # Annual cooling demand [J]
    results["coolingMax"] = df["ZONE 1 IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Supply Air Total Cooling Energy [J](Hourly)"].max() / 3600   # Peak cooling demand [W]
    results["lightingSum"] = df["LIGHTING_ZONE 1:Lights Electricity Energy [J](Hourly)"].sum()              # Annual Lighting electricity usage [J] 
    results["equipmentSum"] = df["ELECTRICEQUIPMENT_ZONE 1:Electric Equipment Electricity Energy [J](Hourly)"].sum()     # Annual equipment usage (will be constant across simulations)
    results["hotWaterSum"] = df["WATER HEATER:Water Heater Heating Energy [J](Hourly)"].sum()            # Annual Hot Water gas usage [J]


    #Overheating related results
    results["temperature>25C"] = df["ZONE 1:Zone Operative Temperature [C](Hourly)"][df["ZONE 1:Zone Operative Temperature [C](Hourly)"] > 25].count() # Hours indoor temperature was greater than 25C [h]
    results["temperature>28C"] = df["ZONE 1:Zone Operative Temperature [C](Hourly)"][df["ZONE 1:Zone Operative Temperature [C](Hourly)"] > 28].count() # Hours indoor temperature was greater than 28C [h]
    results["temperature>30C"] = df["ZONE 1:Zone Operative Temperature [C](Hourly)"][df["ZONE 1:Zone Operative Temperature [C](Hourly)"] > 30].count() # Hours indoor temperature was greater than 30C [h]
    results["temperatureMax"] = df["ZONE 1:Zone Operative Temperature [C](Hourly)"].max() # Peak zone air temperature [C]

    #Illuminance related results
    results["usefulDaylightIlluminance"] = df[(df["DAYLIGHTING CONTROLS_ZONE 1:Daylighting Reference Point 1 Illuminance [lux](Hourly)"] > 100) & (df["DAYLIGHTING CONTROLS_ZONE 1:Daylighting Reference Point 1 Illuminance [lux](Hourly)"] < 2000)].shape[0]

    results["luxHours"] = df["DAYLIGHTING CONTROLS_ZONE 1:Daylighting Reference Point 1 Illuminance [lux](Hourly)"].sum()
    
    """
    # NOTE The monthly sums not being used for the time being.

    # Get monthly sums using resampling
    results["monthlyHeatingSum"] = df.resample(rule ='ME')["ZONE 1 IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Supply Air Total Heating Energy [J](Hourly)"].sum() # Monthly heating demand [J]

    # Get monthly sums using resampling
    results["monthlyCoolingSum"] = df.resample(rule ='ME')["ZONE 1 IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Supply Air Total Cooling Energy [J](Hourly)"].sum() # Monthly cooling demand [J]
    """
    return results


def processResilienceResults (filePath):
    """
    Reads in the results of the annual thermal resilience summary from the eplustbl.csv file

    The format is not conducive to using Pandas_read_csv as there are lots of commas in the headers of the tables.
    Only four of the most relevant metrics are being used, taken from ZONE-1
    * Heat Index Hours
    * Humidex Hours
    * Cooling SET Degree*Hours
    * Heating SET Degree*Hours
    
    """
    resilienceResults = {}

    # Open data as a text file
    with open (filePath, encoding = "UTF-8") as f:
        data = f.readlines()


    # Heat Index
    line = data[12].split(",")

    resilienceResults["HeatIndex:Safe [hr]"] = float(line[2])               # (≤ 26.7°C) [hr]"
    resilienceResults["HeatIndex:Caution [hr]"] = float(line[3])            # (> 26.7°C, ≤ 32.2°C)
    resilienceResults["HeatIndex:Extreme Caution [hr]"] = float(line[4])    #(> 32.2°C, ≤ 39.4°C) 
    resilienceResults["HeatIndex:Danger [hr]"] = float(line[5])             # (> 39.4°C, ≤ 51.7°C) 
    resilienceResults["HeatIndex:Extreme Danger [hr]"] = float(line[6])     # (> 39.4°C, ≤ 51.7°C) 

    # Humidex
    line = data[42].split(",")

    resilienceResults["Humidex:Little to no Discomfort [hr]"] = float(line[2])              # (> 39.4°C, ≤ 51.7°C) 
    resilienceResults["Humidex:Some Discomfort [hr]"] = float(line[3])                      # (> 29, ≤ 40)
    resilienceResults["Humidex:Great Discomfort; Avoid Exertion [hr]"] = float(line[4])     # (> 40, ≤ 45) 
    resilienceResults["Humidex:Dangerous [hr]"] = float(line[5]),                           # (> 45, ≤ 50) 
    resilienceResults["Humidex:Heat Stroke Quite Possible [hr]"] = float(line[6])           #  (> 50)

    # Heating SET Degree-Hours
    # Turned OFF for now because we aren't concerned with cold stress
    """
    line = data[72].split(",")

    d = {}
    d["SET > 30°C Degree-Hours [°C·hr]"] = float(line[2])
    d["SET > 30°C Occupant-Weighted Degree-Hours [°C·hr]"] = float(line[3])
    d["SET > 30°C Occupied Degree-Hours [°C·hr]"] = float(line[4])
    d["Longest SET > 30°C Duration for Occupied Period [hr]"] = float(line[5])
    d["Start Time of the Longest SET > 30°C Duration for Occupied Period"] = line[6]

    resilienceResults["HeatingSETDegreeHours"] = d
    """
    
    # Cooling SET Degree-Hours
    line = data[81].split(",")

    # NOTE: I have turned off the occupant-weighted hours to reduce the amount of stats. 
    resilienceResults["SET > 30°C Degree-Hours [°C·hr]"] = float(line[2])
    #resilienceResults["SET > 30°C Occupant-Weighted Degree-Hours [°C·hr]"] = float(line[3])
    #resilienceResults["SET > 30°C Occupied Degree-Hours [°C·hr]"] = float(line[4])
    resilienceResults["Longest SET > 30°C Duration for Occupied Period [hr]"] = float(line[5])
    resilienceResults["Start Time of the Longest SET > 30°C Duration for Occupied Period"] = line[6]


    return resilienceResults