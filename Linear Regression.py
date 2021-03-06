import pandas as pd
import numpy as np

data = pd.read_csv('housing.data.csv')

print("UNNORMALIZED DATA")

unnormalized_data = np.array(
    data[['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RED', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']])

#np.random.shuffle(unnormalized_data) # Trộn dữ liệu mỗi lần thử để đảm bảo tính khách quan
training_set_unnormalized_data = unnormalized_data[101:507] # Tạo training set
testing_set_unnormalized_data = unnormalized_data[0:101] # Tạo testing set

ones = np.array([np.ones_like(training_set_unnormalized_data.T[0])]).T
ones_and_training_set = np.concatenate((ones, training_set_unnormalized_data), axis=1)

X_unnormalized_data = ones_and_training_set.T[0:14].T  # X của training set
Y_unnormalized_data = np.array([ones_and_training_set.T[-1]]).T  # Y của training set

A_unnormalized_data = np.dot(X_unnormalized_data.T, X_unnormalized_data) # A = X.T * X
b_unnormalized_data = np.dot(X_unnormalized_data.T, Y_unnormalized_data) # b = X.T * Y

w_unnormalized_data = np.dot(np.linalg.pinv(A_unnormalized_data), b_unnormalized_data) # w = 1/A * b

print("w[]:", end=' ') # In các giá trị w
for i in range(w_unnormalized_data.shape[0]):
    print("w{0} = {1}".format(i, w_unnormalized_data[i][0]), end=' ')
print()

MSE_UN1 = 0
MSE_UN2 = 0
MAE_UN1 = 0
MAE_UN2 = 0

for i in range(training_set_unnormalized_data.shape[0]):
    x_unnormalized_data = 0 + w_unnormalized_data[0][0]
    for j in range(0, training_set_unnormalized_data[i].shape[0] - 1):
        x_unnormalized_data += training_set_unnormalized_data[i][j] * w_unnormalized_data[j + 1][0]
    MSE_UN1 += (training_set_unnormalized_data[i][-1] - x_unnormalized_data) ** 2 # Tính MSE
    MAE_UN1 += abs(training_set_unnormalized_data[i][-1] - x_unnormalized_data) # Tính MAE
    #print("{0:.2f} = {1}".format(x_unnormalized_data,training_set_unnormalized_data[i][-1]))
print("MSE training set unnormalized data: {0:.2f}".format(MSE_UN1 / training_set_unnormalized_data.shape[0]))
print("MAE training set unnormalized data: {0:.2f}".format(MAE_UN1 / training_set_unnormalized_data.shape[0]))

print()
print("Ket qua du doan tren testing set:")
for i in range(testing_set_unnormalized_data.shape[0]):
    y_predict = 0 + w_unnormalized_data[0][0]
    for j in range(0, testing_set_unnormalized_data[i].shape[0] - 1):
        y_predict += testing_set_unnormalized_data[i][j] * w_unnormalized_data[j + 1][0]
    MSE_UN2 += (testing_set_unnormalized_data[i][-1] - y_predict) ** 2 # Tính MSE
    MAE_UN2 += abs(testing_set_unnormalized_data[i][-1] - y_predict) # Tính MAE
    print("{0:.2f} = {1}".format(y_predict,testing_set_unnormalized_data[i][-1]))
print("MSE testing set unnormalized data: {0:.2f}".format(MSE_UN2 / testing_set_unnormalized_data.shape[0]))
print("MAE testing set unnormalized data: {0:.2f}".format(MAE_UN2 / testing_set_unnormalized_data.shape[0]))

print()

print("NORMALIZED DATA")

normalized_data = np.array(data[['RM', 'PTRATIO', 'LSTAT', 'MEDV']]) # Bộ dữ liệu normalized chỉ lấy 3 thuộc tính để
                                                                     # dự đoán MEDV là RM, PTRATIO, LSTAT
#np.random.shuffle(normalized_data) # Trộn dữ liệu mỗi lần thử để đảm bảo tính khách quan

training_set_normalized_data = normalized_data[101:507] # Tạo training set
testing_set_normalized_data = normalized_data[0:101] # Tạo testing set

ones = np.array([np.ones_like(training_set_normalized_data.T[0])]).T
ones_and_training_set = np.concatenate((ones, training_set_normalized_data), axis=1)

X_normalized_data = ones_and_training_set.T[0:4].T # X của training set
Y_normalized_data = np.array([ones_and_training_set.T[-1]]).T # Y của training set

A_normalized_data = np.dot(X_normalized_data.T, X_normalized_data) # A = X.T * X
b_normalized_data = np.dot(X_normalized_data.T, Y_normalized_data) # b = X.T * Y

w_normalized_data = np.dot(np.linalg.pinv(A_normalized_data), b_normalized_data) # w = 1/A * b

print("w[]:", end=' ') # In các giá trị w
for i in range(w_normalized_data.shape[0]):
    print("w{0} = {1}".format(i, w_normalized_data[i][0]), end=' ')
print()

MSE_N1 = 0
MSE_N2 = 0
MAE_N1 = 0
MAE_N2 = 0

for i in range(training_set_normalized_data.shape[0]):
    y_predict = 0 + w_normalized_data[0][0]
    for j in range(0, training_set_normalized_data[i].shape[0] - 1):
        y_predict += training_set_normalized_data[i][j] * w_normalized_data[j + 1][0]
    MSE_N1 += (training_set_normalized_data[i][-1] - y_predict) ** 2 # Tính MSE
    MAE_N1 += abs(training_set_normalized_data[i][-1] - y_predict) # Tính MAE
    #print("{0:.2f} = {1}".format(x_normalized_data,training_set_normalized_data[i][-1]))
print("MSE training set normalized data: {0:.2f}".format(MSE_N1 / training_set_normalized_data.shape[0]))
print("MAE training set normalized data: {0:.2f}".format(MAE_N1 / training_set_normalized_data.shape[0]))

print()
print("Ket qua du doan tren testing set:")
for i in range(testing_set_normalized_data.shape[0]):
    y_predict = 0 + w_normalized_data[0][0]
    for j in range(0, testing_set_normalized_data[i].shape[0] - 1):
        y_predict += testing_set_normalized_data[i][j] * w_normalized_data[j + 1][0]
    MSE_N2 += (testing_set_normalized_data[i][-1] - y_predict) ** 2 # Tính MSE
    MAE_N2 += abs(testing_set_normalized_data[i][-1] - y_predict) # Tính MAE
    print("{0:.2f} = {1}".format(y_predict,testing_set_normalized_data[i][-1]))
print("MSE testing set normalized data: {0:.2f}".format(MSE_N2 / testing_set_normalized_data.shape[0]))
print("MAE testing set normalized data: {0:.2f}".format(MAE_N2 / testing_set_normalized_data.shape[0]))
