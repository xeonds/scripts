@REM 备份Phigros的存档数据
@REM 第一句是备份，第二局是还原
adb backup -f phi_data.ab com.PigeonGames.Phigros
adb restore phi_data.ab