import win32com.client
import time
import pythoncom
import time


def force_save_and_close_all_word():
    """强制保存并关闭所有打开的Word文档(不显示保存对话框）"""
    # 初始化 Word 应用对象
    word_app = None
    try:
        # 尝试获取已有的 Word 应用实例，若失败则创建新实例
        word_app = win32com.client.GetActiveObject("Word.Application")
    except win32com.client.DispatchException:
        try:
            word_app = win32com.client.Dispatch("Word.Application")
        except Exception as e:
            print(f"创建或获取 Word 应用实例失败: {str(e)}")
            return
    except Exception as e:
        print(f"获取 Word 应用实例时发生错误: {str(e)}")
        return

    try:
        # 确保 Word 可见（部分操作可能需要界面上下文）
        word_app.Visible = True
        # 处理 COM 线程模型，避免线程相关问题
        pythoncom.CoInitialize()

        # 从最后一个文档开始关闭（避免索引变化问题）
        for i in range(word_app.Documents.Count, 0, -1):
            try:
                doc = word_app.Documents(i)
                # 强制保存（-1 表示 wdSaveChanges，即保存更改  0 表示不保存，2 表示提示保存  ）
                doc.Close(SaveChanges=-1)
                print(f"已强制保存并关闭 Word 文档: {doc.Name}")
                time.sleep(0.3)  # 短暂延迟确保操作完成
            except Exception as doc_e:
                print(
                    f"处理文档 {word_app.Documents(i).Name if i <= word_app.Documents.Count else '未知文档'} 时出错: {str(doc_e)}")

        # 关闭 Word 应用程序本身
        try:
            word_app.Quit()
            print("Word 程序已退出")
        except Exception as quit_e:
            print(f"关闭 Word 应用程序时出错: {str(quit_e)}")

    except Exception as e:
        print(f"操作过程中发生错误: {str(e)}")
    finally:
        # 释放 COM 对象，清理资源
        if word_app:
            win32com.client.Dispatch("Python.Runtime.ComObject").Release()
            del word_app
        pythoncom.CoUninitialize()  # 释放 COM 线程初始化


if __name__ == "__main__":
    force_save_and_close_all_word()
