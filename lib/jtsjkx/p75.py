# -*- coding: UTF-8 -*-
import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model


def trainModel(trainData, features, labels):
    """
    利用训练数据，估计模型参数
    :param trainData: DataFrame，训练数据集，包含特征和标签
    :param features: 特征名列表
    :param labels： 标签名列表
    :return: model: LinearRegression，训练好的线性模型
    """
    model = linear_model.LinearRegression()
    model.fit(trainData[features], trainData[labels])
    return model


def evaluateModel(model, testData, features, labels):
    """
    计算线性模型的均方差和决定系数
    :param model: LinearRegression, 训练完成的线性模型
    :param testData: DataFrame，测试数据
    :param features: list[str]，特征名列表
    :param labels: list[str]，标签名列表
    :return:
    error: np.float64，均方差
    score: np.float64，决定系数
    """
    # 均方差（The mean squared error）， 均方差越小越好
    error = np.mean((model.predict(testData[features]) - testData[labels]) ** 2)
    # 决定系数（Coefficient of determination），决定系数月接近1越好
    score = model.score(testData[features], testData[labels])
    return error, score


def visualizeModel(model, data, features, lables, error, score):
    """
    模型可视化
    :param model:
    :param data:
    :param features:
    :param lables:
    :param error:
    :param score:
    :return:
    """


def linearModel(data):
    """
    线性回归模型建模步骤展示
    :param data: DataFrame，建模数据
    :return:
    """
    features = ["x"]
    labels = ["y"]
    # 将输入数据划分为训练集和测试集数据
    trainData = data[:15]
    testData = data[15:]
    # 产生并训练模型
    model = trainModel(trainData, features, labels)
    # 评价模型效果
    error, score = evaluateModel(model, testData, features, labels)
    # 图形化模型结果
    visualizeModel(model, data, features, labels, error, score)
