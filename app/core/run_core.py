#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : run_core.py
#Revise : 17-07-2024
#----------------------------------------------------------------------------
# Численное моделирование нелинейной динамики пространственного заряда,
# электрического поля и тока в структурах GaAs
# в условиях локализованного оптического
# воздействия в активной области структуры
#----------------------------------------------------------------------------
from numpy import zeros, float64, array, savetxt
from app.core.algorithm import *
from app.settings import WRITE_FREQUENCY, PROFILES_DICT
from app.utils import read_profile

import time

def run_core(U0, shr_j, shr_E, shr_ne, shr_p, shr_Gi,
                  sleep_time, should_terminate):
    #----------------------------------------------------------------------------
    # Массивы
    #----------------------------------------------------------------------------
    Nd    = zeros(ArraySizePy, dtype=float64)
    ne    = zeros(ArraySizePy, dtype=float64)
    E     = zeros(ArraySizePy, dtype=float64)
    v_n   = zeros(ArraySizePy, dtype=float64)
    v_p   = zeros(ArraySizePy, dtype=float64)
    j     = zeros(ArraySizePy, dtype=float64)
    #----------------------------------------------------------------------------
    p     = zeros(ArraySizePy, dtype=float64)
    ne0_x = zeros(ArraySizePy, dtype=float64)
    Fi    = zeros(ArraySizePy, dtype=float64)
    #----------------------------------------------------------------------------
    ain  = -Dn/(h*h)
    aip  = -Dp/(h*h)
    bi  = zeros(ArraySizePy, dtype=float64)
    ci  = zeros(ArraySizePy, dtype=float64)
    di  = zeros(ArraySizePy, dtype=float64)
    A_i = zeros(ArraySizePy, dtype=float64)
    B_i = zeros(ArraySizePy, dtype=float64)
    #----------------------------------------------------------------------------

    #savetxt('profiles/x.csv', x, delimiter=',', fmt='%.6e')
    #savetxt('profiles/DATA51N.csv', Nd, delimiter=',', fmt='%.6e')

    Nd = read_profile(PROFILES_DICT["DATA51N.csv"], 1)
    ne0_x = read_profile(PROFILES_DICT["n0(x).txt"], 1)

    E = E + U0.value/L

    velocity_n(v_n, E)
    velocity_p(v_p, E)
    #----------------------------------------------------------------------------

    U  = 0
    jt = 0
    CNT  = 0

    while not should_terminate.value:
        CNT += 1
        Gi = array(shr_Gi[:])
        fdtd_n(p, ne, ne0_x, v_n, Gi, Nd, ain, bi, ci, di, A_i, B_i)
        fdtd_p(p, v_p, Gi, aip, bi, ci, di, A_i, B_i)

        E_np(E, p, ne, Nd)
        U  = integral(E)
        dU = U - U0.value
        E  = E - dU/L

        velocity_n(v_n, E)
        velocity_p(v_p, E)
    
        j_t(j, ne, p, v_n, v_p)
        jt  = (integral(j)/L)*1E-4

        if not(CNT % WRITE_FREQUENCY):
            CNT = 0
            while sleep_time.value == 100:
                time.sleep(0.5)

            if sleep_time.value:
                time.sleep(sleep_time.value / 1000) # мс

            shr_j[0:-1] = shr_j[1:]
            shr_j[-1] = jt
            shr_E[:] = E*1E-5
            shr_ne[:] = ne*1E-6
            shr_p[:] = p*1E-6