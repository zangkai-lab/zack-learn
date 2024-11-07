from aeneas.executetask import ExecuteTask
from aeneas.task import Task
import os
import subprocess
from aeneas.logger import Logger

def prepare_text_file(input_text_path, output_text_path):
    """准备带有时间戳的文本文件"""
    with open(input_text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 按句子分割文本
    sentences = text.replace('. ', '.\n').replace('? ', '?\n').replace('! ', '!\n').split('\n')
    
    # 创建符合 aeneas 格式的文本
    formatted_text = []
    for i, sentence in enumerate(sentences, 1):
        if sentence.strip():  # 忽略空行
            formatted_text.append(f"{i} {sentence.strip()}")
    
    # 写入处理后的文本
    with open(output_text_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(formatted_text))
    
    return output_text_path

def trim_audio(input_path, output_path, start_time=20, duration=155):
    """
    截取音频的指定时间段
    start_time: 开始时间（秒）
    duration: 持续时间（秒）
    """
    cmd = [
        'ffmpeg', '-i', input_path,
        '-ss', str(start_time),  # 开始时间
        '-t', str(duration),     # 持续时间
        '-acodec', 'pcm_s16le',  # 转换为WAV格式
        '-ar', '44100',          # 采样率44.1kHz
        '-ac', '1',              # 单声道
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"音频截取完成：{output_path}")
    print(f"截取时间段：{start_time}秒 到 {start_time + duration}秒")
    return output_path

def extract_text_segment(text_path, max_words=330):
    """截取文本的前一部分"""
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = text.split()[:max_words]
    temp_text_path = text_path.replace('.txt', '_segment.txt')
    with open(temp_text_path, 'w', encoding='utf-8') as f:
        f.write(' '.join(words))
    print(f"截取的文本保存到: {temp_text_path}")
    print(f"文本长度: {len(words)} 词")
    return temp_text_path

# 设置文件路径
mp3_path = u"/Users/zack/Downloads/Elon_Musk/Elon_Musk.mp3"
text_path = u"/Users/zack/Downloads/Elon_Musk/Elon-Musk-by-Walter-Isaacson.txt"
wav_path = u"/Users/zack/Downloads/Elon_Musk/Elon_Musk_segment.wav"
# 添加 JSON 输出路径
json_path = u"/Users/zack/Downloads/Elon_Musk/output_word.json"

# 检查文件是否存在
if not os.path.exists(mp3_path):
    raise FileNotFoundError(f"音频文件不存在: {mp3_path}")
if not os.path.exists(text_path):
    raise FileNotFoundError(f"文本文件不存在: {text_path}")

os.makedirs(os.path.dirname(json_path), exist_ok=True)

print("开始处理...")

# 截取音频和文本
trimmed_audio = trim_audio(mp3_path, wav_path)
text_segment_path = extract_text_segment(text_path)

print("设置任务参数...")

# 创建配置
config_string = (
    "task_language=eng|"
    "is_text_type=plain|"
    "os_task_file_format=json|"
    "is_text_unparsed_id_regex=^\\d+|"  # 使用数字作为ID
    "is_text_unparsed_id_sort=numeric|"
    "task_adjust_boundary_algorithm=percent|"
    "task_adjust_boundary_percent_value=50"
)

try:
    logger = Logger(tee=True)
    # 创建任务
    task = Task(config_string)
    task.audio_file_path_absolute = trimmed_audio
    # 准备文本文件
    marked_text_path = text_segment_path.replace('.txt', '_marked.txt')
    prepared_text_path = prepare_text_file(text_segment_path, marked_text_path)
    task.text_file_path_absolute = prepared_text_path
    task.sync_map_file_path_absolute = json_path
    task.sync_map_format = "json"


    print("\n处理后的文本预览:")
    with open(prepared_text_path, 'r') as f:
        print(f.read()[:500])

    # 执行任务
    executor = ExecuteTask(task, logger=logger)
    result = executor.execute()
    sync_map = task.sync_map

    if result:
        print("任务执行成功")
    else:
        print("任务执行失败")
    
    # 验证文件是否创建成功
    if sync_map is not None:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        # 保存为JSON
        sync_map.write("json", json_path)
        print(f"同步映射已保存到: {json_path}")
        
        # 显示同步映射内容预览
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                content = f.read()
                print("\nJSON 内容预览（前500字符）:")
                print(content[:500])
    else:
        print("错误：同步映射为空")
except Exception as e:
    print(f"处理过程中出现错误: {str(e)}")
    import traceback
    print(traceback.format_exc())