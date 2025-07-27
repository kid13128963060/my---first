import win32gui
import win32con
import win32api
import time
import psutil


def force_save_and_close_notepad():
    # 记事本窗口类名
    NOTEPAD_CLASS = "Notepad"
    txt_hwnds = []

    # 枚举所有记事本窗口
    def enum_callback(hwnd, extra):
        if win32gui.GetClassName(hwnd) == NOTEPAD_CLASS:
            txt_hwnds.append(hwnd)
        return True

    win32gui.EnumWindows(enum_callback, None)
    print(f"找到 {len(txt_hwnds)} 个记事本窗口")

    for hwnd in txt_hwnds:
        title = win32gui.GetWindowText(hwnd)
        print(f"处理窗口: {title} (句柄: {hwnd})")

        try:
            # 1. 激活窗口
            win32gui.SetForegroundWindow(hwnd)
            win32gui.SetActiveWindow(hwnd)
            time.sleep(0.3)

            # 2. 强制保存 - 使用Ctrl+S快捷键
            # 发送Ctrl+S组合键确保保存
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)  # 按下Ctrl键
            win32api.keybd_event(ord('S'), 0, 0, 0)  # 按下S键
            time.sleep(0.1)  # 等待按键响应
            win32api.keybd_event(
                ord('S'), 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放S键
            win32api.keybd_event(win32con.VK_CONTROL, 0,
                                 win32con.KEYEVENTF_KEYUP, 0)  # 释放Ctrl键
            time.sleep(0.5)  # 等待保存完成

            # 3. 获取编辑控件并清空撤销缓冲区，避免关闭时提示
            edit_hwnd = win32gui.FindWindowEx(hwnd, None, "Edit", None)
            if edit_hwnd:
                # 清空撤销缓冲区，让记事本认为没有未保存的更改
                win32api.SendMessage(
                    edit_hwnd, win32con.EM_EMPTYUNDOBUFFER, 0, 0)
                # 设置 Modified 标志为 False
                win32api.SendMessage(edit_hwnd, win32con.EM_SETMODIFY, 0, 0)
                time.sleep(0.2)

            # 4. 发送关闭消息
            result = win32api.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            if result == 0:
                # 备用：通过进程关闭（针对无响应情况）
                pid = win32api.GetWindowThreadProcessId(hwnd)[1]
                try:
                    p = psutil.Process(pid)
                    p.terminate()
                    print(f"强制终止进程 {pid}")
                except Exception as e:
                    print(f"终止进程失败: {e}")
            time.sleep(0.3)

        except Exception as e:
            print(f"处理窗口时出错: {e}")
            continue

    print(f"已处理 {len(txt_hwnds)} 个记事本窗口")


if __name__ == "__main__":
    force_save_and_close_notepad()
