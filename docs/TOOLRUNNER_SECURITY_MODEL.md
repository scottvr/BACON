## Secure Tool Runner: Component Specification
### 🎯 1. Objective
To create a ToolRunner module that can safely execute a pre-defined allowlist of tools (e.g., API calls, CLI commands) using parameters supplied by an LLM, while preventing parameter-based attacks, unauthorized actions, and data leakage.

### ⚖️ 2. Core Principles
Allowlist, Not Blocklist: The agent can only call tools that are explicitly defined in a configuration file. There is no mechanism for calling arbitrary commands.

Parameter Sanitization: All parameters originating from the LLM are to be treated as untrusted and must be strictly validated and sanitized before being used.

Scoped Credentials: The LLM never has access to secrets like API keys. The ToolRunner module handles credential management on the host.

Human-in-the-Loop (HITL) by Default: Any tool that incurs cost, modifies files, or accesses a network should require explicit user approval by default.

### 🏗️ 3. Proposed Architecture & Lifecycle
Request: The ToolRunner receives a tool_name and a dictionary of parameters from the Executive Planner.

Validation: It looks up the tool_name in its registered tool configuration (tools.yaml). If the tool doesn't exist, the request is rejected immediately.

Approval: It checks the tool's configuration for requires_approval: true. If true, it pauses and presents the user with the exact action to be taken (e.g., Run command: curl https://api.example.com?q=...) and waits for a y/n confirmation.

Sanitization: It validates each parameter against the types and constraints defined in the tool's configuration. For example, it will ensure a filename parameter does not contain path traversal characters (../).

Execution: It invokes the appropriate handler (api_handler, cli_handler) with the sanitized parameters.

Response: It captures the result (e.g., API response JSON, CLI stdout) and returns it to the Executive in a structured format.

### 🔐 4. Key Security Mechanisms
This is where the ToolRunner's security model is enforced.

Strict Parameter Validation: Use a library like Pydantic to define data models for each tool's parameters. This provides strong type checking, validation (e.g., for URLs or numbers), and helps prevent unexpected inputs.

Command Injection Prevention: When executing CLI tools, never use shell=True. All commands must be executed by passing a list of arguments. This is the single most important defense against command injection.

INSECURE: subprocess.run(f"grep '{query}' filename.txt", shell=True)

SECURE: subprocess.run(['grep', query, 'filename.txt'], shell=False, check=True)

Secure Credential Management: API keys, tokens, and other secrets must never be stored in the tool configuration or be visible to the LLM. They should be loaded from the host's environment variables or a secure secret management system (like .env files loaded by the ToolRunner at startup).

Scoped Filesystem Access: Any tool that interacts with the filesystem must be restricted to the agent's current working directory (e.g., output/runs/{uuid}/). All file path parameters must be validated to ensure they are relative paths and do not escape this sandboxed directory.

### 📜 5. Tool Configuration (tools.yaml)
The tool definition is central to its security. The config should be structured to enforce these rules.
```yaml
# tools.yaml

- name: "search_web"
  description: "Searches the web for a given query using the Brave Search API."
  type: "api"
  handler: "api_handler"
  requires_approval: false
  config:
    # The ToolRunner loads the 'BRAVE_API_KEY' from the host environment
    api_key_env: "BRAVE_API_KEY"
    base_url: "https://api.search.brave.com/res/v1/web/search"
    params:
      - name: "q"
        type: "string"
        required: true

- name: "read_file"
  description: "Reads the content of a file from the current working directory."
  type: "cli"
  handler: "cli_handler"
  requires_approval: true
  config:
    # Command and arguments are defined as a list
    command: ["cat"]
    params:
      - name: "filename"
        type: "filepath" # A custom type for validation
        required: true
```

### 📋 6. Implementation Roadmap
[x] Define the tools.yaml schema and create Pydantic models for validation.

[x] Implement the YAML parser that loads and registers the allowlisted tools at startup.

[x] Build the ToolRunner class with the core logic for validation, HITL approval, and dispatching to handlers.

[x] Write the api_handler and cli_handler functions, ensuring they implement the secure practices outlined above (credential loading, shell=False, etc.).

[x] Develop parameter sanitization functions, especially for file paths to prevent directory traversal.

[x] Test with adversarial inputs, such as trying to inject commands (my-query; ls -la) or traverse directories (../../etc/passwd) to ensure the protections work as expected.