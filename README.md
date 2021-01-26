#back_api

#安装环境配置
#一、安装Python
yum install epel-release -y
yum install zlib zlib-devel readline-devel sqlite-devel bzip2-devel openssl-devel gdbm-devel libdbi-devel ncurses-libs kernel-devel libxslt-devel libffi-devel python-devel zlib-devel openldap-devel sshpass gcc git rabbitmq-server supervisor -y
yum localinstall http://dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm
yum install mysql-community-server mysql-devel -y
wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz  #CentOS 7不用安装python2.7
tar -xzvf Python-3.6.6.tgz
cd Python-3.6.6
./configure --prefix=/usr/local/python3
make all
make install
make clean
make distclean  
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3

#二、安装模块
cd /mnt/
git clone -b v3 https://git@github.com:storm0816/back_api.git
mv /mnt/back_api/ /mnt/api_back/
cd /mnt/api_back/
pip3 install -r requirements.txt  #CentOS 7使用pip3

#三、创建项目相关表
cd ../../
python3 manage.py makemigrations
python3 manage.py migrate
#创建超级用户
python3 manage.py createsuperuser

#四、启动部署平台
echo_supervisord_conf > /etc/supervisord.conf
export PYTHONOPTIMIZE=1
vim /etc/supervisord.conf

[program:api_back]
command=/usr/local/python3/bin/python3 manage.py runserver 0.0.0.0:8000 --http_timeout 1200
directory=/mnt/api_back
#stdout_logfile=/var/log/opsmanage-web.log   
#stderr_logfile=/var/log/opsmanage-web-error.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT


#五、插入初始化数据
python3 manage.py shell
from user.models import UserProfile as user
from user.models import Role as role
from django.contrib.auth.models import Group as group

my_user = user.objects.get(id = 1)
my_role = role.objects.create(name='admin, remark='超级管理员')
my_user.groups.add(1)

#插入menu数据，从页面上插入吧，这里后续优化下




