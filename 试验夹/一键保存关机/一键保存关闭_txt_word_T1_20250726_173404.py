import win32com.client
import win32gui
import win32con
import win32api
import psutil
import time
import pythoncom
import threading  # 新增：确保线程独立性


def force_save_and_close_all_word():
    """强制保存并关闭所有打开的Word文档(不显示保存对话框）"""
    word_app = None
    try:
        word_app = win32com.client.GetActiveObject("Word.Application")
    except win32com.client.DispatchException:
        try:
            word_app = win32com.client.Dispatch("Word.Application")
        except Exception as e:
            print(f"创建或获取Word应用实例失败: {str(e)}")
            return
    except Exception as e:
        print(f"获取Word应用实例时发生错误: {str(e)}")
        return

    try:
        word_app.Visible = True
        pythoncom.CoInitialize()  # 初始化COM线程
        # 从最后一个文档开始关闭
        for i in range(word_app.Documents.Count, 0, -1):
            try:
                doc = word_app.Documents(i)
                doc.Close(SaveChanges=-1)  # 强制保存关闭
                print(f"已关闭Word文档: {doc.Name}")
                time.sleep(0.5)  # 延长延迟确保完成
            except Exception as doc_e:
                print(f"处理文档出错: {str(doc_e)}")
        # 关闭Word应用
        word_app.Quit()
        print("Word程序已退出")
    except Exception as e:
        print(f"Word操作错误: {str(e)}")
    finally:
        if word_app:
            del word_app
        pythoncom.CoUninitialize()  # 释放COM线程
        time.sleep(1)  # 新增：等待Word完全退出，释放系统资源


def force_save_and_close_notepad():
    """修复后的记事本处理函数：增强窗口激活和关闭可靠性"""
    NOTEPAD_CLASS = "Notepad"
    txt_hwnds = []

    # 枚举所有记事本窗口（确保线程状态正常）
    def enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetClassName(hwnd) == NOTEPAD_CLASS:
            txt_hwnds.append(hwnd)
        return True

    # 关键修复1：确保枚举窗口时线程无COM干扰
    win32gui.EnumWindows(enum_callback, None)
    print(f"找到 {len(txt_hwnds)} 个记事本窗口（可见状态）")

    for hwnd in txt_hwnds:
        title = win32gui.GetWindowText(hwnd)
        print(f"处理窗口: {title} (句柄: {hwnd})")
        try:
            # 关键修复2：增强窗口激活（先还原窗口，再获取焦点）
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 确保窗口不最小化
            win32gui.SetForegroundWindow(hwnd)  # 激活窗口
            win32gui.SetActiveWindow(hwnd)
            time.sleep(0.5)  # 延长激活等待时间

            # 强制保存（Ctrl+S）
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            win32api.keybd_event(ord('S'), 0, 0, 0)
            time.sleep(0.2)  # 延长按键等待
            win32api.keybd_event(ord('S'), 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(win32con.VK_CONTROL, 0,
                                 win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(1)  # 关键修复3：延长保存等待（确保保存完成）

            # 清空撤销缓冲区，避免关闭提示
            edit_hwnd = win32gui.FindWindowEx(hwnd, None, "Edit", None)
            if edit_hwnd:
                win32api.SendMessage(
                    edit_hwnd, win32con.EM_EMPTYUNDOBUFFER, 0, 0)
                win32api.SendMessage(edit_hwnd, win32con.EM_SETMODIFY, 0, 0)
                time.sleep(0.3)

            # 关键修复4：增强关闭逻辑（先发送关闭消息，再检查是否真的关闭）
            # 发送WM_CLOSE
            win32api.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            time.sleep(0.5)  # 等待关闭响应
            # 检查窗口是否仍存在
            if win32gui.IsWindow(hwnd):
                # 强制终止进程
                pid = win32api.GetWindowThreadProcessId(hwnd)[1]
                p = psutil.Process(pid)
                p.terminate()
                print(f"记事本窗口未响应，已强制终止进程 {pid}")
            else:
                print(f"记事本窗口 {title} 已正常关闭")

            time.sleep(0.3)
        except Exception as e:
            print(f"处理记事本出错: {str(e)}")

    print(f"已处理 {len(txt_hwnds)} 个记事本窗口")


if __name__ == "__main__":
    print("开始处理Word文档...")
    force_save_and_close_all_word()

    print("\n开始处理记事本窗口...")
    force_save_and_close_notepad()  # 此时系统资源已释放，记事本处理不受干扰

    print("\n所有操作已完成")
