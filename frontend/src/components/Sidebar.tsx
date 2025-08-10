import React from 'react'
import { motion } from 'framer-motion'
import { 
  Heart, 
  Moon, 
  Settings, 
  Zap,
  Activity,
  Target,
  TrendingUp,
  Users
} from 'lucide-react'
import { QuickAction } from '../types'

interface SidebarProps {
  isStreaming: boolean
  onStreamingChange: (value: boolean) => void
  isDarkMode: boolean
  onDarkModeChange: (value: boolean) => void
  apiStatus: 'online' | 'offline'
  onQuickAction: (action: QuickAction) => void
}

const quickActions: QuickAction[] = [
  {
    id: 'diet',
    title: '饮食建议',
    message: '我想了解关于健康饮食的建议，包括营养搭配、饮食习惯等方面。',
    icon: '🥗',
    color: 'primary',
    description: '个性化营养搭配'
  },
  {
    id: 'exercise',
    title: '运动指导',
    message: '我需要运动指导，包括适合我的运动类型、运动强度、运动计划等。',
    icon: '🏃',
    color: 'fitness',
    description: '科学运动计划'
  },
  {
    id: 'wellness',
    title: '健康管理',
    message: '我想了解如何改善整体健康状况，包括生活方式、心理健康、预防保健等。',
    icon: '🌿',
    color: 'wellness',
    description: '全方位健康指导'
  },
  {
    id: 'sleep',
    title: '睡眠改善',
    message: '我想了解如何改善睡眠质量，包括睡眠环境、睡前习惯、放松技巧等。',
    icon: '🌙',
    color: 'energy',
    description: '优质睡眠方案'
  }
]

const Sidebar: React.FC<SidebarProps> = ({
  isStreaming,
  onStreamingChange,
  isDarkMode,
  onDarkModeChange,
  apiStatus,
  onQuickAction
}) => {
  const getColorClasses = (color: string) => {
    switch (color) {
      case 'primary':
        return 'bg-primary-500 hover:bg-primary-600 text-white shadow-lg hover:shadow-xl'
      case 'fitness':
        return 'bg-fitness-500 hover:bg-fitness-600 text-white shadow-lg hover:shadow-xl'
      case 'wellness':
        return 'bg-wellness-500 hover:bg-wellness-600 text-white shadow-lg hover:shadow-xl'
      case 'energy':
        return 'bg-energy-500 hover:bg-energy-600 text-white shadow-lg hover:shadow-xl'
      default:
        return 'bg-gray-500 hover:bg-gray-600 text-white'
    }
  }

  return (
    <motion.aside
      initial={{ x: 0 }}
      animate={{ x: 0 }}
      className="w-80 bg-white border-r border-gray-200 flex flex-col shadow-lg h-full"
    >
      {/* Header */}
      <div className="p-4 lg:p-6 border-b border-gray-100">
        <motion.div 
          className="flex items-center space-x-3 mb-2"
          whileHover={{ scale: 1.05 }}
        >
          <div className="w-10 h-10 lg:w-12 lg:h-12 bg-gradient-to-br from-primary-500 to-wellness-500 rounded-2xl flex items-center justify-center shadow-lg">
            <Heart className="w-5 h-5 lg:w-6 lg:h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl lg:text-2xl font-bold bg-gradient-to-r from-primary-600 to-wellness-600 bg-clip-text text-transparent font-['Poppins']">
              维尔必应
            </h1>
            <p className="text-xs lg:text-sm text-gray-600 font-medium font-['Inter']">Made by Runzhe Zhang</p>
          </div>
        </motion.div>
        
        <div className="flex items-center space-x-2 text-xs lg:text-sm text-gray-500">
          <Activity className="w-3 h-3 lg:w-4 lg:h-4" />
          <span className="hidden sm:inline">"Pain is inevitable, Suffering is optional" - Murakami Haruki</span>
          <span className="sm:hidden">健康生活，从现在开始</span>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex-1 p-4 lg:p-6 space-y-4 lg:space-y-6">
        <div>
          <h3 className="text-base lg:text-lg font-semibold text-gray-800 mb-3 lg:mb-4 flex items-center">
            <Target className="w-4 h-4 lg:w-5 lg:h-5 mr-2 text-primary-500" />
            快速咨询
          </h3>
          <div className="space-y-2 lg:space-y-3">
            {quickActions.map((action) => (
              <motion.button
                key={action.id}
                onClick={() => onQuickAction(action)}
                className={`w-full p-3 lg:p-4 rounded-xl text-left transition-all duration-200 ${getColorClasses(action.color)}`}
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
              >
                <div className="flex items-center space-x-2 lg:space-x-3">
                  <span className="text-xl lg:text-2xl">{action.icon}</span>
                  <div className="flex-1">
                    <h4 className="font-semibold text-sm lg:text-base">{action.title}</h4>
                    <p className="text-xs lg:text-sm opacity-90">{action.description}</p>
                  </div>
                </div>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Health Stats Preview */}
        <div className="bg-gradient-to-br from-primary-50 to-wellness-50 rounded-xl p-3 lg:p-4">
          <h4 className="font-semibold text-gray-800 mb-2 lg:mb-3 flex items-center text-sm lg:text-base">
            <TrendingUp className="w-3 h-3 lg:w-4 lg:h-4 mr-2 text-primary-500" />
            今日概览
          </h4>
          <div className="grid grid-cols-2 gap-2 lg:gap-3 text-xs lg:text-sm">
            <div className="bg-white rounded-lg p-2 lg:p-3 text-center">
              <div className="text-lg lg:text-2xl font-bold text-primary-600">8,432</div>
              <div className="text-gray-600">步数</div>
            </div>
            <div className="bg-white rounded-lg p-2 lg:p-3 text-center">
              <div className="text-lg lg:text-2xl font-bold text-wellness-600">7.5h</div>
              <div className="text-gray-600">睡眠</div>
            </div>
          </div>
        </div>
      </div>

      {/* Settings */}
      <div className="p-4 lg:p-6 border-t border-gray-100 space-y-3 lg:space-y-4">
        <h3 className="text-base lg:text-lg font-semibold text-gray-800 flex items-center">
          <Settings className="w-4 h-4 lg:w-5 lg:h-5 mr-2 text-gray-500" />
          设置
        </h3>
        
        <div className="space-y-2 lg:space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 lg:space-x-3">
              <Zap className="w-3 h-3 lg:w-4 lg:h-4 text-energy-500" />
              <span className="text-xs lg:text-sm text-gray-700">流式输出</span>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={isStreaming}
                onChange={(e) => onStreamingChange(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-9 h-5 lg:w-11 lg:h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 lg:after:h-5 lg:after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
            </label>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 lg:space-x-3">
              <Moon className="w-3 h-3 lg:w-4 lg:h-4 text-gray-500" />
              <span className="text-xs lg:text-sm text-gray-700">深色模式</span>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={isDarkMode}
                onChange={(e) => onDarkModeChange(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-9 h-5 lg:w-11 lg:h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 lg:after:h-5 lg:after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
            </label>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 lg:p-6 border-t border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 lg:w-3 lg:h-3 rounded-full ${apiStatus === 'online' ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-xs lg:text-sm text-gray-600">
              {apiStatus === 'online' ? '在线' : '离线'}
            </span>
          </div>
          <div className="flex items-center space-x-1 text-gray-400">
            <Users className="w-3 h-3 lg:w-4 lg:h-4" />
            <span className="text-xs">健康社区</span>
          </div>
        </div>
      </div>
    </motion.aside>
  )
}

export default Sidebar
