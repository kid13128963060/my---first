import os
import shutil
from pathlib import Path
# 融合后的列表：包含原多行字符串 + 处理后的路径字符串
source_path = [
    r"""C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\PathHistory.json""".replace('\n', ''),  # 源文件路径

    r"""C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\Preferences.json""".replace('\n', ''),

    r"""C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\SearchHistory.json""".replace('\n', ''),

    r"""C:\Users\Administrator\AppData\Roaming\IrfanView\i_view64.ini""".replace(
        '\n', ''),
    r"""C:\Users\Administrator\AppData\Roaming\Ditto\005_211_Ditto!2_数据备份.db""".replace(
        '\n', '')
]

dest_dir = [
    r"""E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置
\自定义设置\\""".replace('\n', ''),
    r"""E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置
\自定义设置\\""".replace('\n', ''),
    r"""E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置
\自定义设置\\""".replace('\n', ''),
    r"""E:\备份盘\8000_大文件夹\009_备份文件夹_自
\005_238_irfanview!2_设置备份\\""".replace('\n', ''),
    r"""E:\备份盘\8000_大文件夹\009_备份文件夹_自
\005_211_Ditto!2_数据备份\\""".replace('\n', '')
]
# 验证结果（可选）
print("列表长度：", len(source_path))  # 输出 3，说明包含3个元素
print("路径字符串：", source_path[1])   # 输出处理后的完整路径（无换行）
print("路径字符串：", dest_dir[4])   # 输出处理后的完整路径（无换行）


def copy_file(source_path_str, dest_dir_str, overwrite=False):
    source_path = Path(source_path_str)
    dest_dir = Path(dest_dir_str)
    try:
        # 确保目标目录存在
        os.makedirs(dest_dir, exist_ok=True)
        # 提取源文件的基本名称
        file_name = os.path.basename(source_path)
        # 构建完整的目标路径
        dest_path = os.path.join(dest_dir, file_name)

        # 如果需要强制覆盖且目标文件已存在，则先删除目标文件
        if overwrite and os.path.exists(dest_path):
            os.remove(dest_path)

        # 复制文件（递归参数对单个文件无效）
        shutil.copy2(source_path, dest_path)
        print(f"成功复制文件到: {dest_path}")
    except FileNotFoundError:
        print(f"错误: 源文件不存在 - {source_path}")
    except PermissionError:
        print(f"错误: 权限不足，无法复制文件")
    except IsADirectoryError:
        print(f"错误: 源路径是目录，请使用 copytree 函数进行递归复制")
    except Exception as e:
        print(f"错误: 发生未知错误 - {str(e)}")


j = len(source_path)
for i in range(1, j+1):
    # 执行复制操作，开启强制覆盖功能
    copy_file(source_path[i-1], dest_dir[i-1], overwrite=True)
