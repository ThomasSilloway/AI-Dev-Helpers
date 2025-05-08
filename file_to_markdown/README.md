# AI Dev Helpers

This repository contains scripts to assist with AI-related development tasks. The primary tool helps automate the conversion of file content to Markdown format using the Aider CLI.

## Markdown Conversion Script (`main.py`)

### Purpose

The `main.py` script automates the conversion of a specified source file's content into Markdown. It utilizes the Aider AI tool, invoked via the included `run-aider.bat` helper batch script.

### Prerequisites

1.  **Python 3.x:** Ensure Python 3 is installed on your system.
2.  **Aider CLI:** The [Aider command-line tool](https://aider.chat/docs/install.html) must be installed and accessible in your system's PATH.
3.  **Repository Files:** You'll need `main.py` and `run-aider.bat` from this repository.

### Setup

1.  Clone this repository or download `main.py` and `run-aider.bat` into the same directory.
    ```bash
    git clone [https://github.com/ThomasSilloway/AI-Dev-Helpers.git](https://github.com/ThomasSilloway/AI-Dev-Helpers.git)
    cd AI-Dev-Helpers
    ```
2.  Ensure `run-aider.bat` is executable. (On Windows, batch files are typically executable by default). If Aider is not in your system's PATH, you may need to edit `run-aider.bat` to specify the full path to your `aider` executable.

### Usage

1.  Open your terminal or command prompt.
2.  Navigate to the directory containing `main.py` and `run-aider.bat`.
3.  Run the script:
    ```bash
    python main.py
    ```
4.  **Follow the prompts:**
    * **Source File:** Enter the full path to the source file you want to convert (e.g., `C:\path\to\your\code.py` or `/path/to/your/notes.txt`).
    * **Output File:** Specify the desired path and name for the generated Markdown file (e.g., `output/converted.md`). The script will create parent directories if they don't exist and append `.md` if not specified.

### How It Works

1.  `main.py` prompts for the source and output file paths.
2.  It creates an intermediate copy of the source content in a `scratch-pad` directory.
3.  It calls `run-aider.bat`, passing the intermediate file and a predefined conversion prompt.
4.  `run-aider.bat` executes the `aider` CLI command, which modifies the intermediate file with the Markdown content.
5.  `main.py` copies the content from the modified intermediate file to your specified output file.

### Customization

* **Aider Prompt:** The prompt sent to Aider can be modified within the `aider_prompt` variable in `main.py`.
* **Batch File Name:** If you rename `run-aider.bat`, update the `AIDER_BATCH_FILE_NAME` variable in `main.py`.

---

*This README focuses on the primary functionality. If other scripts are added or purposes evolve, this document should be updated.*

