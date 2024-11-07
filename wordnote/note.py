# https://github.com/openlanguageprofiles/olp-en-cefrj/blob/master/cefrj-vocabulary-profile-1.5.csv
def txt_to_json_safe_string(input_file):
    # 方案1：使用 json.dumps 来正确处理转义字符
    import json
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用 json.dumps 来正确处理转义字符
        json_safe_string = json.dumps(content)[1:-1]  # [1:-1] 去掉 json.dumps 添加的引号
    return json_safe_string

# 或者方案2：直接使用原始字符串，让 JSON 编码器来处理
def txt_to_raw_string(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# 使用示例
input_path = "input.txt"

# 方案1
result1 = txt_to_json_safe_string(input_path)
print(result1)

# 方案2：在需要转换为 JSON 时
import json
result2 = txt_to_raw_string(input_path)
json_obj = {"text": result2}
json_string = json.dumps(json_obj)
print(json_string)