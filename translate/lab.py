import csv
from stardict import DictCsv  # 从ECDICT导入词典工具

def add_word_metadata(words_list):
    # 初始化ECDICT词典
    dictionary = DictCsv("./ecdict.csv")  # 需要下载ecdict.csv文件
    
    for word_item in words_list:
        word = word_item["word"].lower()  # 获取单词并转小写
        dict_entry = dictionary.query(word)  # 查询词典
        
        if dict_entry:
            # 添加中文翻译
            word_item["Chinese"] = dict_entry["translation"]
            
            # 添加难度等级
            level = "unknown"
            tags = dict_entry.get("tag", "").split()
            
            # 根据ECDICT的标签判断难度级别
            if "zk" in tags:  # 中考
                level = "elementary" 
            elif "gk" in tags:  # 高考
                level = "intermediate"
            elif "cet4" in tags:  # 四级
                level = "upper-intermediate"
            elif "cet6" in tags:  # 六级
                level = "advanced"
            elif "ielts" in tags:  # 雅思
                level = "proficient"
            elif "toefl" in tags:  # 托福
                level = "proficient"
            elif "gre" in tags:  # GRE
                level = "master"
            
            # 也可以用Collins星级来判断难度
            collins = dict_entry.get("collins", 0)
            if not level or level == "unknown":
                if collins >= 5:
                    level = "advanced"
                elif collins >= 3:
                    level = "intermediate"
                elif collins > 0:
                    level = "elementary"
                    
            word_item["level"] = level

    return words_list