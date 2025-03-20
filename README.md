# MCP Hello World

A simple example demonstrating the Model Context Protocol (MCP).

## What is MCP?

Model Context Protocol (MCP) is a specification for structured communication between LLMs and their environments. It provides a standardized way to:

- Execute tool calls
- Include hidden reasoning (thinking)
- Handle parallel tool execution
- Manage conditional/streaming content
- And more...

MCP uses a JSON-based message format with specific directives that guide the model's behavior.

## Example

The `mcp_hello.py` script demonstrates two basic MCP messages:

1. A "thinking" directive - Used for internal reasoning that isn't shown to end users
2. A "tool_use" directive - Used to request execution of an external tool

Run the example:

```bash
python mcp_hello.py
```

## Learn More

- [MCP GitHub Repo](https://github.com/anthropics/anthropic-cookbook/tree/main/cookbook/model_context_protocol)
- [Anthropic MCP Documentation](https://docs.anthropic.com/claude/docs/model-context-protocol)