// Chatbot functionality
// This chatbot knows everything about the portfolio owner's skills, projects, and experience
const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions';

// Available models
const GROQ_MODELS = [
    'llama-3.1-8b-instant',
    'llama-3.3-70b-versatile',
    'llama-3.2-3b-preview',
    'mixtral-8x7b-32768',
    'gemma2-9b-it'
];

// State management
// Get API key from config.js file
let apiKey = '';
if (typeof CONFIG !== 'undefined' && CONFIG.GROQ_API_KEY && CONFIG.GROQ_API_KEY !== 'YOUR_API_KEY_HERE') {
    apiKey = CONFIG.GROQ_API_KEY;
} else {
    // Fallback: try localStorage
    apiKey = localStorage.getItem('groq_api_key') || '';
}

// Portfolio information - extracted from the HTML
const portfolioInfo = {
    name: 'James Marwin Bolongon', // Update this with your actual name
    title: 'Full Stack Developer & AI Enthusiast',
    description: 'I create beautiful, functional websites and AI-powered applications',
    about: [
        'I\'m a passionate developer with expertise in web development and artificial intelligence. I love creating innovative solutions that combine cutting-edge technology with user-friendly design.',
        'My journey in tech started with curiosity and has evolved into a career focused on building meaningful applications that make a difference.'
    ],
    stats: {
        projectsCompleted: '50+',
        yearsExperience: '3+',
        clientSatisfaction: '100%'
    },
    skills: [
        {
            name: 'Python',
            description: 'Backend development, AI/ML, Automation'
        },
        {
            name: 'JavaScript',
            description: 'Frontend development, React, Node.js'
        },
        {
            name: 'HTML/CSS',
            description: 'Responsive design, Modern UI/UX'
        },
        {
            name: 'AI/ML',
            description: 'Machine Learning, NLP, Chatbots'
        }
    ],
    projects: [
        {
            name: 'AI Chatbot',
            description: 'An intelligent chatbot powered by Groq AI, featuring multiple model support and real-time conversations.'
        },
        {
            name: 'Web Applications',
            description: 'Modern, responsive web applications built with the latest technologies.'
        },
        {
            name: 'Mobile Apps',
            description: 'Cross-platform mobile applications with beautiful UI and smooth performance.'
        }
    ],
    contact: {
        email: 'jbolongon12@gmail.com',
        github: 'github.com/yourusername',
        linkedin: 'linkedin.com/in/yourprofile'
    }
};

// Build comprehensive system message with portfolio information
function buildSystemMessage() {
    const skillsList = portfolioInfo.skills.map(s => `- ${s.name}: ${s.description}`).join('\n');
    const projectsList = portfolioInfo.projects.map((p, i) => `${i + 1}. ${p.name}: ${p.description}`).join('\n');
    
    return `You are an AI assistant representing ${portfolioInfo.name}, a ${portfolioInfo.title}. 

PORTFOLIO INFORMATION:

Name: ${portfolioInfo.name}
Title: ${portfolioInfo.title}
Description: ${portfolioInfo.description}

ABOUT:
${portfolioInfo.about.join('\n\n')}

STATISTICS:
- Projects Completed: ${portfolioInfo.stats.projectsCompleted}
- Years of Experience: ${portfolioInfo.stats.yearsExperience}
- Client Satisfaction: ${portfolioInfo.stats.clientSatisfaction}

SKILLS:
${skillsList}

PROJECTS:
${projectsList}

CONTACT INFORMATION:
- Email: ${portfolioInfo.contact.email}
- GitHub: ${portfolioInfo.contact.github}
- LinkedIn: ${portfolioInfo.contact.linkedin}

YOUR ROLE:
You are here to help visitors learn about ${portfolioInfo.name}'s portfolio, skills, projects, and experience. You can:
- Answer questions about ${portfolioInfo.name}'s background and expertise
- Discuss the projects and skills listed
- Provide contact information when asked
- Help visitors understand what ${portfolioInfo.name} does
- Be friendly, professional, and helpful

Always provide accurate information based on the portfolio details above. If asked about something not in the portfolio, politely say you don't have that information but can help with what's available in the portfolio.`;
}

let messages = [
    {
        role: 'system',
        content: buildSystemMessage()
    }
];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeChatbot();
    setupEventListeners();
    smoothScroll();
});

