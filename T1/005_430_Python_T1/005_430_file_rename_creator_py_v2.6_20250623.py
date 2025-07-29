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

def generate_filename(prefix="", lang="", version="", year="", month="", day="", source_name=None):
    """标准化文件名生成（增强源文件信息提取，优化语言标识优先级）"""
    # 从源文件提取语言标识（优先于参数）
    if source_name and not lang:
        base_name = os.path.basename(source_name)
        # 检查源文件名中是否包含常见语言标识
        if 'py' in base_name or 'python' in base_name.lower():
            lang = 'Py'
        elif 'ps' in base_name or 'powershell' in base_name.lower():
            lang = 'PowerShell'
        else:
            lang = ''  # 无匹配时留空
    
    # 提取前缀（优先使用参数，其次从源文件名提取）
    if source_name:
        parts = base_name.split('_')
        prefix = prefix or (parts[0] if parts else "")
        prefix = prefix.replace('-', '_')  # 将连字符转换为下划线
        prefix = '_'.join(filter(None, prefix.split()))  # 处理多个连字符或空格
    
    # 提取版本号（优先使用参数，其次从源文件提取）
    if source_name and not version:
        parts = base_name.split('_')
        for part in parts:
            if 'v' in part and '.' in part:
                version = part[1:]
            elif '.' in part and all(p.isdigit() for p in part.split('.')):
                version = part
    
    # 提取日期（严格匹配8位数字）
    if source_name and not (year and month and day):
        parts = base_name.split('_')
        for part in parts:
            if len(part) == 8 and part.isdigit():
                year, month, day = part[:4], part[4:6], part[6:8]
                break
    
    # 日期处理（优先使用参数，其次从源文件提取，最后用当前日期）
    date_part = f"{year}{month.zfill(2)}{day.zfill(2)}" if all([year, month, day]) else datetime.now().strftime("%Y%m%d")
    version = version or "1.0"  # 版本号默认值
    
    # 版本号格式转换：统一为下划线分隔
    if '_' in version:
        version_formatted = version
    elif '.' in version:
        major, minor = version.split('.', 1)
        version_formatted = f"{major}_{minor[:1]}" if len(minor) > 1 else f"{major}_{minor}0"
    else:
        version_formatted = f"{version}_0"
    
    # 组合文件名组件（仅当lang有效时包含语言部分）
    components = filter(None, [prefix, lang, f"v{version_formatted}", date_part])
    return "_".join(components)

def rename_entity(old_folder, new_name, source_name, overwrite=False):
    """重命名文件或文件夹（增强源文件匹配和错误提示）"""
    old_folder = os.path.abspath(old_folder)
    source_path = os.path.join(old_folder, source_name)
    if not os.path.exists(source_path):
        # 模糊匹配源文件或文件夹（不区分大小写）
        source_candidates = [f for f in os.listdir(old_folder) if source_name.lower() in f.lower()]
        if source_candidates:
            source_path = os.path.join(old_folder, source_candidates[0])
            print(f"提示: 自动匹配源文件/文件夹: {source_candidates[0]}")
        else:
            return False, f"错误: 源文件/文件夹不存在 ({source_path})\n当前文件夹内容: {', '.join(os.listdir(old_folder))}"
    new_path = os.path.join(old_folder, new_name)
    
    # 优化错误提示信息格式
    if os.path.exists(new_path):
        if overwrite:
            try:
                if os.path.isfile(new_path):
                    os.remove(new_path)
                    print(f"已删除冲突文件: {new_path}")
                else:
                    import shutil
                    shutil.rmtree(new_path)
                    print(f"已删除冲突文件夹: {new_path}")
            except Exception as e:
                return False, f"删除冲突文件/文件夹失败: {str(e)}"
        else:
            return False, f"错误: 目标文件/文件夹已存在 ({new_path})，请使用 --overwrite 参数覆盖"
    
    try:
        os.rename(source_path, new_path)
        return True, f"成功重命名: {source_path} -> {new_path}"
    except Exception as e:
        return False, f"重命名失败: {str(e)}"
