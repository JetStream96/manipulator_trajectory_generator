import numpy as np
from typing import List, Dict
import matplotlib.pyplot as plt
import sys

def main():
    # list lengths are n, 2, 2, n+1, n+1 => total: 3n+6
    args = sys.argv[1:]
    n = (len(args) - 6) / 3

    if n%1!=0 or n<2:
        print("Invalid input")
        return
    
    n = int(n)
    method = [int(args[i]) for i in range(0, n)]
    init = args[n:n+2]
    final = args[n+2:n+4]
    times = [float(args[i]) for i in range(n+4, 2*n+5)]
    angles = [float(args[i]) for i in range(2*n+5, 3*n+6)]
    
    X = solve(method, init, final, times, angles)
    print("X = ")
    print(X)

    polys = get_polys(method, X)
    for i in polys:
        print(i)
    
    plot(polys, times, angles)

def get_polys(methods, X):
    result = []
    index = 0
    for i in range(0, len(methods)):
        count = methods[i]+1
        result.append([X[index+i] for i in range(0, count)])
        index += count

    return result

def sum(list):
    sum = 0
    for i in list:
        sum += i

    return sum

def get_poly(method) -> List[List[int]]:
    return [get_poly_order(n) for n in method]

def get_poly_order(n: int):
    ''' 
    Coefficients of polynomial, without a_ij's.
    E.g. 1 + 2*t + 3*t^2 is represented as [1, 2, 3].
    This returns the initial coefficients, which are all 1.
    '''    
    return [1 for i in range(0, n+1)]

def differentiate(poly: List[int]):
    return [poly[i+1]*(i+1) for i in range(0, len(poly)-1)]

def apply_poly(poly: List[int], t):
    '''
    E.g. The polynomial is a_0 + 2*a_1*t + 3*a_2*t^2, poly should be [1, 2, 3],
    this returns [1, 2*t, 3*t^2].
    '''
    return [poly[i]*t**i for i in range(0, len(poly))]

def transform_to_matrix_row(method, segment_index, poly) -> List[int]:
    '''
    segment_index is 0 to len(method)-1 
    '''
    row = []
    for i in range(0, len(method)):
        if i==segment_index:
            row += poly
        else:
            row += [0 for j in range(0, method[i]+1)]
    
    return row

def subtract_each(x, y):
    if len(x)!=len(y):
        raise Exception()
    
    return [x[i]-y[i] for i in range(0, len(x))]

def solve(method, init, final, times, angles):
    poly = get_poly(method)

    # Y = AX
    A_rows = []
    Y = []

    # If the current index is i+1, these are the velocity and acceleration coefficients
    # of a_i_0 to a_i_m_i at times[i+1].
    last_vel_end_row = None
    last_acc_end_row = None

    for i in range(0, len(method)):
        t=times[i]
        angle = poly[i]
        vel = differentiate(angle)
        acc = differentiate(vel)

        # angle        
        A_rows.append(transform_to_matrix_row(method, i, apply_poly(angle, t)))
        Y.append(angles[i])
        A_rows.append(transform_to_matrix_row(method, i, apply_poly(angle, times[i+1])))
        Y.append(angles[i+1])

        # Coefficients of a_i's at the start/end of the segment
        vel_start = [0]+apply_poly(vel, t)
        acc_start = [0,0]+apply_poly(acc, t)
        vel_end = [0]+apply_poly(vel, times[i+1])
        acc_end = [0,0]+apply_poly(acc, times[i+1])

        vel_start_row = transform_to_matrix_row(method, i, vel_start)
        acc_start_row = transform_to_matrix_row(method, i, acc_start)
        vel_end_row = transform_to_matrix_row(method, i, vel_end)
        acc_end_row = transform_to_matrix_row(method, i, acc_end)

        if i==0:
            # initial vel/acc
            if init[0] != ':':
                A_rows.append(vel_start_row)
                Y.append(float(init[0]))

            if init[1] != ':':
                A_rows.append(acc_start_row)
                Y.append(float(init[1]))
        elif i==len(method)-1:
            # final vel/acc
            if final[0] != ':':
                A_rows.append(vel_end_row)
                Y.append(float(final[0]))

            if final[1] != ':':
                A_rows.append(acc_end_row)
                Y.append(float(final[1]))
        
        if i!=0:
            # vel and acc should match the last index
            A_rows.append( subtract_each(vel_start_row, last_vel_end_row))
            A_rows.append(subtract_each(acc_start_row, last_acc_end_row))
            Y+=[0,0]
        
        last_vel_end_row=vel_end_row
        last_acc_end_row=acc_end_row

    A = np.array(A_rows)
    Y_array = np.array(Y)

    print("A = ")
    print(A)

    print("Y = ")
    print(Y_array)

    X = np.linalg.solve(A, Y_array)
    return X

def plot(polys, times, angles):
    for i in range(0, len(polys)):
        step = 0.05
        t = np.arange(times[i], times[i+1]+step, step)
        plt.plot(t, sum(apply_poly(polys[i], t)))
        
    plt.show()

main()
