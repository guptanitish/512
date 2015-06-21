
# coding: utf-8

# In[1]:

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
#output_path='/home/stufs1/nitigupta/512/results/dict_10percent.txt' #where to store the output
label_csv_path='/home/rishoo/Downloads/data/trainLabels.csv' #path to csv file mapping filenames to labels
data_path = '/home/rishoo/Downloads/data/train_tiny_subset/' #path to the data
raw_opcode_list=['mov','add','sub','imul'] #list of opcodes to filter
 


# In[6]:


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
    new_opcode_dict=dict()
    for key in opcode_dict.keys():
        new_opcode_dict[key] = 0
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
                        if opcode not in new_opcode_dict.keys():
                            new_opcode_dict[opcode] = 1
                        else:
                            new_opcode_dict[opcode] += 1
                        #opcode_dict_l[label_d[filename_key]-1][opcode]+=1
                        break
        openfile.close()
    except IOError:
        print ("Could not open file!")
    total=1
    for opcode in new_opcode_dict.keys():
        total+=new_opcode_dict[opcode]
    
    for opcode in new_opcode_dict.keys():
        new_opcode_dict[opcode] = float(new_opcode_dict[opcode]/total)
    return new_opcode_dict

count=0
print("Begin...")
for filename in os.listdir(data_path):
    if((filename[-4:])=='.asm'): #.swp files!
        if count > 2:
            break
        else:
            # label=label_d[filename_key]  
            print("Processing...\t",count,"\tfilename: ","\t",filename,"\t")
            sys.stdout.flush()
            print(count_opcodes(data_path,filename))
            count+=1

print("Done!")


# In[ ]:



