import os
import pathlib
import subprocess
# shlex is no longer strictly needed here if we're not using shlex.quote for this part

# Define the scratch directory and the intermediate source file name
SCRATCH_DIR_NAME = "scratch-pad"
INTERMEDIATE_SOURCE_FILE_NAME = "file_to_markdown_source.md"
AIDER_BATCH_FILE_NAME = "run-aider.bat" # Name of the batch file to run Aider

def get_source_content() -> str:
    """
    Prompts the user for source content, either as a file path or direct multi-line input.
    For direct input, it reads multiple lines until a specific delimiter is entered.
    Returns the content as a string.
    """
    print("Please enter the full path to your source file, OR paste the content directly.")
    print("If pasting content, type 'END_OF_PASTE' on a new line by itself after your content and press Enter.")
    
    first_line_input = input("File path or first line of pasted content: ").strip()

    # Check if the first line looks like a file path
    try:
        input_path = pathlib.Path(first_line_input)
        if input_path.is_file():
            print(f"Reading content from file: {input_path}")
            return input_path.read_text(encoding="utf-8")
        elif input_path.exists() and not input_path.is_file(): # It's a directory or something else
             print(f"Error: '{first_line_input}' is a directory or not a regular file. Please provide a valid file path or paste content.")
             return get_source_content() # Recurse to try again
    except OSError as e:
        # Not a valid path, likely due to invalid characters for a path.
        # Assume it's the start of direct content input.
        # We'll print this error only if it's not an empty string (which is handled later)
        if first_line_input: # Only print error if it's not just an empty first line for pasting
            print(f"Could not interpret '{first_line_input}' as a file path (OS error: {e}). Treating as direct content.")
        # Proceed to treat as direct content below

    # If it's not a file, assume it's direct content input (or the start of it)
    print("Interpreting as direct content input. Enter your content now.")
    if not first_line_input: # If the first line was empty, prompt again specifically for content
        print("(If you intended to provide a file path, please restart and enter the path first)")

    lines = []
    if first_line_input: # Add the first line if it wasn't a file and wasn't empty
        lines.append(first_line_input)

    while True:
        try:
            line = input() # Read subsequent lines
            if line.strip().upper() == "END_OF_PASTE":
                break
            lines.append(line)
        except EOFError:
            # This might happen if input is redirected and EOF is reached
            print("EOF reached while reading input.")
            break
    
    pasted_content = "\n".join(lines)
    if not pasted_content.strip():
        print("Input cannot be empty. Please provide a file path or paste content.")
        return get_source_content() # Recurse to try again
        
    return pasted_content

def prepare_intermediate_source_file(content: str) -> pathlib.Path:
    """
    Saves the given content to the intermediate source file in the scratch directory.
    Creates the scratch directory if it doesn't exist.
    Overwrites the file if it already exists.
    Returns the path to the created intermediate file.
    """
    current_dir = pathlib.Path.cwd()
    scratch_dir = current_dir / SCRATCH_DIR_NAME
    
    scratch_dir.mkdir(parents=True, exist_ok=True)
    print(f"Ensured scratch directory exists: {scratch_dir}")

    intermediate_file_path = scratch_dir / INTERMEDIATE_SOURCE_FILE_NAME
    
    intermediate_file_path.write_text(content, encoding="utf-8")
    print(f"Source content written to: {intermediate_file_path}")
    return intermediate_file_path

def get_output_file_path() -> pathlib.Path:
    """
    Prompts the user for the output file path and ensures it ends with '.md'.
    Also ensures parent directories for the output file are created.
    Returns the Path object for the output file.
    """
    while True:
        user_input = input("Please specify the path for the output markdown file (e.g., output/my_doc.md):\n").strip()
        if not user_input:
            print("Output file path cannot be empty. Please try again.")
            continue

        output_path = pathlib.Path(user_input)
        
        if output_path.suffix.lower() != ".md":
            output_path = output_path.with_suffix(".md")
            print(f"Appending .md extension. Output file will be: {output_path}")
            
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            return output_path
        except Exception as e:
            print(f"Error creating parent directories for '{output_path}': {e}. Please specify a valid path.")

def main():
    """
    Main function to orchestrate the file processing setup.
    """
    print("--- Starting File to Markdown Conversion Setup ---")

    source_content = get_source_content()
    # The get_source_content function now loops until valid content is provided or a file is read.
    # So, a separate check like `if not source_content.strip():` might be redundant if the function guarantees content.
    # However, keeping it as a safeguard is fine.
    if not source_content: # get_source_content should ideally not return None, but an empty string if all fails after retries.
                           # Or raise an exception. For now, we assume it returns a string.
        print("No source content could be obtained. Exiting.")
        return
    if not source_content.strip() and not pathlib.Path(source_content).is_file(): # Check if it's empty and not a path.
        print("No source content provided. Exiting.")
        return


    intermediate_file = prepare_intermediate_source_file(source_content)
    output_file = get_output_file_path()

    print("\n--- Setup Complete ---")
    print(f"Intermediate source file ready at: {intermediate_file}")
    print(f"Final output will be generated at: {output_file}")
    
    print("\n--- Processing with Aider via Batch File ---")
    aider_prompt = (
        "Please convert the entire content of this file into well-formatted markdown. "
        "Replace the existing content of this file with *only* the generated markdown. "
        "Do not add any conversational text, commentary, introductions, or summaries before or after the markdown content itself."
    )

    batch_file_path = pathlib.Path.cwd() / AIDER_BATCH_FILE_NAME

    if not batch_file_path.is_file():
        print(f"Error: Batch file '{AIDER_BATCH_FILE_NAME}' not found in the current directory: {pathlib.Path.cwd()}")
        print("Please create this batch file with the content provided previously.")
        return

    batch_command = [
        str(batch_file_path),
        str(intermediate_file), 
        aider_prompt,          
    ]

    print(f"Running batch file command: {' '.join(batch_command)}") # For display, join might not reflect exact execution for shell=False
    print(f"Actual command list for subprocess: {batch_command}") # More accurate representation
    try:
        process = subprocess.run(
            batch_command,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
            shell=False 
        )
        
        print(f"Batch file executed successfully.")
        # if process.stdout.strip():
        #     print(f"Batch file stdout:\n{process.stdout}")
        # if process.stderr.strip():
        #     print(f"Batch file stderr:\n{process.stderr}")

        print(f"Aider (via batch) successfully processed '{intermediate_file}'.")

        markdown_content = intermediate_file.read_text(encoding="utf-8")
        output_file.write_text(markdown_content, encoding="utf-8")
        
        print(f"\nMarkdown content successfully written to: {output_file}")
        print("--- Conversion Complete ---")
        print(f"Final markdown output is available at: {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"\nBatch file execution failed with exit code {e.returncode}.")
        print(f"Command: {' '.join(e.cmd)}") # e.cmd should be the list passed to subprocess.run
        print("Batch file standard output:")
        print(e.stdout if e.stdout else "[No standard output]")
        print("Batch file standard error:")
        print(e.stderr if e.stderr else "[No standard error]")
        print("\nExiting due to batch file processing error.")
        print(f"The intermediate file '{intermediate_file}' might contain partial results or error messages.")
    except FileNotFoundError:
        print(f"\nError: The batch file '{batch_file_path}' (or a command within it like 'aider') was not found.")
        print("Please ensure the batch file exists and Aider is installed and accessible in your system's PATH.")
        print("Exiting.")
    except Exception as e:
        print(f"\nAn unexpected error occurred during batch file processing or file operations: {e}")
        print("Exiting.")

if __name__ == "__main__":
    main()
