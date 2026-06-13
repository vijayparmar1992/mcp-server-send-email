# mcp-server-send-email

MCP server for sending emails via SMTP.

## Installation

```bash
uv pip install -e .
```

## Configuration

Create a `.env` file with your SMTP settings:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your_email@gmail.com
SMTP_STARTTLS=true
```

## Usage

### With MCP Clients (Bob, Claude Desktop, etc.)

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "send-email": {
      "command": "uv",
      "args": ["run", "mcp-server-send-email"],
      "cwd": "/path/to/mcp-server-send-email"
    }
  }
}
```

### Standalone Server

```bash
uv run mcp-server-send-email
```

Server runs on `http://127.0.0.1:8001`

## Tool

**`send_email`** - Send an email via SMTP

Parameters:
- `to` (required): List of recipient email addresses
- `subject` (required): Email subject
- `message` (required): Email body (plain text)
- `cc` (optional): List of CC email addresses
- `bcc` (optional): List of BCC email addresses
- `reply_to` (optional): Reply-to email address

Response:
- `status`: `sent` or `error`
- `to`: List of recipients
- `subject`: Email subject
- `detail`: Status message

## Testing

This server supports dual transport modes and has been verified with:

### MCP Inspector
- ✅ **Streamable HTTP**: Tested via `http://127.0.0.1:8001/mcp`
- ✅ **stdio**: Tested with command-based configuration

### IBM Bob Integration
- ✅ **stdio mode**: Successfully integrated and verified
- ✅ **Dual-mode server**: Automatically detects transport based on `sys.stdin.isatty()`
  - Terminal mode → Streamable HTTP server
  - Piped/subprocess mode → stdio transport

The server intelligently switches between HTTP and stdio modes, making it compatible with both interactive testing (MCP Inspector) and MCP client integration (Bob, Claude Desktop).

## License

MIT