# lowpower-algo
Testing out low power mode threshold algorithms  

## Scripts
* Batch_processor.jl (**Preprocessor**) - Takes 48kHz sample data and filters it with a CCIR Filter then downsamples to 16kHz
* Audacity_Label_Generator_Level_Smoothed.jl (**Processing**) - Slow time weighting of sound power is used for a threshold trigger
* Audacity_Label_Generator_Probabilistic.jl (**Processing**) - Pearson Unimodal vs. bimodal distribution Guassian test is used for a threshold trigger
* Total_Activity_Time.jl (**Post-Processing**) - Takes generated Audacity Labels from scripts (Audacity_Label_Generator_Level_Smoothed.jl or Audacity_Label_Generator_Probabilistic.jl) and calculated the total Detection Duration



## Usage
All script interaction happen within scripts. The user will supply paths to input and output folders. To generate a label first you process the audio with the script 'Batch_processor.jl' then use the outputs with either Audacity_Label_Generator_Level_Smoothed.jl or Audacity_Label_Generator_Probabilistic.jl.

## Running Script
[Youtube Video Running Scripts on Windows](https://www.youtube.com/watch?v=BIdDOgp7qRM)

### Installing Packages
[Julia Documentation on Pkg](https://docs.julialang.org/en/v1/stdlib/Pkg/)


