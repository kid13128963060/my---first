# 方法一：使用'w'模式（文件不存在则创建，存在则覆盖）
with open('new_file.txt', 'w') as file:
    file.write('这是写入的内容\n')  # 写入一行文本
    file.write('第二行内容')       # 再写入一行

# 方法二：使用'x'模式（文件不存在则创建，存在则报错）
try:
    with open('new_file2.txt', 'x') as file:
        file.write('使用x模式创建的文件\n')
except FileExistsError:
    print('文件已存在，无法创建！')
