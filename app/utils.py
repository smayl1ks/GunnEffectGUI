#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : utils.py
#Revise : 16-07-2024
#----------------------------------------------------------------------------

import csv
import numpy as np

def read_profile(nameFile, columns):
    """
    Function for reading data from files
    with csv extension. Data is written in columns
    :param nameFile: file name
    :param columns: count
    :return: list containing numpy arrays of column elements
    """
    if not nameFile.endswith(("txt", "csv")):
        raise TypeError("Файл должен иметь расширение csv или txt")

    if columns == 1:
        with open(nameFile, "r") as file:
            reader = csv.reader(file, delimiter=',')
            data = [float(row[0]) for row in reader]
            return np.array(data)

    data = []
    for i in range(columns):
        with open(nameFile, "r") as file:
            tmp = [float(row[i]) for row in csv.reader(file, delimiter=',')]
            data.append(tmp)

    return np.array(data)

def create_Gi(x0, d, GiMax, x):
    """
    Create Gi
    :return: Gi
    """

    ArraySize = len(x)
    Gi = np.zeros(ArraySize)

    for i in range(ArraySize):
        if (x0 - d/2) <= x[i] <= (x0 + d/2):
            Gi[i] = GiMax*(1 + np.cos(2*np.pi*(x[i] - x0)/d))/2

    return Gi

def validate_float(value, scale):
    try:
        return float(value) * scale
    except ValueError:
        raise ValueError("Данные должны иметь тип float")
