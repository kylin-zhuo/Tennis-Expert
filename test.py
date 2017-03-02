import pandas as pd 

df = pd.read_csv('tennis.csv')
df = df.drop(df.columns[0], axis=1)

print df

from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(df)

T = pca.transform(df)
print T

df_pca = pd.DataFrame(T, columns=['PC1', 'PC2'])
print df_pca
# exit()

import matplotlib
import matplotlib.pyplot as plt

# matplotlib.style.use('ggplot') # Look Pretty
df_pca.plot.scatter(x='PC1', y='PC2')
plt.legend(['A','B','C','D','E'])
plt.show()