@echo off
echo ȷ��Ҫ���ظ����ƶ�����
set /p choice=������ [Y/N]: 
if /i "%choice%"=="Y" (
    echo ���ڱ��ظ����ƶ�����
@echo off
    powershell -WindowStyle Hidden -File "E:\������\�����ļ���\005_�������ѧ����ʽ������,Ӳ��\005_400_���Ա��_1\�ļ�ϵͳ����ģ��\�ļ�����\�ļ�������Ԫ���ݹ���\�ƶ�-��������-����\005_411_PowerShell_���ظ����ƶ�����.ps1"
    echo ���ظ����ƶ����� ok
) else if /i "%choice%"=="N" (
    echo ������ȡ����
) else (
    echo ��Ч���룬���������нű���
)
pause