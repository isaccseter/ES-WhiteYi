import os

def sort_word_list_with_report(input_file: str, output_file: str, report_file: str = None) -> None:
    # 1. 读取所有行
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    parsed_data = []
    invalid_count = 0

    # 2. 预处理：记录原始行号、行内容，并提取权重
    for idx, line in enumerate(lines):
        try:
            # 从右侧分割一次，兼容词条内含 \t 的情况
            weight_str = line.rsplit('\t', 1)[-1].strip()
            weight = float(weight_str)
            parsed_data.append((idx, line, weight))
        except (ValueError, IndexError):
            # 格式错误（如无 \t、权重非数字、空行等）统一计为无效，赋予 0.0 权重保底
            invalid_count += 1
            parsed_data.append((idx, line, 0.0))

    # 3. 按权重降序排序
    # Python 的 sorted() 是稳定排序，相同权重的行会保持原始相对顺序
    sorted_data = sorted(parsed_data, key=lambda x: x[2], reverse=True)

    # 4. 统计位置发生变动的行数
    # 稳定排序下，仅当行的新索引与原索引不一致时，才视为“被移动”
    moved_count = sum(1 for new_idx, (orig_idx, _, _) in enumerate(sorted_data) if new_idx != orig_idx)

    # 5. 写入排序结果
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(line for _, line, _ in sorted_data)

    # 6. 生成报告
    total_lines = len(lines)
    valid_lines = total_lines - invalid_count
    report_content = (
        f"📊 词表排序报告\n"
        f"{'=' * 30}\n"
        f"📁 输入文件: {input_file}\n"
        f"📁 输出文件: {output_file}\n"
        f"{'=' * 30}\n"
        f"总行数          : {total_lines}\n"
        f"✅ 符合格式行数  : {valid_lines}\n"
        f"❌ 不符合格式行数: {invalid_count}\n"
        f"🔄 位置变动行数  : {moved_count}\n"
        f"{'=' * 30}\n"
        f"💡 注: Python 使用稳定排序，权重相同的行保持原相对顺序。\n"
    )
    
    print(report_content)
    
    if report_file:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"📝 详细报告已保存至: {report_file}")

if __name__ == "__main__":
    INPUT_PATH  = "白奕词表.txt"
    OUTPUT_PATH = "白奕词表_sorted.txt"
    REPORT_PATH = "白奕词表_report.txt"
    
    sort_word_list_with_report(INPUT_PATH, OUTPUT_PATH, REPORT_PATH)