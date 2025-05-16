import re

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式替换目标字符串
    processed_content = re.sub(r'/iptv/live/1000\.json\?key=txiptv', '', content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)

if __name__ == "__main__":
    input_file = "itvlist.txt"
    output_file = "processed_itvlist.txt"
    process_file(input_file, output_file)
    print(f"处理完成，结果已保存到 {output_file}")
