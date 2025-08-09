#!/usr/bin/env python3
"""
启动脚本 - 启动Wellbeing Agent后端服务器
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """检查必要的依赖是否已安装"""
    try:
        import fastapi
        import uvicorn
        print("✅ 依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def start_server():
    """启动服务器"""
    print("🚀 正在启动Wellbeing Agent服务器...")
    
    # 检查环境变量
    port = os.getenv("PORT", "8000")
    
    try:
        # 启动服务器
        process = subprocess.Popen([
            sys.executable, "server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"⏳ 服务器启动中，端口: {port}")
        print("请等待几秒钟...")
        
        # 等待服务器启动
        time.sleep(3)
        
        # 检查服务器是否启动成功
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                print("✅ 服务器启动成功!")
                print(f"🌐 前端地址: http://localhost:{port}")
                print(f"📚 API文档: http://localhost:{port}/docs")
                print("\n💡 提示:")
                print("- 在浏览器中打开前端页面")
                print("- 按 Ctrl+C 停止服务器")
                print("- 服务器会自动重启（开发模式）")
                
                # 等待用户中断
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 正在停止服务器...")
                    process.terminate()
                    process.wait()
                    print("👋 服务器已停止")
                    
            else:
                print("⚠️ 服务器响应异常")
                process.terminate()
                
        except requests.exceptions.RequestException:
            print("❌ 无法连接到服务器")
            process.terminate()
            
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")

def main():
    """主函数"""
    print("🌱 Wellbeing Agent 服务器启动器")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        print("\n是否要自动安装依赖? (y/n): ", end="")
        if input().lower() == 'y':
            if not install_dependencies():
                return
        else:
            return
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()
