## Importing all Libraries/Dependencies 

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
import csv
from sklearn.preprocessing import normalize
import numpy as np


'''
	 Convert the recordings to spectrogram and save it to 
	 seperate classes/folders

	params@ :
		wav_file - recording file 
		class_label - label for the recording i.e 'normal' or 'abnormal'  
'''
def graph_spectrogram(wav_file, class_label):
    rate, data = get_wav_info(wav_file)
    nfft = 256  # Length of the windowing segments
    fs = 256    # Sampling frequency
    pxx, freqs, bins, im = plt.specgram(data, nfft,fs)
    plt.axis('off')
    if (class_label == 1):
		print(str(wav_file[23:28]))
    else:
		print(str(wav_file[23:28]))
    		


'''
	Returns the sampling rate and data of the recording 
	params@ :
		wav_file - recording file 
'''   		
def get_wav_info(wav_file):
    rate, data = wavfile.read(wav_file)
    return rate, data


'''
	Returns the class label i.e 'normal' or 'abnormal' 

	params@ :
		label_file_name - label (.hea) file for the recording  
'''
def parse_class_label(label_file_name):

    with open(label_file_name, 'r') as fin:
        header = fin.readlines()

    comments = [line for line in header if line.startswith("#")]
    if not len(comments) == 1:
        raise InvalidHeaderFileException("Invalid label file %s" % label_file_name)

    class_label = str(comments[0]).lstrip("#").rstrip("\r").strip().lower()

    if not class_label in class_name_to_id.keys():
        raise InvalidHeaderFileException("Invalid class label %s" % class_label)

    return class_label 



if __name__ == "__main__":

	class_name_to_id = {"normal": 0, "abnormal": 1}
	nclasses = len(class_name_to_id.keys())
	path = '/home/adityajainkld/workspace_ml/Cardiac-Arrhythmia-ML/ecg_data/training-d'
	wav_file_names = []
	class_labels = []
	samples = 0
	## processing all the recordings in 'training' folder
	for root, dirs, files in os.walk(path):
	    for file in files:
	        if file.endswith('.wav'):
	            label_file_name = os.path.join(root, base_file_name + ".hea")
	            base_file_name = file.rstrip(".wav")
	            class_label = parse_class_label(label_file_name)
	            class_labels.append(class_name_to_id[class_label])
	            wav_file_names.append(os.path.join(root, file))
	            samples +=1


	## After saving all file name to lists, convering to spectrograms
	for i,j in zip(wav_file_names,class_labels):
	    graph_spectrogram(i,j)

	## Logging the number of samples and file names   
	print (len(class_labels), len(wav_file_names))
	for i,j in zip(wav_file_names[:10], class_labels[:10]):
		print (i[23:28], j)


	## saving the labels to a csv file
	with open('labels.csv', 'w') as f:
	    writer = csv.writer(f)
	    for val in class_labels:
	        writer.writerow([val])
            
            