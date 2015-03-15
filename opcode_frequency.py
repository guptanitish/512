
# coding: utf-8

# In[67]:

import pickle
import re
import os, os.path
import pandas as pd
import pickle
import sys

#returns a list 
#searches for ' opcode ' from a specified list of opcodes
#needs:
output_path='/home/rishoo/Downloads/data/pickle/dict.txt' #where to store the output
label_csv_path='/home/rishoo/Downloads/data/trainLabels.csv' #path to csv file mapping filenames to labels
data_path = '/home/rishoo/Downloads/data/train_tiny_subset/' #path to the data
raw_opcode_list=['mov','add','sub'] #list of opcodes to filter

#doubts:
# do i need to filter with .text .much .CODE for beginning of text?
#latin-1 encoding being used instead of utf-8... wtf!! 


# In[68]:

#build label dict - filename->labels
def get_labels(path,label_d):    
    df= pd.read_csv(path)
    for index, row in df.iterrows():
        label_d[row['Id']]=row['Class']
    
label_d=dict()
get_labels(label_csv_path,label_d)


# In[69]:


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
        openfile = open(path,'r',encoding='latin-1')
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


for filename in os.listdir(data_path):
    if((filename[-4:])=='.asm'): #.swp files!
        filename_key= filename[:-4]
        label=label_d[filename_key]  
        print("Processing...\tlabel: ",label,"\t",filename,"\t")
        sys.stdout.flush()
        count_opcodes(data_path,filename)



# In[70]:


dumpfile=open(output_path,'wb')
pickle.dump(opcode_dict_l,dumpfile)
dumpfile.close()
unpickled_file=open(output_path,'rb')

unpickled_dict=pickle.load(unpickled_file)
unpickled_dict


# In[ ]:




# In[ ]:



