import pandas as pd

df1 = pd.read_csv('mero.predictions', sep='\t', names=['X','Y','Actual','Predicted'])
df2 = pd.read_csv('mero.predictions2', sep='\t', names=['Y','X','Actual','Predicted'])
df2 = df2[['X','Y','Actual','Predicted']] # Reorder columns
#s = sum(df[''])
avg1 = df1['Predicted'].mean()
print avg1
avg2 = df2['Predicted'].mean()
print avg2


df3 = pd.read_csv('test.tsv', sep='\t', names=['Y','X','Label'])
df3 = df3[['X','Y','Label']]
new_actual = df3['Label'].values
new_actual = [True if a=='mero' else False for a in new_actual]
df3['Label'] = new_actual
print df3
df3.to_csv('baseline_test.tsv', sep='\t', header=False, index=False)