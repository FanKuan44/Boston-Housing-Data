import pandas as pd
import numpy as np

def cost_unnormalized_data(w): # Hàm tính độ lỗi (cost function):  1/N * norm(Y - Y_predict, 2) ** 2
    N = X_unnormalized_data.shape[0]
    return 1/N * np.linalg.norm(Y_unnormalized_data - X_unnormalized_data.dot(w), 2) ** 2

def cost_normalized_data(w): # Hàm tính độ lỗi (cost function): 1/N * norm(Y - Y_predict, 2) ** 2
    N = X_normalized_data.shape[0]
    return 1/N * np.linalg.norm(Y_normalized_data - X_normalized_data.dot(w), 2) ** 2

def grad_unnormalized_data(w): # Hàm tính đạo hàm cost function: 2/N * X.T * (X.W - Y)
    N = X_unnormalized_data.shape[0]
    return 2 / N * X_unnormalized_data.T.dot(X_unnormalized_data.dot(w) - Y_unnormalized_data)

def grad_normalized_data(w): # Hàm tính đạo hàm cost function: 2/N * X.T * (X.W - Y)
    N = X_normalized_data.shape[0]
    return 2 / N * X_normalized_data.T.dot(X_normalized_data.dot(w) - Y_normalized_data)

def batch_gd_unnormalize_data(w_init, lrate, gamma): # Batch Gradient Descent On Unnormalized Data
    v_old = np.zeros_like(w_init)
    #loss = []
    w = [w_init]
    it = 0
    for it in range(1000000):
        v_new = gamma * v_old + lrate * grad_unnormalized_data(w[-1] - gamma * v_old) # Dùng kĩ thuật momentum và NAG
        w_new = w[-1] - v_new                                                         # để tối ưu độ chính xác
        #loss.append(cost_unnormalized_data(w[-1]))
        if abs(cost_unnormalized_data(w_new) - cost_unnormalized_data(w[-1])) < 0.00001: # Điều kiện dừng
            break
        if cost_unnormalized_data(w[-1]) - cost_unnormalized_data(w_new) > 0.000001: # Nếu độ lỗi giảm chậm thì tăng
            lrate *= 1.00001                                                         # learning rate
        v_old = v_new
        w.append(w_new)
    return w[-1], it # Trả về w và số lần lặp

def batch_gd_normalize_data(w_init, eta, gamma): # Batch Gradient Descent On Normalized Data
    v_old = np.zeros_like(w_init)
    #loss = []
    w = [w_init]
    it = 0
    for it in range(1000000):
        v_new = gamma * v_old + eta * grad_normalized_data(w[-1] - gamma * v_old) # Dùng kĩ thuật momentum và NAG
        w_new = w[-1] - v_new                                                     # để tối ưu độ chính xác
        #loss.append(cost_unnormalized_data(w[-1]))
        if abs(cost_normalized_data(w_new) - cost_normalized_data(w[-1])) < 0.00001: # Điều kiện dừng
            break
        if cost_normalized_data(w[-1]) - cost_normalized_data(w_new) > 0.000001: # Nếu độ lỗi giảm chậm thì tăng
            eta = eta * 1.00001                                                  # learning rate
        v_old = v_new
        w.append(w_new)
    return w[-1], it #Trả về w và số lần lặp

# Input data set
data = pd.read_csv('housing.data.csv')

# UNNORMALIZED DATA

