# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#dictionary of opcodes per file

import pickle
import re
import os, os.path
import pandas as pd
import pickle
import sys
from sklearn.cross_validation import train_test_split
import io
'''
#returns a list 
#searches for ' opcode ' from a specified list of opcodes
#needs:
output_path='/home/rishoo/Downloads/data/pickle/dict.txt' #where to store the output
label_csv_path='/home/rishoo/Downloads/data/trainLabels.csv' #path to csv file mapping filenames to labels
data_path = '/home/rishoo/Downloads/data/train_tiny_subset/' #path to the data
raw_opcode_list=['mov','add','sub'] #list of opcodes to filter
'''
output_path='/home/stufs1/nitigupta/512/results/dict_10percent.txt' #where to store the output
label_csv_path='/home/stufs1/nitigupta/512/data/trainLabels.csv' #path to csv file mapping filenames to labels
data_path = '/home/stufs1/nitigupta/512/data/train/' #path to the data
raw_opcode_list=['mov','add','sub','imul'] #list of opcodes to filter
 

# <codecell>

df_entire= pd.read_csv(label_csv_path)
a_train, a_test= train_test_split(df_entire,test_size=0.001, random_state=42)
df_test=pd.DataFrame.from_records(a_test)

# <codecell>

#build label dict - filename->labels
print("extracting labels..")
def get_labels(path,label_d,df):    
    #df= pd.read_csv(path)
    for index, row in df.iterrows():
        label_d[row[0]]=row[1]
    
label_d=dict()
get_labels(label_csv_path,label_d,df_test)
print("done extracting labels..")

# <codecell>


#making list of dict to store counts

opcode_dict_l=list()
for i in range(0,9):
    opcode_dict=dict()
    for item in raw_opcode_list:
        formatted_opcode=' '+item+' '
        opcode_dict[formatted_opcode]=0
    opcode_dict_l.append(opcode_dict)

def count_opcodes(directory_path,filename):
    #byte_limit=100
    try:
        path=directory_path+filename
        openfile = io.open(path,'r',encoding='latin-1')
        #openfile = open(path,'rb')
        l_lines=openfile.readlines()
        count=0
        for line in l_lines:
            #match_text=re.search("text:",line)
            
            #if match_text:
                for opcode in opcode_dict.keys():
                    #match_opcode=None
                    match_opcode=re.search(opcode,line)
                    if match_opcode:
                    #print (match.group())
                        filename_key= filename[:-4]
                        opcode_dict_l[label_d[filename_key]-1][opcode]+=1
                        break
        openfile.close()
    except IOError:
        print ("Could not open file!")

count=0
print("Begin...")
for filename in os.listdir(data_path):
    if((filename[-4:])=='.asm'): #.swp files!
        filename_key= filename[:-4]
        if((label_d.get(filename_key,-1))!=-1):
            label=label_d[filename_key]  
            print("Processing...\t",count,"\tlabel: ",label,"\t",filename,"\t")
            sys.stdout.flush()
            count_opcodes(data_path,filename)
            count+=1

print("Done!")

# <codecell>

print("Pickling...")
dumpfile=open(output_path,'wb')
pickle.dump(opcode_dict_l,dumpfile)
dumpfile.close()
unpickled_file=open(output_path,'rb')
print("Done Pickling...")
unpickled_dict=pickle.load(unpickled_file)
unpickled_dict

# <codecell>


# <codecell>


