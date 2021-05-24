#! -*- coding: utf-8 -*-
import os
import subprocess
import time
import configparser
import re


# 默认C盘下的文件夹，例：C:\zabbix
dir_name = r"\zabbix"
project_path = os.path.dirname(os.path.abspath(__file__))
hosts_file = os.path.join(project_path, "hosts")
config = configparser.ConfigParser()


def exec_command(command):
    cmd = subprocess.getstatusoutput(command)
    return cmd[1]


# 查看已连接的网络
def check_connected_host():
    print("查看已连接的网络：")
    rs = subprocess.getstatusoutput("net use")
    return rs[1]


# 登录到远程windows服务器
# net use \\10.60.158.101\c$ /user:admin PASSWORD
def generate_login_remote_server_command(ip, user, password):
    # 注意反斜杠转义
    ip_option = r"\\" + ip + r"\c$"
    user_option = "/user:" + user
    password_option = password
    command = "net use " + ip_option + " " + user_option + " " + password_option
    return command


def generate_ip_path(ip, path):
    # \\10.60.158.101\c$
    ip_option = r"\\" + ip + r"\c$"
    path_option = path
    ip_path = ip_option + path_option
    return ip_path


def connect_remote_server(ip, user, password):
    command = generate_login_remote_server_command(ip=ip, user=user, password=password)
    print("连接远程服务器：", command)
    #exec_command(command)
    result = subprocess.getstatusoutput(command)
    return result[0]


# 删除网络连接
# net use \\10.60.158.101\c$ /del
def disconnect_remote_server(ip):
    ip_path = generate_ip_path(ip, "")
    command = "net use " + ip_path + " /del"
    exec_command(command)
    print("断开网络连接：", command)


# 创建zabbix目录
# md \\10.60.158.101\c$\zabbix
def create_dir(ip, dir_name):
    # command = r'wmic /node:10.60.158.190 /user:admin /password:QWEqwe@123 process call create "cmd.exe /c md C:\zabbix"'
    ip_path = generate_ip_path(ip=ip, path=dir_name)
    command = "md " + ip_path
    print("执行创建目录命令：", command)
    exec_command(command)
    rs = exec_command(command)
    print(rs)


# 复制zabbix文件到远程windows
# xcopy zabbix  \\10.70.65.92\c$\zabbix /E
def copy_file_to_remote(ip, dir_name):
    ip_path = generate_ip_path(ip=ip, path=dir_name)
    zabbix_files = os.path.join(project_path, "zabbix")
    # subprocess调用cmd执行命令，copy到远程，这里需要powershell
    command = "xcopy " + zabbix_files + " " + ip_path + " " + "/E" + " " + "/y"
    print("执行拷贝目录命令：", command)
    # rs = exec_command(command)
    #rs = subprocess.check_output(command)
    rs = subprocess.getstatusoutput(command)
    return rs[0]


# 查看文件
# dir \\10.60.158.101\c$\zabbix
def check_remote_files(ip, dir_name):
    ip_path = generate_ip_path(ip=ip, path=dir_name)
    command = "dir " + ip_path
    print("查看远程文件：", command)
    rs = exec_command(command)
    print(rs)


zabbix_command_dict = {"停止zabbix: ": "C:\zabbix\zabbix_agentd.exe -x"}


# wmic /node:10.60.158.101 /user:admin /password:PASSWORD process call create "cmd.exe /c powershell.exe -command C:\zabbix\config-zabbix.exe"
def remote_process_call(ip, user, password, subcommand_k, subcommand_v):
    node_option = " /node:" + ip 
    user_option = " /user:" + '"' + user + '"'
    password_option = " /password:" + '"' + password + '"'
    suffix_option = ' process call create ' + '"' + 'cmd.exe /c powershell.exe -command ' + subcommand_v + '"'
    command = "wmic " + node_option + user_option + password_option + suffix_option
    print(subcommand_k, command)
    rs = exec_command(command)
    print(rs)


def install_zabbix(ip, user, password, dir_name):
    # 连接网络
    #connect_remote_server(ip=ip, user=user, password=password)
    
    # 查看已连接的网络
    #rs1 = check_connected_host()
    #print(rs1)

    # 创建目录
    #create_dir(ip=ip, dir_name=dir_name)
    
    # 复制文件到远程主机
    #copy_file_to_remote(ip=ip, dir_name=dir_name)

    # 查看远程主机文件
    #check_remote_files(ip=ip, dir_name=dir_name)

    # 远程执行命令，配置zabbix
    for k,v in zabbix_command_dict.items():
        time.sleep(2)
        remote_process_call(ip=ip, user=user, password=password, subcommand_k=k, subcommand_v=v)
        
    # 断开网络
    disconnect_remote_server(ip=ip)
    rs2 = check_connected_host()
    print(rs2)


def get_info_to_exec(dir_name):
    # 从hosts文件获取信息，执行配置winrm
    with open(hosts_file, "r", encoding="utf-8") as f:
        for line in f.read().splitlines():
            # print(line[0], type(line[0]))
            # 去掉[开头的行
            if line[0] != "[" and line[0] != "#":
                line_list = re.split(r"[ ]+", line)
                # 所需参数赋值
                ip = line_list[0]
                user = line_list[1].split("=")[-1]
                password = line_list[2].split("=")[-1]
                print()
                print("+++++++++++++++++++开始配置: " + ip  + "+++++++++++++++++++++++++++++++++++++++++")
                print("配置服务器ip:", ip)
                print("登录user:", user)
                print("登录password:", password)
                time.sleep(1)
                
                # 连接网络
                connect_rs = connect_remote_server(ip=ip, user=user, password=password)
                if connect_rs != 0:
                    print("网络连接失败，跳过此主机...")
                    continue
                    
                # 查看已连接的网络
                rs1 = check_connected_host()
                print(rs1)

                # 创建目录
                #create_dir(ip=ip, dir_name=dir_name)
    
                # 复制文件到远程主机
                #copy_rs = copy_file_to_remote(ip=ip, dir_name=dir_name)
                #if copy_rs != 0:
                #    print("此主机已经配置了zabbix agent，且agent正在运行中，跳过此主机...")
                #    # 断开网络
                #    disconnect_remote_server(ip=ip)
                #    rs2 = check_connected_host()
                #    print(rs2)
                #    # 跳过此项
                #    continue
                
                install_zabbix(ip=ip, user=user, password=password, dir_name=dir_name)
            else:
                print()
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("注释行，跳过...")


if __name__ == "__main__":
    get_info_to_exec(dir_name=dir_name)
