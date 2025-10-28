import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from mpl_tooklits.mplots3d import Axes3D

#df = pd.read_csv('stats.csv', delimiter=' ', header=None)


def target_images(images,reference_images,num=10):
    reference_images_10=['LT_i_20070821_077_stack.fits','LT_i_20070820_166_stack.fits','LT_i_20070823_198_stack.fits','LT_i_20070914_052_stack.fits','LT_i_20071002_086_stack.fits','LT_i_20080922_091_stack.fits','LT_i_20070817_038_stack.fits','LT_i_20070914_070_stack.fits','LT_i_20080922_122_stack.fits','LT_i_20070815_041_stack.fits']
    
    
    random_images=np.random.choice([image for image in images if image not in reference_images_10],size=num)

    return pd.Series(random_images)

def filtering(df):
    dates_df = df[0].str.split('_', expand=True)
    dates_df[2] = dates_df[2].astype(int)
    file_names=df[0]
    df = df[dates_df[2] > 20051231]
    df = df.select_dtypes(include=['float64', 'float32'])
    df.columns = ['seeing', 'airmass', 'background']
    file_names = file_names[dates_df[2] > 20051231]
    df['file_names'] = file_names
    df = df[(df['seeing'] >= 4) & (df['seeing'] <= 8)]
    df = df[(df['airmass'] >= 0) & (df['airmass'] <= 1.2)]
    df = df[(df['background'] >= 800) & (df['background'] <= 2500)]
    return df


def ThreeD_plot(df, t=''):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f'3D Plot of Metadata - {t}')
    ax.scatter(df['seeing'], df['airmass'],
               df['background'], c='r', marker='x')
    ax.set_xlabel('Seeing $(pixels)$')
    ax.set_ylabel('Airmass')
    ax.set_zlabel('Background')


def Hists(df, t=''):

    fig, ax = plt.subplots(3, figsize=(10, 6), layout='constrained')
    ax[0].hist(df['seeing'], bins=70)
    ax[1].hist(df['airmass'], bins=70)
    ax[2].hist(df['background'], bins=70)
    ax[0].set_ylabel('Count')
    ax[0].set_xlabel('Seeing')
    ax[1].set_ylabel('Count')
    ax[1].set_xlabel('Airmass')
    ax[2].set_ylabel('Count')
    ax[2].set_xlabel('Background')
    fig.suptitle(f'Histograms of Metadata - {t}')


def min_max(df):
    df['seeing_norm'] = 1-(df['seeing']-df['seeing'].min()) / \
        (df['seeing'].max()-df['seeing'].min())
    df['airmass_norm'] = 1-(df['airmass']-df['airmass'].min()) / \
        (df['airmass'].max()-df['airmass'].min())
    df['background_norm'] = 1-(df['background']-df['background'].min()) / \
        (df['background'].max()-df['background'].min())

    df['quality_score'] = df['seeing_norm'] + \
        df['airmass_norm']+df['background_norm']
    best_images = df.sort_values(by='quality_score', ascending=False).head(30)

    return best_images


def z_score(df):
    df['seeing_norm'] = (df['seeing']-df['seeing'].mean())/(df['seeing'].std())
    df['airmass_norm'] = (df['airmass']-df['airmass'].mean())/(df['airmass'].std())
    df['background_norm'] = (df['background']-df['background'].mean())/(df['background'].std())

    df['quality_score'] = df['seeing_norm']+df['airmass_norm']+df['background_norm']
    best_images = df.sort_values(by='quality_score', ascending=True).head(30)

    return best_images




def opening_DIA_files(path='Workspace_DG/'):
    runs=['run1/','run2/','run3/','run4/','run5/']
    new_runs = [f'run{i}/' for i in range(6, 1296)]  # Generate run6 to run10
    runs.extend(new_runs)   
    stats_files=[path+run+'stats.txt' for run in runs]
    config_files=[path+run+'default_config' for run in runs]
    
    stats_dfs={}
    config_dfs={}
    for sf in range(len(stats_files)):
        df=pd.read_csv(stats_files[sf],delimiter=' ',header=None)
        df=df.drop(columns=[0,2])
        df=df.rename(columns={1:'mean',3:'scatter'})
        stats_dfs[runs[sf].strip('/')]=df
        
        
        config_data={}
        with open(config_files[sf],'r') as file:
            for line in file:
                line=line.strip('/***')
                part=line.split()
                if '/***' in part:
                    part=part[:part.index('/***')]
                elif '/**' in part:
                    part=part[:part.index('/**')]
                config_data[part[0]]=part[1]
        config_data=pd.DataFrame([config_data])
        config_dfs[runs[sf].strip('/')]=config_data
    
    return stats_dfs,config_dfs,runs



def Weighted(df):
    weights=1/df['scatter']**2
    weighted_mean=np.sum(weights*df['mean'])/np.sum(weights)
    weighted_std=1/np.sqrt(np.sum(weights))
    return weighted_mean,weighted_std


def Plotting_mean_scatter(ax, df, name='', suffix='', color=None, marker='o'):
    """
    Plot mean with error bars (scatter/std).
    """
    mean_key = f"{suffix + '_' if suffix else ''}mean"
    std_key = f"{suffix + '_' if suffix else ''}scatter"

    x = np.arange(len(df[mean_key]))  # image/run index

    ax.errorbar(
        x, df[mean_key], df[std_key],
        label=name,
        linestyle='-',  # solid line
        marker=marker,
        markersize=2,
        capsize=3,
        elinewidth=1.5,
        markerfacecolor=color,
        markeredgewidth=1,
        color=color,
        alpha=0.8
    )

