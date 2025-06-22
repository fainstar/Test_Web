#!/usr/bin/env python3
"""
修正API文件 - 移除@exempt裝飾器
"""

def fix_api_file():
    """移除@exempt裝飾器"""
    with open('app/routes/api.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除所有@exempt行
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if line.strip() != '@exempt':
            fixed_lines.append(line)
    
    # 寫回檔案
    with open('app/routes/api.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("已修正API文件，移除所有@exempt裝飾器")

if __name__ == '__main__':
    fix_api_file()
