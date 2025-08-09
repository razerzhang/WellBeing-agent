# 🚀 维尔必应应用部署指南

本指南将帮助你将维尔必应应用部署到阿里云服务器上。

## 📋 部署前准备

### 1. 阿里云服务器要求
- **操作系统**: Ubuntu 20.04+ 或 CentOS 7+
- **内存**: 至少 2GB RAM
- **存储**: 至少 10GB 可用空间
- **网络**: 公网IP地址
- **安全组**: 开放端口 22(SSH)、80(HTTP)、443(HTTPS)、8000(应用)

### 2. 域名配置（可选）
- 购买域名并解析到服务器IP
- 申请SSL证书（推荐使用Let's Encrypt免费证书）

## 🛠️ 部署方式选择

### 方式一：Docker部署（推荐）
- 优点：环境隔离、易于管理、支持滚动更新
- 适用：生产环境、需要容器化管理的场景

### 方式二：传统部署
- 优点：资源占用少、启动快速
- 适用：资源有限的服务器、简单部署场景

## 🚀 快速部署

### 1. 上传代码到服务器
```bash
# 在本地打包代码
tar -czf wellbeing-agent.tar.gz . --exclude=node_modules --exclude=.git

# 上传到服务器
scp wellbeing-agent.tar.gz root@your-server-ip:/home/

# 在服务器上解压
cd /home
tar -xzf wellbeing-agent.tar.gz
cd wellbeing-agent
```

### 2. 运行自动部署脚本
```bash
# 给脚本执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

脚本会自动：
- 检查系统要求
- 安装依赖
- 构建前端
- 配置防火墙
- 启动应用
- 创建系统服务

## 🔧 手动部署步骤

### 1. 安装系统依赖
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-dev build-essential curl wget git

# CentOS/RHEL
sudo yum update -y
sudo yum install -y python3 python3-pip python3-devel gcc curl wget git
```

### 2. 安装Python依赖
```bash
pip3 install --user -r requirements.txt
```

### 3. 安装Node.js（用于构建前端）
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 4. 构建前端
```bash
cd frontend
npm install
npm run build
cd ..
```

### 5. 启动应用
```bash
# 创建必要目录
mkdir -p logs data

# 启动应用
python3 server.prod.py
```

## 🐳 Docker部署

### 1. 安装Docker
```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 构建和启动
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 🌐 配置反向代理（推荐）

### 1. 安装Nginx
```bash
sudo apt-get install nginx
```

### 2. 配置Nginx
```bash
# 复制配置文件
sudo cp nginx.conf /etc/nginx/nginx.conf

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 3. 配置SSL证书（Let's Encrypt）
```bash
# 安装certbot
sudo apt-get install certbot python3-certbot-nginx

# 申请证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔒 安全配置

### 1. 防火墙配置
```bash
# Ubuntu UFW
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp

# CentOS firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 2. 安全组配置
在阿里云控制台配置安全组：
- 入方向：22(SSH)、80(HTTP)、443(HTTPS)、8000(应用)
- 出方向：全部开放

### 3. 系统安全
```bash
# 更新系统
sudo apt-get update && sudo apt-get upgrade -y

# 配置SSH密钥登录
# 禁用密码登录
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

## 📊 监控和维护

### 1. 系统服务管理
```bash
# 查看服务状态
sudo systemctl status wellbeing-agent

# 启动服务
sudo systemctl start wellbeing-agent

# 停止服务
sudo systemctl stop wellbeing-agent

# 重启服务
sudo systemctl restart wellbeing-agent

# 查看日志
sudo journalctl -u wellbeing-agent -f
```

### 2. 应用日志
```bash
# 查看应用日志
tail -f logs/app.log

# 查看Docker日志
docker-compose logs -f
```

### 3. 性能监控
```bash
# 查看系统资源
htop
df -h
free -h

# 查看网络连接
netstat -tlnp
ss -tlnp
```

## 🔄 更新部署

### 1. 代码更新
```bash
# 停止服务
sudo systemctl stop wellbeing-agent

# 备份当前版本
cp -r /home/wellbeing-agent /home/wellbeing-agent-backup-$(date +%Y%m%d)

# 更新代码
cd /home/wellbeing-agent
git pull origin main

# 重新构建前端
cd frontend
npm run build
cd ..

# 重启服务
sudo systemctl start wellbeing-agent
```

### 2. Docker更新
```bash
# 拉取最新代码
git pull origin main

# 重新构建和部署
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🚨 故障排除

### 1. 常见问题
- **端口被占用**: 检查端口占用 `netstat -tlnp | grep 8000`
- **权限问题**: 检查文件权限和用户权限
- **依赖缺失**: 检查Python包和Node.js模块
- **内存不足**: 检查服务器内存使用情况

### 2. 日志分析
```bash
# 查看系统日志
sudo journalctl -xe

# 查看应用日志
tail -f logs/app.log

# 查看Nginx日志
sudo tail -f /var/log/nginx/error.log
```

### 3. 重启服务
```bash
# 重启应用
sudo systemctl restart wellbeing-agent

# 重启Docker服务
docker-compose restart

# 重启Nginx
sudo systemctl restart nginx
```

## 📞 技术支持

如果遇到部署问题，请检查：
1. 系统要求是否满足
2. 依赖是否正确安装
3. 端口是否被占用
4. 防火墙配置是否正确
5. 日志中的错误信息

## 🎯 部署完成检查清单

- [ ] 应用能够正常启动
- [ ] 前端页面可以访问
- [ ] API接口正常工作
- [ ] 流式聊天功能正常
- [ ] 防火墙配置正确
- [ ] SSL证书配置（如果使用HTTPS）
- [ ] 系统服务配置
- [ ] 日志记录正常
- [ ] 监控告警配置

恭喜！你的维尔必应应用已经成功部署到阿里云服务器上！🎉
