@echo off
echo ȷ��Ҫ�ƶ˸��Ǳ�������
set /p choice=������ [Y/N]: 

if /i "%choice%"=="Y" (
    echo ȷ��Ҫ�ƶ˸��Ǳ�������
taskkill /IM Listary.exe /F
echo Listary�ѹر�
    xcopy E:\������\8000-���ļ���\009-�����ļ���-��\005-209-Listary!2-����\�Զ������� C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\ /S /E /Y/I
    taskkill /IM i_view64.exe /F
    echo i_view64�ѹر�
    xcopy E:\������\8000-���ļ���\009-�����ļ���-��\005-238-irfanview!2-���ñ��� C:\Users\Administrator\AppData\Roaming\IrfanView\ /S /E /Y/I
    taskkill /IM Ditto.exe /F
    echo Ditto�ѹر�
    xcopy E:\������\8000-���ļ���\009-�����ļ���-��\005-211-Ditto!2-���ݱ���\ C:\Users\Administrator\AppData\Roaming\Ditto\ /S /E /Y/I
    start "" "C:\Program Files\Ditto\Ditto.exe"
    echo Ditto ������
    start "" "C:\Program Files\Listary\Listary.exe"
    echo Listary ������
    echo �ƶ˸��Ǳ������� ok
) else if /i "%choice%"=="N" (
    echo ������ȡ����
) else (
    echo ��Ч���룬���������нű���
)
pause
