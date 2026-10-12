# --- ШАГ 1: Читаем файлы ---
with open('old.txt', 'r', encoding='utf-8') as f:
    old_lines = [line.strip() for line in f if line.strip()]

with open('new.txt', 'r', encoding='utf-8') as f:
    new_lines = [line.strip() for line in f if line.strip()]

# --- ШАГ 2: Подготовка ---
result = []
old_index = 0

# --- ШАГ 3: Главный цикл сравнения ---
for new_line in new_lines:
    # Проверяем удаленные строки
    while old_index < len(old_lines) and old_lines[old_index] not in new_lines:
        result.append("-" + old_lines[old_index])
        old_index += 1
        
    # Проверяем текущую строку
    if new_line in old_lines:
        result.append(new_line)
        while old_index < len(old_lines) and old_lines[old_index] != new_line:
            old_index += 1
        old_index += 1
    else:
        result.append("+" + new_line)

# --- ШАГ 4: Зачистка  ---
while old_index < len(old_lines):
    if old_lines[old_index] not in new_lines:
        result.append("-" + old_lines[old_index])
    old_index += 1

# --- ШАГ 5: Запись результата ---
with open('diff.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result) + '\n')
