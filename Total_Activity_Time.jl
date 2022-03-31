#=
measure the total amount 
=#

using ReadWriteDlm2,DataFrames

#=
label_data - this is a string path to a folder with audio data to Processed_Snippet
csvpaths - the output location of audacity label
It should be noted that for windows you will need a //
=#
label_data="/Users/phenix/Documents/XMOS_RAP/Low Power Recording/Longterm_Labels/snippets/Probablistic Estimator"  
csvpaths="/Users/phenix/Documents/XMOS_RAP/Low Power Recording/Recordings/Processed_Snippet/Durations"
fldname=splitdir(label_data)
fldname=fldname[end]

#Initializing dataframe that will store the duration for the labels
durz=DataFrame(Track=String[],Detection_Duration=Float64[])

for file in readdir(label_data)
    println("Working on File : ",file)
    #adds the path to the file name so it may be loaded
    fp=joinpath(label_data,file)

    #load tab seperated file
    l_track=readdlm2(fp,'\t')
    
    #size of label array
    lab_size=size(l_track)

    #sees if it has just the default
    if lab_size!=(2, 3)
        #calculate total detection time
        duration=sum((-).(l_track[3:end,2],l_track[3:end,1]))
    else
        #no detection
        duration=0.0
    end
    push!(durz,(file[1:(end-4)],duration))


end
writecsv2(joinpath(csvpaths,fldname*"_durations.csv"),durz)
println("Saved File : ",fldname*"_durations.csv")