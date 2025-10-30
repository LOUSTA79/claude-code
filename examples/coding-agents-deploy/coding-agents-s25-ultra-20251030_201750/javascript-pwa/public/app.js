/**
 * Samsung S25 Ultra Coding Agent App - Client-Side JavaScript
 * ==========================================================
 */

class CodingAgentApp {
    constructor() {
        this.currentAgent = 'chat';
        this.chatHistory = [];
        this.recognition = null;
        this.init();
    }

    init() {
        this.setupTabs();
        this.setupChat();
        this.setupRead();
        this.setupList();
        this.setupBash();
        this.setupEdit();
        this.setupSearch();
        this.setupGenerate();
        this.setupVoice();
        this.addWelcomeMessage();
    }

    // ============================================================================
    // TAB SWITCHING
    // ============================================================================

    setupTabs() {
        const tabs = document.querySelectorAll('.agent-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const agent = tab.dataset.agent;
                this.switchAgent(agent);
            });
        });
    }

    switchAgent(agent) {
        // Update tabs
        document.querySelectorAll('.agent-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.agent === agent);
        });

        // Update panels
        document.querySelectorAll('.agent-panel').forEach(panel => {
            panel.classList.toggle('active', panel.id === `panel-${agent}`);
        });

        this.currentAgent = agent;
    }

    // ============================================================================
    // CHAT AGENT
    // ============================================================================

    setupChat() {
        const input = document.getElementById('chat-input');
        const sendBtn = document.getElementById('chat-send');

        const sendMessage = () => this.sendChatMessage();

        sendBtn.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    addWelcomeMessage() {
        this.addMessage('system', '👋 Welcome to Coding Agent! Running on your Samsung S25 Ultra.');
    }

    addMessage(type, content) {
        const messagesDiv = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = content;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    async sendChatMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message) return;

        this.addMessage('user', message);
        input.value = '';

        this.addMessage('system', 'Thinking...');

        try {
            const response = await this.apiCall('/api/agent/chat', {
                message: message,
                history: this.chatHistory.slice(-10) // Last 10 messages
            });

            // Remove "Thinking..." message
            const messages = document.getElementById('chat-messages');
            messages.removeChild(messages.lastChild);

            this.addMessage('agent', response.response);

            this.chatHistory.push(
                { role: 'user', content: message },
                { role: 'assistant', content: response.response }
            );
        } catch (error) {
            this.showToast('error', error.message);
        }
    }

    // ============================================================================
    // READ AGENT
    // ============================================================================

    setupRead() {
        document.getElementById('read-btn').addEventListener('click', () => this.readFile());
    }

    async readFile() {
        const path = document.getElementById('read-path').value.trim();
        if (!path) {
            this.showToast('warning', 'Please enter a file path');
            return;
        }

        const resultDiv = document.getElementById('read-result');
        resultDiv.innerHTML = '<div class="loading"></div> Reading file...';

        try {
            const response = await this.apiCall('/api/agent/read', { path });

            resultDiv.innerHTML = `
                <div style="margin: 16px 0;">
                    <strong>📄 ${path}</strong><br>
                    <small>${response.lines} lines · ${this.formatBytes(response.size)}</small>
                </div>
                <div class="code-block">${this.escapeHtml(response.content.substring(0, 1000))}${response.content.length > 1000 ? '\n\n... (truncated)' : ''}</div>
                <div style="margin: 16px 0;">
                    <strong>🤖 AI Analysis:</strong><br>
                    ${this.escapeHtml(response.analysis)}
                </div>
            `;

            this.showToast('success', 'File read successfully');
        } catch (error) {
            resultDiv.innerHTML = `<div class="message system" style="background: var(--danger);">❌ ${error.message}</div>`;
            this.showToast('error', error.message);
        }
    }

    // ============================================================================
    // LIST AGENT
    // ============================================================================

    setupList() {
        document.getElementById('list-btn').addEventListener('click', () => this.listDirectory());
    }

    async listDirectory() {
        const path = document.getElementById('list-path').value.trim() || '.';
        const listDiv = document.getElementById('file-list');

        listDiv.innerHTML = '<div class="loading"></div> Loading...';

        try {
            const response = await this.apiCall('/api/agent/list', { path });

            if (response.files.length === 0) {
                listDiv.innerHTML = '<div class="message system">No files found</div>';
                return;
            }

            listDiv.innerHTML = response.files.map(file => `
                <li class="file-item ${file.type}" data-path="${file.path}">
                    ${file.type === 'directory' ? '📁' : '📄'} ${file.name}
                </li>
            `).join('');

            // Add click handlers
            document.querySelectorAll('.file-item').forEach(item => {
                item.addEventListener('click', () => {
                    const filePath = item.dataset.path;
                    if (item.classList.contains('directory')) {
                        document.getElementById('list-path').value = filePath;
                        this.listDirectory();
                    } else {
                        document.getElementById('read-path').value = filePath;
                        this.switchAgent('read');
                    }
                });
            });

            this.showToast('success', `Found ${response.files.length} items`);
        } catch (error) {
            listDiv.innerHTML = `<div class="message system" style="background: var(--danger);">❌ ${error.message}</div>`;
            this.showToast('error', error.message);
        }
    }

    // ============================================================================
    // BASH AGENT
    // ============================================================================

    setupBash() {
        const input = document.getElementById('bash-cmd');
        const btn = document.getElementById('bash-btn');

        btn.addEventListener('click', () => this.executeCommand());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.executeCommand();
            }
        });
    }

    async executeCommand() {
        const command = document.getElementById('bash-cmd').value.trim();
        if (!command) {
            this.showToast('warning', 'Please enter a command');
            return;
        }

        const outputDiv = document.getElementById('bash-output');
        outputDiv.textContent = 'Executing...';

        try {
            const response = await this.apiCall('/api/agent/bash', { command });

            let output = '';
            if (response.stdout) output += response.stdout;
            if (response.stderr) output += '\n[stderr]\n' + response.stderr;

            outputDiv.textContent = output || '(no output)';
            this.showToast('success', 'Command executed');
        } catch (error) {
            outputDiv.textContent = `Error: ${error.message}\n\n${error.stdout || ''}\n${error.stderr || ''}`;
            this.showToast('error', 'Command failed');
        }
    }

    // ============================================================================
    // EDIT AGENT
    // ============================================================================

    setupEdit() {
        document.getElementById('edit-btn').addEventListener('click', () => this.saveFile());
    }

    async saveFile() {
        const path = document.getElementById('edit-path').value.trim();
        const content = document.getElementById('edit-content').value;

        if (!path) {
            this.showToast('warning', 'Please enter a file path');
            return;
        }

        try {
            const response = await this.apiCall('/api/agent/edit', {
                path,
                content,
                operation: 'write'
            });

            document.getElementById('edit-result').innerHTML = `
                <div class="message agent">
                    ✅ File saved successfully<br>
                    <small>${response.path} · ${this.formatBytes(response.size)}</small>
                </div>
            `;

            this.showToast('success', 'File saved');
        } catch (error) {
            document.getElementById('edit-result').innerHTML = `
                <div class="message system" style="background: var(--danger);">❌ ${error.message}</div>
            `;
            this.showToast('error', error.message);
        }
    }

    // ============================================================================
    // SEARCH AGENT
    // ============================================================================

    setupSearch() {
        document.getElementById('search-btn').addEventListener('click', () => this.searchCode());
    }

    async searchCode() {
        const query = document.getElementById('search-query').value.trim();
        const path = document.getElementById('search-path').value.trim() || '.';

        if (!query) {
            this.showToast('warning', 'Please enter a search term');
            return;
        }

        const resultsDiv = document.getElementById('search-results');
        resultsDiv.innerHTML = '<div class="loading"></div> Searching...';

        try {
            const response = await this.apiCall('/api/agent/search', { query, path });

            if (response.results.length === 0) {
                resultsDiv.innerHTML = '<div class="message system">No results found</div>';
                return;
            }

            resultsDiv.innerHTML = `
                <div style="margin-bottom: 12px;">
                    <strong>Found ${response.count} matches</strong>
                </div>
                ${response.results.map(result => `
                    <div class="file-item file">
                        <strong>${result.file}:${result.line}</strong><br>
                        <code>${this.escapeHtml(result.content)}</code>
                    </div>
                `).join('')}
            `;

            this.showToast('success', `Found ${response.count} matches`);
        } catch (error) {
            resultsDiv.innerHTML = `<div class="message system" style="background: var(--danger);">❌ ${error.message}</div>`;
            this.showToast('error', error.message);
        }
    }

    // ============================================================================
    // GENERATE AGENT
    // ============================================================================

    setupGenerate() {
        document.getElementById('generate-btn').addEventListener('click', () => this.generateCode());
    }

    async generateCode() {
        const prompt = document.getElementById('generate-prompt').value.trim();
        const language = document.getElementById('generate-lang').value;

        if (!prompt) {
            this.showToast('warning', 'Please describe what you want to generate');
            return;
        }

        const outputDiv = document.getElementById('generate-output');
        outputDiv.textContent = '🤖 Generating code...';

        try {
            const response = await this.apiCall('/api/agent/generate', { prompt, language });

            outputDiv.textContent = response.code;
            this.showToast('success', 'Code generated');
        } catch (error) {
            outputDiv.textContent = `Error: ${error.message}`;
            this.showToast('error', error.message);
        }
    }

    // ============================================================================
    // VOICE INPUT
    // ============================================================================

    setupVoice() {
        const voiceBtn = document.getElementById('voice-btn');

        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            voiceBtn.style.display = 'none';
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('chat-input').value = transcript;
            this.showToast('success', 'Voice recognized');
        };

        this.recognition.onerror = (event) => {
            this.showToast('error', 'Voice recognition error');
            voiceBtn.classList.remove('recording');
        };

        this.recognition.onend = () => {
            voiceBtn.classList.remove('recording');
        };

        voiceBtn.addEventListener('click', () => {
            if (voiceBtn.classList.contains('recording')) {
                this.recognition.stop();
                voiceBtn.classList.remove('recording');
            } else {
                this.recognition.start();
                voiceBtn.classList.add('recording');
                this.showToast('success', 'Listening...');
            }
        });
    }

    // ============================================================================
    // UTILITIES
    // ============================================================================

    async apiCall(endpoint, data) {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok || !result.ok) {
            throw new Error(result.error || 'API request failed');
        }

        return result;
    }

    showToast(type, message) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new CodingAgentApp());
} else {
    new CodingAgentApp();
}
