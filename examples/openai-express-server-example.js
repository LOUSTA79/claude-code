#!/usr/bin/env node
/**
 * OpenAI Express Server - Proper Initialization Example
 * =====================================================
 *
 * This example demonstrates the correct way to initialize the OpenAI client
 * in a Node.js Express server to avoid "ReferenceError: oai is not defined"
 *
 * Common mistakes:
 * - Using `oai.chat.completions.create()` without first initializing the OpenAI client
 * - Mixing CommonJS (require) and ES modules (import) syntax incorrectly
 * - Missing or incorrect environment variable loading
 *
 * This example shows TWO approaches:
 * 1. CommonJS (using require) - recommended for Termux/mobile environments
 * 2. ES Modules (using import) - recommended for modern Node.js projects
 */

// ============================================================================
// APPROACH 1: CommonJS (most compatible, works in Termux)
// ============================================================================

// Load environment variables FIRST
require('dotenv').config();

// Import required packages
const express = require('express');
const { OpenAI } = require('openai');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// ⚠️ CRITICAL: Initialize OpenAI client BEFORE using it
const oai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Middleware
app.use(express.json({ limit: "1mb" }));

// Health check endpoint
app.get("/health", (_req, res) => {
  res.json({
    status: "OK",
    timestamp: new Date().toISOString(),
    openai: oai ? "initialized" : "not initialized"
  });
});

// Chat model configuration
const CHAT_MODEL = process.env.OPENAI_MODEL || "gpt-4o-mini";

// GET chat endpoint (query parameter)
app.get("/ai/chat", async (req, res) => {
  try {
    const q = (req.query.q || "").toString().trim();
    if (!q) {
      return res.status(400).json({
        ok: false,
        error: "Missing query parameter ?q="
      });
    }

    console.log(`📥 Chat request: ${q.substring(0, 50)}...`);

    // ✅ Now we can safely use oai because it was initialized above
    const completion = await oai.chat.completions.create({
      model: CHAT_MODEL,
      messages: [{ role: "user", content: q }],
      max_tokens: 256,
    });

    const text = completion.choices?.[0]?.message?.content ?? "No response";
    console.log(`📤 AI response: ${text.substring(0, 50)}...`);

    res.json({
      ok: true,
      model: CHAT_MODEL,
      text: text
    });
  } catch (err) {
    console.error("❌ Chat error:", err.message);
    res.status(500).json({
      ok: false,
      error: err.message,
      suggestion: "Check OPENAI_API_KEY in .env file"
    });
  }
});

// POST chat endpoint (request body)
app.post("/ai/chat", async (req, res) => {
  try {
    const prompt = (req.body?.prompt || "").toString().trim();
    if (!prompt) {
      return res.status(400).json({
        ok: false,
        error: "Missing 'prompt' in request body"
      });
    }

    console.log(`📥 POST Chat request: ${prompt.substring(0, 50)}...`);

    // ✅ Using the initialized oai client
    const completion = await oai.chat.completions.create({
      model: CHAT_MODEL,
      messages: [{ role: "user", content: prompt }],
      max_tokens: 256,
    });

    const text = completion.choices?.[0]?.message?.content ?? "No response";

    res.json({
      ok: true,
      model: CHAT_MODEL,
      text: text
    });
  } catch (err) {
    console.error("❌ POST Chat error:", err.message);
    res.status(500).json({
      ok: false,
      error: err.message
    });
  }
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log('🚀 OpenAI Express Server Started');
  console.log(`🌐 Server: http://localhost:${PORT}`);
  console.log(`🔗 Health: http://localhost:${PORT}/health`);
  console.log(`💬 Chat GET: http://localhost:${PORT}/ai/chat?q=Hello`);
  console.log(`📮 Chat POST: curl -X POST http://localhost:${PORT}/ai/chat -H "Content-Type: application/json" -d '{"prompt":"Hello"}'`);
  console.log(`🤖 Model: ${CHAT_MODEL}`);
  console.log('✅ Ready!');
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down gracefully...');
  process.exit(0);
});

// ============================================================================
// APPROACH 2: ES Modules (for reference)
// ============================================================================
//
// To use ES modules, add "type": "module" to your package.json, then:
//
// import fs from "fs";
// import path from "path";
// import express from "express";
// import { OpenAI } from "openai";
// import dotenv from "dotenv";
//
// // Load environment variables
// dotenv.config();
//
// const app = express();
// const PORT = process.env.PORT || 3000;
//
// // ⚠️ CRITICAL: Initialize OpenAI client BEFORE using it
// const oai = new OpenAI({
//   apiKey: process.env.OPENAI_API_KEY,
// });
//
// // ... rest of the code remains the same

// ============================================================================
// ENVIRONMENT SETUP
// ============================================================================
//
// Create a .env file in the same directory:
//
// OPENAI_API_KEY=sk-proj-...your-key-here...
// OPENAI_MODEL=gpt-4o-mini
// PORT=3000
//
// ============================================================================
// PACKAGE.JSON DEPENDENCIES
// ============================================================================
//
// {
//   "name": "openai-express-server",
//   "version": "1.0.0",
//   "dependencies": {
//     "express": "^4.18.2",
//     "openai": "^4.0.0",
//     "dotenv": "^16.3.1"
//   }
// }
//
// Install with: npm install express openai dotenv
//
// ============================================================================
// TESTING
// ============================================================================
//
// 1. Start the server:
//    node examples/openai-express-server-example.js
//
// 2. Test health endpoint:
//    curl http://localhost:3000/health
//
// 3. Test GET chat:
//    curl "http://localhost:3000/ai/chat?q=Hello"
//
// 4. Test POST chat:
//    curl -X POST http://localhost:3000/ai/chat \
//      -H "Content-Type: application/json" \
//      -d '{"prompt": "Hello, how are you?"}'
//
// ============================================================================
// TROUBLESHOOTING
// ============================================================================
//
// Error: "ReferenceError: oai is not defined"
// → Solution: Make sure to initialize `const oai = new OpenAI(...)`
//   BEFORE any route handlers that use it
//
// Error: "Cannot use import statement outside a module"
// → Solution: Either use CommonJS (require) or add "type": "module"
//   to package.json
//
// Error: "429 You exceeded your current quota"
// → Solution: Check your OpenAI account billing and usage limits
//   at https://platform.openai.com/account/billing
//
// Error: "401 Incorrect API key provided"
// → Solution: Verify OPENAI_API_KEY in .env file is correct
//
// ============================================================================
