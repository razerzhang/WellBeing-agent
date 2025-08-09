export interface Message {
  id: string
  type: 'user' | 'agent'
  content: string
  timestamp: Date
  isStreaming: boolean
}

export interface QuickAction {
  id: string
  title: string
  message: string
  icon: string
  color: string
  description: string
}

export interface HealthMetric {
  date: string
  steps: number
  calories: number
  sleep: number
  water: number
  mood: 'excellent' | 'good' | 'neutral' | 'poor' | 'terrible'
}

export interface UserProfile {
  name: string
  age: number
  weight: number
  height: number
  activityLevel: 'sedentary' | 'lightly_active' | 'moderately_active' | 'very_active' | 'extremely_active'
  goals: string[]
  healthConditions: string[]
}
