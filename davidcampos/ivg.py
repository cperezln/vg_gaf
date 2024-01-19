import numpy as np
import matplotlib.pyplot as plt


def isVisible(x):
    n = len(x)
    if n <= 2:
        return True
    return all([x[k] < x[0] + k / (n - 1) * (x[n - 1] - x[0]) for k in range(1, n - 1)])


def ivg(im):
    n = len(im)
    edgesL = []
    edgesR = []
    for i in range(n):
        for j in range(n):
            # Filas
            for k in range(1, n - j):
                if isVisible([im[i][j + m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i, j + k))
            # Columnas
            for k in range(1, n - i):
                if isVisible([im[i + m][j] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j))
            # Diagonales principales
            for k in range(1, min(n - i, n - j)):
                if isVisible([im[i + m][j + m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j + k))
            # Antidiagonales
            for k in range(1, min(n - i, j)):
                if isVisible([im[i + m][j - m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j - k))
    return edgesL, edgesR


def ivg8(im):
    n = len(im)
    edgesL = []
    edgesR = []
    for i in range(n):
        for j in range(n):
            # Filas
            for k in range(1, n - j):
                if isVisible([im[i][j + m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i, j + k))
            # Columnas
            for k in range(1, n - i):
                if isVisible([im[i + m][j] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j))
            # Diagonales principales
            for k in range(1, min(n - i, n - j)):
                if isVisible([im[i + m][j + m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j + k))
            # Antidiagonales
            for k in range(1, min(n - i, j)):
                if isVisible([im[i + m][j - m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j - k))
            # Otras diagonales
            for k in range(1, min(n - i, int(np.floor((n - j) / 2)))):
                if isVisible([im[i + m][j + 2 * m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j + 2 * k))
            for k in range(1, min(int(np.floor((n - i) / 2)), n - j)):
                if isVisible([im[i + 2 * m][j + m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + 2 * k, j + k))
            for k in range(1, min(n - i, int(np.floor(j / 2)))):
                if isVisible([im[i + m][j - 2 * m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + k, j - 2 * k))
            for k in range(1, min(int(np.floor((n - i) / 2)), n - j)):
                if isVisible([im[i + 2 * m][j - m] for m in range(k + 1)]):
                    edgesL.append((i, j))
                    edgesR.append((i + 2 * k, j - k))
    return edgesL, edgesR


def degMat(n, edgesL, edgesR):
    M = [[0] * n for _ in range(n)]
    edges = edgesL + edgesR
    for (i, j) in edges:
        M[i][j] += 1
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


def compare(image, noiseCoeff):
    image = np.array(image).tolist()
    n = len(image)
    noise = createNoise(n)
    imageNoise = addNoise(image, noise, noiseCoeff)

    imageEdgesL, imageEdgesR = ivg(image)
    imageNoiseEdgesL, imageNoiseEdgesR = ivg(imageNoise)
    noiseEdgesL, edgesN2noiseEdgesR = ivg(noise)

    imageEdgesL2, imageEdgesR2 = ivg8(image)
    imageNoiseEdgesL2, imageNoiseEdgesR2 = ivg8(imageNoise)
    noiseEdgesL2, noiseEdgesR2 = ivg8(noise)

    imageMat = degMat(n, imageEdgesL, imageEdgesR)
    imageNoiseMat = degMat(n, imageNoiseEdgesL, imageNoiseEdgesR)
    noiseMat = degMat(n, noiseEdgesL, edgesN2noiseEdgesR)

    imageMat2 = degMat(n, imageEdgesL2, imageEdgesR2)
    imageNoiseMat2 = degMat(n, imageNoiseEdgesL2, imageNoiseEdgesR2)
    noiseMat2 = degMat(n, noiseEdgesL2, noiseEdgesR2)

    imageHist = flatten(imageMat)
    imageNoiseHist = flatten(imageNoiseMat)
    noiseHist = flatten(noiseMat)

    imageHist2 = flatten(imageMat2)
    imageNoiseHist2 = flatten(imageNoiseMat2)
    noiseHist2 = flatten(noiseMat2)

    f, ((im1, im2, im3, im4, im5),
        (imNo1, imNo2, imNo3, imNo4, imNo5),
        (no1, no2, no3, no4, no5)) = plt.subplots(3, 5)
    f.set_figwidth(15)
    f.set_figheight(9)

    im1.imshow(image, cmap='gray', vmin=0, vmax=255)
    im1.axis('off')
    im2.imshow(imageMat, cmap='gray')
    im2.axis('off')
    im3.imshow(imageMat2, cmap='gray')
    im3.axis('off')
    im4.hist(imageHist, bins=max(imageHist + imageNoiseHist + noiseHist))
    im5.hist(imageHist2, bins=max(imageHist2 + imageNoiseHist2 + noiseHist2))

    imNo1.imshow(imageNoise, cmap='gray', vmin=0, vmax=255)
    imNo1.axis('off')
    imNo2.imshow(imageNoiseMat, cmap='gray')
    imNo2.axis('off')
    imNo3.imshow(imageNoiseMat2, cmap='gray')
    imNo3.axis('off')
    imNo4.hist(imageNoiseHist, bins=max(imageHist + imageNoiseHist + noiseHist))
    imNo5.hist(imageNoiseHist2, bins=max(imageHist2 + imageNoiseHist2 + noiseHist2))

    no1.imshow(noise, cmap='gray', vmin=0, vmax=255)
    no1.axis('off')
    no2.imshow(noiseMat, cmap='gray')
    no2.axis('off')
    no3.imshow(noiseMat2, cmap='gray')
    no3.axis('off')
    no4.hist(noiseHist, bins=max(imageHist + imageNoiseHist + noiseHist))
    no5.hist(noiseHist2, bins=max(imageHist2 + imageNoiseHist2 + noiseHist2))
    return None
