import numpy as np
import matplotlib.pyplot as plt
n = 5;
r = np.random.normal(0,1,pow(n,2))
rnorm = [(i-min(r))/(max(r)-min(r)) for i in r]
m = [[rnorm[(j-1)*n+i] for j in range(n)] for i in range(n)]

plt.imshow(m, cmap='gray')
plt.title('Ruido gaussiano normalizado 5x5')
plt.colorbar()
plt.show()

#Calcular cuando dos nodos del VG están conectados
def vgBool(x,i,j):
	if abs(i-j)<=1:
		return True
	v = [x[i]+(k-i)/(j-i)*(x[j]-x[i])-x[k] for k in range(min(i,j)+1,max(i,j))]
	return pow(2,(sum(np.sign(v))-len(v)))==1

#Calcular cuando dos nodos del IVG están conectados
def boole(M,i_1,j_1,i_2,j_2):
	if (i_1-i_2)==0:
		return vgBool(M[i_1][min(j_1,j_2):max(j_1,j_2)+1],0,abs(j_2-j_1))
	if (j_1-j_2)==0:
		return vgBool([M[i][j_1] for i in range(min(i_1,i_2),max(i_1,i_2)+1)],0,abs(i_2-i_1))
	if i_1-i_2==j_1-j_2:
		[dirx,diry] = [-int((i_1-i_2)/abs(i_1-i_2)),-int((j_1-j_2)/abs(i_1-i_2))]
		return vgBool([M[i_1+k*dirx][j_1+k*diry] for k in range(abs(i_1-i_2)+1)],0,abs(i_2-i_1))
	return False

#Calcular la matriz de pesos
def weightMat(M):
	return [[sum([sum([[ boole(M,i,j,k,l) for i in range(n)] for j in range(n)][t]) for t in range(n)])for k in range(n)] for l in range(n)]

#Calcular los valores de los grados, sus máximos y los respectivos porcentajes
xaxis = range(1,pow(n,2)+1)
wimg = weightMat(m)
degrees = [wimg[i%n][int(np.floor(i/n))] for i in range(pow(n,2))]
maxdegrees = [2*n-2+len(np.diag(m,(int(np.floor(i/n))-i%n))) for i in range(pow(n,2))]
percentages = [degrees[i]/maxdegrees[i]*100 for i in range(pow(n,2))]

plt.xticks(range(1,pow(n,2)+1))
plt.yticks(range(1,3*n-1))
plt.bar(xaxis, degrees, color='blue', alpha=0.7)
plt.title('Grados de los nodos')
plt.xlabel('Nodo')
plt.ylabel('Grado')
plt.show()


plt.yticks([10*i for i in range(1,11)])
plt.bar(xaxis, percentages, color='blue', alpha=0.7)
plt.title('Porcentaje de grados')
plt.xlabel('Nodo')
plt.ylabel('Porcentaje de conexiones del nodo respecto de su máximo')
plt.show()
