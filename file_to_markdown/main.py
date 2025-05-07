# For running with Astral's 'uv':
# uv run this_script_name.py
# The metadata below (PEP 723) tells uv 'inputimeout' is a dependency.
# uv add --script this_script_name.py inputimeout
#
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "inputimeout",
# ]
# ///

import os
import pathlib
import subprocess
import sys
import time

# 'inputimeout' is required for the paste functionality.
# Ensure it's installed: pip install inputimeout OR uv pip install inputimeout
from inputimeout import inputimeout, TimeoutOccurred

SCRATCH_DIR_NAME = "scratch-pad"
INTERMEDIATE_SOURCE_FILE_NAME = "file_to_markdown_source.md"
AIDER_BATCH_FILE_NAME = "run-aider.bat"
# Timeout for waiting for the next line during paste (in seconds)
DEFAULT_LINE_INPUT_TIMEOUT_SECONDS = 2

def get_source_content() -> str:
    """
    Prompts for source content (file path or direct paste).
    Uses standard input() for the first line, then 'inputimeout'
    to detect end of paste via timeout for subsequent lines.
    """
    print("Enter file path OR paste content directly (first line then subsequent lines).")
    print(f"(If pasting, subsequent lines finalize if no new line for {DEFAULT_LINE_INPUT_TIMEOUT_SECONDS:.1f}s)")

    initial_user_input = ""
    try:
        # Use standard input() for the first line. No timeout here.
        initial_user_input = input("File path or first line of content: ").strip()
    except KeyboardInterrupt:
        print("\nInput aborted by user.")
        return ""
    except Exception as e: # Catch other rare input issues
        print(f"\nError during initial input: {e}. Try again.")
        return get_source_content() # Recurse

    # If the user just pressed Enter, treat as start of multi-line paste
    if not initial_user_input:
        print("Empty first line. Assuming direct multi-line paste mode...")
        # Fall through to paste handling logic, initial_user_input is empty
    elif initial_user_input: # If some input was provided for the first line
        try:
            input_path = pathlib.Path(initial_user_input)
            if input_path.is_file():
                print(f"Reading from file: {input_path}")
                return input_path.read_text(encoding="utf-8")
            elif input_path.exists():
                print(f"Error: '{initial_user_input}' is a directory. Provide a file path or paste content.")
                # Treat as first line of paste if user continues
        except OSError as e:
            # This means initial_user_input was not a valid path string (e.g., bad chars)
            # or some other OS error occurred trying to treat it as a path.
            # Assume it's the first line of pasted content.
            print(f"Not a valid file path ('{initial_user_input}', OS error: {e}). Treating as pasted content.")
        # If initial_user_input was not a successfully read file, it's the first line of paste.

    # --- Paste Handling Logic for subsequent lines ---
    # This part is reached if:
    # 1. User pressed Enter on the first prompt (initial_user_input is empty).
    # 2. User typed something that wasn't a valid, readable file path.
    
    print("Paste mode active for subsequent lines. (End paste by pausing input)")
    lines = []
    # Add initial_user_input if it was provided and was not a processed file path
    # and it's not an empty string from just pressing Enter.
    if initial_user_input and not (pathlib.Path(initial_user_input).is_file() and pathlib.Path(initial_user_input).exists()):
        lines.append(initial_user_input)

    line_number = len(lines) # Start line_number based on whether initial_user_input was added
    
    while True:
        try:
            # Only prompt if it's truly the start of multi-line paste after an empty first line,
            # or for lines after the first pasted line.
            prompt_char = "> " if line_number == 0 else ".. "
            line = inputimeout(prompt=prompt_char, timeout=DEFAULT_LINE_INPUT_TIMEOUT_SECONDS)
            lines.append(line)
            line_number += 1
        except TimeoutOccurred:
            # If lines is empty here, it means user provided a non-file first line,
            # then immediately timed out waiting for the second line.
            # Or user pressed Enter for first line, then timed out on the "> " prompt.
            if not lines and not initial_user_input.strip(): # Check if initial_user_input was also effectively empty
                 print("\nNo input received during paste.")
            else:
                 print(f"\n--- Input finalized (paused >{DEFAULT_LINE_INPUT_TIMEOUT_SECONDS:.1f}s) ---")
            break
        except EOFError:
            print("\n--- Input stream ended (EOF) ---")
            break
        except KeyboardInterrupt:
            print("\nInput aborted during paste.")
            return ""
        except Exception as e:
            print(f"\nError during input: {e}. Finalizing input.")
            break

    pasted_content = "\n".join(lines)
    if not pasted_content.strip():
        print("No content provided.")
        return ""
    return pasted_content

