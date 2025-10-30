#!/usr/bin/env node
/**
 * Samsung S25 Ultra Coding Agent App - Express Server
 * ===================================================
 *
 * Mobile-optimized coding agent system for Samsung Galaxy S25 Ultra
 * Combines chat, file operations, bash execution, and AI assistance
 */

require('dotenv').config();
const express = require('express');
const { OpenAI } = require('openai');
const fs = require('fs').promises;
const { exec } = require('child_process');
const util = require('util');
const path = require('path');

const execAsync = util.promisify(exec);

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize OpenAI
const oai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const CHAT_MODEL = process.env.OPENAI_MODEL || "gpt-4o-mini";

// Middleware
app.use(express.json({ limit: "10mb" }));
app.use(express.static(path.join(__dirname, '../public')));

// Logging middleware
app.use((req, res, next) => {
  console.log(`📱 ${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// ============================================================================
// AGENT ENDPOINTS
// ============================================================================

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    device: 'Samsung S25 Ultra',
    timestamp: new Date().toISOString(),
    agents: ['chat', 'read', 'list', 'bash', 'edit', 'search']
  });
});

// Chat Agent - General conversation and assistance
app.post('/api/agent/chat', async (req, res) => {
  try {
    const { message, history = [] } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    console.log(`💬 Chat request: ${message.substring(0, 50)}...`);

    // Build conversation history
    const messages = [
      {
        role: 'system',
        content: 'You are a helpful coding assistant running on a Samsung S25 Ultra. Be concise and mobile-friendly in your responses.'
      },
      ...history,
      { role: 'user', content: message }
    ];

    const completion = await oai.chat.completions.create({
      model: CHAT_MODEL,
      messages: messages,
      max_tokens: 1000,
    });

    const response = completion.choices[0].message.content;

    res.json({
      ok: true,
      agent: 'chat',
      response: response,
      model: CHAT_MODEL
    });
  } catch (error) {
    console.error('❌ Chat error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Read Agent - File reading and analysis
app.post('/api/agent/read', async (req, res) => {
  try {
    const { path: filePath } = req.body;

    if (!filePath) {
      return res.status(400).json({ error: 'File path is required' });
    }

    console.log(`📖 Reading file: ${filePath}`);

    // Security check - prevent directory traversal
    const safePath = path.resolve(filePath);
    if (!safePath.startsWith(process.cwd())) {
      return res.status(403).json({ error: 'Access denied' });
    }

    const content = await fs.readFile(safePath, 'utf-8');

    // Get AI analysis
    const analysis = await oai.chat.completions.create({
      model: CHAT_MODEL,
      messages: [
        {
          role: 'system',
          content: 'You are a code analysis assistant. Provide concise summaries suitable for mobile viewing.'
        },
        {
          role: 'user',
          content: `Analyze this file (${path.basename(filePath)}):\n\n${content.substring(0, 3000)}`
        }
      ],
      max_tokens: 500,
    });

    res.json({
      ok: true,
      agent: 'read',
      path: filePath,
      content: content,
      lines: content.split('\n').length,
      size: Buffer.byteLength(content, 'utf-8'),
      analysis: analysis.choices[0].message.content
    });
  } catch (error) {
    console.error('❌ Read error:', error);
    res.status(500).json({ error: error.message });
  }
});

// List Agent - Directory listing
app.post('/api/agent/list', async (req, res) => {
  try {
    const { path: dirPath = '.' } = req.body;

    console.log(`📁 Listing directory: ${dirPath}`);

    const safePath = path.resolve(dirPath);
    const entries = await fs.readdir(safePath, { withFileTypes: true });

    const files = entries.map(entry => ({
      name: entry.name,
      type: entry.isDirectory() ? 'directory' : 'file',
      path: path.join(dirPath, entry.name)
    }));

    res.json({
      ok: true,
      agent: 'list',
      path: dirPath,
      count: files.length,
      files: files
    });
  } catch (error) {
    console.error('❌ List error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Bash Agent - Command execution
app.post('/api/agent/bash', async (req, res) => {
  try {
    const { command, cwd = process.cwd() } = req.body;

    if (!command) {
      return res.status(400).json({ error: 'Command is required' });
    }

    console.log(`⚡ Executing: ${command}`);

    // Security check - warn about dangerous commands
    const dangerousPatterns = ['rm -rf /', 'dd if=', 'mkfs', ':(){:|:&};:'];
    if (dangerousPatterns.some(pattern => command.includes(pattern))) {
      return res.status(403).json({ error: 'Dangerous command blocked' });
    }

    const { stdout, stderr } = await execAsync(command, {
      cwd: cwd,
      timeout: 30000, // 30 second timeout
      maxBuffer: 1024 * 1024 // 1MB buffer
    });

    res.json({
      ok: true,
      agent: 'bash',
      command: command,
      stdout: stdout,
      stderr: stderr,
      cwd: cwd
    });
  } catch (error) {
    console.error('❌ Bash error:', error);
    res.status(500).json({
      error: error.message,
      stdout: error.stdout || '',
      stderr: error.stderr || ''
    });
  }
});

// Edit Agent - File modification
app.post('/api/agent/edit', async (req, res) => {
  try {
    const { path: filePath, content, operation = 'write' } = req.body;

    if (!filePath) {
      return res.status(400).json({ error: 'File path is required' });
    }

    console.log(`✏️  Editing file: ${filePath}`);

    const safePath = path.resolve(filePath);

    if (operation === 'write') {
      // Create directory if it doesn't exist
      await fs.mkdir(path.dirname(safePath), { recursive: true });
      await fs.writeFile(safePath, content, 'utf-8');

      res.json({
        ok: true,
        agent: 'edit',
        operation: 'write',
        path: filePath,
        size: Buffer.byteLength(content, 'utf-8')
      });
    } else if (operation === 'append') {
      await fs.appendFile(safePath, content, 'utf-8');

      res.json({
        ok: true,
        agent: 'edit',
        operation: 'append',
        path: filePath
      });
    } else {
      res.status(400).json({ error: 'Invalid operation' });
    }
  } catch (error) {
    console.error('❌ Edit error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Search Agent - Code searching
app.post('/api/agent/search', async (req, res) => {
  try {
    const { query, path: searchPath = '.', fileType = '*' } = req.body;

    if (!query) {
      return res.status(400).json({ error: 'Search query is required' });
    }

    console.log(`🔍 Searching for: ${query}`);

    // Use grep for searching
    const grepCommand = `grep -r -n -i "${query}" ${searchPath} --include="*.${fileType === '*' ? '*' : fileType}"`;

    try {
      const { stdout } = await execAsync(grepCommand, {
        timeout: 10000,
        maxBuffer: 1024 * 1024
      });

      const results = stdout.split('\n')
        .filter(line => line.trim())
        .map(line => {
          const [filePath, lineNum, ...contentParts] = line.split(':');
          return {
            file: filePath,
            line: parseInt(lineNum),
            content: contentParts.join(':').trim()
          };
        })
        .slice(0, 50); // Limit to 50 results

      res.json({
        ok: true,
        agent: 'search',
        query: query,
        count: results.length,
        results: results
      });
    } catch (error) {
      // No results found
      res.json({
        ok: true,
        agent: 'search',
        query: query,
        count: 0,
        results: []
      });
    }
  } catch (error) {
    console.error('❌ Search error:', error);
    res.status(500).json({ error: error.message });
  }
});

// AI-Assisted Code Generation
app.post('/api/agent/generate', async (req, res) => {
  try {
    const { prompt, language = 'javascript' } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' });
    }

    console.log(`🤖 Generating code: ${prompt.substring(0, 50)}...`);

    const completion = await oai.chat.completions.create({
      model: CHAT_MODEL,
      messages: [
        {
          role: 'system',
          content: `You are a code generation assistant. Generate clean, well-commented ${language} code. Return only the code without explanations.`
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      max_tokens: 1500,
    });

    const code = completion.choices[0].message.content;

    res.json({
      ok: true,
      agent: 'generate',
      language: language,
      code: code,
      model: CHAT_MODEL
    });
  } catch (error) {
    console.error('❌ Generate error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Voice input processing
app.post('/api/voice/transcribe', async (req, res) => {
  try {
    // Placeholder for voice transcription
    // In a full implementation, you would use Whisper API or similar
    res.json({
      ok: true,
      message: 'Voice transcription not yet implemented',
      suggestion: 'Use Web Speech API on the client side'
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// START SERVER
// ============================================================================

app.listen(PORT, '0.0.0.0', () => {
  console.log('\n╔══════════════════════════════════════════════════════╗');
  console.log('║  🤖 Coding Agent App - Samsung S25 Ultra           ║');
  console.log('╠══════════════════════════════════════════════════════╣');
  console.log(`║  📱 Server: http://localhost:${PORT}                    ║`);
  console.log(`║  🌐 Network: http://[your-ip]:${PORT}                  ║`);
  console.log('╠══════════════════════════════════════════════════════╣');
  console.log('║  Agents Available:                                   ║');
  console.log('║    💬 Chat    - AI conversation                      ║');
  console.log('║    📖 Read    - File reading & analysis              ║');
  console.log('║    📁 List    - Directory listing                    ║');
  console.log('║    ⚡ Bash    - Command execution                     ║');
  console.log('║    ✏️  Edit    - File modification                    ║');
  console.log('║    🔍 Search  - Code searching                       ║');
  console.log('║    🤖 Generate- AI code generation                   ║');
  console.log('╠══════════════════════════════════════════════════════╣');
  console.log(`║  🎯 Model: ${CHAT_MODEL.padEnd(42)} ║`);
  console.log('║  ✅ Ready for mobile access!                         ║');
  console.log('╚══════════════════════════════════════════════════════╝\n');
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down Coding Agent App...');
  process.exit(0);
});

process.on('uncaughtException', (error) => {
  console.error('💥 Uncaught exception:', error);
});

process.on('unhandledRejection', (error) => {
  console.error('💥 Unhandled rejection:', error);
});
