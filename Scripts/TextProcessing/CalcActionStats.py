from __future__ import division
import re
import os
import glob
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

FPS=25

def frames_to_time(num_frames):
    return num_frames/FPS

# Get the frames stats
annotations_dir = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/VideoAnnotation/ActionAnnotations'
action_times_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/Analysisaction_times.p'
action_durations_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/Analysisaction_durations.p'

actions_times = []
for action_filename in glob.glob(os.path.join(annotations_dir, '*.csv')):
    action_name = os.path.splitext(os.path.basename(action_filename))[0]
    annotations = open(action_filename).readlines()
    times = []
    for annotation in annotations:
        fields = annotation.split('\t')
        times.append((int(fields[1]), int(fields[2]), int(fields[2])-int(fields[1]))) #start and end frame
    actions_times.append((action_name, times))

pickle.dump(actions_times, open(action_times_path,'w'))

actions_durations = []
for action_times in actions_times:
    action_name = action_times[0]
    action_dur = filter(lambda x: x!=0, zip(*action_times[1])[2])  #Remove all those non-captured clips
    actions_durations.append((action_name, action_dur))
    
pickle.dump(actions_durations, open(action_durations_path,'w'))

# Make Data object made up of 4 Box objects
action_names = zip(*actions_durations)[0]
data = zip(*actions_durations)[1]

action_names = action_names[0:1]+action_names[3:len(action_names)-1]
data = data[0:1]+data[3:len(data)-1]

fig, ax1 = plt.subplots(figsize=(10, 6))
fig.canvas.set_window_title('Action Durations')
plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='black')
plt.setp(bp['fliers'], color='red', marker='+')

# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

# Hide these grid behind plot objects
ax1.set_axisbelow(True)
ax1.set_title('Action Duration Distribution')
ax1.set_xlabel('Action')
ax1.set_ylabel('Frames')

light_green_color = '#92CD00'
yellow_color = '#FFCC00'
blue_color = '#3333FF'
orange_color = '#FF6600'

boxColors = [light_green_color, orange_color]
numBoxes = len(action_names)
medians = list(range(numBoxes))
for i in range(numBoxes):
    box = bp['boxes'][i]
    boxX = []
    boxY = []
    for j in range(5):
        boxX.append(box.get_xdata()[j])
        boxY.append(box.get_ydata()[j])
    boxCoords = list(zip(boxX, boxY))
    # Alternate between Dark Khaki and Royal Blue
    k = i % 2
    boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
    ax1.add_patch(boxPolygon)
    # Now draw the median lines back over what we just filled in
    med = bp['medians'][i]
    medianX = []
    medianY = []
    for j in range(2):
        medianX.append(med.get_xdata()[j])
        medianY.append(med.get_ydata()[j])
        plt.plot(medianX, medianY, 'k')
        medians[i] = medianY[0]
    # Finally, overplot the sample averages, with horizontal alignment
    # in the center of each box
    plt.plot([np.average(med.get_xdata())], [np.average(data[i])],
             color='w', marker='*', markeredgecolor='k')

# Set the axes ranges and axes labels
ax1.set_xlim(0.5, numBoxes + 0.5)
top = 200
bottom = 0
ax1.set_ylim(bottom, top)
xtickNames = plt.setp(ax1, xticklabels=action_names)
plt.setp(xtickNames, rotation=45, fontsize=12)


pos = np.arange(numBoxes) + 1
upperLabels = [str(np.round(s, 2)) for s in medians]
weights = ['bold', 'semibold']
for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
    k = tick % 2
    ax1.text(pos[tick], top - (top*0.05), upperLabels[tick],
             horizontalalignment='center', size='x-small', weight=weights[k],
             color=boxColors[k])

# Finally, add a basic legend
plt.figtext(0.80, 0.015, '*', color='white', backgroundcolor='silver',
            weight='roman', size='medium')
plt.figtext(0.815, 0.013, ' Average Value', color='black', weight='roman',
            size='x-small')

plt.show()