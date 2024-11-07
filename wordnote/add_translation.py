from google.cloud import translate
import pandas as pd
import time
from google.api_core import retry
import os

# 设置代理环境变量
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

def translate_csv():
    # 初始化翻译客户端
    client = translate.TranslationServiceClient(
        client_options={
            "api_endpoint": "translate.googleapis.com:443",
        }
    )
    
    # 设置项目信息
    project_id = "braided-grammar-408110"
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    
    # 读取CSV文件
    df = pd.read_csv('./input/merged_vocabulary_profile.csv')
    
    # 添加新列
    df['chinese'] = ''
    
    # 设置重试装饰器
    @retry.Retry(predicate=retry.if_exception_type(Exception))
    def translate_with_retry(text):
        return client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": "en",
                "target_language_code": "zh-CN",
            }
        )
    
    # 遍历每一行进行翻译
    for index, row in df.iterrows():
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                word = row['headword']
                response = translate_with_retry(word)
                translation = response.translations[0].translated_text
                df.at[index, 'chinese'] = translation
                
                # 每100个词保存一次文件并打印进度
                if index % 100 == 0:
                    print(f"已翻译 {index} 个单词...")
                    df.to_csv('./output/merged_vocabulary_profile_with_chinese_temp.csv', index=False)
                    print(f"已保存临时文件，当前进度：{index}个单词")
                
                time.sleep(0.1)
                break
                
            except Exception as e:
                retry_count += 1
                print(f"翻译 {word} 时出错 (尝试 {retry_count}/{max_retries}): {str(e)}")
                if retry_count < max_retries:
                    time.sleep(2 ** retry_count)
                continue

    # 保存结果到新的CSV文件
    df.to_csv('./output/merged_vocabulary_profile_with_chinese.csv', index=False)
    print("翻译完成！")

if __name__ == "__main__":
    translate_csv()