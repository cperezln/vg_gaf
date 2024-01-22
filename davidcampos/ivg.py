import numpy as np
import matplotlib.pyplot as plt


def isVisible(x, horizontal=False):
    n = len(x)
    if n <= 2:
        return True
    if not horizontal:
        aux = (x[n - 1] - x[0]) / (n - 1)
        return all(x[k] < x[0] + k * aux for k in range(1, n - 1))
    else:
        aux = min(x[0], x[n - 1])
        return all(x[k] < aux for k in range(1, n - 1))


def ivg(im, horizontal=False):
    n = len(im)
    edgesL = []
    edgesR = []
    for i in range(n):
        for j in range(n):
            # Filas
            for k in range(1, n - j):
                if isVisible([im[i][j + m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i, j + k))
            # Columnas
            for k in range(1, n - i):
                if isVisible([im[i + m][j] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j))
            # Diagonales principales
            for k in range(1, min(n - i, n - j)):
                if isVisible([im[i + m][j + m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j + k))
            # Antidiagonales
            for k in range(1, min(n - i, j)):
                if isVisible([im[i + m][j - m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j - k))
    return (edgesL, edgesR)


def ivg2(im, horizontal=False):
    n = len(im)
    edgesL = []
    edgesR = []
    for i in range(n):
        for j in range(n):
            # Filas
            for k in range(1, n - j):
                if isVisible([im[i][j + m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i, j + k))
            # Columnas
            for k in range(1, n - i):
                if isVisible([im[i + m][j] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j))
            # Diagonales principales
            for k in range(1, min(n - i, n - j)):
                if isVisible([im[i + m][j + m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j + k))
            # Antidiagonales
            for k in range(1, min(n - i, j)):
                if isVisible([im[i + m][j - m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j - k))
            # Otras diagonales
            for k in range(1, min(n - i, int(np.floor((n - j) / 2)))):
                if isVisible([im[i + m][j + 2 * m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j + 2 * k))
            for k in range(1, min(int(np.floor((n - i) / 2)), n - j)):
                if isVisible([im[i + 2 * m][j + m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + 2 * k, j + k))
            for k in range(1, min(n - i, int(np.floor(j / 2)))):
                if isVisible([im[i + m][j - 2 * m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j - 2 * k))
            for k in range(1, min(int(np.floor((n - i) / 2)), n - j)):
                if isVisible([im[i + 2 * m][j - m] for m in range(k + 1)], horizontal):
                    edgesL.append((i, j))
                    edgesR.append((i + 2 * k, j - k))
    return (edgesL, edgesR)


def degMat(n, edgesL, edgesR):
    deg = [[0] * n for _ in range(n)]
    edges = edgesL + edgesR
    for (i, j) in edges:
        deg[i][j] += 1
    return deg


# def clustCoeff(i, j, n, edgesL, edgesR):
#     neighbors = []
#     for (k, l) in zip(edgesL, edgesR):
#         if k == (i, j):
#             neighbors.append(l)
#         if l == (i, j):
#             neighbors.append(k)
#     deg = len(neighbors)
#     coeff = 2 * sum(1 for x, y in zip(edgesL, edgesR)
#                     if x in neighbors and y in neighbors) / (deg * (deg - 1))
#     return coeff


def clustCoeff(i, j, n, edgesL, edgesR):
    neighbors = set()
    for (k, l) in zip(edgesL, edgesR):
        if k == (i, j):
            neighbors.add(l)
        if l == (i, j):
            neighbors.add(k)
    deg = len(neighbors)
    lambdav = 0
    for neighbor1 in neighbors:
        for neighbor2 in neighbors:
            if neighbor1 in edgesL and neighbor2 in edgesR:
                lambdav += 1
    tauv = deg * (deg - 1) // 2
    coeff = lambdav / tauv
    return coeff


def clustMat(n, edgesL, edgesR):
    M = [[clustCoeff(i, j, n, edgesL, edgesR) for j in range(n)] for i in range(n)]
    return M


def createNoise(n):
    r = np.random.normal(0, 1, pow(n, 2))
    maxr = max(r)
    minr = min(r)
    rnorm = [510 * (i - minr) / (maxr - minr) - 255 for i in r]
    noise = [[rnorm[(j - 1) * n + i] for j in range(n)] for i in range(n)]
    return noise


def addNoise(image, noise, coeff):
    return np.clip(
        [[z + coeff * w for (z, w) in zip(x, y)] for (x, y) in zip(image, noise)], 0, 255)


def flatten(xss):
    return [x for xs in xss for x in xs]


def getIvgs(image, noiseCoeff, horizontal=False):
    image = np.array(image).tolist()
    n = len(image)
    noise = createNoise(n)
    imageNoise = addNoise(image, noise, noiseCoeff)

    imageEdges = ivg(image, horizontal)
    imageNoiseEdges = ivg(imageNoise, horizontal)
    noiseEdges = ivg(noise, horizontal)

    imageEdges2 = ivg2(image, horizontal)
    imageNoiseEdges2 = ivg2(imageNoise, horizontal)
    noiseEdges2 = ivg2(noise, horizontal)
    return (image, imageNoise, noise,
            imageEdges, imageNoiseEdges, noiseEdges,
            imageEdges2, imageNoiseEdges2, noiseEdges2)


def compareDeg(image, imageNoise, noise,
               imageEdges, imageNoiseEdges, noiseEdges,
               imageEdges2, imageNoiseEdges2, noiseEdges2):
    n = len(image)

    imageMat = degMat(n, imageEdges[0], imageEdges[1])
    imageNoiseMat = degMat(n, imageNoiseEdges[0], imageNoiseEdges[1])
    noiseMat = degMat(n, noiseEdges[0], noiseEdges[1])

    imageMat2 = degMat(n, imageEdges2[0], imageEdges2[1])
    imageNoiseMat2 = degMat(n, imageNoiseEdges2[0], imageNoiseEdges2[1])
    noiseMat2 = degMat(n, noiseEdges2[0], noiseEdges2[1])

    imageHist = flatten(imageMat)
    imageNoiseHist = flatten(imageNoiseMat)
    noiseHist = flatten(noiseMat)

    imageHist2 = flatten(imageMat2)
    imageNoiseHist2 = flatten(imageNoiseMat2)
    noiseHist2 = flatten(noiseMat2)

    f, (im,
        imNo,
        no) = plt.subplots(3, 5)
    f.set_figwidth(15)
    f.set_figheight(9)

    im[0].imshow(image, cmap='gray', vmin=0, vmax=255)
    im[0].axis('off')
    im[1].imshow(imageMat, cmap='gray')
    im[1].axis('off')
    im[2].imshow(imageMat2, cmap='gray')
    im[2].axis('off')
    im[3].hist(imageHist, bins=max(imageHist))
    im[3].set_xlim([0, max(imageHist + imageNoiseHist + noiseHist)])
    im[4].hist(imageHist2, bins=max(imageHist2))
    im[4].set_xlim([0, max(imageHist2 + imageNoiseHist2 + noiseHist2)])

    imNo[0].imshow(imageNoise, cmap='gray', vmin=0, vmax=255)
    imNo[0].axis('off')
    imNo[1].imshow(imageNoiseMat, cmap='gray')
    imNo[1].axis('off')
    imNo[2].imshow(imageNoiseMat2, cmap='gray')
    imNo[2].axis('off')
    imNo[3].hist(imageNoiseHist, bins=max(imageNoiseHist))
    imNo[3].set_xlim([0, max(imageHist + imageNoiseHist + noiseHist)])
    imNo[4].hist(imageNoiseHist2, bins=max(imageNoiseHist2))
    imNo[4].set_xlim([0, max(imageHist2 + imageNoiseHist2 + noiseHist2)])

    no[0].imshow(noise, cmap='gray', vmin=-255, vmax=255)
    no[0].axis('off')
    no[1].imshow(noiseMat, cmap='gray')
    no[1].axis('off')
    no[2].imshow(noiseMat2, cmap='gray')
    no[2].axis('off')
    no[3].hist(noiseHist, bins=max(noiseHist))
    im[3].set_xlim([0, max(imageHist + imageNoiseHist + noiseHist)])
    no[4].hist(noiseHist2, bins=max(noiseHist2))
    im[4].set_xlim([0, max(imageHist2 + imageNoiseHist2 + noiseHist2)])
    return None