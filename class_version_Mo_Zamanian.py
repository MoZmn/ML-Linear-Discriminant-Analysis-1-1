# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# %% class version: "FLD" algorithm from the scratch 


import numpy as np
import matplotlib.pyplot as plt

# %% part 1 - load dataset and print summary

training_dataset = np.loadtxt('fld.txt', delimiter=',')
X_training_dataset = training_dataset[::, :2]
y_training_dataset = training_dataset[::, 2]

X_class_0_idx = np.where(y_training_dataset == 0)
X_class_1_idx = np.where(y_training_dataset == 1)
X_class_0 = X_training_dataset[X_class_0_idx]  # per-class sub-dataset for label "0"
X_class_1 = X_training_dataset[X_class_1_idx]  # per-class sub-dataset for label "1"

print('----------------------------------------------------------------------')
print('----------------------------------------------------------------------')
print('Summary of the Dataset:')
print('Class "0" info: Shape - Head - Tail')
print('Shape:', X_class_0.shape)
print('Head:\n', X_class_0[:5, ::])
print('Tail:\n', X_class_0[-5:, ::])
print('----------------------------------------------------------------------')
print('Class "1" info: Shape - Head - Tail')
print('Shape:', X_class_1.shape)
print('Head:\n', X_class_1[:5, ::])
print('Tail:\n', X_class_1[-5:, ::])
print('----------------------------------------------------------------------')

# %% part 2 - perform Fisher Linear Discriminant (FLD)

# compute means of classes

u_class_0 = np.mean(X_class_0, 0)
u_class_1 = np.mean(X_class_1, 0)

# remove means from classes
X0_mean_red = X_class_0 - u_class_0
X1_mean_red = X_class_1 - u_class_1

# calculate covariance matrices
S0 = np.dot(X0_mean_red.T, X0_mean_red)
S1 = np.dot(X1_mean_red.T, X1_mean_red)
Sw = S0 + S1

# calculate slope (projector)
w = np.dot(np.linalg.inv(Sw), (u_class_0 - u_class_1))
threshold = 0

# %% part 3 - prediction

print('----------------------------------------------------------------------')
print('FLD >> Slope and Intercept:')
print('Slope =', w, ', Intercept =', float(threshold))
print('----------------------------------------------------------------------')

predictions = (np.sign(np.dot(w, X_training_dataset.T) + threshold) + 1) / 2
error_possibility_1 = sum(predictions != y_training_dataset)
error_possibility_2 = sum((1 - predictions) != y_training_dataset)
rel_error_1 = error_possibility_1 / len(y_training_dataset)
rel_error_2 = error_possibility_2 / len(y_training_dataset)

if rel_error_1 < rel_error_2:
    final_predictions = predictions
else:
    final_predictions = 1 - predictions

num_preds_to_print = 20
print(f'Some of predictions are: [first {num_preds_to_print}]\n',
      final_predictions[:num_preds_to_print])
print(f'Some of predictions are: [last {num_preds_to_print}]\n',
      final_predictions[-num_preds_to_print:])

# %% part 4 - error report

errorIndex = np.argwhere(final_predictions != y_training_dataset)
errorPts = X_training_dataset[errorIndex]
errorPts = np.squeeze(errorPts)

print('----------------------------------------------------------------------')
print('FLD >> Error:', 100 * min(rel_error_2, rel_error_1), '%.')
print('----------------------------------------------------------------------')
print('----------------------------------------------------------------------')

# %% part 5 - visualization

#  init. parameters
figure_width = 20
original_data_linewidth = 5
legend_fontsize = 20

#  first plot
plt.figure(figsize=(figure_width, figure_width / 1.618))
plt.scatter(X_class_0[:, 0], X_class_0[:, 1],
            c='r', marker='.',
            linewidths=original_data_linewidth)
plt.scatter(X_class_1[:, 0], X_class_1[:, 1],
            c='b', marker='.',
            linewidths=original_data_linewidth)

k0, k1 = 3000, 2000
plt.plot([- k0 * w[0], k1 * w[0]],
         [-k0 * w[1], k1 * w[1]],
         'g--', lw=5)

plt.xlabel('first axis (x0)', size=legend_fontsize)
plt.ylabel('second axis (x1)', size=legend_fontsize)
plt.legend(['FLD line', 'original data - class 0', 'original data - class 1'],
           fontsize=legend_fontsize)
plt.savefig('class--img-1.png', dpi=300)
plt.grid(True)
plt.savefig('class--img-1-grid.png', dpi=300)
plt.show()

# second plot
plt.figure(figsize=(figure_width, figure_width / 1.618))
plt.scatter(X_class_0[:, 0],
            X_class_0[:, 1],
            c='r', marker='.',
            linewidths=original_data_linewidth)
plt.scatter(X_class_1[:, 0],
            X_class_1[:, 1],
            c='b', marker='.',
            linewidths=original_data_linewidth)

k0, k1 = 3000, 2000
plt.plot([- k0 * w[0], k1 * w[0]],
         [-k0 * w[1], k1 * w[1]],
         'g--', lw=5)

plt.scatter(errorPts[:, 0],
            errorPts[:, 1],
            c='orange',
            marker='o')

plt.xlabel('first axis (x0)', size=legend_fontsize)
plt.ylabel('second axis (x1)', size=legend_fontsize)
plt.legend(['FLD line',
            'original data - class 0',
            'original data - class 1',
            'FLD error samples'],
           fontsize=legend_fontsize)
plt.savefig('class--img-2.png', dpi=300)
plt.grid(True)
plt.savefig('class--img-2-grid.png', dpi=300)
plt.show()

