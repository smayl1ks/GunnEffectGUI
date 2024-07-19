#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : algorithm.py
#Revise : 17-07-2024
#----------------------------------------------------------------------------
from numba import njit
#----------------------------------------------------------------------------
# Константы
#----------------------------------------------------------------------------
eps0  = 8.85E-12
eps   = 12.9
q     = 1.6E-19
Dn    = 3E-2
miun  = 0.8
vs    = 0.8E5
Ea    = 3.8*100000
#----------------------------------------------------------------------------
Dp    = 10.35E-4
miup  = 0.04
alfa  = 1E4
beta  = 1
tau   = 5E-9 # Время жизни для электронов и дырок
#----------------------------------------------------------------------------
# Параметры
#----------------------------------------------------------------------------
t  = 4.6E-13   # Шаг по времени
h  = 0.14E-6   # Шаг по координате
L  = 5.1842E-4
#----------------------------------------------------------------------------
const = (q*h)/(eps*eps0)
#----------------------------------------------------------------------------
L = h*round(L/h) # Длина активной области
ArraySize   = round(L/h)
ArraySizePy = ArraySize + 1
#----------------------------------------------------------------------------

# Numerical integration. Trapezoidal rule
@njit(fastmath=True)
def integral(a):
    n = len(a) - 1
    s = 0
    for i in range(n):
        s += (a[i] + a[i + 1]) * h / 2
    return s


# Drift velocity of electrons
@njit(fastmath=True)
def velocity_n(v_n, E):
    for i in range(ArraySizePy):
        if E[i] > 0 or E[i] == 0:
            sgn = 1
        else:
            sgn = -1
        v_n[i] = sgn * ((miun * abs(E[i]) + vs * (E[i] ** 4) / (Ea ** 4)) / (1 + (E[i] ** 4) / (Ea ** 4)))


# Drift velocity of holes
@njit(fastmath=True)
def velocity_p(p_v, E):
    for i in range(ArraySizePy):
        if E[i] > 0 or E[i] == 0:
            sgn = 1
        else:
            sgn = -1
        p_v[i] = sgn * (miup * abs(E[i]) / (1 + miup * abs(E[i]) / vs))


# Electric field
@njit(fastmath=True)
def E_np(E, p, ne, Nd):
    for i in range(ArraySize):
        E[i + 1] = E[i] + const * (ne[i] - Nd[i] - p[i])

    E[0] = E[1]
    E[ArraySize] = E[ArraySize - 1]

# Сurrent density
@njit(fastmath=True)
def j_t(j, ne, p, v_n, v_p):
    for i in range(ArraySize):
        j[i] = q * ne[i] * v_n[i] + q * p[i] * v_p[i] - q * Dn * (ne[i + 1] - ne[i]) / h + q * Dp * (
                    p[i + 1] - p[i]) / h
    j[ArraySize] = j[ArraySize - 1]


# Finite-difference time-domain for electrons
@njit(fastmath=True)
def fdtd_n(p, ne, ne0_x, v_n, Gi, Nd, ain, bi, ci, di, A_i, B_i):
    for i in range(1, ArraySize):
        bi[i] = 1 / t - 2 * ain - v_n[i] / h + (v_n[i] - v_n[i - 1]) / h
        ci[i] = v_n[i] / h + ain
        if p[i] != 0:
            di[i] = ne[i] / t + alfa * beta * Gi[i] * 1E6 - (ne[i] - ne0_x[i]) / tau
        else:
            di[i] = ne[i] / t + alfa * beta * Gi[i] * 1E6

    di[1] = di[1] - ain * ne[0]
    di[ArraySize - 1] = di[ArraySize - 1] - ci[ArraySize - 1] * ne[ArraySize]

    # Straight account
    A_i[1] = -(ci[1] / bi[1])
    B_i[1] = (di[1] / bi[1])
    for i in range(2, ArraySize - 1):
        e_i = ain * A_i[i - 1] + bi[i]
        A_i[i] = -(ci[i] / e_i)
        B_i[i] = (di[i] - ain * B_i[i - 1]) / e_i

    # Back account
    ne[ArraySize - 1] = (di[ArraySize - 1] - ain * B_i[ArraySize - 2]) / (bi[ArraySize - 1] + ain * A_i[ArraySize - 2])

    for i in range(ArraySize - 2, 0, -1):
        ne[i] = A_i[i] * ne[i + 1] + B_i[i]

    ne[0] = Nd[0]
    ne[ArraySize] = Nd[ArraySize]


# Finite-difference time-domain for holes
@njit(fastmath=True)
def fdtd_p(p, v_p, Gi, aip, bi, ci, di, A_i, B_i):
    for i in range(1, ArraySize):
        bi[i] = 1 / t - 2 * aip + v_p[i] / h - (v_p[i] - v_p[i - 1]) / h
        ci[i] = -v_p[i] / h + aip
        di[i] = p[i] / t + alfa * beta * Gi[i] * 1E6 - p[i] / tau

    di[1] = di[1] - aip * p[0]
    di[ArraySize - 1] = di[ArraySize - 1] - ci[ArraySize - 1] * p[ArraySize]

    # Straight account
    A_i[1] = -(ci[1] / bi[1])
    B_i[1] = (di[1] / bi[1])
    for i in range(2, ArraySize - 1):
        e_i = aip * A_i[i - 1] + bi[i]
        A_i[i] = -(ci[i] / e_i)
        B_i[i] = (di[i] - aip * B_i[i - 1]) / e_i

    # Back account
    p[ArraySize - 1] = (di[ArraySize - 1] - aip * B_i[ArraySize - 2]) / (bi[ArraySize - 1] + aip * A_i[ArraySize - 2])

    for i in range(ArraySize - 2, 0, -1):
        p[i] = A_i[i] * p[i + 1] + B_i[i]

    p[0] = 0
    p[ArraySize] = 0