import os
import pathlib
import subprocess # Imported as per earlier discussion, though not used in this specific step

# Define the scratch directory and the intermediate source file name
SCRATCH_DIR_NAME = "scratch-pad"
INTERMEDIATE_SOURCE_FILE_NAME = "file_to_markdown_source.md"

def get_source_content() -> str:
    """
    Prompts the user for source content, either as a file path or direct input.
    Returns the content as a string.
    """
    while True:
        user_input = input(
            "Please enter the full path to your source file, or paste the content directly:\n"
        ).strip()

        if not user_input:
            print("Input cannot be empty. Please provide a file path or paste content.")
            continue

        input_path = pathlib.Path(user_input)

        try:
            # Check if the input string is a path to an existing file
            if input_path.is_file():  # is_file() also checks for existence
                print(f"Reading content from file: {input_path}")
                return input_path.read_text(encoding="utf-8")
            else:
                # If it's not an existing file (or not a file at all),
                # assume the input is the content itself.
                print("Input is not a valid file path or file does not exist. Interpreting as direct content.")
                return user_input
        except OSError as e:
            # This can happen if user_input is a string that's invalid as a path on the OS
            # (e.g., contains null characters, is too long, or other OS-level path errors).
            # In such cases, it's definitely not a file path we can use.
            print(f"Could not interpret '{user_input}' as a file path due to an OS error: {e}.")
            print("Interpreting input as direct content.")
            return user_input
        except Exception as e:
            # Catch other potential errors like permission issues for read_text
            print(f"An error occurred while trying to process '{user_input}' as a file path: {e}.")
            print("Interpreting input as direct content.")
            return user_input

def prepare_intermediate_source_file(content: str) -> pathlib.Path:
    """
    Saves the given content to the intermediate source file in the scratch directory.
    Creates the scratch directory if it doesn't exist.
    Overwrites the file if it already exists.
    Returns the path to the created intermediate file.
    """
    current_dir = pathlib.Path.cwd()
    scratch_dir = current_dir / SCRATCH_DIR_NAME
    
    # Create scratch directory if it doesn't exist
    scratch_dir.mkdir(parents=True, exist_ok=True)
    print(f"Ensured scratch directory exists: {scratch_dir}")

    intermediate_file_path = scratch_dir / INTERMEDIATE_SOURCE_FILE_NAME
    
    # Write content to the intermediate file, overwriting if it exists
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
        
        # Ensure the output path ends with .md
        if output_path.suffix.lower() != ".md":
            output_path = output_path.with_suffix(".md")
            print(f"Appending .md extension. Output file will be: {output_path}")
            
        # Ensure parent directory for the output file exists
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            return output_path
        except Exception as e:
            print(f"Error creating parent directories for '{output_path}': {e}. Please specify a valid path.")
            # Loop again to ask for a valid path

def main():
    """
    Main function to orchestrate the file processing setup.
    """
    print("--- Starting File to Markdown Conversion Setup ---")

    # 1. Get source content from user
    source_content = get_source_content()
    if not source_content.strip(): # Double check, though get_source_content should loop
        print("No source content provided. Exiting.")
        return

    # 2. Prepare and write to the intermediate source file
    intermediate_file = prepare_intermediate_source_file(source_content)

    # 3. Get the desired output file path from the user
    output_file = get_output_file_path()

    print("\n--- Setup Complete ---")
    print(f"Intermediate source file ready at: {intermediate_file}")
    print(f"Final output will be generated at: {output_file}")
    # 4. Process with Aider and save
    print("\n--- Processing with Aider ---")
    aider_prompt = (
        "Please convert the entire content of this file into well-formatted markdown. "
        "Replace the existing content of this file with *only* the generated markdown. "
        "Do not add any conversational text, commentary, introductions, or summaries before or after the markdown content itself."
    )
    aider_command = [
        "aider",
        "--yes",  # Automatically accept changes from Aider
        str(intermediate_file),  # The file Aider should read and modify
        "--message", aider_prompt,  # The instruction for Aider
    ]

    print(f"Running Aider command: {' '.join(aider_command)}")
    try:
        # Run Aider. It is expected to modify intermediate_file in place.
        process = subprocess.run(
            aider_command,
            capture_output=True,  # Capture stdout/stderr
            text=True,            # Decode stdout/stderr as text
            check=True,           # Raise CalledProcessError for non-zero exit codes
            encoding="utf-8",     # Specify encoding for text mode
        )
        
        # Optional: Log Aider's output for debugging, even on success.
        # Useful if Aider's behavior needs to be inspected.
        # if process.stdout.strip():
        #     print(f"Aider stdout:\n{process.stdout}")
        # if process.stderr.strip():
        #     print(f"Aider stderr:\n{process.stderr}")

        print(f"Aider successfully processed '{intermediate_file}'.")

        # Read the markdown content from the (now modified) intermediate file
        markdown_content = intermediate_file.read_text(encoding="utf-8")

        # Write the extracted markdown content to the final output file
        output_file.write_text(markdown_content, encoding="utf-8")
        
        print(f"\nMarkdown content successfully written to: {output_file}")
        print("--- Conversion Complete ---")
        print(f"Final markdown output is available at: {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"\nAider command failed with exit code {e.returncode}.")
        print(f"Command: {' '.join(e.cmd)}")
        print("Aider's standard output:")
        print(e.stdout if e.stdout else "[No standard output]")
        print("Aider's standard error:")
        print(e.stderr if e.stderr else "[No standard error]")
        print("\nExiting due to Aider processing error.")
        print(f"The intermediate file '{intermediate_file}' might contain partial results or Aider's error messages.")
        print("You may want to inspect it or the Aider log files for more details.")
    except FileNotFoundError:
        print("\nError: The 'aider' command was not found.")
        print("Please ensure Aider is installed and accessible in your system's PATH.")
        print("See Aider installation instructions if needed.")
        print("Exiting.")
    except Exception as e:
        print(f"\nAn unexpected error occurred during Aider processing or file operations: {e}")
        print("Exiting.")

if __name__ == "__main__":
    main()
