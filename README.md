# 说明

该项目主要是部署MinIO持久化存储，以及使用Python3进行上传下载查询等代码操作
这只是一个可以部署成功，能够使用python3进行操作的示例项目

使用docker以及docker-compose.yml进行部署

对外开放API端口是：9000
控制台端口是：9001

默认用户名是：admin
默认密码是：minioadmin

项目启动方式
1、进入MinIO-deploy目录
2、修改docker-compose.yml文件中的volumes挂载目录，修改为部署电脑上真实有效路径
3、使用命令:docker-compose up -d 进行启动
4、浏览器输入地址：服务器IP:9001  进行控制台访问