def create_new_entity(folder_path, entity_name):
    """创建新文件或文件夹"""
    entity_path = os.path.join(folder_path, entity_name)
    try:
        if '.' in entity_name:
            with open(entity_path, 'w') as f:
                pass  # 创建空文件
            return True, f"成功创建新文件: {entity_path}"
        else:
            os.makedirs(entity_path)
            return True, f"成功创建新文件夹: {entity_path}"
    except Exception as e:
        return False, f"创建新文件/文件夹失败: {str(e)}"
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='文件和文件夹重命名与创建工具')
    parser.add_argument('--old_folder', help='文件夹路径', default=None)
    parser.add_argument('--prefix', help='文件名/文件夹名前缀', default='')  # 默认为空，避免强制添加
    parser.add_argument('--lang', help='语言标识（如py/ps）', default='')  # 默认留空，优先从源文件提取
    parser.add_argument('-e', '--ext', help='文件扩展名（可带点号）', default=None)
    parser.add_argument('--version', help='版本号', default='1.0')
    parser.add_argument('--year', help='年份', default='')
    parser.add_argument('--month', help='月份', default='')
    parser.add_argument('--day', help='日期', default='')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在文件/文件夹')
    parser.add_argument('--source', help='源文件名/文件夹名（重命名时必选）', required=False)
    parser.add_argument('--new_entity_name', help='手动指定新文件名/文件夹名', default=None)
    parser.add_argument('--create', action='store_true', help='执行创建新文件/文件夹操作')
    
    args = parser.parse_args()
    
    # 处理文件夹路径
    if args.old_folder:
        args.old_folder = os.path.abspath(args.old_folder)
        if not os.path.exists(args.old_folder):
            print(f"警告: 文件夹不存在，尝试获取资源管理器路径: {args.old_folder}")
            args.old_folder = get_last_active_explorer_path(args.old_folder)
    else:
        args.old_folder = get_last_active_explorer_path()
    
    # 最终校验文件夹有效性
    if not args.old_folder or not os.path.exists(args.old_folder):
        print("\n错误: 无法找到有效文件夹！")
        exit(1)
    
    # 区分创建新文件/文件夹和重命名操作
    if args.create:
        # 创建操作的ext处理逻辑
        args.ext = args.ext if args.ext else None
        if not args.ext:
            # 根据语言标识自动设置扩展名（仅当lang有效时）
            if args.lang.lower() == 'ps':
                args.ext = '.ps'
            else:
                args.ext = '.py'
        args.ext = args.ext or '.py'
        
        if args.new_entity_name:
            full_name = args.new_entity_name.replace('-', '_')
            if '.' not in full_name:
                full_name += args.ext
        else:
            full_name = generate_filename(
                args.prefix, args.lang, args.version,
                args.year, args.month, args.day
            )
            if '.' not in full_name:
                full_name += args.ext
        success, msg = create_new_entity(args.old_folder, full_name)
    
    else:
        if not args.source:
            parser.error("--source 参数在重命名时为必填项")
        source_name = args.source
        source_path = os.path.join(args.old_folder, source_name)
        
        # 先进行模糊匹配找到正确源文件
        if not os.path.exists(source_path):
            source_candidates = [f for f in os.listdir(args.old_folder) if source_name.lower() in f.lower()]
            if source_candidates:
                source_path = os.path.join(args.old_folder, source_candidates[0])
                print(f"提示: 自动匹配源文件/文件夹: {source_candidates[0]}")
            else:
                parser.error(f"错误: 源文件/文件夹不存在 ({source_path})")
        
        # 重命名操作的ext处理逻辑（优先使用源文件扩展名）
        if not args.ext:
            if os.path.isfile(source_path):
                _, ext = os.path.splitext(source_path)
                args.ext = ext if ext else ('.ps' if args.lang.lower() == 'ps' else '.py')
            else:
                args.ext = '.ps' if args.lang.lower() == 'ps' else '.py'  # 文件夹默认扩展名
        args.ext = args.ext or ('.ps' if args.lang.lower() == 'ps' else '.py')
        
        is_file = os.path.isfile(source_path)
        if args.new_entity_name:
            full_name = args.new_entity_name.replace('-', '_')
            if '.' not in full_name and is_file:
                full_name += args.ext
        else:
            full_name = generate_filename(
                args.prefix, args.lang, args.version,
                args.year, args.month, args.day, source_name
            )
            if '.' not in full_name and is_file:
                full_name += args.ext
        
        # 执行重命名时传入overwrite参数
        success, msg = rename_entity(args.old_folder, full_name, source_name, args.overwrite)
    
    # 输出调试信息
    print(f"\n[调试信息]")
    print(f"args.ext: {args.ext}")
    print(f"full_name: {full_name}")
    print(f"source_path: {source_path}")
    print(f"is_file: {is_file}")
    print(f"overwrite参数: {args.overwrite}")
    
    # 输出结果
    print(f"\n执行详情:")
    print(msg)
    print(f"目标路径: {os.path.join(args.old_folder, full_name)}")
    
    exit(0 if success else 1)