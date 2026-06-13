from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import sys

from .models import EmailRequest, EmailResponse
from .smtp_client import send_email as send_email_smtp

mcp = FastMCP("send-email",
              host="127.0.0.1",
              port=8001,
              )


@mcp.tool()
def send_email(
    to: list[str],
    subject: str,
    message: str,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    reply_to: str | None = None,
) -> EmailResponse:
    """Send an email to one or more recipients using the configured SMTP server."""
    request = EmailRequest(
        to=to,
        subject=subject,
        message=message,
        cc=cc or [],
        bcc=bcc or [],
        reply_to=reply_to,
    )

    return send_email_smtp(request)


def main() -> None:
    # Check if running in stdio mode 
    if sys.stdin.isatty():
        # Running in terminal - start HTTP server
        app = mcp.streamable_http_app()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["Mcp-Session-Id"],
        )
        uvicorn.run(app, host="127.0.0.1", port=8001)
    else:
        # Running via stdio (piped) - use stdio transport
        mcp.run()
