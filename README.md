# Astral Documentation

This repository contains the official documentation for the Astral Python SDK, a powerful toolkit for building AI-powered applications.

## Overview

The Astral Python SDK provides a unified interface to interact with various AI models and services, including:
- OpenAI
- AWS Bedrock
- Azure OpenAI
- Google Vertex AI
- Hugging Face
- And more

## Documentation Structure

- **Getting Started**: Installation guides and basic usage
- **Authentication**: Methods for authenticating with different AI providers
- **API Reference**: Detailed documentation of all SDK components
- **Examples**: Code samples demonstrating common use cases

## Using Code Block Components

To include code examples in your documentation, use the following syntax in your MDX files:

```
<CodeBlock language="python" code={`print("hello world")`} />
```

You can also use the `REPLACE_WITH:` directive to automatically insert code from files in the `code-blocks` directory:

```
REPLACE_WITH:CodeBlock filename:quickstart.py language:python
```

The above directive will be replaced with:

```
<CodeBlock language="python" code={`contents_of_quickstart.py_file`} />
```

Or for terminal commands:

```
<TerminalCommand language="bash" packageManager="npm" code={`npm install astral`} />
```

Using the directive:

```
REPLACE_WITH:TerminalCommand filename:install.sh language:bash package:npm
```

Place your code files in the `code-blocks` directory, and they will be automatically inserted into your documentation during the build process.

### Options for REPLACE_WITH directive:

- `filename` - Name of the file in the code-blocks directory (required)
- `language` - Programming language for syntax highlighting (optional)
- `package` - Package manager to use (npm, yarn, pip, etc.) - for TerminalCommand only (optional)

## Contributing

Contributions to improve the documentation are welcome. Please see our contributing guidelines for more information.
