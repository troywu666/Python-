'''
@Description: 
@Version: 1.0
@Autor: Troy Wu
@Date: 2020-06-29 11:15:05
@LastEditors: Troy Wu
@LastEditTime: 2020-06-29 16:04:39
'''
import numpy as np

class OLSLinearRegression:
    '''基于最小二乘法的线性回归'''
    def _ols(self, X, y):
        '''最小二乘法估算W'''
        tmp = np.linalg.inv(np.matmul(X.T, X))
        tmp = np.matmul(tmp, X.T)
        return np.matmul(tmp, y)
    
    def _preprocess_data_X(self, X):
        '''数据预处理'''
        m, n = X.shape
        X_ = np.empty((m, n+1))
        X_[:, 0] = 1
        X_[:, 1: ] = X
        return X_

    def train(self, X_train, y_train):
        '''训练模型'''
        X_train = self._preprocess_data_X(X_train)
        self.w = self._ols(X_train, y_train)
        
    def predict(self, X):
        '''预测'''
        X = self._preprocess_data_X(X)
        return np.matmul(X, self.w)

class GDLinearRegression:
    def __init__(self, n_iter = 200, eta = 1e-3, tol = None):
        # 训练迭代次数
        self.n_iter = n_iter
        # 学习率
        self.eta = eta
        # 误差变化阈值
        self.tol = tol
        # 模型参数w（训练时初始化）
        self.w = None

    def _loss(self, y, y_pred):
        '''计算损失'''
        return np.sum((y_pred - y) ** 2) / y.size

    def _gradient(self, X, y ,y_pred):
        '''计算梯度'''
        return np.matmul(y_pred - y, X) / y.size

    def _gradient_descent(self, w, X, y):
        '''梯度下降算法'''
        if self.tol is not None:
            loss_old = np.inf
        # 使用梯度下降，至多迭代n_iter次，更新w
        for step_i in range(self.n_iter):
            y_pred = self._predict(X, w)
            # 计算损失
            loss = self._loss(y, y_pred)
            print('Epoch is {}. The loss is {}'.format(step_i, loss))
            
            # 早期停止法
            if self.tol is not None:
                if loss_old - loss < self.tol:
                    break
                loss_old = loss
            # 计算梯度
            grad = self._gradient(X, y, y_pred)
            # 更新参数
            w -= self.eta * grad

    def _preprocess_data_X(self, X):
        '''数据预处理'''
        m, n = X.shape
        X_ = np.empty((m, n + 1))
        X_[:, 0] = 1
        X_[:, 1: ] = X
        return X_

    def train(self, X_train, y_train):
        '''训练'''
        X_train = self._preprocess_data_X(X_train)
        # 初始化参数向量w
        _, n = X_train.shape
        self.w = np.random.random(n) * 0.5
        
        # 执行梯度下降训练w
        self._gradient_descent(self.w, X_train, y_train)
    
    def _predict(self, X, w):
        '''预测内部接口'''
        return np.matmul(X, w)
    
    def predict(self, X):
        X = self._preprocess_data_X(X)
        return self._predict(X, self.w)