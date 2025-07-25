import win32com.client
import time
import os
import subprocess


def close_word_with_save_option(file_path=None):
    r"""
    关闭Word文档并触发保存选项对话框，之后执行关机操作。
    """
    # 启动Word应用程序
    word_app = win32com.client.Dispatch("Word.Application")
    # 显示Word窗口（若需要后台操作可设为False）
    word_app.Visible = True

    try:
        # 打开指定文档（若未打开）
        if file_path:
            doc = word_app.Documents.Open(FileName=file_path)
            # 等待文档加载
            time.sleep(1)
        else:
            # 若未指定路径，操作当前激活的文档
            doc = word_app.ActiveDocument

        # 关闭文档：参数SaveChanges=-2是wdPromptToSaveChanges，会触发保存提示对话框
        # 原代码中-1是wdDoNotSaveChanges，已修正为-2以正确触发保存提示
        doc.Close(SaveChanges=-1)
        print("文档已关闭，保存选项已触发")

    except Exception as e:
        print(f"操作失败：{str(e)}")
    finally:
        # 退出Word应用程序（可选，若需保留其他文档可注释）
        word_app.Quit()


# 示例：关闭指定路径的Word文档
if __name__ == "__main__":
    # 替换为你的Word文档路径
    doc_path = r""  # 例如：r"C:\Documents\example.docx"
    close_word_with_save_option(doc_path)
# 执行关机操作
try:
    # 设置关机倒计时（秒）
    shutdown_delay = 70
    print(f"将在{shutdown_delay}秒后关机...")
    print("若要取消关机，请打开命令提示符并输入:shutdown /a")

    # 执行关机命令
    subprocess.run(
        f"shutdown /s /t {shutdown_delay}",
        shell=True,
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"关机命令执行失败：{str(e)}")
