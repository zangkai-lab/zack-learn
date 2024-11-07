from pyzerox import zerox
import os
import asyncio

async def main():
    # 设置文件路径
    file_path = "./pdf-cases/NASDAQ_TSLA_2019.pdf"
    
    # 设置OpenAI配置
    os.environ["OPENAI_API_KEY"] = ""  # 请替换成你的OpenAI API密钥
    
    # 设置要处理的页面范围（50-70页）
    select_pages = list(range(50, 71))  # 创建50到70的页码列表
    
    # 设置输出目录
    output_dir = "./tesla_output"
    
    # 执行转换
    result = await zerox(
        file_path=file_path,
        model="gpt-4o-mini",
        output_dir=output_dir,
        select_pages=select_pages,
        cleanup=True,  # 处理完成后清理临时文件
        concurrency=10  # 并发处理数量
    )
    
    return result

# 运行主函数
if __name__ == "__main__":
    result = asyncio.run(main())
    print("转换完成！输出已保存到tesla_output目录")

