#!/usr/bin/env python3
"""
生产环境启动脚本
用于在阿里云服务器上启动维尔必应应用
"""

import os
import sys
import subprocess
import time
import signal
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('production.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import langgraph
        logger.info("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        logger.error(f"❌ 缺少依赖: {e}")
        logger.info("请运行: pip install -r requirements.txt")
        return False

def build_frontend():
    """构建前端"""
    try:
        logger.info("🔨 构建前端...")
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            logger.error("❌ frontend 目录不存在")
            return False
            
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("✅ 前端构建成功")
            return True
        else:
            logger.error(f"❌ 前端构建失败: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ 前端构建异常: {e}")
        return False

def start_server():
    """启动后端服务器"""
    try:
        logger.info("🚀 启动后端服务器...")
        
        # 设置环境变量
        env = os.environ.copy()
        env["HOST"] = "0.0.0.0"
        env["PORT"] = "8000"
        
        # 启动服务器
        process = subprocess.Popen(
            [sys.executable, "production_server.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        logger.info(f"✅ 后端服务器已启动 (PID: {process.pid})")
        logger.info("🌐 服务地址: http://0.0.0.0:8000")
        
        return process
        
    except Exception as e:
        logger.error(f"❌ 启动服务器失败: {e}")
        return None

def main():
    """主函数"""
    logger.info("🚀 启动维尔必应生产环境...")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 构建前端
    if not build_frontend():
        sys.exit(1)
    
    # 启动服务器
    server_process = start_server()
    if not server_process:
        sys.exit(1)
    
    try:
        # 等待服务器启动
        time.sleep(3)
        
        # 检查服务器状态
        if server_process.poll() is None:
            logger.info("✅ 应用启动成功！")
            logger.info("📱 前端: http://localhost:8000")
            logger.info("🔌 API: http://localhost:8000/api")
            logger.info("💚 健康检查: http://localhost:8000/api/health")
            
            # 保持运行
            server_process.wait()
        else:
            logger.error("❌ 服务器启动失败")
            stdout, stderr = server_process.communicate()
            logger.error(f"STDOUT: {stdout}")
            logger.error(f"STDERR: {stderr}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 收到停止信号，正在关闭服务器...")
        server_process.terminate()
        server_process.wait()
        logger.info("✅ 服务器已关闭")
    except Exception as e:
        logger.error(f"❌ 运行时错误: {e}")
        server_process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()
