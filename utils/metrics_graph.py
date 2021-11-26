import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-bright')

labels = ['Model #2', 'Model #4', 'Model #5']
recall = [85.88, 79.91, 82.01]
precision = [79.31, 90.85, 90.41]
fscore = [82.47, 85.03, 86.01]

x = np.arange(len(labels))
y = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
width = 0.20

fig, ax = plt.subplots()
recall_bar = ax.bar(x - width, recall, width, label='Recall', color='red')
precision_bar = ax.bar(x, precision, width, label='Precision', color='blue')
fscore_bar = ax.bar(x + width, fscore, width, label='F-Score', color='limegreen')

ax.set_ylabel('Score')
ax.set_title('Metrics score per model')
ax.set_xticks(x)
ax.set_yticks(y)
ax.set_xticklabels(labels)
ax.legend(fontsize=9, loc='upper right')

for index, value in enumerate(recall):
    ax.text(index - 0.27, value + 1.5, str(value), color='black')

fig.tight_layout()

plt.show()