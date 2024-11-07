import pandas as pd

# 定义CEFR级别的顺序，用于比较
cefr_order = {
    'A1': 0, 'A2': 1, 'B1': 2, 'B2': 3, 'C1': 4, 'C2': 5
}

# 读取两个CSV文件
cefrj_df = pd.read_csv('./input/cefrj-vocabulary-profile-1.5.csv')
octanove_df = pd.read_csv('./input/octanove-vocabulary-profile-c1c2-1.0.csv')

# 只保留需要的列
cefrj_df = cefrj_df[['headword', 'pos', 'CEFR']]
octanove_df = octanove_df[['headword', 'pos', 'CEFR']]

# 合并数据框
merged_df = pd.concat([cefrj_df, octanove_df])

# 定义一个函数来选择较低的CEFR级别
def select_lower_level(group):
    if len(group) == 1:
        return group.iloc[0]
    
    levels = [cefr_order[cefr] for cefr in group]
    return group.iloc[levels.index(min(levels))]

# 按headword和pos分组，并选择较低的CEFR级别
result_df = merged_df.groupby(['headword', 'pos'])['CEFR'].agg(select_lower_level).reset_index()

# 按headword字母顺序排序
result_df = result_df.sort_values('headword')

# 保存结果到新的CSV文件
result_df.to_csv('merged_vocabulary_profile.csv', index=False)