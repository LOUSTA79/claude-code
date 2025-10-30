# 🎥 Video Tutorial Script - Coding Agents for S25 Ultra

**Duration:** ~10-15 minutes
**Target Audience:** Mobile developers, AI enthusiasts
**Platform:** Samsung Galaxy S25 Ultra with Termux

---

## 🎬 Opening (0:00 - 0:30)

**[Screen Recording of S25 Ultra Home Screen]**

**Narrator:**
> "Hey everyone! Today I'm going to show you something amazing - two complete AI coding agent systems running entirely on my Samsung Galaxy S25 Ultra. Whether you prefer a beautiful web interface or lightning-fast terminal commands, I've got you covered. Let's dive in!"

**[Show both apps side by side on split screen]**

---

## 📱 Part 1: JavaScript PWA Demo (0:30 - 5:00)

### Scene 1: Opening the App (0:30 - 1:00)

**[Tap the home screen icon]**

**Narrator:**
> "First up is the JavaScript PWA - a Progressive Web App with a gorgeous mobile interface. I've already installed it to my home screen, and it launches just like a native app."

**[App opens, showing the main interface with agent tabs]**

> "Look at this beautiful dark theme, optimized for the S25 Ultra's display. We have 7 specialized AI agents: Chat, Read, List, Bash, Edit, Search, and Generate."

### Scene 2: Chat Agent (1:00 - 2:00)

**[Tap the Chat tab]**

**Narrator:**
> "Let's start with the Chat agent. I can type my question, or..."

**[Tap the microphone button]**

> "...use voice input! Watch this:"

**[Speak into phone]**
> "Write a Python function to calculate fibonacci numbers"

**[AI responds with code]**

**Narrator:**
> "And there we go! The AI generated a complete function with explanation. This uses OpenAI's GPT-4o-mini model."

### Scene 3: File Operations (2:00 - 3:30)

**[Switch to List tab]**

**Narrator:**
> "The List agent lets me browse my project files with a beautiful touch interface."

**[Tap through directories]**

> "I can tap any file to read it..."

**[File opens in Read tab]**

> "The Read agent not only shows me the code but also provides AI analysis of what it does."

**[Switch to Edit tab]**

> "And the Edit agent lets me create or modify files right here."

### Scene 4: Code Generation (3:30 - 4:30)

**[Switch to Generate tab]**

**Narrator:**
> "My favorite feature is the Generate agent. I can describe what I want, choose a programming language, and let AI write the code for me."

**[Type: "Create a REST API endpoint for user authentication"]**
**[Select language: Go]**
**[Tap Generate]**

**[Code appears]**

> "Beautiful! Ready to copy and use."

### Scene 5: Command Execution (4:30 - 5:00)

**[Switch to Bash tab]**

**Narrator:**
> "The Bash agent executes commands safely, with dangerous commands blocked for security."

**[Type: ls -la]**
**[Output appears]**

> "Perfect for quick tasks without leaving the app."

---

## ⚡ Part 2: Go CLI Demo (5:00 - 8:00)

### Scene 1: Terminal Launch (5:00 - 5:30)

**[Switch to Termux app]**

**Narrator:**
> "Now let's look at the Go CLI - perfect for when I'm already in the terminal and need quick answers."

**[Type: cd ~/aic_projects/go-coding-agent-workshop]**
**[Type: ./bin/agent --help]**

**[Shows available commands]**

> "We have 6 agents here: Chat, Read, List, Bash, Edit, and Search. The startup time is instant - under 100 milliseconds!"

### Scene 2: Chat Demo (5:30 - 6:30)

**[Type: ./bin/agent chat]**

**[Agent starts]**

**Narrator:**
> "The chat agent uses Anthropic's Claude - one of the most powerful AI models available."

**[Type: "Explain goroutines and channels in Go"]**

**[Response appears]**

> "Notice how fast the responses are, and the colored output makes it easy to read on mobile."

### Scene 3: File Operations (6:30 - 7:30)

**[Exit chat, run: ./bin/agent read]**

**Narrator:**
> "The Read agent can analyze any file in my project."

**[Enter file path]**
**[AI analysis appears]**

**[Run: ./bin/agent list]**

> "List shows directory contents with file sizes and types."

**[Enter directory path]**
**[Formatted list appears]**

### Scene 4: Search (7:30 - 8:00)

**[Run: ./bin/agent search]**

**Narrator:**
> "The Search agent is incredibly useful for finding code across my entire project."

**[Enter search query: "func main"]**
**[Results appear with file paths and line numbers]**

---

## 🔄 Part 3: Comparison & Use Cases (8:00 - 10:00)

### Scene 1: Side-by-Side (8:00 - 9:00)

**[Split screen: PWA on left, CLI on right]**

**Narrator:**
> "So which one should you use? Actually, I use both!"

**[Show PWA]**
> "The JavaScript PWA is perfect for:
> - Visual file browsing
> - Code generation with syntax highlighting
> - Voice coding
> - Multi-agent workflows
> - Sharing results

**[Show CLI]**
> "The Go CLI excels at:
> - Quick terminal questions
> - Integration with shell scripts
> - Low battery usage
> - SSH sessions
> - Background tasks with tmux"

### Scene 2: Real Workflow (9:00 - 10:00)

**Narrator:**
> "Here's my typical workflow:"

**[Demo workflow]**

