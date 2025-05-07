import os
import pathlib
import subprocess
import sys
import time # Kept for potential future use, though not critical now

SCRATCH_DIR_NAME = "scratch-pad"
INTERMEDIATE_SOURCE_FILE_NAME = "file_to_markdown_source.md"
AIDER_BATCH_FILE_NAME = "run-aider.bat"

def get_source_content() -> str:
    """
    Prompts the user for the full path to a source file.
    Ensures the file exists and reads its content.
    Returns the content as a string, or an empty string if aborted.
    """
    while True:
        try:
            user_input = input("Please enter the full path to your source file: ").strip()
            if not user_input:
                print("File path cannot be empty. Please try again or Ctrl+C to exit.")
                continue

            input_path = pathlib.Path(user_input)

            if input_path.is_file():
                print(f"Reading content from file: {input_path}")
                return input_path
            elif input_path.exists():
                print(f"Error: '{input_path}' is a directory, not a file. Please provide a path to a file.")
            else:
                print(f"Error: File not found at '{input_path}'. Please check the path and try again.")
        
        except KeyboardInterrupt:
            print("\nFile input aborted by user.")
            return "" # Return empty to signal abortion
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")
            # Loop again

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
            raise # Propagate to main to exit
        except Exception as e:
            print(f"Error with output path '{user_input}': {e}. Try a valid path.")

def main():
    """Main script logic."""
    print("--- Starting File to Markdown Conversion Setup ---")
    try:
        source_content = get_source_content()
        if not source_content: # Handles empty string from aborted get_source_content
            print("No source file provided. Exiting.")
            return
        intermediate_file = source_content
        # intermediate_file = prepare_intermediate_source_file(source_content)
        output_file = get_output_file_path()

    except KeyboardInterrupt:
        print("\nOperation cancelled during setup. Exiting.")
        return
    except Exception as e: # Catch any other unexpected errors during setup
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
        # Check if it's findable by just its name (i.e., in PATH)
        # A more robust check would involve shutil.which(), but for simplicity:
        if not any(
            os.access(os.path.join(path, AIDER_BATCH_FILE_NAME), os.X_OK)
            for path in os.environ["PATH"].split(os.pathsep)
        ):
             print(f"Error: Batch file '{AIDER_BATCH_FILE_NAME}' not found in CWD or PATH.")
             return
        # If found in PATH, batch_file_path_str remains AIDER_BATCH_FILE_NAME
    else: # Found in CWD
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
            shell=False # Recommended for security with list args
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
    except FileNotFoundError: # This means the batch_command[0] was not found by the OS
        print(f"\nError: Command '{batch_command[0]}' not found. Ensure '{AIDER_BATCH_FILE_NAME}' is in CWD or PATH and executable.")
    except KeyboardInterrupt:
        print("\nOperation cancelled during Aider processing.")
    except Exception as e:
        print(f"\nUnexpected error during batch processing: {e}")

if __name__ == "__main__":
    main()
