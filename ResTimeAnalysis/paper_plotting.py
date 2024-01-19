import matplotlib.pyplot as plt
import pandas as pd

# Your data
data = {
    'VL': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    'CPA': [417, 471, 507, 340, 183, 350, 744, 533, 744, 511, 632, 396, 609],
    'RTA': [417, 471, 507, 340, 183, 350, 744, 533, 744, 511, 632, 396, 609],
    'NC': [401.911, 420.994, 443.627, 312.16, 266.764, 420.212, 699.366, 507.494, 699.366, 465.147, 620.064, 255.92, 563.543],
    'RTA_New': [401, 455, 447, 310, 175, 334, 716, 519, 502, 451, 415, 368, 549],
    'Ernst': [371, 401, 401, 293, 58, 128, 467, 415, 453, 112, 415, 126, 150]
}

# Create a DataFrame
df = pd.DataFrame(data)

x = [i+1 for i in range(13)]

CPA = [417, 471, 507, 340, 183, 350, 744, 533, 744, 511, 632, 396, 609]
RTA = [417, 471, 507, 340, 183, 350, 744, 533, 744, 511, 632, 396, 609]
NC = [401.911, 420.994, 443.627, 312.16, 266.764, 420.212, 699.366, 507.494, 699.366, 465.147, 620.064, 255.92, 563.543]
RTA_new = [401, 455, 447, 310, 175, 334, 716, 519, 502, 451, 415, 368, 549]
Ernst = [371, 401, 401, 293, 58, 128, 467, 415, 453, 112, 415, 126, 150]

plt.plot(x, RTA, color='tab:red',marker='o',label='RTA') 
plt.plot(x, RTA_new, color='tab:orange',marker='s',label='RTA_New')
plt.plot(x, CPA, color='tab:green',marker='p',label='CPA')  
plt.plot(x, Ernst, color='y',marker='p',label='Ernst')
plt.plot(x, NC, color='c',marker='*',label='NC') 

# for index, row in df.iterrows():
#     for column in df.columns[1:]:
#         plt.annotate(f'{row[column]}', (row['VL'], row[column]), textcoords="offset points", xytext=(0,5), ha='center')

plt.xlabel('virtual link index')
plt.ylabel('worst case delay (us)')
plt.title('WCD Summary of Approaches')
plt.legend()
plt.show()