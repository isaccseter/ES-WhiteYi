input_file = "白奕词表-已赋码.txt"
output_file = "白奕词表.txt"

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8", newline="") as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue  # 跳过空行
        parts = line.split("\t")
        if len(parts) >= 3:
            text, code, weight = parts[0], parts[1], parts[2]
            fout.write(f"{text}\t{weight}\n")
        else:
            # 如果格式不符合预期，可保留原行或忽略
            print(f"跳过不符合格式的行: {line}")