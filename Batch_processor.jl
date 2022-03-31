#=
The script takes 48kHz sample data and filters it with a CCIR Filter then downsamples to 16kHz
=#
using DSP,WAV
#=
Library python equivalent
DSP - scipy.signal
WAV - soundfile
=#

b_48k=[0.59277,-0.64278,0.1597,0.010847,-0.0093632,0.045265,-0.14758,0.012525,0.034439,-0.025168,0.021699,-0.043273,-0.069614,0.13181,-0.038812,-0.076451,0.011089,0.019465,0.014415];
a_48k=[1,-3.1159,5.4642,-6.6845,6.5435,-5.4023,3.8997,-2.4889,1.4974,-0.93754,0.70747,-0.62996,0.48873,-0.15423,-0.21824,0.35243,-0.26741,0.11689,-0.026244];
ccir_48k=PolynomialRatio(b_48k,a_48k);

#directories for input and output
out_dir="/Users/phenix/Documents/XMOS_RAP/Low Power Recording/Recordings/Processed_Snippet/CCIR/16k"
input_dir="/Users/phenix/Documents/XMOS_RAP/Low Power Recording/Recordings/Snippets"

#needed variables
chnlabel=["Channel 1","Channel 2"]
chnlabelns=["Channel_1","Channel_2"]

for file in readdir(input_dir)
    if file[1]=='.'
        #removes hidden files
    else
        #adds the path to the file name so it may be loaded
        fp=joinpath(input_dir,file)
        println("Working on File : ",file)
        snpt=wavread(fp) #reads wave file
        chanz=size(snpt[1]) #gets dimension of sample array
        NN=chanz[1] #length 
        chanz=chanz[2] #gets number of channels
        for chnl in 1:chanz
            smp=snpt[1][1:end,chnl] #loaded specified Channel
            smpccir=filt(ccir_48k,smp) #Filters Signal
            smpccir=resample(smpccir,(1//3),dims=1) #Decimates Signal by 3
            wavwrite(smpccir,joinpath(out_dir,"ccir_"*chnlabelns[chnl]*"_"*file),Fs=16000) #Saves the processed Signal in the output directory

        end

    end
    
end

