import numpy as np
def svd_rv(F, flip=True):
    if (len(F.shape) == 2):
        F = F[None, :, :]


    d = F.shape[1]
    [U, S, VT] = np.linalg.svd(F)

    # check if S
    V = VT.transpose([0, 2, 1])

    I = np.tile(np.identity(d), (F.shape[0], 1, 1))
    S = I * S[:, None, :]

    L = I

    if flip:
        L[:, d-1, d-1] = np.linalg.det(U @ V)

    detU = np.linalg.det(U)
    detV = np.linalg.det(V)
    uI = np.logical_and(detU < 0, detV > 0)[:, None, None]
    vI = np.logical_and(detV < 0, detU > 0)[:, None, None]

    Ut = uI * U @ L + np.logical_not(uI) * U
    Vt = vI * V @ L + np.logical_not(vI) * V
    St = S @ L

    return Ut, St, Vt

def polar_svd(F, flip=True):
    if flip:
        [U, S, V] = svd_rv(F, flip=flip)
        VT = V.transpose([0, 2, 1])
    else:
        [U, s, VT] = np.linalg.svd(F)
        V = VT.transpose([0, 2, 1])
        I = np.tile(np.identity(d), (F.shape[0], 1, 1))
        S = I * S[:, None, :]

    R = U @ VT
    SS = V @ S @ VT

    return R, SS