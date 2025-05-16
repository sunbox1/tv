import re

def process_line(line):
    # 处理 rtsp 开头的行
    if 'rtsp://' in line.lower():
        # 找到 http 到 rtsp 的部分并删除
        line = re.sub(r'^.*?(?=rtsp://)', '', line, flags=re.IGNORECASE)
    
    # 处理 rtp 或 udp 开头的行
    elif any(proto in line.lower() for proto in ['rtp://', 'udp://']):
        # 删除 / 后面的 @ 符号
        line = re.sub(r'(?<=/)(@)', '', line, flags=re.IGNORECASE)
    
    return line.strip()

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    processed_lines = []
    for line in lines:
        # 跳过空行和注释行
        if not line.strip() or line.strip().startswith('#'):
            processed_lines.append(line)
            continue
        
        # 分割频道名和URL
        if ',' in line:
            channel, url = line.split(',', 1)
            processed_url = process_line(url)
            processed_lines.append(f"{channel},{processed_url}\n")
        else:
            processed_lines.append(line)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

if __name__ == "__main__":
    input_file = "itvlist.txt"
    output_file = "processed_itvlist.txt"
    process_file(input_file, output_file)
    print(f"处理完成，结果已保存到 {output_file}")
