# Sample Test Projects for Code Analysis

This directory contains sample projects with various code quality issues, security vulnerabilities, and outdated dependencies to test the Gen AI Code Analysis features of the Azure DevOps MCP Agent.

## Projects Overview

### 1. Vulnerable API (`vulnerable_api/`)

A Python FastAPI application with multiple security vulnerabilities including:
- SQL injection vulnerabilities
- Command injection vulnerabilities
- Path traversal issues
- Hardcoded credentials
- Insecure authentication mechanisms
- Missing rate limiting
- Broken access control

**Key files:**
- `app.py` - Main application with security issues
- `requirements.txt` - Dependencies with known vulnerabilities

### 2. Problematic Frontend (`problematic_frontend/`)

A React application with code quality issues and security vulnerabilities:
- XSS vulnerabilities (via dangerouslySetInnerHTML)
- React performance anti-patterns
- Memory leaks
- Hard-coded credentials
- DOM manipulation anti-patterns
- Insecure eval() usage
- Missing dependency arrays in hooks
- Local storage of sensitive information

**Key files:**
- `src/App.js` - Main application with issues
- `package.json` - Outdated dependencies

### 3. Data Pipeline (`data_pipeline/`)

A Python data processing pipeline with multiple issues:
- Inefficient data processing patterns
- SQL injection vulnerabilities
- Command injection vulnerabilities
- Hardcoded credentials
- Memory leaks
- Unsafe deserialization
- Poor error handling
- Improper resource cleanup

**Key files:**
- `data_processor.py` - Main processing script with issues
- `config.py` - Configuration with hardcoded credentials
- `requirements.txt` - Outdated dependencies

### 4. ADF Pipeline (`adf_pipeline/`)

Azure Data Factory pipeline configurations with various issues:
- Hardcoded credentials in linked services
- Insecure connection strings
- SQL injection via raw queries
- Command injection vulnerabilities
- Excessive permissions
- Missing error handling
- Poor security practices

**Key files:**
- `pipeline.json` - Pipeline definition with issues
- `linkedService.json` - Connection definitions with credentials
- `dataset.json` - Dataset definition
- `AzureBlobStorage.json` - Storage connection with issues

## Using These Projects

These projects are designed to be used with the Azure DevOps MCP Agent's code scanning features. You can upload them to Azure DevOps repositories and then use the prompts from `Prompts_v2.md` to test the scanning capabilities.

### Example Usage

```
Scan the vulnerable_api repository for security vulnerabilities.
```

```
Check the problematic_frontend repository for dependency issues and React-specific problems.
```

```
Analyze the data_pipeline repository for code quality issues and inefficient data patterns.
```

```
Perform a security scan on the adf_pipeline repository focusing on credential exposure issues.
```

## Notes

- These samples are deliberately vulnerable and should NOT be used in production environments.
- They contain various security issues for testing purposes only.
- Some issues might be obvious while others are more subtle to test the effectiveness of the scanning tools.
