import fnmatch
from datetime import datetime
import glob
import os




def diff_(li1, li2):
    return (list(set(li1) - set(li2)))


def div_(li1, li2):
    result = []
    for i, j in zip(li1, li2):
        if j != 0:
            result += [i / j]
        else:
            result += [0]
    return result


def total(df, column1, value1, column2='none', value2='none'):
    total_monthly = []
    current_year = datetime.now().year
    for i in range(1, 13):

        try:
            if value2 == 'none':

                total_ = df[(df[column1] == value1)][f'{current_year}-{i}'].shape[0]
            else:
                total_ = df[(df[column1] == value1) & (df[column2] == value2)][f'{current_year}-{i}'].shape[0]

            total_monthly += [total_]
        except KeyError:
            total_monthly += [0]

    return total_monthly


def category_count(df, category_list):
    """
    :type category_list: list
    :type df: pandas.core.frame.DataFrame
    """
    total_category =[]
    current_month = int(datetime.now().month)
    current_year = int(datetime.now().year)

    for i in category_list:
        try:
            total_ = df[(df['Category'] == i)][f'{current_year}-{current_month}'].shape[0]
            total_category += [total_]
        except:
            total_category += [0]

    return total_category


def latest_file(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            # if self.result:
            #     os.remove(os.path.join(root, name))
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    file = max(result, key=os.path.getctime)
    return file


# def category_priority_count(df, category_list, priority=False):
#     """
#     :type priority: bool
#     :type category_list: list
#     :type df: pandas.core.frame.DataFrame
#     """
#     total_category =[]
#     current_month = datetime.now().year
#     current_year = datetime.now().year
#     category_list.remove('PPM')
#     if not priority:
#     for i in category_list:
#
#         try:
#
#                 total_ = df[(df['Category'] == i)][f'{current_year}-{current_month}'].shape[0]
#                 total_category += [total_]
#
#
#                 priority_list = df['Category'].unique().tolist()
#
#                     try:
#
#                         total_priority = df[(df['Category'] == i) & (df["Priority"] == j)][f'{current_year}-{current_month}'].shape[0]
#                         total_category += [total_]
#
#         except KeyError:
#             total_category += [0]
#     return total_category

# total = category_ppm_count()

