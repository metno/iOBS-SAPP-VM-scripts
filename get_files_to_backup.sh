#!/bin/bash
cp /opt/ve1/sapp/git/macz/sapp/scripts/ext_sched.py /home/ma/macz/backup/ #Extraction schedule, including extraction window
cp /opt/ve1/sapp/git/macz/sapp/ecflow/sapp/maint/ext/ext_ms_backup.ecf /home/ma/macz/backup/  #(SAPP backup schedule)
cp /opt/ve1/sapp/git/macz/sapp/scripts/settings.py /home/ma/macz/backup/ #(settings for acquisition and processing)
cp /opt/ve1/sapp/git/macz/sapp/scripts/local.py /home/ma/macz/backup/ #(settings for acquisition and processing)
cp /opt/ve1/sapp/git/macz/sapp/scripts/sapp.sh /home/ma/macz/backup/ #(start/stop/status SAPP script)
/opt/ve1/sapp/mysql/msb/my sqldump sapp_oper extraction > /home/ma/macz/backup/extraxtion.sql #(extraction table in sapp_oper database) 
crontab -l > "/home/ma/macz/backup/crontab.txt"
pushd "/home/ma/macz/backup/" > /dev/null  2>&1    
git add /home/ma/macz/backup/*  > /dev/null  2>&1
git commit -m "Automatic commit: backup"   > /dev/null  2>&1
git push origin staging  > /dev/null  2>&1
git push github staging  > /dev/null  2>&1
popd > /dev/null

