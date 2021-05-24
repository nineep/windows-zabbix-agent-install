#! -*- coding: utf-8 -*-
import os
import socket
import time


# 获取本机计算机名称
hostname = socket.gethostname()
# 获取本机ip
ip = socket.gethostbyname(hostname)

replaced_str="YOURHOSTNAME"
replace_str=ip

zabbix_template_conf="C:\zabbix\zabbix_agentd.win.conf.template"
zabbix_conf="C:\zabbix\zabbix_agentd.win.conf"

#with open(zabbix_conf, 'w+', encoding="utf-8") as fout:
#    with open(zabbix_template_conf, 'r+', encoding="utf-8") as fin:
#        fin_content=fin.read()
#        for line in fin_content:
#            #print(line, end="")
#            fout.write(line.replace(replaced_str, replace_str))
            
fin = open(zabbix_template_conf, 'r+', encoding="utf-8")
fout = open(zabbix_conf, 'w+', encoding="utf-8")
for line in fin:
    fout.write(line.replace(replaced_str, replace_str))
fin.close()
fout.close()
print(replaced_str, "替换为", replace_str)
print("文件修改成功")

time.sleep(2)