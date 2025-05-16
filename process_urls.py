import re

def process_url(url):
    # 先统一删除 /iptv/live/1000.json?key=txiptv
    url = re.sub(r'/iptv/live/1000\.json\?key=txiptv', '', url, flags=re.IGNORECASE)
    
    # 处理 rtsp 协议（删除 http 到 rtsp 的部分）
    if 'rtsp://' in url.lower():
        url = re.sub(r'^.*?(?=rtsp://)', '', url, flags=re.IGNORECASE)
    
    # 处理 rtp/udp 协议（删除 / 后面的 @）
    elif any(proto in url.lower() for proto in ['rtp://', 'udp://']):
        url = re.sub(r'(?<=/)(@)', '', url, flags=re.IGNORECASE)
    
    return url  # 不再使用 strip() 避免破坏原有格式

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()  # 这会保留每行末尾的 \n
    
    processed_lines = []
    for line in lines:
        # 直接保留空行和注释行（包括它们的原始换行符）
        if not line.strip() or line.strip().startswith('#'):
            processed_lines.append(line)
            continue
        
        # 分割频道名和URL（注意保留右侧原始换行符）
        if ',' in line:
            parts = line.split(',', 1)
            channel = parts[0]
            url = parts[1] if len(parts) > 1 else ''
            processed_url = process_url(url)
            # 重新组合时保留原始行尾的 \n
            processed_lines.append(f"{channel},{processed_url}")
        else:
            processed_lines.append(line)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)  # 使用 writelines 保留所有换行符

if __name__ == "__main__":
    input_file = "itvlist.txt"
    output_file = "processed_itvlist.txt"
    process_file(input_file, output_file)
    print(f"处理完成，结果已保存到 {output_file}")
