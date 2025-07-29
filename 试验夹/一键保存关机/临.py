import win32com.client
import pythoncom


def close_all_word_documents():
    try:
        # 初始化COM
        pythoncom.CoInitialize()

        # 获取正在运行的Word实例
        word = win32com.client.GetActiveObject("Word.Application")

        # 检查是否有文档打开
        if word.Documents.Count > 0:
            print(f"发现 {word.Documents.Count} 个打开的Word文档，正在关闭并保存...")
            # 记录初始文档数，防止异常导致死循环
            max_count = word.Documents.Count
            closed_count = 0
            # 由于关闭文档会改变集合，需每次都取第一个文档，直到全部关闭
            while word.Documents.Count > 0 and closed_count < max_count:
                try:
                    doc = word.Documents(1)
                    try:
                        doc.Save()
                        print(f"已保存: {doc.Name}")
                    except Exception as e:
                        print(f"保存文档 {doc.Name} 时出错: {repr(e)}")
                    try:
                        doc.Close()
                        print(f"已关闭: {doc.Name}")
                    except Exception as e:
                        print(f"关闭文档 {doc.Name} 时出错: {repr(e)}")
                except Exception as e:
                    print(f"获取文档对象时出错: {repr(e)}")
                closed_count += 1
        else:
            print("没有打开的Word文档")

        # 可以选择退出Word应用程序
        # word.Quit()
        # print("Word应用程序已退出")

    except Exception as e:
        print(f"操作出错: {repr(e)}")
    finally:
        # 释放COM资源
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    close_all_word_documents()
    print("操作完成")
