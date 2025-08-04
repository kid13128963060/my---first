@echo off
echo ȷ��Ҫ�ƶ˸��Ǳ�������
set /p choice=������ [Y/N]: 
if /i "%choice%"=="Y" (
    echo ���ڱ��ظ����ƶ�����
@echo off
    powershell -WindowStyle Hidden -File "E:\������\�����ļ���\005_�������ѧ����ʽ������,Ӳ��\005_400_���Ա��!1\Scripts\005_490_���������\�����\005_411_PowerShell_�ƶ˸��Ǳ�������_T1.ps1"
    echo ���ظ����ƶ����� ok
) else if /i "%choice%"=="N" (
    echo ������ȡ����
) else (
    echo ��Ч���룬���������нű���
)
