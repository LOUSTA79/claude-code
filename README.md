# Claude Code

![](https://img.shields.io/badge/Node.js-18%2B-brightgreen?style=flat-square) [![npm]](https://www.npmjs.com/package/@anthropic-ai/claude-code)

[npm]: https://img.shields.io/npm/v/@anthropic-ai/claude-code.svg?style=flat-square

Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows -- all through natural language commands. Use it in your terminal, IDE, or tag @claude on Github.

**Learn more in the [official documentation](https://docs.anthropic.com/en/docs/claude-code/overview)**.

<img src="./demo.gif" />

## Get started

1. Install Claude Code:

```sh
npm install -g @anthropic-ai/claude-code
```

2. Navigate to your project directory and run `claude`.

## Plugin Development & Deployment

This repository includes a comprehensive deployment toolkit for plugin developers and maintainers:

- **Deployment Script**: Run `./scripts/deploy-claude-code.sh` for interactive plugin management
- **Documentation**: See [DEPLOYMENT_INDEX.md](./DEPLOYMENT_INDEX.md) for complete guides
- **Quick Start**: Check [DEPLOYMENT_QUICKSTART.md](./DEPLOYMENT_QUICKSTART.md) for rapid setup

### For Plugin Developers
```sh
# Create a new plugin
./scripts/deploy-claude-code.sh
# Select option 1: Create new plugin
```

### For Users
Claude Code is a CLI tool installed via npm. You do not need to deploy anything - just install and use:
```sh
npm install -g @anthropic-ai/claude-code
```

For detailed deployment information, see [DEPLOYMENT_README.md](./DEPLOYMENT_README.md).

## Reporting Bugs

We welcome your feedback. Use the `/bug` command to report issues directly within Claude Code, or file a [GitHub issue](https://github.com/anthropics/claude-code/issues).

## Connect on Discord

Join the [Claude Developers Discord](https://anthropic.com/discord) to connect with other developers using Claude Code. Get help, share feedback, and discuss your projects with the community.

## Data collection, usage, and retention

When you use Claude Code, we collect feedback, which includes usage data (such as code acceptance or rejections), associated conversation data, and user feedback submitted via the `/bug` command.

### How we use your data

See our [data usage policies](https://docs.anthropic.com/en/docs/claude-code/data-usage).

### Privacy safeguards

We have implemented several safeguards to protect your data, including limited retention periods for sensitive information, restricted access to user session data, and clear policies against using feedback for model training.

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).
