import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats

# We first produce a sample:

TRUE_LAMBDA = 6
X = np.random.poisson(TRUE_LAMBDA, 10000)


# For our sample, we estimate a value for  λ  using MLE:
def poisson_lambda_MLE(X):
    # TODO
    λ=sum(X)/10000
    return λ

lambda_mle = poisson_lambda_MLE(X)
print(lambda_mle)

pillar = 15
a = plt.hist(X, bins=pillar, normed=True, range=[0, pillar], color='g', alpha=0.5)
plt.plot(a[1][0:pillar], a[0], 'r')
plt.grid()
plt.show()
