<<<<<<< HEAD
import subprocess
# 执行关机操作
try:
    # 设置关机倒计时（秒）
    shutdown_delay = 80
    print(f"将在{shutdown_delay}秒后关机...")
    print("若要取消关机，请打开命令提示符并输入：shutdown /a")

    # 执行关机命令
    subprocess.run(
        f"shutdown /s /t {shutdown_delay}",
        shell=True,
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"关机命令执行失败：{str(e)}")
=======
import subprocess
# 执行关机操作
try:
    # 设置关机倒计时（秒）
    shutdown_delay = 80
    print(f"将在{shutdown_delay}秒后关机...")
    print("若要取消关机，请打开命令提示符并输入：shutdown /a")

    # 执行关机命令
    subprocess.run(
        f"shutdown /s /t {shutdown_delay}",
        shell=True,
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"关机命令执行失败：{str(e)}")
>>>>>>> dcb2bd4413adc8b529063e4a9adb64a4d0dc99e9
