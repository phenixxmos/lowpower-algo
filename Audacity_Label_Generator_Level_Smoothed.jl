#=
This uses slow weighted of sound power for a threshold trigger 
=#
using DSP,WAV,StatsBase,ReadWriteDlm2,DataFrames,Dates
#=
Library python equivalent
DSP - scipy.signal
WAV - soundfile
StatsBase - scipy.stats
ReadWriteDlm2 - csv 
DataFrames - Pandas
Dates - datetime
=#

#=
audio_data - this is a string path to a folder with audio data to Processed_Snippet
csvpaths - the output location of audacity label
It should be noted that for windows you will need a //
=#
audio_data="/Users/phenix/Documents/XMOS_RAP/Low Power Recording/Recordings/Processed_Snippet/CCIR/16k" 
csvpaths="/Users/phenix/Documents/XMOS_RAP/Low Power Recording/Longterm_Labels/snippets"

#threshold_setting=10.6e-9
threshold_setting=4.9e-8

println("Threshold : ",string(threshold_setting))

#This is a threshold function for the signal level metric
function threshold_lever(sig::Float64,cutoff::Float64)

    if sig>=cutoff
        return 1
    else
        return -1
    end

end

#Indexing over files in folder represented by  audio_data
for file in readdir(audio_data)
    #adds the path to the file name so it may be loaded
    fp=joinpath(audio_data,file)

    #Initializing dataframe for that will store the sample and dection staturs
    result=DataFrame(sample=Int[],true_result=Int[])

    #Initializing dataframe that will store the audacity labels
    label=DataFrame(start=Float64[],stop=Float64[],label=String[])


    if (file[1]=='.')||(isdir(fp))
        #removes hidden files
    else
        
        println("Working on File : ",file) #Shows which file is being processed
        println(Dates.now()) #print current time to terminal
        snpt=wavread(fp) #reads wave file
        fs=Int(snpt[2]) #gets the in sample rate and cast it to your default integer Int64 on 64bit systems
        scaler=1 #This is the gain applies to the input signal
        snpt=(*).(snpt[1],scaler) #This applies the gain from scaler and copies the data values without any other information
        snpt=abs2.(snpt) #gets the power signal of the inputing signal
        smoothing=digitalfilter(Lowpass(1,fs=16000),Butterworth(1)) #generating the time weighted
        snpt=filt(smoothing,snpt) #applies expontial weighting to the signal

        NN=length(snpt) #Length of the signal in samples
        #Sets the size to step thru
        step_size=512

        #=
        start_value:step_size:end_value
        This loop starts at 1 second and shifts by the step size in samples. The loop goes until the step size is less than the end. 
        The initial rise time is clipped 
        =#
        for step in (1*fs):step_size:NN
            step_smp=snpt[step] #obtians the smoothed level
            distr_result=threshold_lever(step_smp,threshold_setting) #Calcating the if it surpasses the threshold or not
            push!(result,(step,distr_result)) #Storing threshold state and sample number
            
        end

        #writecsv2(file[1:(end-4)]*"_Threshold_"*string(threshold_setting)*"dB_"*"_Estimators.csv",result)

        #Initializing labels array
        println("Finding Trigger section")
        push!(label,(0.0,29.9999375,"Buffer Filling"))
        start_val=0.0
        end_val=0.0
        result_l=length(result.sample)

        for indx=1:result_l
            #Finds start point of detection
            if (start_val==0.0)&&(result[indx,2]==1)
                start_val=Float64(result[indx,1]-1)/fs
            end

            #Finds end point of detection
            if (start_val!=0.0)&&(end_val==0.0)&&(result[indx,2]==-1)
                #the minus step_size+1 is for julia starting at 1 and then the step before the change happens
                end_val=Float64((result[indx,1]-(step_size+1)))/fs
            end

            #stores end points and then re-initialize endpoint values
            if (start_val!=0.0)&&(end_val!=0.0)
                println("Start Second: ",start_val," , Stop Second: ",end_val)
                push!(label,(start_val,end_val,"Activity Detected"))
                start_val=0.0
                end_val=0.0
            end

        end

        #If the whole file is a detection it will store properly 
        if (start_val!=0.0)&&(end_val==0.0)
            println("Start Second: ",start_val," , Stop Second: ",Float64(NN-1)/fs)
            push!(label,(start_val,Float64(NN-1)/fs,"Activity Detected"))

        end


    end

    #writes label out for audacity
    writedlm2(joinpath(csvpaths,file[1:(end-4)]*"_Threshold_"*string(threshold_setting)*"_Estimators.txt"),label,'\t',decimal='.')

end
