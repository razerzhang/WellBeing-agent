// Wellbeing Agent Frontend JavaScript
class WellbeingAgent {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendMessage');
        this.clearButton = document.getElementById('clearChat');
        this.loadingModal = document.getElementById('loadingModal');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.charCount = document.querySelector('.char-count');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.statusText = document.getElementById('statusText');
        
        this.messageHistory = [];
        this.isTyping = false;
        this.apiBaseUrl = 'http://localhost:8000';
        this.apiOnline = false;
        this.streamingEnabled = true; // Default to true
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.setupQuickActions();
        this.loadMessageHistory();
        this.updateCharCount();
        this.checkAPIStatus();
    }
    
    bindEvents() {
        // Send message on Enter key
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Send button click
        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Clear chat button
        const clearButton = document.getElementById('clearChat');
        if (clearButton) {
            clearButton.addEventListener('click', () => {
                this.clearChat();
            });
        }
        
        // Streaming toggle
        const streamingToggle = document.getElementById('streamingToggle');
        if (streamingToggle) {
            streamingToggle.addEventListener('change', (e) => {
                this.streamingEnabled = e.target.checked;
                console.log('Streaming enabled:', this.streamingEnabled);
            });
        }
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.autoResize();
            this.updateCharCount();
        });
        
        // Load message history on page load
        window.addEventListener('load', () => {
            this.loadMessageHistory();
        });
    }
    
    setupQuickActions() {
        const actionButtons = document.querySelectorAll('.action-btn');
        actionButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const intent = btn.dataset.intent;
                this.handleQuickAction(intent);
            });
        });
    }
    
    handleQuickAction(intent) {
        let message = '';
        let icon = '';
        
        switch(intent) {
            case 'diet':
                message = '我想了解关于健康饮食的建议，包括营养搭配、饮食习惯等方面。';
                icon = '🥗';
                break;
            case 'exercise':
                message = '我需要运动指导，包括适合我的运动类型、运动强度、运动计划等。';
                icon = '🏃';
                break;
            case 'wellness':
                message = '我想了解如何改善整体健康状况，包括生活方式、心理健康、预防保健等。';
                icon = '🌿';
                break;
            case 'custom':
                message = '我有一些特定的健康问题想要咨询，请帮我分析。';
                icon = '💬';
                break;
        }
        
        if (message) {
            this.addMessage(message, 'user');
            this.messageInput.value = message;
            this.updateCharCount();
            this.processUserMessage(message);
        }
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;
        
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.updateCharCount();
        this.processUserMessage(message);
    }
    
    async processUserMessage(message) {
        this.showTypingIndicator();
        
        try {
            // Check if streaming is available and enabled
            if (this.apiOnline && this.streamingEnabled) {
                await this.callBackendAPIStream(message);
            } else if (this.apiOnline) {
                // Use non-streaming API
                const response = await this.callBackendAPI(message);
                this.hideTypingIndicator();
                this.addMessage(response, 'agent');
            } else {
                // Fallback to mock responses
                const response = this.generateFallbackResponse(message);
                this.hideTypingIndicator();
                this.addMessage(response, 'agent');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('抱歉，处理你的请求时出现了问题。请稍后再试。', 'agent');
            console.error('Error processing message:', error);
        }
    }
    
    async callBackendAPIStream(message) {
        try {
            // Create a new message container for streaming
            const messageId = 'msg_' + Date.now();
            this.addMessage('', 'agent', messageId);
            
            // Start streaming request
            const response = await fetch(`${this.apiBaseUrl}/api/chat/stream`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Get the message element to update
            const messageElement = document.getElementById(messageId);
            if (!messageElement) return;
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            
            while (true) {
                const { done, value } = await reader.read();
                
                if (done) break;
                
                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            await this.handleStreamData(data, messageElement);
                        } catch (e) {
                            console.error('Error parsing stream data:', e);
                        }
                    }
                }
            }
            
            this.hideTypingIndicator();
            
        } catch (error) {
            console.error('Error in streaming API call:', error);
            this.hideTypingIndicator();
            
            // Fallback to mock responses if streaming fails
            const response = this.generateFallbackResponse(message);
            this.addMessage(response, 'agent');
        }
    }
    
    async callBackendAPI(message) {
        try {
            // Show loading indicator
            this.showTypingIndicator();
            
            // Call the regular backend API
            const response = await fetch(`${this.apiBaseUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Hide loading indicator
            this.hideTypingIndicator();
            
            return data.response;
            
        } catch (error) {
            console.error('Error calling backend API:', error);
            this.hideTypingIndicator();
            
            // Fallback to mock responses if API fails
            return this.generateFallbackResponse(message);
        }
    }
    
    async handleStreamData(data, messageElement) {
        const messageText = messageElement.querySelector('.message-text');
        if (!messageText) return;
        
        switch (data.type) {
            case 'start':
                messageText.innerHTML = data.message;
                break;
                
            case 'step':
                messageText.innerHTML += '<br><br>' + data.message;
                break;
                
            case 'content':
                messageText.innerHTML += data.content;
                this.scrollToBottom();
                break;
                
            case 'follow_up':
                messageText.innerHTML += '<br><br>' + data.message;
                if (data.questions && Array.isArray(data.questions)) {
                    data.questions.forEach((question, index) => {
                        messageText.innerHTML += `<br>${index + 1}. ${question}`;
                    });
                }
                break;
                
            case 'summary':
                messageText.innerHTML += '<br><br>' + data.message;
                break;
                
            case 'error':
                messageText.innerHTML = '❌ ' + data.message;
                break;
        }
        
        this.scrollToBottom();
    }
    
    async checkAPIStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            if (response.ok) {
                this.setAPIStatus(true);
            } else {
                this.setAPIStatus(false);
            }
        } catch (error) {
            console.log('API is offline, using fallback responses');
            this.setAPIStatus(false);
        }
    }
    
    setAPIStatus(online) {
        this.apiOnline = online;
        if (online) {
            this.statusIndicator.className = 'status-indicator online';
            this.statusText.textContent = '在线';
            this.statusText.style.color = '#27ae60';
        } else {
            this.statusIndicator.className = 'status-indicator offline';
            this.statusText.textContent = '离线';
            this.statusText.style.color = '#e74c3c';
        }
    }
    
    generateFallbackResponse(message) {
        // Fallback responses when API is not available
        const lowerMessage = message.toLowerCase();
        
        if (lowerMessage.includes('饮食') || lowerMessage.includes('营养') || lowerMessage.includes('食物')) {
            return this.generateDietResponse(message);
        } else if (lowerMessage.includes('运动') || lowerMessage.includes('锻炼') || lowerMessage.includes('健身')) {
            return this.generateExerciseResponse(message);
        } else if (lowerMessage.includes('健康') || lowerMessage.includes('生活方式') || lowerMessage.includes('保健')) {
            return this.generateWellnessResponse(message);
        } else if (lowerMessage.includes('睡眠') || lowerMessage.includes('休息')) {
            return this.generateSleepResponse(message);
        } else if (lowerMessage.includes('压力') || lowerMessage.includes('心理') || lowerMessage.includes('情绪')) {
            return this.generateMentalHealthResponse(message);
        } else {
            return this.generateGeneralResponse(message);
        }
    }
    
    generateDietResponse(message) {
        const responses = [
            `根据你的需求，我建议你关注以下几个方面：

🥗 **均衡营养搭配**
- 蛋白质：瘦肉、鱼类、豆类、蛋类
- 碳水化合物：全谷物、蔬菜、水果
- 健康脂肪：坚果、橄榄油、牛油果
- 维生素和矿物质：深色蔬菜、水果

🍽️ **饮食习惯建议**
- 定时定量，避免暴饮暴食
- 细嚼慢咽，享受食物
- 多喝水，少喝含糖饮料
- 减少加工食品摄入

💡 **个性化建议**
如果你能告诉我你的具体目标（减重、增肌、改善特定健康问题等），我可以提供更精准的建议。`,

            `关于健康饮食，这里有几点重要建议：

🌱 **植物性食物为主**
- 每天至少5份蔬菜水果
- 选择全谷物而非精制谷物
- 适量摄入坚果和种子

🥩 **优质蛋白质**
- 鱼类：每周2-3次
- 瘦肉：适量摄入
- 豆类：植物蛋白的好来源

🚫 **需要限制的食物**
- 高糖、高盐、高脂肪食品
- 过度加工的食品
- 含反式脂肪的食品

你有什么具体的饮食问题想要了解吗？`
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    generateExerciseResponse(message) {
        const responses = [
            `基于你的运动需求，我为你制定以下运动计划：

🏃 **有氧运动** (每周3-5次)
- 快走：30-45分钟
- 慢跑：20-30分钟
- 游泳：30分钟
- 骑自行车：45分钟

💪 **力量训练** (每周2-3次)
- 俯卧撑：3组×10-15次
- 深蹲：3组×15-20次
- 平板支撑：3组×30-60秒
- 哑铃训练：全身肌肉群

🧘 **柔韧性训练** (每周2-3次)
- 拉伸运动：15-20分钟
- 瑜伽：30-45分钟

⚠️ **注意事项**
- 循序渐进，不要操之过急
- 运动前充分热身
- 注意运动强度，以能正常说话为宜
- 如有不适立即停止

你想了解哪个具体运动项目的详细指导？`,

            `运动指导来啦！这里是一个科学的运动方案：

🎯 **运动频率**
- 每周至少150分钟中等强度有氧运动
- 每周2-3次力量训练
- 每天进行柔韧性练习

🔥 **运动强度分级**
- 轻度：能轻松说话唱歌
- 中度：能说话但无法唱歌
- 高强度：无法连续说话

📱 **运动追踪建议**
- 使用运动手环记录步数
- 记录运动时间和强度
- 设定每周运动目标

🏥 **安全提醒**
运动前请咨询医生，特别是如果你有慢性疾病或长期不运动。

你希望我详细解释哪种运动方式？`
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    generateWellnessResponse(message) {
        const responses = [
            `整体健康管理是一个综合性的概念，我为你提供以下建议：

🌅 **日常作息管理**
- 保持规律的睡眠时间（7-9小时）
- 建立健康的生物钟
- 避免熬夜和过度疲劳

🥗 **营养均衡**
- 多样化饮食，不挑食
- 适量饮水（每天1.5-2升）
- 减少烟酒摄入

🏃 **适度运动**
- 每天至少30分钟中等强度运动
- 结合有氧和力量训练
- 保持身体活力

🧘 **心理健康**
- 学会压力管理技巧
- 培养兴趣爱好
- 保持社交联系
- 定期放松和冥想

💊 **预防保健**
- 定期体检
- 接种必要疫苗
- 关注身体信号

你希望我重点介绍哪个方面？`,

            `健康生活方式的核心要素：

🌟 **身心平衡**
- 工作与休息的平衡
- 运动与放松的结合
- 社交与独处的协调

🌿 **环境健康**
- 保持居住环境清洁
- 减少接触有害物质
- 增加绿色植物

📱 **数字健康**
- 控制屏幕使用时间
- 保护眼睛健康
- 避免久坐不动

💧 **水分管理**
- 根据活动量调整饮水量
- 选择健康饮品
- 避免过度依赖咖啡因

🎯 **目标设定**
建议你设定具体的健康目标，比如：
- 每周运动3次
- 每天喝8杯水
- 每周至少1次户外活动

你想从哪个方面开始改善？`
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    generateSleepResponse(message) {
        return `关于睡眠质量，这里有专业的建议：

😴 **优质睡眠要素**
- 睡眠时长：7-9小时
- 睡眠环境：安静、黑暗、凉爽
- 睡眠时间：保持规律作息

🌙 **睡前准备**
- 避免咖啡因和酒精
- 减少屏幕使用时间
- 进行放松活动（阅读、冥想）
- 保持卧室舒适温度

🛏️ **睡眠卫生**
- 床只用于睡眠和亲密关系
- 避免在床上工作或看电视
- 如果20分钟内无法入睡，起床做其他事情

💤 **改善睡眠的方法**
- 建立睡前仪式
- 规律运动（但避免睡前剧烈运动）
- 管理压力和焦虑
- 考虑使用白噪音或助眠音乐

你目前遇到什么睡眠问题？我可以提供更具体的建议。`;
    }
    
    generateMentalHealthResponse(message) {
        return `心理健康同样重要，这里有几点建议：

🧠 **压力管理技巧**
- 深呼吸练习：每天5-10分钟
- 渐进性肌肉放松
- 正念冥想：专注当下
- 时间管理：合理安排任务

😊 **情绪调节方法**
- 识别和接受情绪
- 寻找情绪出口（运动、艺术、写作）
- 培养积极思维习惯
- 学会自我安慰

🤝 **社交支持**
- 与朋友家人保持联系
- 寻求专业心理咨询
- 参加兴趣小组或社区活动
- 学会寻求帮助

🎯 **日常心理健康习惯**
- 保持规律作息
- 培养兴趣爱好
- 定期自我反思
- 设定合理目标

如果你感到持续的情绪困扰，建议寻求专业帮助。你想了解哪个具体的心理健康话题？`;
    }
    
    generateGeneralResponse(message) {
        const responses = [
            `感谢你的咨询！作为你的健康顾问，我建议：

🔍 **健康评估**
首先了解你的具体情况：
- 年龄、性别、体重
- 当前健康状况
- 运动习惯和饮食偏好
- 健康目标和关注点

📋 **个性化建议**
基于你的情况，我可以提供：
- 饮食营养方案
- 运动锻炼计划
- 生活方式改善建议
- 健康风险预防

💡 **下一步行动**
请告诉我你的具体需求，或者：
- 描述你的健康问题
- 分享你的健康目标
- 询问特定的健康话题

我会为你提供专业、个性化的健康建议！`,

            `很高兴你关注健康！让我为你提供全面的健康指导：

🎯 **健康管理框架**
- 身体检查：定期体检，了解身体状况
- 风险评估：识别健康风险因素
- 预防措施：采取积极的健康行动
- 持续监测：跟踪健康改善情况

🌱 **健康生活方式**
- 均衡饮食：营养丰富的多样化食物
- 规律运动：适合个人情况的运动计划
- 充足休息：高质量的睡眠和放松
- 心理健康：压力管理和情绪调节

📚 **知识获取**
- 了解健康知识
- 识别可靠信息源
- 咨询专业医生
- 持续学习健康管理

请告诉我你的具体健康需求，我会为你量身定制建议！`
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    addMessage(text, sender, messageId = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        
        const icon = document.createElement('i');
        if (sender === 'agent') {
            icon.className = 'fas fa-heartbeat';
        } else {
            icon.className = 'fas fa-user';
        }
        avatar.appendChild(icon);
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.innerHTML = text;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        
        content.appendChild(messageText);
        content.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Save to history
        this.messageHistory.push({
            text,
            sender,
            timestamp: new Date().toISOString()
        });
        this.saveMessageHistory();

        if (messageId) {
            messageDiv.id = messageId;
        }
    }
    
    getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        this.typingIndicator.style.display = 'flex';
        this.sendButton.disabled = true;
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        this.typingIndicator.style.display = 'none';
        this.sendButton.disabled = false;
    }
    
    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = `${count}/500`;
        
        if (count > 450) {
            this.charCount.style.color = '#e74c3c';
        } else if (count > 400) {
            this.charCount.style.color = '#f39c12';
        } else {
            this.charCount.style.color = '#999';
        }
    }
    
    autoResize() {
        // If we change to textarea later, this will handle auto-resize
        // Currently using input, so this is a placeholder
    }
    
    clearChat() {
        if (confirm('确定要清空所有对话记录吗？')) {
            this.chatMessages.innerHTML = '';
            this.messageHistory = [];
            this.saveMessageHistory();
            
            // Add welcome message back
            this.addMessage(`你好！我是你的智能健康顾问 🌱 我可以为你提供：
<ul>
    <li>🥗 个性化饮食建议</li>
    <li>🏃 科学运动指导</li>
    <li>🌿 健康生活方式建议</li>
    <li>💪 特定健康问题咨询</li>
</ul>
请告诉我你的健康需求，或者点击上方的快速咨询按钮！`, 'agent');
        }
    }
    
    saveMessageHistory() {
        try {
            localStorage.setItem('wellbeingAgentHistory', JSON.stringify(this.messageHistory));
        } catch (error) {
            console.error('Failed to save message history:', error);
        }
    }
    
    loadMessageHistory() {
        try {
            const saved = localStorage.getItem('wellbeingAgentHistory');
            if (saved) {
                this.messageHistory = JSON.parse(saved);
                // Optionally restore messages from history
                // For now, we'll just keep the welcome message
            }
        } catch (error) {
            console.error('Failed to load message history:', error);
        }
    }
    
    showLoadingModal() {
        this.loadingModal.style.display = 'block';
    }
    
    hideLoadingModal() {
        this.loadingModal.style.display = 'none';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WellbeingAgent();
    
    // Add some interactive features
    addInteractiveFeatures();
});

function addInteractiveFeatures() {
    // Add hover effects to tip cards
    const tipCards = document.querySelectorAll('.tip-card');
    tipCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add click effects to action buttons
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(btn => {
        btn.addEventListener('mousedown', () => {
            btn.style.transform = 'scale(0.95)';
        });
        
        btn.addEventListener('mouseup', () => {
            btn.style.transform = 'scale(1)';
        });
        
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'scale(1)';
        });
    });
    
    // Add smooth scrolling for chat
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.style.scrollBehavior = 'smooth';
    
    // Add focus effect to input
    const messageInput = document.getElementById('messageInput');
    messageInput.addEventListener('focus', () => {
        messageInput.parentElement.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
    });
    
    messageInput.addEventListener('blur', () => {
        messageInput.parentElement.style.boxShadow = 'none';
    });
}

// Add some utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to send message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('sendMessage').click();
    }
    
    // Escape to clear input
    if (e.key === 'Escape') {
        document.getElementById('messageInput').value = '';
        document.querySelector('.char-count').textContent = '0/500';
    }
});

// Add some animations
function addAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.quick-actions, .health-tips');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Initialize animations when page loads
window.addEventListener('load', addAnimations);

// Health Tracking System
class HealthTracker {
    constructor() {
        this.healthData = this.loadHealthData();
        this.initTracking();
        this.updateWeeklySummary();
        this.initChart();
    }
    
    loadHealthData() {
        const defaultData = {
            water: 0,
            steps: 0,
            exercise: 0,
            diet: 0,
            lastReset: new Date().toDateString(),
            weeklyData: this.generateWeeklyData()
        };
        
        try {
            const saved = localStorage.getItem('wellbeingHealthData');
            if (saved) {
                const parsed = JSON.parse(saved);
                // Check if it's a new day, reset daily values
                if (parsed.lastReset !== new Date().toDateString()) {
                    parsed.water = 0;
                    parsed.steps = 0;
                    parsed.exercise = 0;
                    parsed.diet = 0;
                    parsed.lastReset = new Date().toDateString();
                }
                return parsed;
            }
        } catch (error) {
            console.error('Failed to load health data:', error);
        }
        
        return defaultData;
    }
    
    generateWeeklyData() {
        const week = [];
        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            week.push({
                date: date.toDateString(),
                water: Math.floor(Math.random() * 8),
                steps: Math.floor(Math.random() * 10000),
                exercise: Math.floor(Math.random() * 30),
                diet: Math.floor(Math.random() * 5)
            });
        }
        return week;
    }
    
    saveHealthData() {
        try {
            localStorage.setItem('wellbeingHealthData', JSON.stringify(this.healthData));
        } catch (error) {
            console.error('Failed to save health data:', error);
        }
    }
    
    initTracking() {
        this.updateDisplay();
        this.setupTrackingButtons();
    }
    
    setupTrackingButtons() {
        // Water tracking
        window.addWater = () => {
            if (this.healthData.water < 8) {
                this.healthData.water++;
                this.updateDisplay();
                this.saveHealthData();
                this.updateWeeklySummary();
                this.showAchievement('水分摄入', '继续保持！');
            }
        };
        
        window.resetWater = () => {
            this.healthData.water = 0;
            this.updateDisplay();
            this.saveHealthData();
            this.updateWeeklySummary();
        };
        
        // Steps tracking
        window.addSteps = (amount) => {
            this.healthData.steps += amount;
            this.updateDisplay();
            this.saveHealthData();
            this.updateWeeklySummary();
            if (this.healthData.steps >= 10000) {
                this.showAchievement('步数目标', '恭喜达到每日步数目标！');
            }
        };
        
        window.resetSteps = () => {
            this.healthData.steps = 0;
            this.updateDisplay();
            this.saveHealthData();
            this.updateWeeklySummary();
        };
        
        // Exercise tracking
        window.addExercise = (minutes) => {
            this.healthData.exercise += minutes;
            this.updateDisplay();
            this.saveHealthData();
            this.updateWeeklySummary();
            if (this.healthData.exercise >= 30) {
                this.showAchievement('运动目标', '太棒了！达到每日运动目标！');
            }
        };
        
        window.resetExercise = () => {
            this.healthData.exercise = 0;
            this.updateDisplay();
            this.saveHealthData();
            this.updateWeeklySummary();
        };
        
        // Diet tracking
        window.addDiet = () => {
            if (this.healthData.diet < 5) {
                this.healthData.diet++;
                this.updateDisplay();
                this.saveHealthData();
                this.updateWeeklySummary();
                if (this.healthData.diet >= 5) {
                    this.showAchievement('饮食目标', '健康饮食，身体棒棒！');
                }
            }
        };
        
        window.resetDiet = () => {
            this.healthData.diet = 0;
            this.updateDisplay();
            this.saveHealthData();
            this.updateWeeklySummary();
        };
    }
    
    updateDisplay() {
        // Update water progress
        const waterProgress = document.getElementById('waterProgress');
        const waterCurrent = document.getElementById('waterCurrent');
        if (waterProgress && waterCurrent) {
            const percentage = (this.healthData.water / 8) * 100;
            waterProgress.style.width = `${percentage}%`;
            waterCurrent.textContent = this.healthData.water;
        }
        
        // Update steps progress
        const stepsProgress = document.getElementById('stepsProgress');
        const stepsCurrent = document.getElementById('stepsCurrent');
        if (stepsProgress && stepsCurrent) {
            const percentage = Math.min((this.healthData.steps / 10000) * 100, 100);
            stepsProgress.style.width = `${percentage}%`;
            stepsCurrent.textContent = this.healthData.steps.toLocaleString();
        }
        
        // Update exercise progress
        const exerciseProgress = document.getElementById('exerciseProgress');
        const exerciseCurrent = document.getElementById('exerciseCurrent');
        if (exerciseProgress && exerciseCurrent) {
            const percentage = (this.healthData.exercise / 30) * 100;
            exerciseProgress.style.width = `${percentage}%`;
            exerciseCurrent.textContent = this.healthData.exercise;
        }
        
        // Update diet progress
        const dietProgress = document.getElementById('dietProgress');
        const dietCurrent = document.getElementById('dietCurrent');
        if (dietProgress && dietCurrent) {
            const percentage = (this.healthData.diet / 5) * 100;
            dietProgress.style.width = `${percentage}%`;
            dietCurrent.textContent = this.healthData.diet;
        }
    }
    
    updateWeeklySummary() {
        const totalGoals = 8 + 10000 + 30 + 5; // water + steps + exercise + diet
        const currentTotal = this.healthData.water + this.healthData.steps / 1000 + this.healthData.exercise + this.healthData.diet;
        const completion = Math.round((currentTotal / (totalGoals / 1000)) * 100);
        
        const weeklyCompletion = document.getElementById('weeklyCompletion');
        if (weeklyCompletion) {
            weeklyCompletion.textContent = `${Math.min(completion, 100)}%`;
        }
        
        // Calculate streak days
        const streakDays = document.getElementById('streakDays');
        if (streakDays) {
            const streak = this.calculateStreak();
            streakDays.textContent = `${streak} 天`;
        }
        
        // Update health trend
        const healthTrend = document.getElementById('healthTrend');
        if (healthTrend) {
            const trend = this.calculateHealthTrend();
            healthTrend.textContent = trend;
        }
        
        this.updateChart();
    }
    
    calculateStreak() {
        // Simple streak calculation based on daily completion
        let streak = 0;
        for (let i = this.healthData.weeklyData.length - 1; i >= 0; i--) {
            const day = this.healthData.weeklyData[i];
            const dayCompletion = day.water + day.steps / 1000 + day.exercise + day.diet;
            if (dayCompletion >= 20) { // Threshold for "good day"
                streak++;
            } else {
                break;
            }
        }
        return streak;
    }
    
    calculateHealthTrend() {
        const recent = this.healthData.weeklyData.slice(-3);
        const older = this.healthData.weeklyData.slice(-6, -3);
        
        const recentAvg = recent.reduce((sum, day) => 
            sum + day.water + day.steps / 1000 + day.exercise + day.diet, 0) / recent.length;
        const olderAvg = older.reduce((sum, day) => 
            sum + day.water + day.steps / 1000 + day.exercise + day.diet, 0) / older.length;
        
        if (recentAvg > olderAvg * 1.1) return '上升';
        if (recentAvg < olderAvg * 0.9) return '下降';
        return '稳定';
    }
    
    initChart() {
        const canvas = document.getElementById('weeklyChart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        this.chartCtx = ctx;
        this.updateChart();
    }
    
    updateChart() {
        if (!this.chartCtx) return;
        
        const canvas = document.getElementById('weeklyChart');
        const ctx = this.chartCtx;
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw chart
        this.drawWeeklyChart(ctx, canvas.width, canvas.height);
    }
    
    drawWeeklyChart(ctx, width, height) {
        const padding = 40;
        const chartWidth = width - 2 * padding;
        const chartHeight = height - 2 * padding;
        
        // Draw background
        ctx.fillStyle = '#f8f9fa';
        ctx.fillRect(padding, padding, chartWidth, chartHeight);
        
        // Draw grid lines
        ctx.strokeStyle = '#e9ecef';
        ctx.lineWidth = 1;
        
        // Vertical grid lines (days)
        for (let i = 0; i <= 7; i++) {
            const x = padding + (i / 7) * chartWidth;
            ctx.beginPath();
            ctx.moveTo(x, padding);
            ctx.lineTo(x, padding + chartHeight);
            ctx.stroke();
        }
        
        // Horizontal grid lines (values)
        for (let i = 0; i <= 4; i++) {
            const y = padding + (i / 4) * chartHeight;
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(padding + chartWidth, y);
            ctx.stroke();
        }
        
        // Draw data lines
        const colors = ['#667eea', '#ff9a9e', '#a8edea', '#ffecd2'];
        const metrics = ['water', 'steps', 'exercise', 'diet'];
        
        metrics.forEach((metric, index) => {
            const color = colors[index];
            ctx.strokeStyle = color;
            ctx.lineWidth = 3;
            ctx.fillStyle = color;
            
            const points = this.healthData.weeklyData.map((day, i) => {
                let value;
                switch(metric) {
                    case 'water': value = day.water; break;
                    case 'steps': value = day.steps / 1000; break;
                    case 'exercise': value = day.exercise; break;
                    case 'diet': value = day.diet; break;
                }
                
                const x = padding + (i / 6) * chartWidth;
                const y = padding + chartHeight - (value / 10) * chartHeight;
                return { x, y, value };
            });
            
            // Draw line
            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            points.forEach(point => {
                ctx.lineTo(point.x, point.y);
            });
            ctx.stroke();
            
            // Draw points
            points.forEach(point => {
                ctx.beginPath();
                ctx.arc(point.x, point.y, 4, 0, 2 * Math.PI);
                ctx.fill();
            });
        });
        
        // Draw labels
        ctx.fillStyle = '#2c3e50';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        
        // Day labels
        const dayLabels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
        dayLabels.forEach((label, i) => {
            const x = padding + (i / 6) * chartWidth;
            ctx.fillText(label, x, height - 10);
        });
        
        // Value labels
        ctx.textAlign = 'right';
        for (let i = 0; i <= 4; i++) {
            const y = padding + (i / 4) * chartHeight;
            const value = 10 - (i * 2.5);
            ctx.fillText(value.toString(), padding - 5, y + 4);
        }
    }
    
    showAchievement(title, message) {
        // Create achievement notification
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.innerHTML = `
            <div class="achievement-content">
                <div class="achievement-icon">🏆</div>
                <div class="achievement-text">
                    <h4>${title}</h4>
                    <p>${message}</p>
                </div>
            </div>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            transform: translateX(400px);
            transition: transform 0.5s ease;
            max-width: 300px;
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 500);
        }, 3000);
    }
}

// Initialize health tracker when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WellbeingAgent();
    new HealthTracker();
    
    // Add some interactive features
    addInteractiveFeatures();
});
