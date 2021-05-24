# 目的
已有一批windows服务器，需要装上zabbix agent获取显卡监控指标，      
这批服务器没有集中的账户管理和其他下发工具，但是知道admin用户密码。    

*确保windows服务器 135，445端口打开，供net use连接远程windows*      

*配置zabbix时，将config-zabbix打包为exe文件，传到远程windows执行配置*     

# python安装zabbix

## 下载安装python

    https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe


## 修改host文件

    hosts

## 执行脚本        

    python3 zabbix-install.py
    python3 zabbix-stop.py


# 手动执行流程

## 与远程windows建立连接
net use \\10.60.158.101\c$ /user:admin PASSWORD

## 删除连接
net use \\10.60.158.101\c$ /del

## 查看远程文件夹
dir \\10.60.158.101\c$\zabbix

## 查看远程文件内容
type \\10.70.65.92\c$\zabbix\zabbix_agentd.win.conf

## 复制文件到远程主机
xcopy zabbix  \\10.70.65.92\c$\zabbix /E

## 远程命令调用
wmic /node:10.60.158.101 /user:"USERNAME" /password:"PASSWORD" process call create "cmd.exe /c powershell.exe -command YOUR_COMMAND"

	## 以下命令替换 YOUR_COMMAND调用
	
	# 修改zabbix配置文件
	C:\zabbix\config-zabbix.exe    （将zabbix_agentd.win.conf.template中的YOURHOSTNAME修改为远程主机的IP，生成新的配置文件zabbix_agentd.win.conf）
 
	# 安装zabbix
	C:\zabbix\zabbix_agentd.exe -i -c C:\zabbix\zabbix_agentd.win.conf

	# 启动zabbix
	C:\zabbix\zabbix_agentd.exe -s -c C:\zabbix\zabbix_agentd.win.conf

	# 关闭防火墙
	netsh advfirewall set allprofiles state off
