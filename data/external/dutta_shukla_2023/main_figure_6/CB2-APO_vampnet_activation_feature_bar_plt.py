import numpy as np 
import matplotlib.pyplot as plt 
import glob 

#1. load the necessary numpy files 
#2. 
def rgb_to_hex(r, g, b):
    return ('#{:02X}{:02X}{:02X}').format(r, g, b)

dica =  {'Ex13_distance':0,'Ex14_distance':1,'Ex15_distance':2,'Ex16_distance':3,'Ex17_distance':4,
             'Ex23_distance':5,'Ex24_distance':6,'Ex25_distance':7,'Ex26_distance':8,'Ex27_distance':9,
             'Helix2M_Nloop':10,'ECL2_Nloop':11,'TG_TRP_helix2': 12,'TG_TRP_helix5': 13,'TG_PHE_helix2': 14,'TG_PHE_helix5': 15,
             'In6_chi2':16,'In57_distance':17,'In36_distance':18,'In27_distance':19,'TG_diff_x':20,'TG_diff_y':21,'TG_diff_z':22,
             'TG_angle_z':23,'In27_back1':24,'In27_back2':25,
             'In5_1_chi1':26,'In5_2_chi1':27,'In5_1_chi2':28,'In5_2_chi2':29,'In53_distance':30,'In52_distance':31
             }
def load_feature(count):
    matrics = np.empty([6,20,1000])
    for i in range(6):
        for j in range(20):
            filename =  '../Bootstrap_files/CB2_macrostate_' + str(i) + '_bt_' + str(j) + '_feature.npy'
            matrics[i,j,:] = np.load(filename)[:,count]

    return matrics


def bar_plot(macrostate_matrics,macrostate,c):
    activation_mean_per_bt = np.mean(macrostate_matrics,axis=2)
    activation_mean =  np.mean(activation_mean_per_bt,axis=1)
    activation_std =  np.std(activation_mean_per_bt,axis=1)

    fig, axs = plt.subplots(1,1,figsize=(10,7)) 
    width = 0.8
    x = [i*2 for i in range(5)]
    plt.bar(x, activation_mean, yerr=activation_std, width=width, align='center', color=c, alpha=0.5, ecolor='black', capsize=10)
    
    for i in range(len(x)):
        axs.scatter(x[i] + np.random.random(activation_mean_per_bt[i,:].size) * width *0.5 - width*0.5 / 2, activation_mean_per_bt[i,:], color='black',alpha=1.0,s=16)

    axs.set_xticks([i*2 for i in range(5)])
    axs.set_xticklabels(['[1]','[2]','[3]','[4]', '[5]'])
    axs.set_xlim(-1,9)
    axs.set_ylim(0,1)
    plt.rc('xtick', labelsize=30)
    plt.rc('ytick', labelsize=30)

    plt.xticks(fontsize=35)
    plt.yticks(fontsize=35)
    plt.tight_layout()

    plt.savefig('./CB2_'+macrostate+'_vampnet_state.png',dpi=300)
    plt.close()

if __name__=='__main__':
    interested_feature = ['Ex16_distance','In6_chi2','In52_distance','In36_distance','In57_distance']
    activation_matrics = np.empty([len(interested_feature),6,20,1000])

    states = ['3','0','1','2','4','5']
    labels = ['Inactive','I1','I2','I3','I4','Active']

    for i,feature in enumerate(interested_feature):
        matrices = load_feature(i)
        maximum = np.max(np.mean(matrices,axis=2))
        minimum = np.min(np.mean(matrices,axis=2))
        activation_matrics[i,:,:,:] = (matrices-minimum)/(maximum-minimum)

    for j,state in enumerate(states):
        macrostate_matrix = activation_matrics[:,int(state),:,:]
        bar_plot(macrostate_matrix,labels[j],rgb_to_hex(int(255*(0.0+0.9/5*j)),int(255*(1.0-1.0/5*j)),int(255*(0.0+0.38/5*j))))
