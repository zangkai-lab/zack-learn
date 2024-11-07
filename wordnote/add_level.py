# 上述是我的我的一个json文件，我想在words这个list下面的每一个dict做一个操作，就是@merged_vocabulary_profile.csv 根据这个词汇表，根据"word"字段增加字段“level”,"translation_zh";其中"translation_zh"的格式是“pos. + (使用Google翻译的结果)”

import json
import csv
import copy

# 读取词汇表并创建查找字典
vocab_dict = {}
with open('./output/merged_vocabulary_profile_with_chinese.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # 将词汇表中的词作为key(转为小写以便匹配)
        word = row['headword'].lower()
        if word not in vocab_dict:
            vocab_dict[word] = {
                'level': row['CEFR'],
                'pos': row['pos'],
                'chinese': row['chinese']
            }

# 读取JSON文件
with open('./output/output_word.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 处理每个单词
for word_item in data['words']:
    word = word_item['word'].lower()  # 转为小写以便匹配
    
    if word in vocab_dict:
        # 添加新字段
        word_item['level'] = vocab_dict[word]['level']
        word_item['chinese'] = f"{vocab_dict[word]['pos']}. {vocab_dict[word]['chinese']}"
    else:
        # 如果在词汇表中找不到，添加默认值
        word_item['level'] = 'unknown'
        word_item['chinese'] = 'unknown'

# 保存修改后的JSON
with open('./output/output_word_with_level.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
