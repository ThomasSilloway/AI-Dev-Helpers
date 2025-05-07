import os
import pathlib
import subprocess
import shlex # For safely quoting arguments

# Define the scratch directory and the intermediate source file name
SCRATCH_DIR_NAME = "scratch-pad"
INTERMEDIATE_SOURCE_FILE_NAME = "file_to_markdown_source.md"
AIDER_BATCH_FILE_NAME = "run-aider.bat" # Name of the batch file to run Aider

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
            if input_path.is_file():
                print(f"Reading content from file: {input_path}")
                return input_path.read_text(encoding="utf-8")
            else:
                print("Input is not a valid file path or file does not exist. Interpreting as direct content.")
                return user_input
        except OSError as e:
            print(f"Could not interpret '{user_input}' as a file path due to an OS error: {e}.")
            print("Interpreting input as direct content.")
            return user_input
        except Exception as e:
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
    if not source_content.strip():
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

    # Path to the batch file - assumed to be in the same directory as the Python script
    batch_file_path = pathlib.Path.cwd() / AIDER_BATCH_FILE_NAME

    # Ensure the batch file exists (you'll create this file separately)
    if not batch_file_path.is_file():
        print(f"Error: Batch file '{AIDER_BATCH_FILE_NAME}' not found in the current directory: {pathlib.Path.cwd()}")
        print("Please create this batch file.")
        # Create a placeholder hello_world.bat if run_aider.bat is missing for testing purposes
        hello_world_bat_path = pathlib.Path.cwd() / "hello_world.bat"
        if not hello_world_bat_path.is_file():
             print(f"Also, the 'hello_world.bat' file is missing. You can create it with the content provided separately.")
        return

    # Command to execute the batch file, passing the intermediate file and prompt as arguments
    # We need to quote the arguments in case they contain spaces
    batch_command = [
        str(batch_file_path),
        str(intermediate_file), # Argument %1 for the batch file
        aider_prompt,          # Argument %2 for the batch file
    ]

    print(f"Running batch file: {' '.join(batch_command)}")
    try:
        process = subprocess.run(
            batch_command,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
            shell=False # Important for security and proper argument handling with shlex
        )
        
        print(f"Batch file executed successfully.")
        # Optional: Log batch file's output for debugging
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
        print(f"Command: {' '.join(e.cmd)}")
        print("Batch file standard output:")
        print(e.stdout if e.stdout else "[No standard output]")
        print("Batch file standard error:")
        print(e.stderr if e.stderr else "[No standard error]")
        print("\nExiting due to batch file processing error.")
        print(f"The intermediate file '{intermediate_file}' might contain partial results or error messages.")
    except FileNotFoundError:
        # This error would now typically mean the batch file itself wasn't found,
        # though we added a check for it earlier.
        print(f"\nError: The batch file '{batch_file_path}' was not found or another command within it was not found.")
        print("Please ensure the batch file exists and Aider is accessible from the command line.")
        print("Exiting.")
    except Exception as e:
        print(f"\nAn unexpected error occurred during batch file processing or file operations: {e}")
        print("Exiting.")

if __name__ == "__main__":
    main()
