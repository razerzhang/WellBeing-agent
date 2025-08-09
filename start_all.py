#!/usr/bin/env python3
"""
启动脚本 - 同时启动前后端服务
"""

import os
import sys
import subprocess
import time
import requests
import threading
import signal
from pathlib import Path

class ServiceManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """处理退出信号"""
        print("\n🛑 正在停止所有服务...")
        self.stop_all()
        sys.exit(0)
    
    def start_backend(self):
        """启动后端服务"""
        print("🚀 启动后端FastAPI服务器...")
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, "server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 等待后端启动
            for i in range(10):
                try:
                    response = requests.get("http://localhost:8000/health", timeout=2)
                    if response.status_code == 200:
                        print("✅ 后端服务器启动成功 (端口: 8000)")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"⏳ 等待后端启动... ({i+1}/10)")
            
            print("❌ 后端启动超时")
            return False
            
        except Exception as e:
            print(f"❌ 后端启动失败: {e}")
            return False
    
    def start_frontend(self):
        """启动前端服务"""
        print("🌐 启动前端Vite开发服务器...")
        try:
            # 检查是否在Windows系统上
            if os.name == 'nt':
                npm_cmd = "npm.cmd"
            else:
                npm_cmd = "npm"
            
            self.frontend_process = subprocess.Popen([
                npm_cmd, "run", "dev"
            ], cwd="frontend", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 等待前端启动
            for i in range(15):  # 增加等待时间，因为Vite需要更多时间启动
                try:
                    response = requests.get("http://localhost:3000", timeout=2)
                    if response.status_code == 200:
                        print("✅ 前端Vite服务器启动成功 (端口: 3000)")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"⏳ 等待前端Vite启动... ({i+1}/15)")
            
            print("❌ 前端启动超时")
            return False
            
        except Exception as e:
            print(f"❌ 前端启动失败: {e}")
            return False
    
    def check_services(self):
        """检查服务状态"""
        while self.running:
            try:
                # 检查后端
                backend_ok = False
                try:
                    response = requests.get("http://localhost:8000/health", timeout=2)
                    backend_ok = response.status_code == 200
                except:
                    pass
                
                # 检查前端
                frontend_ok = False
                try:
                    response = requests.get("http://localhost:3000", timeout=2)
                    frontend_ok = response.status_code == 200
                except:
                    pass
                
                # 显示状态
                backend_status = "🟢 运行中" if backend_ok else "🔴 已停止"
                frontend_status = "🟢 运行中" if frontend_ok else "🔴 已停止"
                
                print(f"\r📊 服务状态 - 后端: {backend_status} | 前端: {frontend_status}", end="", flush=True)
                
                time.sleep(5)
                
            except KeyboardInterrupt:
                break
    
    def stop_all(self):
        """停止所有服务"""
        self.running = False
        
        if self.backend_process:
            print("🛑 停止后端服务...")
            self.backend_process.terminate()
            self.backend_process.wait()
        
        if self.frontend_process:
            print("🛑 停止前端服务...")
            self.frontend_process.terminate()
            self.frontend_process.wait()
        
        print("✅ 所有服务已停止")
    
    def run(self):
        """运行服务管理器"""
        print("🌱 Wellbeing Agent 服务管理器")
        print("=" * 50)
        
        # 启动后端
        if not self.start_backend():
            return False
        
        # 启动前端
        if not self.start_frontend():
            return False
        
        print("\n🎉 所有服务启动成功!")
        print("=" * 50)
        print("🌐 前端地址: http://localhost:3000")
        print("🔗 后端API: http://localhost:8000")
        print("📚 API文档: http://localhost:8000/docs")
        print("\n💡 提示:")
        print("- 在浏览器中打开前端页面")
        print("- 按 Ctrl+C 停止所有服务")
        print("- 服务状态会实时显示")
        print("\n" + "=" * 50)
        
        # 启动状态监控
        try:
            self.check_services()
        except KeyboardInterrupt:
            pass
        
        return True

def main():
    """主函数"""
    manager = ServiceManager()
    success = manager.run()
    
    if not success:
        print("❌ 服务启动失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
