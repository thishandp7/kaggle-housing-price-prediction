"""
trim_types: 'zscore', 'iqr', 'percentile'
"""
import matplotlib.pyplot as plt
import seaborn as sns


def trim_outliers(data, column, trim_type):
    upper_bound = 0
    lower_bound = 0
    if trim_type == 'zscore':
        upper_bound = data[column].mean() + 3 * data[column].std()
        lower_bound = data[column].mean() - 3 * data[column].std()
    elif trim_type == 'iqr':
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        upper_bound = q3 + 1.5 * iqr
        lower_bound = q1 - 1.5 * iqr
    elif trim_type == 'percentile':
        upper_bound = data[column].quantile(0.99)
        lower_bound = data[column].quantile(0.05)

    outlier_ids = data.loc[(data[column] > upper_bound) | (data[column] < lower_bound)].Id.tolist()
    clean_data = data.loc[(data[column] <= upper_bound) & (data[column] >= lower_bound)]

    return outlier_ids, clean_data


def trim_outliers_by_percentile(data, column, lower_percentile, upper_percentile):
    lower_bound = data[column].quantile(lower_percentile)
    upper_bound = data[column].quantile(upper_percentile)

    outlier_ids = data.loc[(data[column] > upper_bound) | (data[column] < lower_bound)].Id.tolist()
    clean_data = data.loc[(data[column] <= upper_bound) & (data[column] >= lower_bound)]

    return outlier_ids, clean_data


def cap_outliers(data, column, trim_type):
    upper_bound = 0
    lower_bound = 0
    if trim_type == 'zscore':
        upper_bound = data[column].mean() + 3 * data[column].std()
        lower_bound = data[column].mean() - 3 * data[column].std()
    elif trim_type == 'iqr':
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        upper_bound = q3 + 1.5 * iqr
        lower_bound = q1 - 1.5 * iqr
    elif trim_type == 'percentile':
        upper_bound = data[column].quantile(0.95)
        lower_bound = data[column].quantile(0.05)
    data.loc[data[column] > upper_bound, column] = upper_bound
    data.loc[data[column] < lower_bound, column] = lower_bound
    return data

def plot_box_and_dist(data, column):
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))
    sns.boxplot(data[column], ax=ax[0])
    sns.histplot(data[column], ax=ax[1])
    plt.show()