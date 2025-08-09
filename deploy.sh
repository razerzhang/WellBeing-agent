#!/bin/bash

# 维尔必应应用部署脚本
# 用于在阿里云服务器上部署应用

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为root用户
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "检测到root用户，建议使用普通用户运行"
        read -p "是否继续？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# 检查系统要求
check_system() {
    log_info "检查系统要求..."
    
    # 检查操作系统
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_success "操作系统: Linux"
    else
        log_error "不支持的操作系统: $OSTYPE"
        exit 1
    fi
    
    # 检查Python版本
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        log_success "Python版本: $PYTHON_VERSION"
    else
        log_error "Python3未安装"
        exit 1
    fi
    
    # 检查pip
    if command -v pip3 &> /dev/null; then
        log_success "pip3已安装"
    else
        log_error "pip3未安装"
        exit 1
    fi
    
    # 检查Docker
    if command -v docker &> /dev/null; then
        log_success "Docker已安装"
        DOCKER_AVAILABLE=true
    else
        log_warning "Docker未安装，将使用传统部署方式"
        DOCKER_AVAILABLE=false
    fi
    
    # 检查Docker Compose
    if command -v docker-compose &> /dev/null; then
        log_success "Docker Compose已安装"
        COMPOSE_AVAILABLE=true
    else
        log_warning "Docker Compose未安装"
        COMPOSE_AVAILABLE=false
    fi
}

# 安装系统依赖
install_dependencies() {
    log_info "安装系统依赖..."
    
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y curl wget git build-essential python3-dev
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum update -y
        sudo yum install -y curl wget git gcc python3-devel
    else
        log_error "不支持的包管理器"
        exit 1
    fi
    
    log_success "系统依赖安装完成"
}

# 安装Python依赖
install_python_deps() {
    log_info "安装Python依赖..."
    
    if [[ -f "requirements.txt" ]]; then
        pip3 install --user -r requirements.txt
        log_success "Python依赖安装完成"
    else
        log_error "requirements.txt文件不存在"
        exit 1
    fi
}

# 构建前端
build_frontend() {
    log_info "构建前端..."
    
    if [[ -d "frontend" ]]; then
        cd frontend
        
        # 检查Node.js
        if ! command -v node &> /dev/null; then
            log_info "安装Node.js..."
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        fi
        
        # 安装依赖并构建
        npm install
        npm run build
        
        cd ..
        log_success "前端构建完成"
    else
        log_error "frontend目录不存在"
        exit 1
    fi
}

# 使用Docker部署
deploy_with_docker() {
    log_info "使用Docker部署..."
    
    if [[ "$DOCKER_AVAILABLE" == true && "$COMPOSE_AVAILABLE" == true ]]; then
        # 构建并启动服务
        docker-compose up -d --build
        
        log_success "Docker部署完成"
        log_info "应用地址: http://localhost"
        log_info "查看日志: docker-compose logs -f"
        log_info "停止服务: docker-compose down"
    else
        log_error "Docker或Docker Compose不可用"
        exit 1
    fi
}

# 传统部署方式
deploy_traditional() {
    log_info "使用传统方式部署..."
    
    # 创建必要的目录
    mkdir -p logs data
    
    # 启动应用
    log_info "启动应用..."
    nohup python3 server.prod.py > logs/app.log 2>&1 &
    
    # 获取进程ID
    APP_PID=$!
    echo $APP_PID > app.pid
    
    log_success "应用已启动 (PID: $APP_PID)"
    log_info "应用地址: http://localhost:8000"
    log_info "查看日志: tail -f logs/app.log"
    log_info "停止应用: kill $APP_PID"
}

# 配置防火墙
configure_firewall() {
    log_info "配置防火墙..."
    
    if command -v ufw &> /dev/null; then
        # Ubuntu UFW
        sudo ufw allow 8000/tcp
        sudo ufw allow 80/tcp
        sudo ufw allow 443/tcp
        log_success "UFW防火墙配置完成"
    elif command -v firewall-cmd &> /dev/null; then
        # CentOS firewalld
        sudo firewall-cmd --permanent --add-port=8000/tcp
        sudo firewall-cmd --permanent --add-port=80/tcp
        sudo firewall-cmd --permanent --add-port=443/tcp
        sudo firewall-cmd --reload
        log_success "firewalld防火墙配置完成"
    else
        log_warning "未检测到防火墙，请手动配置端口8000、80、443"
    fi
}

# 创建systemd服务
create_systemd_service() {
    log_info "创建systemd服务..."
    
    if [[ "$DOCKER_AVAILABLE" == true ]]; then
        # Docker Compose服务
        sudo tee /etc/systemd/system/wellbeing-agent.service > /dev/null <<EOF
[Unit]
Description=Wellbeing Agent Docker Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$(pwd)
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF
    else
        # Python服务
        sudo tee /etc/systemd/system/wellbeing-agent.service > /dev/null <<EOF
[Unit]
Description=Wellbeing Agent Python Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 server.prod.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    fi
    
    sudo systemctl daemon-reload
    sudo systemctl enable wellbeing-agent.service
    
    log_success "systemd服务创建完成"
    log_info "启动服务: sudo systemctl start wellbeing-agent"
    log_info "查看状态: sudo systemctl status wellbeing-agent"
}

# 主函数
main() {
    log_info "开始部署维尔必应应用..."
    
    # 检查系统
    check_root
    check_system
    
    # 安装依赖
    install_dependencies
    install_python_deps
    
    # 构建前端
    build_frontend
    
    # 配置防火墙
    configure_firewall
    
    # 选择部署方式
    if [[ "$DOCKER_AVAILABLE" == true && "$COMPOSE_AVAILABLE" == true ]]; then
        read -p "是否使用Docker部署？(Y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            deploy_traditional
        else
            deploy_with_docker
        fi
    else
        deploy_traditional
    fi
    
    # 创建systemd服务
    read -p "是否创建systemd服务？(Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        create_systemd_service
    fi
    
    log_success "部署完成！"
    log_info "请访问: http://localhost:8000"
}

# 运行主函数
main "$@"
