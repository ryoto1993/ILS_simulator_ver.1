# coding: UTF-8


def calc_regression_coefficient(dataset_a, dataset_b):
    if len(dataset_a) != len(dataset_b):
        print("相関係数の計算ができません．データセットの数が異なります．")
        return 0, 0

    num = len(dataset_a)

    sum_pow_a = 0
    sum_ab = 0
    sum_a = 0
    sum_b = 0

    for i in range(num):
        sum_pow_a += dataset_a[i]**2
        sum_a += dataset_a[i]
        sum_b += dataset_b[i]
        sum_ab += dataset_a[i] * dataset_b[i]

    denominator = num * sum_pow_a - sum_a**2
    if denominator == 0:
        denominator = 0.05

    a = (num * sum_ab - sum_a * sum_b) / denominator
    b = (num * sum_pow_a * sum_b - sum_a * sum_ab) / denominator

    return a, b