function initializeChatbot() {
    // Check if API key is configured
    if (!apiKey || apiKey === 'YOUR_API_KEY_HERE') {
        console.error('API key not configured. Please add your Groq API key to config.js');
        showApiKeyError();
        return;
    }
    
    // Show chatbot interface directly
    document.getElementById('chatbotInterface').style.display = 'flex';
}

function showApiKeyError() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = `
        <div class="message bot-message">
            <div class="message-avatar">
                <i class="fas fa-exclamation-triangle"></i>
            </div>
            <div class="message-content">
                <p><strong>API Key Not Configured</strong></p>
                <p>Please add your Groq API key to the <code>config.js</code> file.</p>
                <p>Get your free API key from: <a href="https://console.groq.com/keys" target="_blank">Groq Console</a></p>
            </div>
        </div>
    `;
}

function setupEventListeners() {
    // Send message
    document.getElementById('sendButton').addEventListener('click', sendMessage);
    
    // Enter key in chat input
    document.getElementById('chatInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Clear chat
    document.getElementById('clearChat').addEventListener('click', clearChat);
}

function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        messages = [
            {
                role: 'system',
                content: buildSystemMessage()
            }
        ];
        
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>Chat cleared! I'm here to help you learn about ${portfolioInfo.name}'s portfolio. What would you like to know?</p>
                </div>
            </div>
        `;
    }
}

async function sendMessage() {
    // Check if API key is configured
    if (!apiKey || apiKey === 'YOUR_API_KEY_HERE') {
        addMessageToUI('bot', 'Please configure your API key in config.js file first.');
        return;
    }
    
    const input = document.getElementById('chatInput');
    const userMessage = input.value.trim();
    
    if (!userMessage) return;
    
    // Disable input
    input.disabled = true;
    document.getElementById('sendButton').disabled = true;
    
    // Add user message to UI
    addMessageToUI('user', userMessage);
    input.value = '';
    
    // Add user message to conversation
    messages.push({ role: 'user', content: userMessage });
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const selectedModel = document.getElementById('modelSelect').value;
        const response = await fetch(GROQ_API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: selectedModel,
                messages: messages,
                temperature: 0.7,
                max_tokens: 1024
            })
        });
        
        removeTypingIndicator(typingId);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const errorMessage = errorData.error?.message || `API Error: ${response.status}`;
            addMessageToUI('bot', `Sorry, I encountered an error: ${errorMessage}`);
            return;
        }
        
        const data = await response.json();
        const botMessage = data.choices[0].message.content;
        
        // Add bot message to conversation
        messages.push({ role: 'assistant', content: botMessage });
        
        // Add bot message to UI
        addMessageToUI('bot', botMessage);
        
        // Keep conversation manageable (last 10 exchanges + system)
        if (messages.length > 21) {
            messages = [messages[0], ...messages.slice(-20)];
        }
        
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessageToUI('bot', `Sorry, I encountered an error: ${error.message}`);
    } finally {
        // Re-enable input
        input.disabled = false;
        document.getElementById('sendButton').disabled = false;
        input.focus();
    }
}

function addMessageToUI(role, content) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const avatar = role === 'user' 
        ? '<i class="fas fa-user"></i>'
        : '<i class="fas fa-robot"></i>';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            ${avatar}
        </div>
        <div class="message-content">
            <p>${formatMessage(content)}</p>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return 'typing-indicator';
}

function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatMessage(text) {
    // Remove markdown formatting
    // Remove bold markdown (**text** or __text__)
    text = text.replace(/\*\*([^*]+)\*\*/g, '$1');
    text = text.replace(/__([^_]+)__/g, '$1');
    
    // Remove italic markdown (*text* or _text_)
    text = text.replace(/\*([^*]+)\*/g, '$1');
    text = text.replace(/_([^_]+)_/g, '$1');
    
    // Remove strikethrough (~~text~~)
    text = text.replace(/~~([^~]+)~~/g, '$1');
    
    // Escape HTML to prevent XSS
    text = escapeHtml(text);
    
    // Convert code blocks (keep these as they're useful)
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Convert links
    text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// Smooth scrolling for navigation
function smoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Mobile menu toggle (if needed)
document.querySelector('.hamburger')?.addEventListener('click', () => {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
});

