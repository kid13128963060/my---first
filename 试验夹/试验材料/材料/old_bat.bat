<<<<<<< HEAD
@echo off
echo ȷ��Ҫ���ظ����ƶ�����
set /p choice=������ [Y/N]: 
if /i "%choice%"=="Y" (
    echo ���ڱ��ظ����ƶ�����
@echo off
    powershell -WindowStyle Hidden -File "E:\������\�����ļ���\005_�������ѧ����ʽ������,Ӳ��\005_400_���Ա��!1\Scripts\005_410_PowerShell\005_411_PowerShell_���ظ����ƶ�����.ps1"
    echo ���ظ����ƶ����� ok
) else if /i "%choice%"=="N" (
    echo ������ȡ����
) else (
    echo ��Ч���룬���������нű���
)
=======
@echo off
echo ȷ��Ҫ���ظ����ƶ�����
set /p choice=������ [Y/N]: 
if /i "%choice%"=="Y" (
    echo ���ڱ��ظ����ƶ�����
@echo off
    powershell -WindowStyle Hidden -File "E:\������\�����ļ���\005_�������ѧ����ʽ������,Ӳ��\005_400_���Ա��!1\Scripts\005_410_PowerShell\005_411_PowerShell_���ظ����ƶ�����.ps1"
    echo ���ظ����ƶ����� ok
) else if /i "%choice%"=="N" (
    echo ������ȡ����
) else (
    echo ��Ч���룬���������нű���
)
>>>>>>> dcb2bd4413adc8b529063e4a9adb64a4d0dc99e9
pause