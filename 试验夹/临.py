# 融合后的列表：包含原多行字符串 + 处理后的路径字符串
source_path = [
    r'''C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\PathHistory.json'''.replace('\n', ''),  # 源文件路径

    r'''C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\Preferences.json'''.replace('\n', ''),

    r'''C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\SearchHistory.json'''.replace('\n', ''),

    r'''C:\Users\Administrator\AppData\Roaming\IrfanView\i_view64.ini'''.replace(
        '\n', ''),
    r'''C:\Users\Administrator\AppData\Roaming\Ditto\005_211_Ditto!2_数据备份.db
    '''.replace('\n', '')

]


dest_dir = [
    r'''E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置
    \自定义设置\\'''.replace('\n', ''),  # 目标文件夹路径

    r'''E:\备份盘\8000_大文件夹\009_备份文件夹_自
    \005_238_irfanview!2_设置备份\\'''.replace('\n', ''),

    r'''E:\备份盘\8000_大文件夹\009_备份文件夹_自
    \005_211_Ditto!2_数据备份\\'''.replace('\n', '')
]
# 验证结果（可选）
print("列表长度：", len(source_path))  # 输出 3，说明包含3个元素
print("路径字符串：", source_path[1])   # 输出处理后的完整路径（无换行）
print("路径字符串：", dest_dir[0])   # 输出处理后的完整路径（无换行）
