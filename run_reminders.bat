@echo off
REM 上课提醒任务批处理文件
REM 可以通过Windows任务计划程序定期执行此文件

cd /d "%~dp0"
python run_reminders.py

REM 如果需要查看输出，取消下面一行的注释
REM pause