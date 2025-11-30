import numpy as np

to_kcal = (627.509, "kcal/mol")
to_mev = (27.2114 * 1000, "meV")
to_hartree = (1, "Hartree")
to_cm_1 = (2.194746 * 10**5, r"$\mathrm{cm}^{-1}$")
to_K = (3.1577464 * 10**5, "K")


def helgaker_hf_cbs(E_x, E_y):
    a = 1.63
    return (E_y - (E_x * np.exp(-a))) / (1 - np.exp(-a))


def cc_helgaker_cbs_2pts(E_X, E_Y, X, Y):
    return (E_X * X**3 - E_Y * Y**3) / (X**3 - Y**3)
