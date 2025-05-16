import re

def process_url(url):
    # 先统一删除 /iptv/live/1000.json?key=txiptv
    url = re.sub(r'/iptv/live/1000\.json\?key=txiptv', '', url, flags=re.IGNORECASE)
    
    # 处理 rtsp 协议（删除 http 到 rtsp 的部分）
    if 'rtsp://' in url.lower():
        url = re.sub(r'^.*?(?=rtsp://)', '', url, flags=re.IGNORECASE)
    
    # 处理 rtp/udp 协议（在协议前添加 /，并删除 / 后面的 @）
    elif any(proto in url.lower() for proto in ['rtp://', 'udp://']):
        # 将 rtp:// 或 udp:// 替换为 rtp/ 或 udp/
        url = re.sub(r'(rtp|udp)://', r'\1/', url, flags=re.IGNORECASE)
        # 删除 / 后面的 @（如果有）
        url = re.sub(r'(?<=/)(@)', '', url, flags=re.IGNORECASE)
        # 在 rtp/ 或 udp/ 前添加 /（但不在开头添加）
        url = re.sub(r'(?<!:)(rtp/|udp/)', r'/\1', url, flags=re.IGNORECASE)
    
    return url

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
            processed_url = process_url(url)
            processed_lines.append(f"{channel},{processed_url}")
        else:
            processed_lines.append(line)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

if __name__ == "__main__":
    input_file = "itvlist.txt"
    output_file = "processed_itvlist.txt"
    process_file(input_file, output_file)
    print(f"处理完成，结果已保存到 {output_file}")
