from pathlib import Path

# Locate the path to the root directory
current_dir = Path().absolute()
root_dir = current_dir.parent


def modifyIDF (baseline_idf_path, new_idf_path, inputs):
    """"
    This function modifies an idf template based on the given inputs.
    The function uses a search and replace method to inject values in to the idf
    The variables to be replaced in the idf are denoted by @ signs either side of the variable name. eg '@u_windows@'
    If variable does not exist, the replace function will return the existing contents.
    """

    # Open the baseline idf as a text file.
    with open (baseline_idf_path, "r") as f:
        contents = f.read()

    # Loop through the variables in the inputs dictionary.
    # Some variables, such as building geometry and air infiltration require pre-processing before being inserted into the idf
    # Other variables can be done using a search and replace method which finds the key denoted with @ signs either side and injects the values into the idf.
    for k, v in inputs.items():
        if k == "wwr":
            contents = windowGeometry (contents, inputs)
            contents = internalMass(contents, inputs)

        elif k == "ach_50":
            # Convert the ach_50 into a flow coefficient for use with the AIM-2/ZoneInfiltration:FlowCoefficient object
            Volume = inputs["height"] * inputs["length"] * inputs["width"]
            c_zone = ACH_to_flowCoefficient(v, Volume)
            contents = contents.replace("@flowCoefficient@", str(c_zone))

            """
            This code is for use with the airflow network. It is turned off for now.

            # Convert the ach_50 into an effective leakage area for use with the AirflowNetwork:Surface:EffectiveLeakageArea
            contents = flowCoefficient_to_effectiveLeakageArea_10(contents, c_zone, inputs["height"], inputs["width"], inputs["height"])
            """
        else:
            key = f"@{k}@"
            contents = contents.replace(key, str(v))

    # Find the centre points of the plan geometry for the daylighting reference point

    contents = daylightingReferencePoint (contents, inputs["length"], inputs["width"] )

    # Write the updated idf file to the new_idf_path where it can then be run.
    with open(new_idf_path, "w") as f:
        f.write(contents)

def windowGeometry(contents, inputs, openingWidth = 0.15):
    """
    This function edits the window geometry based on the given WWR and the overall dimensions of the building.
    The window is assumed to be perfectly centred in the wall surface.
    The windows for each orientation are modified accordingly
    For each surface:
        x_surface is defined as the building width [m]
        y_surface is defined as the building length [m]
        z_surface is defined as the building height [m]

    For operable windows, it is assumed that the they are casement windows which turn about the vertical axis. 
    It assumed that they have a default openingWidth of 0.15m. Too big and we encounter the oscillation issue of simultaneous venting and heating which distorts results.
    """

    x_surface = inputs["width"]
    y_surface = inputs["length"]
    z_surface = inputs["height"]
    wwr = inputs["wwr"]

    # First do the North facing window by getting the window coordinates and then placing the coordinates into the idf file.
    x_0, x_1, z_0, z_1 = getWindowCoordinates (x_surface, z_surface, wwr)
    key = "@windowNorth_x0@"
    contents = contents.replace(key, str(x_0))
    key = "@windowNorth_x1@"
    contents = contents.replace(key, str(x_1))
    key = "@windowNorth_z0@"
    contents = contents.replace(key, str(z_0))
    key = "@windowNorth_z1@"
    contents = contents.replace(key, str(z_1))

    # Determine the opening area of the window to use in the Wind and Stack Open Area object
    A_opening = (z_1 - z_0) * openingWidth

    key = "@windowOpeningArea_N@"
    contents = contents.replace(key, str(A_opening))


    # Repeat for the East window
    y_0, y_1, z_0, z_1 = getWindowCoordinates (y_surface, z_surface, wwr)
    key = "@windowEast_y0@"
    contents = contents.replace(key, str(y_0))
    key = "@windowEast_y1@"
    contents = contents.replace(key, str(y_1))
    key = "@windowEast_z0@"
    contents = contents.replace(key, str(z_0))
    key = "@windowEast_z1@"
    contents = contents.replace(key, str(z_1))

    A_opening = (z_1 - z_0) * openingWidth

    key = "@windowOpeningArea_E@"
    contents = contents.replace(key, str(A_opening))


    #Repeat this for the South window
    x_0, x_1, z_0, z_1 = getWindowCoordinates (x_surface, z_surface, wwr)
    key = "@windowSouth_x0@"
    contents = contents.replace(key, str(x_0))
    key = "@windowSouth_x1@"
    contents = contents.replace(key, str(x_1))
    key = "@windowSouth_z0@"
    contents = contents.replace(key, str(z_0))
    key = "@windowSouth_z1@"
    contents = contents.replace(key, str(z_1))

    A_opening = (z_1 - z_0) * openingWidth

    key = "@windowOpeningArea_S@"
    contents = contents.replace(key, str(A_opening))

    # Repeat for the West window
    y_0, y_1, z_0, z_1 = getWindowCoordinates (y_surface, z_surface, wwr)
    key = "@windowWest_y0@"
    contents = contents.replace(key, str(y_0))
    key = "@windowWest_y1@"
    contents = contents.replace(key, str(y_1))
    key = "@windowWest_z0@"
    contents = contents.replace(key, str(z_0))
    key = "@windowWest_z1@"
    contents = contents.replace(key, str(z_1))

    A_opening = (z_1 - z_0) * openingWidth

    key = "@windowOpeningArea_W@"
    contents = contents.replace(key, str(A_opening))


    return contents