def plotting_weighted_mean(ax, weighted_df, color='black', marker='s'):
    """
    Plot weighted means with error bars
    """
    mean_key = 'Weighted_mean'
    std_key = 'Weighted_scatter'
    x = np.arange(len(weighted_df))

    ax.errorbar(
        x, weighted_df[mean_key], weighted_df[std_key],
        label='Weighted mean',
        linestyle='--',
        marker=marker,
        markersize=4,
        capsize=4,
        elinewidth=1.5,
        color=color,
        markerfacecolor='k'
    )

# --- Main plotting ---
stats_dfs, config_dfs, runs = opening_DIA_files()

weighted_values = []

fig, ax = plt.subplots(1, 2, figsize=(16, 5), layout='constrained')
colors = plt.cm.tab10.colors  # color cycle

# Plot individual run means
ax[0].set_title('Mean per image/run', fontsize=14)
ax[0].set_xlabel('Image number', fontsize=12)
ax[0].set_ylabel('Mean value', fontsize=12)
ax[0].grid(True, linestyle='--', alpha=0.5)

for i, run in enumerate(runs):
    run_name = run.strip('/')
    df = stats_dfs[run_name]
    weighted_values.append(Weighted(df))
    Plotting_mean_scatter(ax[0], df, name=run_name, color=colors[i % len(colors)], marker='o')

ax[0].legend(loc='center left', fontsize=10, frameon=True)

# Plot weighted means
weighted_values = np.array(weighted_values)
Weighted_df = pd.DataFrame(data=weighted_values, columns=['Weighted_mean', 'Weighted_scatter'])

ax[1].set_title('Weighted Means per Run', fontsize=14)
ax[1].set_xlabel('Run number', fontsize=12)
ax[1].set_ylabel('Weighted mean', fontsize=12)
ax[1].grid(True, linestyle='--', alpha=0.5)

plotting_weighted_mean(ax[1], Weighted_df, color='red', marker='s')

fig.suptitle('Means with Scatter (std) across varied parameters', fontsize=16)
plt.show()



def polynomial_coefficients(order):
    return (order+1)*(order+2)/2

def free_variable_num(config_df):
    total=0
    total+=polynomial_coefficients(config_df['deg_bg'].astype(float))
    total+=polynomial_coefficients(config_df['deg_gauss1'].astype(float))
    total+=polynomial_coefficients(config_df['deg_gauss2'].astype(float))                 
    total+=polynomial_coefficients(config_df['deg_gauss3'].astype(float))
    total+=config_df['ngauss'].astype(float)
    total+=config_df['sigma_gauss1'].astype(float)
    total+=config_df['sigma_gauss2'].astype(float)
    total+=config_df['sigma_gauss3'].astype(float)
    return total

def averages_each_run(config_dfs,stats_dfs):
    #stats_dfs[['average_mean','average_scatter']]=stats_dfs.mean(axis='columns')
    #print(stats_dfs)
    pass

#averages_each_run(config_dfs, stats_dfs)    

#run1_free_variables=free_variable_num(config_dfs['run1'])
#print('free_variables:',run1_free_variables)


"""Filtering the images by year, seeing, airmass and background"""
#df=filtering(df)

"""finding the best images according to the min_max algorithm and saving to csv"""

#best_images_min_max = min_max(df)
#min_max_quality=best_images_min_max['quality_score']



#best_images_min_max['file_names'].to_csv('best_images_min_max.csv', index=False)
#ThreeD_plot(best_images_min_max, t='min_max')
#Hists(best_images_min_max, t='min_max')

"""finding the best images according to z_score and saving to csv"""


#best_images_z_score = z_score(df)
#z_score_quality=best_images_z_score['quality_score']
#best_images_z_score['file_names'].to_csv('best_images_z_score.csv', index=False)


"""finding a colletion of target images that doesnt include any of the reference images"""
#targets=target_images(df['file_names'],best_images_z_score['file_names'])

#targets.to_csv('target_images.csv',index=False)



#ThreeD_plot(best_images_z_score, t='z_score')
#Hists(best_images_z_score, t='z_score')
#print(best_images_min_max['quality_score'])
#print(best_images_z_score['quality_score'])

"""creates a mask of the difference between the two methods which only includes null values - the values that are the same, and then removes them from an indicies list to find\
    images in both lists that are different and outputs them"""
#mask=(best_images_min_max[['seeing','airmass','background']]-best_images_z_score[['seeing','airmass','background']]).isnull()
#indicies_differnces=(best_images_min_max[['seeing','airmass','background']][mask].dropna().index,best_images_z_score[['seeing','airmass','background']][mask].dropna().index)
#print(indicies_differnces)
#print('min_max:',best_images_min_max.loc[indicies_differnces[0][0]]['file_names'])
#print('z_score:',best_images_z_score.loc[indicies_differnces[1][0]]['file_names'])
#print(best_images_min_max.equals(best_images_z_score))

#merged=best_images_min_max.merge(best_images_z_score,on='file_names',suffixes=('_z_score','_min_max'))