def prepare_intermediate_source_file(content: str) -> pathlib.Path:
    """Saves content to a temporary file in the scratch directory."""
    current_dir = pathlib.Path.cwd()
    scratch_dir = current_dir / SCRATCH_DIR_NAME
    scratch_dir.mkdir(parents=True, exist_ok=True)
    intermediate_file_path = scratch_dir / INTERMEDIATE_SOURCE_FILE_NAME
    intermediate_file_path.write_text(content, encoding="utf-8")
    print(f"Source content written to: {intermediate_file_path}")
    return intermediate_file_path

def get_output_file_path() -> pathlib.Path:
    """Prompts for and validates the output markdown file path."""
    while True:
        try:
            user_input = input("Specify path for output markdown file (e.g., output/my_doc.md):\n").strip()
            if not user_input:
                print("Output file path cannot be empty.")
                continue
            output_path = pathlib.Path(user_input)
            if output_path.suffix.lower() != ".md":
                output_path = output_path.with_suffix(".md")
                print(f"Appending .md extension. Output: {output_path}")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            return output_path
        except KeyboardInterrupt:
            print("\nOutput path specification aborted.")
            raise
        except Exception as e:
            print(f"Error with output path '{user_input}': {e}. Try a valid path.")

def main():
    """Main script logic."""
    print("--- Starting File to Markdown Conversion Setup ---")
    try:
        source_content = get_source_content()
        if not source_content.strip():
            print("No source content. Exiting.")
            return

        intermediate_file = prepare_intermediate_source_file(source_content)
        output_file = get_output_file_path()

    except KeyboardInterrupt:
        print("\nOperation cancelled during setup. Exiting.")
        return
    except Exception as e:
        print(f"Error during setup: {e}. Exiting.")
        return

    print(f"\n--- Setup Complete ---\nIntermediate: {intermediate_file}\nOutput: {output_file}")
    print("\n--- Processing with Aider via Batch File ---")

    aider_prompt = (
        "Please convert the entire content of this file into well-formatted markdown. "
        "Replace the existing content of this file with *only* the generated markdown. "
        "Do not add any conversational text, commentary, introductions, or summaries."
    )

    batch_file_path_str = AIDER_BATCH_FILE_NAME
    # Check if batch file is in Current Working Directory, if not, it must be in PATH
    if not (pathlib.Path.cwd() / AIDER_BATCH_FILE_NAME).is_file():
        print(f"Info: '{AIDER_BATCH_FILE_NAME}' not in CWD. Assuming it's in PATH.")
    else:
        batch_file_path_str = str(pathlib.Path.cwd() / AIDER_BATCH_FILE_NAME)


    batch_command = [batch_file_path_str, str(intermediate_file), aider_prompt]

    print(f"Running command: {batch_command}")
    try:
        process = subprocess.run(
            batch_command,
            capture_output=True,
            text=True,
            check=True, # Raises CalledProcessError for non-zero exit codes
            encoding="utf-8",
            shell=False
        )
        print("Batch file executed successfully.")
        # print(f"Aider stdout:\n{process.stdout}") # Uncomment for Aider's direct output
        # if process.stderr.strip(): print(f"Aider stderr:\n{process.stderr}")


        print(f"Aider processed '{intermediate_file}'.")
        markdown_content = intermediate_file.read_text(encoding="utf-8")
        output_file.write_text(markdown_content, encoding="utf-8")
        
        print(f"\nMarkdown content written to: {output_file}")
        print("--- Conversion Complete ---")

    except subprocess.CalledProcessError as e:
        print(f"\nBatch file failed (exit code {e.returncode}). Command: {e.cmd}")
        print(f"Stdout:\n{e.stdout if e.stdout else '[No standard output]'}")
        print(f"Stderr:\n{e.stderr if e.stderr else '[No standard error]'}")
        print(f"\nIntermediate file '{intermediate_file}' might contain partial results.")
    except FileNotFoundError:
        print(f"\nError: Command '{batch_command[0]}' not found. Ensure '{AIDER_BATCH_FILE_NAME}' is in CWD or PATH.")
    except KeyboardInterrupt:
        print("\nOperation cancelled during Aider processing.")
    except Exception as e:
        print(f"\nUnexpected error during batch processing: {e}")

if __name__ == "__main__":
    # Ensure inputimeout is available (it's imported at the top without try-except)
    # If it's missing, the script would have failed at import time.
    main()
