# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

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
output_path='/home/stufs1/nitigupta/512/results/dict.txt' #where to store the output
label_csv_path='/home/stufs1/nitigupta/512/data/trainLabels.csv' #path to csv file mapping filenames to labels
data_path = '/home/stufs1/nitigupta/512/data/train/' #path to the data
raw_opcode_list=['mov','add','sub','imul'] #list of opcodes to filter

#doubts:
# do i need to filter with .text .much .CODE for beginning of text?
#latin-1 encoding being used instead of utf-8... wtf!! 

# <codecell>

unpickled_file=open(output_path,'rb')
print("Done Pickling...")
unpickled_dict=pickle.load(unpickled_file)
unpickled_dict

# <codecell>

#count_list[9] = list()
cl=list()    
for i in range(0,9):
    #print(i)
    #cl[i]=list()
    cl.append(unpickled_dict[i].values())


def convert_to_percentage():
    for i in range(0,9):
        sum=0
        for val in cl[i]:
            sum+=val
        #print(sum)
        for j in range(0,4):
            cl[i][j]=(float)(cl[i][j]*10000/(sum+1))
            
convert_to_percentage()

for i in range(0,9):
    print(cl[i])

# <codecell>

class_labels = list()
for i in range(0,9):
    class_labels.append(i+1)
class_labels

# <codecell>