1. **[Type in CLI]**
   > "I ask the CLI quick questions while coding..."

2. **[Switch to PWA]**
   > "Then use the PWA to browse files and generate code..."

3. **[Back to CLI]**
   > "And return to CLI for follow-up questions."

> "They complement each other perfectly!"

---

## 🎓 Part 4: Getting Started (10:00 - 12:00)

### Installation (10:00 - 11:00)

**[Show Terminal]**

**Narrator:**
> "Want to try this yourself? It's super easy to install."

**[Type commands, shown on screen]**

```bash
cd ~/aic_projects
git clone [repo-url]
cd coding-agents
bash install.sh
```

> "The installer sets up both systems and guides you through API key configuration."

### API Keys (11:00 - 11:30)

**[Show browser on phone]**

**Narrator:**
> "You'll need two API keys:
> - OpenAI for the JavaScript PWA (platform.openai.com)
> - Anthropic for the Go CLI (console.anthropic.com)

> Both have free tiers to get started!"

### First Run (11:30 - 12:00)

**[Run launcher]**

**Narrator:**
> "Then just run the launcher script, choose your agent, and start coding!"

**[Show launcher menu]**

---

## 💡 Part 5: Tips & Tricks (12:00 - 13:30)

### PWA Tips (12:00 - 12:45)

**Narrator:**
> "Pro tips for the PWA:"

1. **[Show installation]**
   > "Install to home screen for full-screen experience"

2. **[Show PM2]**
   > "Use PM2 to run the server in the background"

3. **[Show voice]**
   > "Use voice input for hands-free coding"

4. **[Show tabs]**
   > "Keep multiple agents open in tabs for multitasking"

### CLI Tips (12:45 - 13:30)

**Narrator:**
> "And for the CLI:"

1. **[Show tmux]**
   > "Run in tmux to keep sessions alive"

2. **[Show script]**
   > "Integrate into your shell scripts"

3. **[Show alias]**
   > "Create aliases for common commands"

4. **[Show verbose]**
   > "Use --verbose flag for debugging"

---

## 🚀 Part 6: Advanced Features (13:30 - 14:30)

### Customization (13:30 - 14:00)

**Narrator:**
> "Both systems are highly customizable:"

**[Show code editor]**

> "Change AI models, adjust response lengths, modify prompts, or even add your own agents!"

### Integration (14:00 - 14:30)

**Narrator:**
> "And they integrate with your existing workflow:"

- Git operations
- Package management
- Automated testing
- CI/CD pipelines

---

## 🎬 Closing (14:30 - 15:00)

**[Back to home screen showing both apps]**

**Narrator:**
> "So there you have it - two powerful AI coding systems running entirely on my Samsung Galaxy S25 Ultra. Whether you want a beautiful touch interface or blazing-fast terminal commands, you're covered."

**[Show GitHub link]**

> "All the code is open source and available on GitHub. Links in the description. Give it a try and let me know what you think in the comments!"

**[Show final screen with key points]**

> "Thanks for watching! Don't forget to like and subscribe for more mobile development content. Happy coding!"

---

## 📋 Video Description Template

```
🤖 Build AI Coding Agents on Your Samsung Galaxy S25 Ultra!

In this video, I show you two complete AI coding agent systems that run entirely on your phone:

📱 JavaScript PWA:
• 7 AI agents with beautiful UI
• Voice input support
• Installable to home screen
• OpenAI GPT-4o-mini integration

⚡ Go CLI:
• 6 terminal-based agents
• Lightning fast (<100ms startup)
• Low memory usage
• Anthropic Claude integration

🔗 Links:
• GitHub Repository: [link]
• OpenAI API Keys: https://platform.openai.com/
• Anthropic API Keys: https://console.anthropic.com/
• Installation Guide: [link]
• Full Documentation: [link]

⏱️ Timestamps:
0:00 - Introduction
0:30 - JavaScript PWA Demo
5:00 - Go CLI Demo
8:00 - Comparison & Use Cases
10:00 - Installation Guide
12:00 - Tips & Tricks
13:30 - Advanced Features
14:30 - Closing

💬 Questions? Drop them in the comments!
👍 Like if you found this helpful!
🔔 Subscribe for more mobile dev content!

#AI #CodingAgents #Samsung #S25Ultra #Termux #MobileDevelopment #OpenAI #AnthropicClaude
```

---

## 🎥 B-Roll Suggestions

- Phone being used in different locations (coffee shop, commute, office)
- Split-screen comparisons
- Code being generated in real-time
- File browsing animations
- Terminal commands typing
- Successful builds and tests
- Happy developer reactions

---

## 🎵 Music Suggestions

- Upbeat tech/electronic music
- Lower volume during narration
- Crescendo during impressive demos
- Soft outro music

---

## 📸 Thumbnail Ideas

**Option 1: Split Screen**
- Left: PWA interface
- Right: Terminal CLI
- Text: "AI CODING ON YOUR PHONE"
- S25 Ultra logo

**Option 2: Action Shot**
- Hand holding S25 Ultra
- Code visible on screen
- AI chat bubble overlay
- Text: "2 POWERFUL AI AGENTS"

**Option 3: Before/After**
- Before: Blank editor
- After: Generated code
- Text: "FROM IDEA TO CODE"
- AI robot icon

---

Happy recording! 🎬📱
