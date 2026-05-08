import os

def generate_word_codes(word_file: str, code_file: str, output_file: str, report_file: str = None) -> None:
    if not os.path.exists(word_file):
        raise FileNotFoundError(f"❌ 未找到词表文件: {word_file}")
    if not os.path.exists(code_file):
        raise FileNotFoundError(f"❌ 未找到字码映射文件: {code_file}")

    # 1. 加载字码映射表 (character -> code)
    char_map = {}
    with open(code_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '\t' not in line:
                continue
            char, code = line.split('\t', 1)
            char_map[char.strip()] = code.strip()
    print(f"✅ 已加载 {len(char_map):,} 个汉字的编码映射。")

    # 2. 辅助函数：安全获取单字编码片段
    def get_seg(char: str, length: int) -> str | None:
        code = char_map.get(char)
        if code is None:
            return None
        return code[:length]  # 自动处理编码不足长度的情况

    # 3. 核心编码规则实现
    def encode_word(word: str) -> str | None:
        n = len(word)
        if n == 0: return None
        
        if n == 2:
            c1 = get_seg(word[0], 2)
            c2 = get_seg(word[1], 2)
            return (c1 + c2) if c1 and c2 else None
            
        elif n == 3:
            c1 = get_seg(word[0], 1)
            c2 = get_seg(word[1], 1)
            c3 = get_seg(word[2], 2)
            return (c1 + c2 + c3) if c1 and c2 and c3 else None
            
        elif n == 4:
            codes = [get_seg(c, 1) for c in word]
            return "".join(codes) if all(codes) else None
            
        else:  # n >= 5
            codes = [
                get_seg(word[0], 1),
                get_seg(word[1], 1),
                get_seg(word[2], 1),
                get_seg(word[-1], 1)
            ]
            return "".join(codes) if all(codes) else None

    # 4. 遍历词表、赋码并写入
    total_lines = 0
    format_errors = 0
    success_count = 0
    missing_char_count = 0

    with open(word_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:

        for line in fin:
            line = line.strip()
            if not line:
                continue
            total_lines += 1

            # 解析 text \t weight
            parts = line.rsplit('\t', 1)
            if len(parts) != 2:
                format_errors += 1
                continue

            word, weight = parts[0].strip(), parts[1].strip()
            
            # 赋码
            code = encode_word(word)
            if code:
                success_count += 1
                fout.write(f"{word}\t{code}\t{weight}\n")
            else:
                missing_char_count += 1
                # 保留原词与权重，编码位留空，便于后续人工核对或过滤
                fout.write(f"{word}\t\t{weight}\n")

    # 5. 生成并输出报告
    report = (
        f"📊 词表赋码完成报告\n"
        f"{'='*45}\n"
        f"📁 输入词表   : {word_file}\n"
        f"📁 字码映射表 : {code_file}\n"
        f"📁 输出文件   : {output_file}\n"
        f"{'='*45}\n"
        f"📝 总处理行数       : {total_lines}\n"
        f"✅ 成功赋码行数     : {success_count}\n"
        f"⚠️  含未知汉字行数   : {missing_char_count} (编码位留空)\n"
        f"❌ 格式异常行数     : {format_errors} (缺失 \\t 或空行)\n"
        f"{'='*45}\n"
        f"💡 提示: 若需按权重降序排列，可对本脚本输出文件运行之前的排序脚本。\n"
    )
    
    print(report)
    if report_file:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📝 详细报告已保存至: {report_file}")

if __name__ == "__main__":
    WORD_FILE  = "白奕词表.txt"
    CODE_FILE  = "奕单_三定.txt"
    OUT_FILE   = "白奕词表_带码.txt"
    REPORT_FILE= "赋码报告.txt"

    generate_word_codes(WORD_FILE, CODE_FILE, OUT_FILE, REPORT_FILE)