unnormalized_data = np.array(
    data[['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RED', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']])

#np.random.shuffle(unnormalized_data) # Trộn dữ liệu mỗi lần thử để đảm bảo tính khách quan

training_set_unnormalized_data = unnormalized_data[101:507] # Tạo training set
testing_set_unnormalized_data = unnormalized_data[0:101] # Tạo testing set

ones = np.array([np.ones_like(training_set_unnormalized_data.T[0])]).T
ones_and_training_set = np.concatenate((ones, training_set_unnormalized_data), axis=1)

X_unnormalized_data = ones_and_training_set.T[0:14].T # X của training set
Y_unnormalized_data = np.array([ones_and_training_set.T[-1]]).T # Y của training set

# Training
w_init = np.array([np.zeros(training_set_unnormalized_data.T.shape[0])]).T # Khởi tạo w ban đầu [0. ... 0.]
w_unnormalized_data,it = batch_gd_unnormalize_data(w_init, 0.0000001, 0.9) # Tính w, chọn learing rate
                                                                           # ban đầu là 10^-7
                                                                           # và hệ số gamma là 0.9

print("UNNORMALIZED DATA")

print("Da tinh toan duoc w sau {0} vong lap.".format(it)) # In ra số vòng lặp đã thực hiện
print("w[]:", end=' ') #In các giá trị w
for i in range(w_unnormalized_data.shape[0]):
    print("w{0} = {1}".format(i, w_unnormalized_data[i][0]), end=' ')
print()

MSE_UN1 = 0
MSE_UN2 = 0
MAE_UN1 = 0
MAE_UN2 = 0

for i in range(training_set_unnormalized_data.shape[0]):
    y_predict = 0 + w_unnormalized_data[0][0]
    for j in range(0, training_set_unnormalized_data[i].shape[0] - 1):
        y_predict += training_set_unnormalized_data[i][j] * w_unnormalized_data[j + 1][0]
    MSE_UN1 += (training_set_unnormalized_data[i][-1] - y_predict) ** 2 # Tính MSE
    MAE_UN1 += abs(training_set_unnormalized_data[i][-1] - y_predict) # Tính MAE
    #print("{0:.2f} = {1}".format(x_unnormalized_data,training_set_unnormalized_data[i][-1]))
print("MSE in training unnormalized data: {0:.2f}".format(MSE_UN1 / training_set_unnormalized_data.shape[0]))
print("MAE in training unnormalized data: {0:.2f}".format(MAE_UN1 / training_set_unnormalized_data.shape[0]))

print()
print("Ket qua du doan tren testing set:")
for i in range(testing_set_unnormalized_data.shape[0]):
    y_predict = 0 + w_unnormalized_data[0][0]
    for j in range(0, testing_set_unnormalized_data[i].shape[0] - 1):
        y_predict += testing_set_unnormalized_data[i][j] * w_unnormalized_data[j + 1][0]
    MSE_UN2 += (testing_set_unnormalized_data[i][-1] - y_predict) ** 2 # Tính MSE
    MAE_UN2 += abs(testing_set_unnormalized_data[i][-1] - y_predict) # Tính MAE
    print("{0:.2f} = {1}".format(y_predict,testing_set_unnormalized_data[i][-1])) # In các giá trị dự đoán
                                                                                  # trên testing set

print("MSE testing set unnormalized data: {0:.2f}".format(MSE_UN2 / testing_set_unnormalized_data.shape[0]))
print("MAE testing set unnormalized data: {0:.2f}".format(MAE_UN2 / testing_set_unnormalized_data.shape[0]))
print()

# NORMALIZED DATA

normalized_data = np.array(data[['RM', 'PTRATIO', 'LSTAT', 'MEDV']]) # Bộ dữ liệu normalized chỉ lấy 3 thuộc tính để
                                                                     # dự đoán MEDV là RM, PTRATIO, LSTAT
#np.random.shuffle(normalized_data) # Trộn dữ liệu mỗi lần thử để đảm bảo tính khách quan

training_set_normalized_data = normalized_data[101:507] # Tạo training set
testing_set_normalized_data = normalized_data[0:101] # Tạo testing set

ones = np.array([np.ones_like(training_set_normalized_data.T[0])]).T
ones_and_training_set = np.concatenate((ones, training_set_normalized_data), axis=1)

X_normalized_data = ones_and_training_set.T[0:4].T # X của training set
Y_normalized_data = np.array([ones_and_training_set.T[-1]]).T # Y của training set

#Training
w_init1 = np.array([np.zeros(training_set_normalized_data.T.shape[0])]).T # Khởi tạo w ban đầu [0. ... 0.]
w_normalized_data, it1 = batch_gd_normalize_data(w_init1, 0.0000001, 0.9) # Tính w, chọn learing rate
                                                                          # ban đầu là 10^-7
                                                                          # và hệ số gamma là 0.9

print("NORMALIZED DATA")

print("Da tinh toan duoc w sau {0} vong lap.".format(it1)) # In ra số vòng lặp đã thực hiện
print("w[]:", end = ' ') # In các giá trị w
for i in range(w_normalized_data.shape[0]):
    print("w{0} = {1}".format(i, w_normalized_data[i][0]), end=' ')
print()

MSE_N1 = 0
MSE_N2 = 0
MAE_N1 = 0
MAE_N2 = 0

for i in range(training_set_normalized_data.shape[0]):
    y_predict= 0 + w_normalized_data[0][0]
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
    print("{0:.2f} = {1}".format(y_predict,testing_set_normalized_data[i][-1])) # In các giá trị dự đoán
                                                                                # trên testing set
print("MSE testing set normalized data: {0:.2f}".format(MSE_N2 / testing_set_normalized_data.shape[0]))
print("MAE testing set normalized data: {0:.2f}".format(MAE_N2 / testing_set_normalized_data.shape[0]))
