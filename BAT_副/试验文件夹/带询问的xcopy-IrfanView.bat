@echo off
echo ȷ��Ҫ���ظ����ƶ�����
set /p choice=������ [Y/N]: 

if /i "%choice%"=="Y" (
    echo ���ڱ��ظ����ƶ�����
    xcopy C:\Users\Administrator\AppData\Roaming\IrfanView E:\������\8000-���ļ���\009-�����ļ���-��\005-238-irfanview!2-���ñ���\ /S /E /Y/I
    echo ���ظ����ƶ����� ok
) else if /i "%choice%"=="N" (
    echo ������ȡ����
) else (
    echo ��Ч���룬���������нű���
)
pause