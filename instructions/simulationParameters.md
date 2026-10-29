These are the parameters which are editable using the simulationParameters.json files. The first three should remain fixed for your coursework, but the others will need to be evaluated as part of your parametric and sensitivity analysis.

| Parameter Name | Units | Description |
| -------------- | ----- | ----------- |
| coolingSetpoint | &deg;C | constant | Interior temperature at which mechanical cooling system is turn on. Set this to 99 &deg;C to convert this model to a naturally ventilated building. This parameter should remain fixed at 99 &deg;C for your coursework. |
| length | m | Plan dimension of the East and West facades. This parameter should remain fixed at your chosen value for your coursework. |
| width | m | Plan dimension of the North and South facades. This parameter should remain fixed at your chosen value for your coursework. |
| height | m | Height of the building |
| u_windows | W/m<sup>2</sup>K | The u-value of the window including thermal bridging effects of the frame. |
| g_value | [0, 1] | The g-value of the windows including the effects of the frame. |
| wwr | [0, 1] | The window to wall ratio expressed as a ratio between 0 and 1. The wwr is identical for each orientation. |
| ach_50 | 1/h | The infiltration rate expressed as air changes per hour (ACH) at a test pressure of 50 Pa. Note that this parameter is converted in pre-processing to a flow coefficient to be compatible with EnergyPlus' AIM-2 flow coefficient infiltration. |
| ventilationRate | m<sup>3</sup>/s | The mechanical ventilation rate. The system is connected to a heat recovery ventilator with an efficiency of 70%. |
| slabInsulationThickness | m | The thickness of the underfloor insulation. |
| wallInsulationThickness | m | The thickness of the wall insulation. |
| roofInsulationThickness | m | The thickness of the roof insulation. |
| fixedShadingDepth | m | The overhang depth of the fixed shading over each of the windows. |
| roofAbsorptance | [0, 1] | The solar absorptance of the roof tiles. |


