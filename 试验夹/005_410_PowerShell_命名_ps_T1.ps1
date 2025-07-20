# 定义路径：用反引号`换行，确保反引号后无空格
$pythonScript = @"
E:\备份盘\带零文件夹\005_计算机科学、程式、资料,硬件\005_400_电脑编程!1\Scripts
\005_490_运行与调试\试验夹\005_430_file_rename_creator_py_T1.py
"@ -replace "`r`n", "\"  # 将换行符替换为\

# 调用 Python 脚本（参数用空格分隔）
python $pythonScript --source "old_ps" --prefix "new" --version 10 `
--overwrite