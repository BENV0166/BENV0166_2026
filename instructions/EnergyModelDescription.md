# The Energy Plus Model
A description of the EnergyPlus model being used for the coursework *1-storey_baseline.idf* is described here. 

The model is intended to represent a small single-family home. The model is a simple *one-zone* shoebox model with simple rectangualar geometry and an *ideal loads* HVAC systems for ventilation and heating, and naturally ventilated for cooling in summer. It was an intentional decision to keep the model simple to reduce simulation times and be simple and intuitive to edit. This decision comes at the expense of real-world accuracy and does not exploit the capabilities of a state-of-the-art tool such as EnergyPlus.

Important features of the idf file are briefly explained. Note what assumptions or simplifications have been made and which parameters are variable and which are fixed.

# Geometry
The building is a single-zone, with rectangular plan geometry including a flat roof and a ground floor slab. The building’s overall dimensions are editable using width, length, and height parameters. Other parameters such as window sizes, and infiltration flow coefficients are dependant on the building geometry.

The idf contains a number of coordinate keystrings [x<sub>0</sub>, x<sub>1</sub>, y<sub>0</sub>, y<sub>1</sub>, z<sub>0</sub>, z<sub>1</sub>] which identify each of the main vertices of the building. 

## Overall Dimensions
For the coursework, you should use the same floor area throughout - ie a constant length and width for all of your simulations. You can choose your own length and width or use the default values in the simulation parameters json file. 

In this model, the length is defined as the plan dimension of the East and West facades and the width as the plan dimension of the North and South facades. The building is aligned with the four cardinal directions.

The building height is a variable parameter which you will evaluate as part of your exercises.

## Window to Wall Ratios
The window to wall ratio is a variable parameter and is dependent on the length, width and height of the building. The wwr is assumed to be the same on each facade and there is one window on each facade. Each window is assumed to be centered in the wall.

# Envelope
## Windows and Doors
Windows are modelled using the simple glazing method where only a u-value and g-value and that any thermal bridging effects of the window frame are included in those values. The u-value and g-value are variable parameters. In addition, the visible transmittance of the window is assumed to be the same as the g-value. This is important if you are considering daylighting.

Each window has fixed shading which sits 0.5 m above the window and extends 0.5 m either side. The fixed shading depth is a variable parameter.

There is no door included in the model. The occupants love my minimalist design so much, they never want to leave!


## Materials and Constructions

### Insulation Materials
The thermal resistance of an opaque wall assembly can only be modified by changing the thickness of the insulation material, not the conductivity. You can not enter a u-value directly in EnergyPlus.

To follow best EnergyPlus modelling procedures, the conductivity of the insulation should be the effective R-value accounting for thermal bridging through wooden studs, not the nominal value of the insulation. For the purposes of these exercises, we assume that all insulation has a conductivity of 0.05 W/m-K inclusive of all thermal bridging. This is equivalent to a wood-framed wall with internal insulation of conductivity 0.035 W/m-K. A common insulation material was assumed for basement, walls, and attics. To improve the accuracy of the conduction transfer functions, the density and specific heat capacity of the insulation material vs frame materials was area-weighted. 

If needed, the U-values of the walls can be calculated in post-processing based on the thickness and conductivity of the insulation.

The wall, roof, and slab insulation thickness are variable parameters.

Also note that EnergyPlus does not allow the thickness of any layer to be zero. If necessary to model an uninsulated wall, use a small value for thickness such as 0.001m and the impact should be negligible.

## Constructions

The constructions used in the model are simple. The exterior walls are assumed to be 200 mm of double-wythe brick with interior insulation and stucco/gypsum renderings on both sides.

The basement slab is assumed to be 100 mm of concrete with under-slab insulation in contact with the ground. The Kiva slab model was chosen to model ground heat transfer.

The roof is assumed to be a lightweight insulated wood-framed roof with clay tiles.

Internal mass was added to the model as a dedicated interior wall construction consisting of one layer of concrete (100 mm) with two layers of gypsum board. An interior wall is assumed to span both the length and width of the floor plate. As the building's width and length change the surface area of the internal mass changes with it.

## Infiltration and Ventilation

Infiltration and ventilation rates are both variable parameters.

Air infiltration is modelled using the AIM-2 flow coefficient model. The user input for this model is the Air Changes per Hour (ACH). This input gets translated into a flow coefficient (c<sub>r</sub>) to be compatible with EnergyPlus during pre-processing.

Natural ventilation via operable windows is modelled using EnergyPlus' *Wind and Stack Open Area* object. Windows open to 100% of their assigned opening area once the temperature reaches a certain threshold of 24 &deg;C. Each window is assumed to have a opening width of 150 mm only regardless of the window's actual size.

In addition to natural ventilation, mechanical ventilation is included as a variable parameter and this system is connected to a heat recovery ventilator with an efficiency of 70%.

# Internal Loads and Schedules

Note the following are *peak* loads and are dependant on the operational schedules
## Occupants
It is assumed that there are only two occupants living in the building.

## Electrical
The peak receptacle load is set at 5 W/m<sup>2</sup>. 

## Lighting
The peak interior lighting load is set at 5 W/m<sup>2</sup>. No exterior lighting is modelled.

A simple daylighting control is implemented with a threshold of 500 lux with a reference point located in the geometric centre of the floor plan set 0.8m above the floor.

## Domestic Hot Water
Domestic Hot Water is modelled with an average daily water consumption of 90 L/day. The peak usage is 3.2 E-06 m<sup>3</sup>/s, but the average flow rate is 28% of that.

## Schedules
Schedules which modify the number of occupants and the intensity of lighting, electrical, and hot water loads at each hour the day have been included. These are modelled after the National Energy Code for Buildings of Canada (Schedule B - Multi-residential buildings).

## Setpoints
The heating setpoint is set at 21 &deg;C during the day with a setback of 18 &deg;C during the night.

The cooling setpoint is a variable parameter. By default it is set to 99 &deg;C which is a trick to quickly deactivate mechanical cooling and revert to a naturally ventilated building. If a mechanically cooled building needs to be modelled, it can be converted by choosing an appropriate cooling setpoint.

# Mechanical Systems
Mechanical systems are modelled using an *ideal loads air system*. This is a fictitious system which delivers energy to the space to keep the temperature within the ranges defined by the setpoints. The heating and cooling systems are automatically sized.

The idealised model precludes the need to model heat pumps, boilers, furnaces, chillers etc. explicitly. This makes the model easier to build and a little quicker to run but has its downsides in that we can only measure **heating and cooling load** and **not heating and cooling energy consumption** as we don't know the efficiency or COP of the equipment.