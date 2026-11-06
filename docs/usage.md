# Using Local Model Chat Desk

## Quick start

Install Ollama and pull a model using its official instructions. Start Ollama, run `python server.py`, and open localhost:8080. Select a model and send a message. No external model host is configured. Offline tests validate payload handling, not inference.

## Supported workflow

1. Installed-model discovery.
2. Real local Ollama chat with conversation history.
3. Same-origin loopback proxy and JSON export.

## Validation and troubleshooting

Run the commands in the README. Invalid inputs produce explicit errors rather than silently changing the requested operation. Browser audio requires a user gesture; microphone apps require HTTPS or localhost and permission. For file tools, supply supported input formats and writable output directories.

## Limitations

Requires Ollama and a downloaded model. The interface displays an unavailable state rather than fabricated responses.

Tests use synthetic fixtures. These tests do not certify hardware compatibility, real-world forecast quality, trained-model accuracy, or production suitability for every input.
