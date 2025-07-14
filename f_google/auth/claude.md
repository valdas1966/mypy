# Google Authentication Module

## Overview
This module provides static authentication utilities for Google services using service account credentials. It handles the authentication flow for multiple Google service accounts through environment variables and provides a clean factory pattern for credential management.

## Architecture

### Core Components

#### `main.py` - Auth Class
- **Purpose**: Main authentication handler with static methods
- **Key Method**: `get_creds(account: ServiceAccount) -> Credentials`
- **Functionality**: 
  - Loads service account credentials from JSON files
  - Applies required Google API scopes
  - Returns authenticated `Credentials` object

#### `_enums.py` - ServiceAccount Enum
- **Purpose**: Defines available service accounts
- **Values**: 
  - `RAMI`: Maps to `RAMI_JSON_PATH` environment variable
  - `VALDAS`: Maps to `VALDAS_JSON_PATH` environment variable
- **Usage**: Type-safe account selection for authentication

#### `_factory.py` - Factory Class
- **Purpose**: Convenience factory methods for common authentication patterns
- **Methods**:
  - `rami() -> Credentials`: Quick access to RAMI credentials
  - `valdas() -> Credentials`: Quick access to VALDAS credentials

#### `_tester.py` - Testing Functions
- **Purpose**: Validation tests for authentication functionality
- **Tests**: Verifies correct project IDs for each service account

## Environment Variables

### Required Setup
```bash
# For RAMI service account
export RAMI_JSON_PATH="/path/to/rami-service-account.json"

# For VALDAS service account  
export VALDAS_JSON_PATH="/path/to/valdas-service-account.json"
```

### Project Mappings
- **RAMI**: `noteret` project
- **VALDAS**: `natural-nimbus-291415` project

## Usage Examples

### Basic Authentication

```python
from f_google.auth import Auth, ServiceAccount

# Get credentials for specific account
creds = Auth.get_creds(ServiceAccount.RAMI)
```

### Using Factory Pattern

```python
from f_google.auth import Auth

# Quick access to RAMI credentials
creds = Auth.Factory.rami()

# Quick access to VALDAS credentials
creds = Auth.Factory.valdas()
```

### Type Safety

```python
from f_google.auth import Auth, ServiceAccount

# Type-safe account selection
account = ServiceAccount.VALDAS
creds = Auth.get_creds(account)
```

## Google API Scopes

The module automatically applies these scopes to all credentials:
- `https://www.googleapis.com/auth/cloud-platform`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/presentations`

## Dependencies

- `google.oauth2.service_account`: Google's official OAuth2 library
- `os.environ`: Environment variable access

## Error Handling

### Common Issues
1. **Missing Environment Variables**: Ensure `{ACCOUNT}_JSON_PATH` variables are set
2. **Invalid JSON Files**: Verify service account JSON files are valid and accessible
3. **Incorrect Permissions**: Ensure service account has required permissions for target APIs

### Troubleshooting
```python
# Check if environment variable exists
import os
if 'RAMI_JSON_PATH' not in os.environ:
    raise ValueError("RAMI_JSON_PATH environment variable not set")

# Verify file exists
json_path = os.environ['RAMI_JSON_PATH']
if not os.path.exists(json_path):
    raise FileNotFoundError(f"Service account file not found: {json_path}")
```

## Testing

Run the authentication tests:

```python
from f_google.auth._tester import test_rami, test_valdas

test_rami()  # Verifies RAMI -> noteret project
test_valdas()  # Verifies VALDAS -> natural-nimbus-291415 project
```

## Extension Guidelines

### Adding New Service Accounts
1. **Add to Enum**: Add new account to `ServiceAccount` enum in `_enums.py`
2. **Environment Variable**: Follow pattern `{ACCOUNT_NAME}_JSON_PATH`
3. **Factory Method**: Add convenience method in `_factory.py`
4. **Test**: Add validation test in `_tester.py`

### Example Extension
```python
# _enums.py
class ServiceAccount(Enum):
    RAMI = 'RAMI'
    VALDAS = 'VALDAS'
    NEW_ACCOUNT = 'NEW_ACCOUNT'  # Add new account

# _factory.py
@staticmethod
def new_account() -> Credentials:
    account = ServiceAccount.NEW_ACCOUNT
    return Auth.get_creds(account)

# _tester.py
def test_new_account() -> None:
    creds = Auth.Factory.new_account()
    assert creds.project_id == 'expected-project-id'
```

## Design Decisions

### Why Static Methods?
- **Stateless**: Authentication doesn't require instance state
- **Global Access**: Credentials needed throughout the application
- **Simplicity**: Reduces object creation overhead

### Why Enum for Service Accounts?
- **Type Safety**: Prevents typos in account names
- **Extensibility**: Easy to add new accounts
- **Consistency**: Enforces naming conventions

### Why Factory Pattern?
- **Convenience**: Common authentication patterns simplified
- **Abstraction**: Hides enum details from consumers
- **Testability**: Easy to mock specific accounts

## Security Considerations

1. **Environment Variables**: Keep JSON paths secure, never commit to version control
2. **Credential Storage**: Store service account JSON files securely
3. **Scope Limitation**: Only grants necessary API permissions
4. **Access Control**: Limit who can modify service account configurations

## Integration with Other Modules

This authentication module is designed to be imported by other Google service modules:
- BigQuery clients
- Google Sheets clients
- Google Storage clients
- Google Slides clients

All should use this centralized authentication approach for consistency and maintainability.