import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Trash2, Download, Bot, User, Clock, Zap, Menu } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import { Message } from '../types'

interface ChatInterfaceProps {
  messages: Message[]
  onSendMessage: (message: string) => void
  onClearChat: () => void
  isStreaming: boolean
  onToggleSidebar?: () => void
  isSidebarOpen?: boolean
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  onSendMessage,
  onClearChat,
  isStreaming,
  onToggleSidebar
}) => {
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [autoScroll, setAutoScroll] = useState(true)
  const [isStreamingActive, setIsStreamingActive] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    if (!autoScroll) return // 如果用户禁用了自动滚动，直接返回
    
    if (messagesEndRef.current) {
      // 检查是否已经在底部附近
      const container = messagesEndRef.current.parentElement
      if (container) {
        const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100
        if (isNearBottom) {
          // 如果接近底部，使用平滑滚动
          messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
        } else {
          // 如果用户已经向上滚动，不强制滚动到底部
          return
        }
      }
    }
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // 只在消息数组变化时滚动，不在内容更新时强制滚动
  useEffect(() => {
    const lastMessage = messages[messages.length - 1]
    if (lastMessage && lastMessage.isStreaming && messages.length > 1) {
      // 只在新增流式消息时滚动，不在内容更新时滚动
      scrollToBottom()
    }
  }, [messages.length])

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [inputValue])

  // 监听流式输出状态
  useEffect(() => {
    const hasStreamingMessage = messages.some(msg => msg.isStreaming)
    setIsStreamingActive(hasStreamingMessage)
  }, [messages])

  const handleSend = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue.trim())
      setInputValue('')
      setIsTyping(true)
      
      // 模拟打字指示器
      setTimeout(() => setIsTyping(false), 2000)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('zh-CN', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const exportChat = () => {
    const chatText = messages
      .map(msg => `${msg.type === 'user' ? '用户' : 'AI'}: ${msg.content}`)
      .join('\n\n')
    
    const blob = new Blob([chatText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `wellbeing-chat-${new Date().toISOString().split('T')[0]}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-gray-50 to-white">
      {/* Header */}
      <motion.header 
        className="bg-white border-b border-gray-200 px-4 lg:px-6 py-4 shadow-sm"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3 lg:space-x-4">
            {/* 移动端菜单按钮 */}
            {onToggleSidebar && (
              <motion.button
                onClick={onToggleSidebar}
                className="lg:hidden w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-xl flex items-center justify-center transition-colors"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Menu className="w-5 h-5 text-gray-600" />
              </motion.button>
            )}
            
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-wellness-500 rounded-xl flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg lg:text-xl font-semibold text-gray-800">Wellbeing AI</h2>
              <p className="text-xs lg:text-sm text-gray-600">你的健康搭子</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 lg:space-x-3">
            <motion.button
              onClick={onClearChat}
              className="flex items-center space-x-1 lg:space-x-2 px-2 lg:px-4 py-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Trash2 className="w-4 h-4" />
              <span className="text-xs lg:text-sm hidden sm:inline">清空对话</span>
            </motion.button>
            
            <motion.button
              onClick={exportChat}
              className="flex items-center space-x-1 lg:space-x-2 px-2 lg:px-4 py-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Download className="w-4 h-4" />
              <span className="text-xs lg:text-sm hidden sm:inline">导出对话</span>
            </motion.button>
          </div>
        </div>
      </motion.header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 lg:px-6 py-4 space-y-4 lg:space-y-6">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex max-w-full lg:max-w-3xl ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                {/* Avatar */}
                <div className={`w-8 h-8 lg:w-10 lg:h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                  message.type === 'user' 
                    ? 'bg-gradient-to-br from-primary-500 to-primary-600 ml-2 lg:ml-3' 
                    : 'bg-gradient-to-br from-wellness-500 to-wellness-600 mr-2 lg:mr-3'
                }`}>
                  {message.type === 'user' ? (
                    <User className="w-4 h-4 lg:w-5 lg:h-5 text-white" />
                  ) : (
                    <Bot className="w-4 h-4 lg:w-5 lg:h-5 text-white" />
                  )}
                </div>

                {/* Message Content */}
                <motion.div
                  className={`relative ${message.type === 'user' ? 'text-right' : 'text-left'}`}
                  initial={{ scale: 0.95 }}
                  animate={{ scale: 1 }}
                >
                  <div className={`inline-block px-4 lg:px-6 py-3 lg:py-4 rounded-2xl shadow-sm ${
                    message.type === 'user'
                      ? 'bg-primary-500 text-white'
                      : 'bg-white border border-gray-200 text-gray-800'
                  }`}>
                    {message.type === 'agent' ? (
                      <div className="prose prose-sm max-w-none">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeHighlight]}
                          className="markdown-content"
                        >
                          {message.content}
                        </ReactMarkdown>
                        
                        {/* Streaming indicator */}
                        {message.isStreaming && (
                          <motion.div 
                            className="flex items-center space-x-2 mt-3 text-sm text-gray-500"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                          >
                            <Zap className="w-4 h-4 text-energy-500 animate-pulse" />
                            <span>AI 正在思考...</span>
                          </motion.div>
                        )}
                      </div>
                    ) : (
                      <p className="text-sm font-medium">{message.content}</p>
                    )}
                  </div>
                  
                  {/* Timestamp */}
                  <div className={`flex items-center space-x-1 mt-2 text-xs text-gray-500 ${
                    message.type === 'user' ? 'justify-end' : 'justify-start'
                  }`}>
                    <Clock className="w-3 h-3" />
                    <span>{formatTime(message.timestamp)}</span>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Typing Indicator */}
        {isTyping && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
          >
            <div className="flex max-w-3xl">
              <div className="w-10 h-10 bg-gradient-to-br from-wellness-500 to-wellness-600 rounded-full flex items-center justify-center mr-3">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-white border border-gray-200 rounded-2xl px-6 py-4 shadow-sm">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <motion.div
                      className="w-2 h-2 bg-gray-400 rounded-full"
                      animate={{ opacity: [0.3, 1, 0.3] }}
                      transition={{ duration: 1.4, repeat: Infinity, repeatType: "reverse" }}
                    />
                    <motion.div
                      className="w-2 h-2 bg-gray-400 rounded-full"
                      animate={{ opacity: [0.3, 1, 0.3] }}
                      transition={{ duration: 1.4, repeat: Infinity, repeatType: "reverse", delay: 0.2 }}
                    />
                    <motion.div
                      className="w-2 h-2 bg-gray-400 rounded-full"
                      animate={{ opacity: [0.3, 1, 0.3] }}
                      transition={{ duration: 1.4, repeat: Infinity, repeatType: "reverse", delay: 0.4 }}
                    />
                  </div>
                  <span className="text-sm text-gray-500">AI 正在输入...</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 bg-white px-4 lg:px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-end space-x-2 lg:space-x-3">
            <div className="flex-1 relative">
              <textarea
                ref={textareaRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={isStreamingActive ? "AI正在回复中..." : "输入您的健康问题..."}
                className={`w-full px-3 lg:px-4 py-2 lg:py-3 border border-gray-300 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-sm lg:text-base ${
                  isStreamingActive ? 'bg-gray-100 cursor-not-allowed' : ''
                }`}
                rows={1}
                maxLength={1000}
                disabled={isStreamingActive}
              />
              <div className="absolute bottom-2 right-3 text-xs text-gray-400">
                {inputValue.length}/1000
              </div>
            </div>
            
            <motion.button
              onClick={handleSend}
              disabled={!inputValue.trim() || isStreamingActive}
              className={`w-10 h-10 lg:w-12 lg:h-12 rounded-xl flex items-center justify-center transition-all duration-200 ${
                inputValue.trim() && !isStreamingActive
                  ? 'bg-primary-500 hover:bg-primary-600 text-white shadow-lg hover:shadow-xl'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
              whileHover={inputValue.trim() && !isStreamingActive ? { scale: 1.05 } : {}}
              whileTap={inputValue.trim() && !isStreamingActive ? { scale: 0.95 } : {}}
            >
              <Send className="w-4 h-4 lg:w-5 lg:h-5" />
            </motion.button>
          </div>
          
          {/* Streaming Status and Auto-scroll Control */}
          <div className="flex items-center justify-between mt-3">
            <div className="flex items-center space-x-2 text-xs lg:text-sm text-gray-500">
              <Zap className={`w-3 h-3 lg:w-4 lg:h-4 ${isStreaming ? 'text-energy-500' : 'text-gray-400'}`} />
              <span className="hidden sm:inline">{isStreaming ? '流式输出已启用' : '流式输出已禁用'}</span>
              <span className="sm:hidden">{isStreaming ? '流式' : '普通'}</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setAutoScroll(!autoScroll)}
                className={`flex items-center space-x-1 lg:space-x-2 px-2 lg:px-3 py-1 rounded-lg text-xs transition-colors ${
                  autoScroll 
                    ? 'bg-primary-100 text-primary-700 hover:bg-primary-200' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <div className={`w-2 h-2 rounded-full ${autoScroll ? 'bg-primary-500' : 'bg-gray-400'}`} />
                <span className="hidden sm:inline">{autoScroll ? '自动滚动' : '手动滚动'}</span>
                <span className="sm:hidden">{autoScroll ? '自动' : '手动'}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
