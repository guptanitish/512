# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#get the dictionary of all opcodes present in the dataset

import pickle
import re
import os, os.path
import pandas as pd
import pickle
import sys
from sklearn.cross_validation import train_test_split
import io

output_path='/home/stufs1/nitigupta/512/results/opcodes_temp.txt' #where to store the output
label_csv_path='/home/stufs1/nitigupta/512/data/trainLabels.csv' #path to csv file mapping filenames to labels
data_path = '/home/stufs1/nitigupta/512/data/train/' #path to the data
raw_opcode_list=['mov','add','sub','imul'] #list of opcodes to filter


# <codecell>

df_entire= pd.read_csv(label_csv_path)
a_train, a_test= train_test_split(df_entire,test_size=0.001, random_state=24)
df_test=pd.DataFrame.from_records(a_test)

# <codecell>

len(df_test)

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

d=dict()
def make_dict_of_opcodes(d,line):
    opcode_group = re.search('\s\s\s[a-z][a-z]+\s\s\s',line)
    if opcode_group:
        opcode = opcode_group.group()
        opcode.strip()
        
        if opcode not in d:
            d[opcode]=1
        else:
            d[opcode]+=1
#making list of dict to store counts
def count_opcodes(directory_path,filename):
    #byte_limit=100
    try:
        path=directory_path+filename
        openfile = io.open(path,'r',encoding='latin-1')
        l_lines=openfile.readlines()

        count=0
        for line in l_lines:
            label = label_d[filename[:-4]]
            make_dict_of_opcodes(d,line)
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
pickle.dump(d,dumpfile)
dumpfile.close()
unpickled_file=open(output_path,'rb')
print("Done Pickling...")
unpickled_dict=pickle.load(unpickled_file)
#unpickled_dict

# <codecell>

unpickled_file=open(output_path,'rb')
unpickled_dict=pickle.load(unpickled_file)

import opcodes.x86 as op_32
import opcodes.x86_64 as op_64
in_set=op_32.read_instruction_set("/home/stufs1/nitigupta/512/code/lib/x86.xml")

inst_set_dict=dict()

for i in range(0,len(in_set)):
    inst_set_dict[in_set[i].name.lower()]=1

#print (len(in_set))
instr_present=dict()
for key in unpickled_dict.keys():
    #if "\t" in str
    if key.strip() in inst_set_dict:
        instr_present[key.strip()]=1

len(instr_present)


# <codecell>


