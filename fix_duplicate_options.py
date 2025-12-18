#!/usr/bin/env python3
import os
import re

def clean_proto_file(filepath):
    """清理proto文件中的重复选项"""
    with open(filepath, 'r') as f:
        content = f.read()

    # 查找重复的java_package和java_multiple_files
    lines = content.split('\n')
    result = []
    seen_package = False
    seen_multiple = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('option java_package ='):
            if not seen_package:
                result.append(line)
                seen_package = True
            else:
                # 跳过重复的
                continue
        elif stripped.startswith('option java_multiple_files ='):
            if not seen_multiple:
                result.append(line)
                seen_multiple = True
            else:
                # 跳过重复的
                continue
        else:
            result.append(line)

    # 检查是否有修改
    new_content = '\n'.join(result)
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed: {filepath}")
        return True
    else:
        print(f"No changes needed: {filepath}")
        return False

# 清理所有proto文件
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.proto'):
            filepath = os.path.join(root, file)
            clean_proto_file(filepath)