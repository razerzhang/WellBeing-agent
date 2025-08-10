import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Sidebar from './components/Sidebar'
import ChatInterface from './components/ChatInterface'
import { Message, QuickAction } from './types'

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      type: 'agent',
      content: `👋 欢迎使用 维尔必应！

我是您的维尔必应搭子，可以为您提供：

🥗 **个性化饮食建议** - 营养搭配、饮食习惯优化
🏃 **科学运动指导** - 运动计划、强度控制  
🌿 **健康生活方式** - 睡眠改善、压力管理
💪 **特定健康咨询** - 针对性健康问题解答

请告诉我您的健康需求，或点击左侧的快速咨询按钮开始！`,
      timestamp: new Date(),
      isStreaming: false
    }
  ])
  
  const [isStreaming, setIsStreaming] = useState(true)
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [apiStatus, setApiStatus] = useState<'online' | 'offline'>('online')
  const [isSidebarOpen, setIsSidebarOpen] = useState(false) // 移动端侧边栏控制

  // 检查API状态
  const checkApiStatus = async () => {
    try {
      const response = await fetch('/api/health')
      if (response.ok) {
        setApiStatus('online')
      } else {
        setApiStatus('offline')
      }
    } catch (error) {
      setApiStatus('offline')
    }
  }

  // 在组件挂载时检查API状态
  React.useEffect(() => {
    checkApiStatus()
    // 每30秒检查一次API状态
    const interval = setInterval(checkApiStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content,
      timestamp: new Date(),
      isStreaming: false
    }
    
    setMessages(prev => [...prev, userMessage])
    
    // 创建AI响应消息
    const agentMessage: Message = {
      id: (Date.now() + 1).toString(),
      type: 'agent',
      content: '',
      timestamp: new Date(),
      isStreaming: true
    }
    
    setMessages(prev => [...prev, agentMessage])
    
    try {
      if (isStreaming) {
        // 使用流式API
        await callStreamingAPI(content, agentMessage.id)
      } else {
        // 使用普通API
        await callRegularAPI(content, agentMessage.id)
      }
    } catch (error) {
      console.error('API调用失败:', error)
      // 更新消息显示错误
      setMessages(prev => prev.map(msg => 
        msg.id === agentMessage.id 
          ? { ...msg, content: '抱歉，服务暂时不可用，请稍后重试。', isStreaming: false }
          : msg
      ))
    }
  }

  // 调用普通聊天API
  const callRegularAPI = async (userMessage: string, messageId: string) => {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      setMessages(prev => prev.map(msg => 
        msg.id === messageId 
          ? { ...msg, content: data.response, isStreaming: false }
          : msg
      ))
    } catch (error) {
      throw error
    }
  }

  // 调用流式聊天API
  const callStreamingAPI = async (userMessage: string, messageId: string) => {
    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      if (!reader) {
        throw new Error('无法获取响应流')
      }

      let fullContent = ''
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              console.log('Received streaming data:', data) // 调试日志
              
              if (data.type === 'start') {
                // 开始生成
                setMessages(prev => prev.map(msg => 
                  msg.id === messageId 
                    ? { ...msg, content: '正在生成建议...', isStreaming: true }
                    : msg
                ))
              } else if (data.type === 'step') {
                // 步骤更新
                setMessages(prev => prev.map(msg => 
                  msg.id === messageId 
                    ? { ...msg, content: data.message, isStreaming: true }
                    : msg
                ))
              } else if (data.type === 'content') {
                // 内容更新 - 支持两种字段名
                const content = data.content || data.message || ''
                fullContent += content
                setMessages(prev => prev.map(msg => 
                  msg.id === messageId 
                    ? { ...msg, content: fullContent, isStreaming: true }
                    : msg
                ))
              } else if (data.type === 'follow_up') {
                // 后续问题
                const followUpText = data.message + '\n\n' + (data.questions || []).map((q: string, i: number) => `${i + 1}. ${q}`).join('\n')
                setMessages(prev => prev.map(msg => 
                  msg.id === messageId 
                    ? { ...msg, content: fullContent + '\n\n' + followUpText, isStreaming: false }
                    : msg
                ))
              } else if (data.type === 'summary') {
                // 总结完成
                setMessages(prev => prev.map(msg => 
                  msg.id === messageId 
                    ? { ...msg, content: fullContent + '\n\n' + data.message, isStreaming: false }
                    : msg
                ))
              } else if (data.type === 'end') {
                // 生成完成
                setMessages(prev => prev.map(msg => 
                  msg.id === messageId 
                    ? { ...msg, isStreaming: false }
                    : msg
                ))
              } else if (data.type === 'error') {
                // 错误处理
                setMessages(prev => prev.map(msg => 
                  msg.id === messageId 
                    ? { ...msg, content: `错误: ${data.message}`, isStreaming: false }
                    : msg
                ))
              }
            } catch (parseError) {
              console.warn('解析流数据失败:', parseError, '原始数据:', line)
            }
          }
        }
      }
    } catch (error) {
      console.error('流式API调用失败:', error)
      // 更新消息显示错误
      const errorMessage = error instanceof Error ? error.message : String(error)
      setMessages(prev => prev.map(msg => 
        msg.id === messageId 
          ? { ...msg, content: `请求失败: ${errorMessage}`, isStreaming: false }
          : msg
      ))
    }
  }

  const handleQuickAction = (action: QuickAction) => {
    handleSendMessage(action.message)
    // 移动端点击快速操作后关闭侧边栏
    setIsSidebarOpen(false)
  }

  const clearChat = () => {
    setMessages([messages[0]]) // 保留欢迎消息
  }

  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark' : ''}`}>
      <div className="flex h-screen bg-gray-50">

        {/* 侧边栏 - 桌面端显示，移动端抽屉式 */}
        <div className="hidden lg:block lg:flex-shrink-0">
          <Sidebar
            isStreaming={isStreaming}
            onStreamingChange={setIsStreaming}
            isDarkMode={isDarkMode}
            onDarkModeChange={setIsDarkMode}
            apiStatus={apiStatus}
            onQuickAction={handleQuickAction}
          />
        </div>
        
        {/* 移动端抽屉式侧边栏 */}
        <AnimatePresence>
          {isSidebarOpen && (
            <>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
                onClick={() => setIsSidebarOpen(false)}
              />
              <motion.div
                initial={{ x: -320 }}
                animate={{ x: 0 }}
                exit={{ x: -320 }}
                transition={{ type: "spring", damping: 25, stiffness: 200 }}
                className="fixed lg:hidden z-50 h-full"
              >
                <Sidebar
                  isStreaming={isStreaming}
                  onStreamingChange={setIsStreaming}
                  isDarkMode={isDarkMode}
                  onDarkModeChange={setIsDarkMode}
                  apiStatus={apiStatus}
                  onQuickAction={handleQuickAction}
                />
              </motion.div>
            </>
          )}
        </AnimatePresence>
        
        <main className="flex-1 flex flex-col">
          <ChatInterface
            messages={messages}
            onSendMessage={handleSendMessage}
            onClearChat={clearChat}
            isStreaming={isStreaming}
            onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
            isSidebarOpen={isSidebarOpen}
          />
        </main>
      </div>
    </div>
  )
}

export default App
