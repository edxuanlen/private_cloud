




nmap -sP 172.20.10.15/24



useradd -d /home/undead -m undead

chown -R undead:undead /home/undead
chmod 760 /home/undead




## 挂载

fdisk -l

fdisk /dev/sda1

mkfs -t ext4 /dev/sda1


mount /dev/sda1 ./mnt

vi /etc/fstab 

/dev/sda1   /mnt    ext4    defaults    1   1


下载 hdparm 测速

hdparm -Tt /dev/sda


## 换源
https://blog.csdn.net/u014091490/article/details/99675366

buster
## samba 文件共享协议

sudo apt update && sudo apt upgrade && sudo apt-get install -y samba


mkdir data 

chown -R edxuanlen:edxuanlen /mnt/data

chmod -R ug=rwx,o=rx /mnt/data



# 新建用户
smbdpasswd -a username




## 公共
# 配置段名称，可以随意取
[public]
# 共享段备注
comment = public folder
# 共享文件夹路径，必填
path = /home/edxuanlen/mnt/public
# 允许可以写入
read only = no
# 允许匿名访问
public = yes
# 是否出现在网络发现中
browseable = yes

[edxuanlen]
comment = edxuanlen files
path = /home/edxuanlen/mnt/public
# 不出现在网络发现中
browseable = no
# 禁止匿名访问
public = no
writable = yes
# 只允许pi用户访问
valid users = edxuanlen




mysql -uroot -p'你的密码' -e 
'create user nextcloud@"%" identified by "nextcloud数据库密码"; 
create database nextcloud default charset=utf8mb4; grant all privileges on nextcloud.* to nextcloud@"%"; flush privileges;'