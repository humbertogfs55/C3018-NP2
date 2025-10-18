# C3018-NP2

___

## Development Setup

### 1. Create a virtual environment

```bash

python -m venv .venv

```

### 2. Activate venv

```bash linux
source .venv/bin/activate
```

```cmd windows
.venv\Scripts\activate
```

```powershell windows
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

1. install pip tools

    ```bash
    pip install pip-tools
    ```

2. compile and install dependencies

    ```bash
    pip-compile requirements.in
    pip install -r requirements.txt
    ```
