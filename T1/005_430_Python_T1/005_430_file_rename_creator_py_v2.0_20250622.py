import os
import argparse
import win32con
import ctypes
from ctypes import wintypes
import pythoncom
from win32com.client import Dispatch
import win32gui
import win32process
from datetime import datetime

def get_last_active_explorer_path(path=None):
    """获取资源管理器最后活动的后台窗口路径"""
    try:
        pythoncom.CoInitialize()
        shell_windows = Dispatch("Shell.Application").Windows()
        explorer_windows = []
        for window in shell_windows:
            if window and window.LocationURL and window.LocationURL.startswith("file:///"):
                hwnd = window.HWND
                title = win32gui.GetWindowText(hwnd)
                path = window.LocationURL[8:].replace("/", "\\")
                explorer_windows.append((hwnd, title, path))
        if not explorer_windows:
            print("未找到资源管理器窗口")
            return path if path is not None else None
        user32 = ctypes.windll.user32
        active_hwnd = user32.GetForegroundWindow()
        non_active_explorers = [win for win in explorer_windows if win[0] != active_hwnd]
        if not non_active_explorers:
            print("使用当前活动窗口路径")
            path = explorer_windows[0][2]
        else:
            def get_window_z_order(hwnd):
                z_order = 0
                current = hwnd
                while True:
                    current = win32gui.GetWindow(current, win32con.GW_HWNDPREV)
                    if not current:
                        break
                    z_order += 1
                return z_order
            non_active_explorers.sort(key=lambda x: get_window_z_order(x[0]))
            path = non_active_explorers[0][2]
        print(f"资源管理器最后活动窗口路径: {path}")
        return path
    except Exception as e:
        print(f"获取路径时出错: {e}")
        return path if path is not None else None
    finally:
        pythoncom.CoUninitialize()

def generate_filename(prefix="", lang="Python", version="", year="", month="", day="", source_name=None):
    """标准化文件名生成（增强源文件信息提取）"""
    if source_name:
        base_name = os.path.basename(source_name)
        parts = base_name.split('_')
        # 提取前缀（优先使用参数，其次从源文件名提取）
        prefix = prefix or (parts[0] if parts else "")
        # 提取版本号（支持vX.X或X.X格式）
        for part in parts:
            if 'v' in part and '.' in part:
                version = part[1:]
            elif '.' in part and all(p.isdigit() for p in part.split('.')):
                version = part
        # 提取日期（严格匹配8位数字）
        for part in parts:
            if len(part) == 8 and part.isdigit():
                year, month, day = part[:4], part[4:6], part[6:8]
                break
    # 强制版本号格式（如32→3.2）
    if version and "." not in version:
        version = f"{version[:-1]}.{version[-1]}"
    # 日期处理（优先使用参数，其次从源文件提取，最后用当前日期）
    date_part = f"{year}{month.zfill(2)}{day.zfill(2)}" if all([year, month, day]) else datetime.now().strftime("%Y%m%d")
    return "_".join(filter(None, [prefix, lang, f"v{version}" if version else "", date_part]))

def rename_file(old_folder, new_name, source_name=None, overwrite=False):
    """重命名文件（增强源文件匹配和错误提示）"""
    old_folder = os.path.abspath(old_folder)
    # 校验文件夹
    if not os.path.exists(old_folder):
        return False, f"错误: 文件夹不存在 ({old_folder})"
    if not os.path.isdir(old_folder):
        return False, f"错误: 路径不是文件夹 ({old_folder})"
    # 处理源文件
    if source_name:
        source_path = os.path.join(old_folder, source_name)
        if not os.path.exists(source_path):
            # 模糊匹配源文件（不区分大小写）
            source_candidates = [f for f in os.listdir(old_folder)
                                if source_name.lower() in f.lower()]
            if source_candidates:
                source_path = os.path.join(old_folder, source_candidates[0])
                print(f"提示: 自动匹配源文件: {source_candidates[0]}")
            else:
                return False, f"错误: 源文件不存在 ({source_path})\n" \
                              f"当前文件夹文件: {', '.join(os.listdir(old_folder))}"
    else:
        source_path = os.path.join(old_folder, new_name)
        if not os.path.exists(source_path):
            return False, f"错误: 源文件不存在 ({source_path})\n" \
                          f"当前文件夹文件: {', '.join(os.listdir(old_folder))}"
    # 处理重命名
    new_path = os.path.join(old_folder, new_name)
    if os.path.exists(new_path):
        if overwrite:
            try:
                os.remove(new_path)
                print(f"已删除冲突文件: {new_path}")
            except Exception as e:
                return False, f"删除失败: {str(e)}"
        else:
            return False, f"错误: 目标文件已存在 ({new_path})"
    try:
        os.rename(source_path, new_path)
        return True, f"成功重命名: {source_path} -> {new_path}"
    except Exception as e:
        return False, f"重命名失败: {str(e)}"

def create_new_file(folder_path, file_name):
    """创建新文件"""
    file_path = os.path.join(folder_path, file_name)
    try:
        with open(file_path, 'w') as f:
            pass  # 创建空文件
        return True, f"成功创建新文件: {file_path}"
    except Exception as e:
        return False, f"创建新文件失败: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='文件重命名与创建工具')
    parser.add_argument('--old_file', help='文件夹路径', default=None)
    parser.add_argument('--prefix', help='文件名前缀', default='销售统计')
    parser.add_argument('--lang', help='语言标识', default='py')
    parser.add_argument('--version', help='版本号', default='3.2')
    parser.add_argument('--year', help='年份', default='')
    parser.add_argument('--month', help='月份', default='')
    parser.add_argument('--day', help='日期', default='')
    parser.add_argument('--ext', help='文件扩展名', default='.xlsx')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在文件')
    parser.add_argument('--source', help='源文件名（重命名时必选）', required=False)
    parser.add_argument('--new_file_name', help='手动指定新文件名', default=None)
    parser.add_argument('--create', action='store_true', help='执行创建新文件操作')
    
    args = parser.parse_args()
    
    # 处理文件夹路径
    if args.old_file:
        args.old_file = os.path.abspath(args.old_file)
        if not os.path.exists(args.old_file):
            print(f"警告: 文件夹不存在，尝试获取资源管理器路径: {args.old_file}")
            args.old_file = get_last_active_explorer_path(args.old_file)
    else:
        args.old_file = get_last_active_explorer_path()
    
    # 最终校验文件夹有效性
    if not args.old_file or not os.path.exists(args.old_file):
        print("\n错误: 无法找到有效文件夹！")
        exit(1)
    
    # 区分创建新文件和重命名操作
    if args.create:
        # 创建新文件逻辑（无需source参数）
        if args.new_file_name:
            full_name = args.new_file_name
        else:
            full_name = generate_filename(
                args.prefix, args.lang, args.version,
                args.year, args.month, args.day,
                source_name=None  # 创建新文件不依赖源文件
            ) + args.ext
        success, msg = create_new_file(args.old_file, full_name)
    
    else:
        # 重命名操作逻辑（必须提供source）
        if not args.source:
            parser.error("--source 参数在重命名操作中为必填项")
        full_name = generate_filename(
            args.prefix, args.lang, args.version,
            args.year, args.month, args.day,
            args.source
        ) + args.ext
        success, msg = rename_file(args.old_file, full_name, args.source, args.overwrite)
    
    # 输出结果
    print(f"\n执行详情:")
    print(msg)
    print(f"目标文件路径: {os.path.join(args.old_file, full_name)}")
    
    exit(0 if success else 1)