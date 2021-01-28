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
>python3 manage.py shell
>from user.models import UserProfile as user
from user.models import Role as role
my_role = role.objects.create(name='admin',remark='管理组')
my_user = user.objects.get(id=1)
my_role.user_set.add(my_user)
菜单数据
Menu.objects.create(parentId=0,name='首页',url='/dashboard',code='dashboard',type=1,icon='el-icon-s-home',sort=1)
Menu.objects.create(parentId=0,name='系统管理',url='/system',code='system',type=1,icon='el-icon-setting',sort=10)
>子菜单
Menu.objects.create(parentId=2,name='用户管理',url='/system/user',code='user',type=2,icon='el-icon-user-solid',sort=1)
Menu.objects.create(parentId=2,name='角色管理',url='/system/role',code='role',type=2,icon='el-icon-coin',sort=2)
Menu.objects.create(parentId=2,name='菜单管理',url='/system/menu',code='menu',type=2,icon='el-icon-menu',sort=3)

>权限按钮，权限ID需要和auth_permission表中相关
Menu.objects.create(parentId=3,name='user:view',code='user:view',type=3,sort=1,permissionId=28)
Menu.objects.create(parentId=3,name='user:change',code='user:change',type=3,sort=2,permissionId=26)
Menu.objects.create(parentId=3,name='user:add',code='user:add',type=3,sort=3,permissionId=25)
Menu.objects.create(parentId=3,name='user:delete',code='user:delete',type=3,sort=4,permissionId=27)
Menu.objects.create(parentId=4,name='role:view',code='role:view',type=3,sort=1,permissionId=24)
Menu.objects.create(parentId=4,name='role:change',code='role:change',type=3,sort=2,permissionId=22)
Menu.objects.create(parentId=4,name='role:add',code='role:add',type=3,sort=3,permissionId=21)
Menu.objects.create(parentId=4,name='role:delete',code='role:delete',type=3,sort=4,permissionId=23)
Menu.objects.create(parentId=5,name='menu:view',code='menu:view',type=3,sort=1,permissionId=32)
Menu.objects.create(parentId=5,name='menu:change',code='menu:change',type=3,sort=2,permissionId=30)
Menu.objects.create(parentId=5,name='menu:add',code='menu:add',type=3,sort=3,permissionId=29)
Menu.objects.create(parentId=5,name='menu:delete',code='menu:delete',type=3,sort=4,permissionId=31)

>用户权限赋予
my_role.permissions.add(21)
my_role.permissions.add(22)
my_role.permissions.add(23)
my_role.permissions.add(24)
my_role.permissions.add(25)
my_role.permissions.add(26)
my_role.permissions.add(27)
my_role.permissions.add(28)
my_role.permissions.add(29)
my_role.permissions.add(30)
my_role.permissions.add(31)
my_role.permissions.add(32)

#问题
django 2.和 python3   兼容性不足
报错
>File "/usr/local/python3/lib/python3.7/site-packages/rest_framework_simplejwt/backends.py", line 44, in encode
    return token.decode('utf-8')
AttributeError: 'str' object has no attribute 'decode'


>vim /usr/local/python3/lib/python3.7/site-packages/rest_framework_simplejwt/backends.py
注释掉
>return token.decode('utf-8')
>return token


>File "/usr/local/python3/lib/python3.7/site-packages/django/db/backends/mysql/operations.py", line 146, in last_executed_query
    query = query.decode(errors='replace')
AttributeError: 'str' object has no attribute 'decode'

>vim /usr/local/python3/lib/python3.7/site-packages/django/db/backends/mysql/operations.py
注释掉
query = query.decode(errors='replace')
query = query.encode(errors='replace')