def internalMass(contents, inputs):
    """
    This function calculates the amount internal Mass surface area [m^2] and injects that value into the idf file.
    Assumes that there is one internal wall running the length of the building and running the width of the building. Therefore the amount of thermal mass changes depending on the footprint of the building
    
    """
    A_internalMass = (inputs["length"] + inputs["width"]) * inputs["height"]

    key = "@internalMass@"
    contents = contents.replace(key, str(A_internalMass))\
    
    return contents


def getWindowCoordinates (l_surface, z_surface, wwr):
    """
    This function returns the window coordinated centred within the wall surface width length (l_surface) and width (w_surface).
    To determine the length and height of the centred window, the ssquare root of the wwr is taken. Explanaion in idf_notes.tex
    The variable name l is used here to distinguish between the x and y notation used in windowGeometry().
    """

    alpha  = wwr ** 0.5

    l_window = alpha * l_surface
    z_window = alpha * z_surface

    l_offset = (l_surface - l_window) / 2
    z_offset = (z_surface - z_window) / 2

    l_0 = l_offset
    l_1 = l_surface - l_offset

    z_0 = z_offset
    z_1 = z_surface - z_offset
    if z_0 < 0:
         pass
    
    return l_0, l_1, z_0, z_1

    
def ACH_to_flowCoefficient (ACH, V, n_zones = 1, n = 0.67):
    """
    Converts the air infiltration rate obtained from a blower door test (ACH_50) and converts it into a flow coefficient (c) to be used with EnergyPlus' ZoneInfiltration:FlowCoefficient object and a Effective Leakage Area to be used by EnergyPlus' AirflowNetwork:Surface:EffectiveLeakageArea object.
    Divide that c equally by the number of zones to be inserted into the idf for each occupied zone.
    NOTE: There are more advanced ways of partitioning c by zone which accounts for percentage leakage around floors, walls, and ceilings.
    """

    Q_50 = ACH * V / 3600 # Convert ACH into a flow rate in m3/s
    c = Q_50 / 50**n #Calculate whole building flow coefficient [m^3/s/Pa^n]
    c_zone = c / n_zones
    return c_zone
     
def flowCoefficient_to_effectiveLeakageArea_10 (contents, c_r, height, width, length, n = 0.67, rho = 1.204, C_D = 0.611):
    """
    Converts the flowCoefficient for a single-zone building into equivalent Effective Leakage Areas at 10 pascals (ELA_10) for each above grade surface.
    The ELA calculated for the whole building is apportioned to each above-grade surface based on percentage of total surface area.
    The equation for converting the flowCoefficient (C_r) into ELA_10 comes from ASHRAE Handbook of Fundamentals 2009 Section 16. An equivalent formula is presented in CSA/CGSB-149 Determination of the airtightness of building envelopes by the fan depressurization method Section 7.5.3. NOTE that this formula uses different units for c_r and the constant incorporates a C_D of 0.611 and the sqrt(2) from the ASHRAE formula.

    NOTE: EnergyPlus uses SI Units of m^2 while the ASHRAE formula uses cm^2. Therefore the 10000 in the numerator disappears in this equation. For this equation we assume that the pressure differential is 10 Pa

    """

    ELA = 1 * c_r / C_D * (rho / 2) ** 0.5 * 10 ** (n - 0.5) # [m^2]
    # Calculate the areas of each surface
    A_North = width * height
    A_South = width * height
    A_East = length * height
    A_West = length * height
    A_Roof = length * width

    A_Total = A_North + A_South + A_East + A_West + A_Roof

    # Calculate the fraction of the ELA for each surface
    ELA_North = A_North / A_Total * ELA
    ELA_South = A_South / A_Total * ELA
    ELA_East = A_East / A_Total * ELA
    ELA_West = A_West / A_Total * ELA
    ELA_Roof = A_Roof / A_Total * ELA

    # Insert the values into the idf
    contents = contents.replace("@ELA_North@", str(ELA_North))
    contents = contents.replace("@ELA_South@", str(ELA_South))
    contents = contents.replace("@ELA_East@", str(ELA_East))
    contents = contents.replace("@ELA_West@", str(ELA_West))
    contents = contents.replace("@ELA_Roof@", str(ELA_Roof))

    return contents

def daylightingReferencePoint (contents, length, width):

    x_centre = width / 2
    y_centre = length / 2

    key = "@daylightReference_x@"
    contents = contents.replace(key, str(x_centre))
 
    key = "@daylightReference_y@"
    contents = contents.replace(key, str(y_centre))

    return contents