#!/usr/bin/env python
###############################################################################
#                                                                             #
#    stackedBarGraph.py - code for creating purdy stacked bar graphs          #
#                                                                             #
###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = "Michael Imelfort"
__copyright__ = "Copyright 2014"
__credits__ = ["Michael Imelfort"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Michael Imelfort"
__email__ = "mike@mikeimelfort.com"
__status__ = "Development"

###############################################################################

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

###############################################################################

class StackedBarGrapher:
    """Container class"""
    def __init__(self): pass

    def demo(self):
        '''
        d = np.array([[101.,0.,0.,0.,0.,0.,0.],
                      [92.,3.,0.,4.,5.,6.,0.],
                      [56.,7.,8.,9.,23.,4.,5.],
                      [81.,2.,4.,5.,32.,33.,4.],
                      [0.,45.,2.,3.,45.,67.,8.],
                      [99.,5.,0.,0.,0.,43.,56.]])
        '''
        ''' 
        d = np.array([[101.,0.,0.,0.],
                      [92.,3.,0.,4.],
                      [56.,7.,8.,9.]])
                      '''
        d=np.array(cl)
        d_heights = [1.,2.,3.,4.,5.,6.]
        d_widths = [.5,1.,3.,2.,1.,2.]
        d_labels = class_labels
        d_colors = ['#2166ac', '#fee090', '#fdbb84', '#fc8d59']
        #d_colors = ['r','g','b','y']
        gap = 0.05

        fig = plt.figure()
        
        ax6 = fig.add_subplot(111)
        self.stackedBarPlot(ax6,
                            d,
                            d_colors,
                            edgeCols=['#000000']*9,
                            xLabels=d_labels,
                            scale=True,
                            gap=gap,
                            endGaps=True
                            )
        plt.title("Ratio of mov,imul,add and sub instructions for each class of malware")
        plt.xlabel("Class of malware")
        plt.ylabel("Percentage of instruction")
        #red_patch = mpatches.Patch(color='red', label='The red data')
        plt.legend()

        # We change the fontsize of minor ticks label
        fig.subplots_adjust(bottom=0.4)

        plt.tight_layout()
        plt.show()
        plt.close(fig)
        del fig
        print(d)
    def stackedBarPlot(self,
                       ax,                                 # axes to plot onto
                       data,                               # data to plot
                       cols,                               # colors for each level
                       xLabels = None,                     # bar specific labels
                       yTicks = 6.,                        # information used for making y ticks ["none", <int> or [[tick_pos1, tick_pos2, ... ],[tick_label_1, tick_label2, ...]]
                       edgeCols=None,                      # colors for edges
                       showFirst=-1,                       # only plot the first <showFirst> bars
                       scale=False,                        # scale bars to same height
                       widths=None,                        # set widths for each bar
                       heights=None,                       # set heights for each bar
                       ylabel='',                          # label for x axis
                       xlabel='',                          # label for y axis
                       gap=0.,                             # gap between bars
                       endGaps=False                       # allow gaps at end of bar chart (only used if gaps != 0.)
                       ):

#------------------------------------------------------------------------------
# data fixeratering

        # make sure this makes sense
        if showFirst != -1:
            showFirst = np.min([showFirst, np.shape(data)[0]])
            data_copy = np.copy(data[:showFirst]).transpose().astype('float')
            data_shape = np.shape(data_copy)
            if heights is not None:
                heights = heights[:showFirst]
            if widths is not None:
                widths = widths[:showFirst]
            showFirst = -1
        else:
            data_copy = np.copy(data).transpose()
        data_shape = np.shape(data_copy)

        # determine the number of bars and corresponding levels from the shape of the data
        num_bars = data_shape[1]
        levels = data_shape[0]

        if widths is None:
            widths = np.array([1] * num_bars)
            x = np.arange(num_bars)
        else:
            x = [0]
            for i in range(1, len(widths)):
                x.append(x[i-1] + (widths[i-1] + widths[i])/2)

        # stack the data --
        # replace the value in each level by the cumulative sum of all preceding levels
        data_stack = np.reshape([float(i) for i in np.ravel(np.cumsum(data_copy, axis=0))], data_shape)

        # scale the data is needed
        if scale:
            data_copy /= data_stack[levels-1]
            data_stack /= data_stack[levels-1]
            if heights is not None:
                print "WARNING: setting scale and heights does not make sense."
                heights = None
        elif heights is not None:
            data_copy /= data_stack[levels-1]
            data_stack /= data_stack[levels-1]
            for i in np.arange(num_bars):
                data_copy[:,i] *= heights[i]
                data_stack[:,i] *= heights[i]

#------------------------------------------------------------------------------
# ticks

        if yTicks is not "none":
            # it is either a set of ticks or the number of auto ticks to make
            real_ticks = True
            try:
                k = len(yTicks[1])
            except:
                real_ticks = False

            if not real_ticks:
                yTicks = float(yTicks)
                if scale:
                    # make the ticks line up to 100 %
                    y_ticks_at = np.arange(yTicks)/(yTicks-1)
                    y_tick_labels = np.array(["%0.2f"%(i * 100) for i in y_ticks_at])
                else:
                    # space the ticks along the y axis
                    y_ticks_at = np.arange(yTicks)/(yTicks-1)*np.max(data_stack)
                    y_tick_labels = np.array([str(i) for i in y_ticks_at])
                yTicks=(y_ticks_at, y_tick_labels)

#------------------------------------------------------------------------------
# plot

        if edgeCols is None:
            edgeCols = ["none"]*len(cols)

        # take cae of gaps
        gapd_widths = [i - gap for i in widths]

        # bars
        ax.bar(x,
               data_stack[0],
               color=cols[0],
               edgecolor=edgeCols[0],
               width=gapd_widths,
               linewidth=0.5,
               align='center'
               )

        for i in np.arange(1,levels):
            ax.bar(x,
                   data_copy[i],
                   bottom=data_stack[i-1],
                   color=cols[i],
                   edgecolor=edgeCols[i],
                   width=gapd_widths,
                   linewidth=0.5,
                   align='center'
                   )

        # borders
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)

        # make ticks if necessary
        if yTicks is not "none":
            ax.tick_params(axis='y', which='both', labelsize=8, direction="out")
            ax.yaxis.tick_left()
            plt.yticks(yTicks[0], yTicks[1])
        else:
            plt.yticks([], [])

        if xLabels is not None:
            ax.tick_params(axis='x', which='both', labelsize=8, direction="out")
            ax.xaxis.tick_bottom()
            plt.xticks(x, xLabels, rotation='vertical')
        else:
            plt.xticks([], [])

        # limits
        if endGaps:
            ax.set_xlim(-1.*widths[0]/2. - gap/2., np.sum(widths)-widths[0]/2. + gap/2.)
        else:
            ax.set_xlim(-1.*widths[0]/2. + gap/2., np.sum(widths)-widths[0]/2. - gap/2.)
        ax.set_ylim(0, yTicks[0][-1])#np.max(data_stack))

        # labels
        if xlabel != '':
            plt.xlabel(xlabel)
        if ylabel != '':
            plt.ylabel(ylabel)


###############################################################################
###############################################################################
###############################################################################
###############################################################################

if __name__ == '__main__':

    SBG = StackedBarGrapher()
    SBG.demo()

###############################################################################
###############################################################################
###############################################################################
###############################################################################

# <codecell>

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

red_patch = mpatches.Patch(color='red', label='The red data')
plt.legend([red_patch])

plt.show()

# <codecell>

plt.plot([1,2,3], label='Line 2')

# <codecell>

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

red_patch1 = mpatches.Patch(color='red', label='The red data')
plt.legend([red_patch1])

plt.show()

# <codecell>


