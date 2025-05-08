## File(s) to Edit

* `<file_or_directory1> [<file_or_directory2> ...]`

  * Specify one or more files or directories to add to the chat session. Aider can create new files if they don't exist.

## Main Model & API Keys

* `--model MODEL` (Env: `AIDER_MODEL`)

  * Specify the main model to use (e.g., `gpt-4o`, `claude-3-opus-20240229`).
* `--openai-api-key VALUE` (Env: `AIDER_OPENAI_API_KEY`)

  * Your OpenAI API key.
* `--anthropic-api-key VALUE` (Env: `AIDER_ANTHROPIC_API_KEY`)

  * Your Anthropic API key.
* `--api-key provider=KEY_VALUE` (Env: `AIDER_API_KEY`)

  * Set an API key for a specific provider (e.g., `deepseek=YOUR_DEEPSEEK_KEY`). Can be used multiple times.
* `--openai-api-base VALUE` (Env: `AIDER_OPENAI_API_BASE`)

  * Custom base URL for OpenAI-compatible APIs.
* `--openai-api-type VALUE` (Env: `AIDER_OPENAI_API_TYPE`)

  * OpenAI API type (e.g., `azure`).
* `--openai-api-version VALUE` (Env: `AIDER_OPENAI_API_VERSION`)

  * OpenAI API version, for Azure.
* `--openai-api-deployment-id VALUE` (Env: `AIDER_OPENAI_API_DEPLOYMENT_ID`)

  * OpenAI deployment ID, for Azure.
* `--openai-organization-id VALUE` (Env: `AIDER_OPENAI_ORGANIZATION_ID`)

  * Your OpenAI organization ID.
* `--list-models [MODEL_PATTERN]` or `--models [MODEL_PATTERN]` (Env: `AIDER_LIST_MODELS`)

  * List known models, optionally matching a pattern.
* `--model-settings-file FILE_PATH` (Env: `AIDER_MODEL_SETTINGS_FILE`)

  * Specify a YAML file with settings for unknown models (default: `.aider.model.settings.yml`).
* `--model-metadata-file FILE_PATH` (Env: `AIDER_MODEL_METADATA_FILE`)

  * Specify a JSON file with context window and costs for unknown models (default: `.aider.model.metadata.json`).
* `--alias ALIAS_NAME:MODEL_NAME` (Env: `AIDER_ALIAS`)

  * Add a model alias (e.g., `mygpt4:gpt-4-turbo`). Can be used multiple times.
* `--reasoning-effort VALUE` (Env: `AIDER_REASONING_EFFORT`)

  * Set the `reasoning_effort` API parameter for models that support it.
* `--thinking-tokens VALUE` (Env: `AIDER_THINKING_TOKENS`)

  * Set the thinking token budget for models that support it (e.g., `8k`, `16384`).

## Chat & Interaction

* `--message COMMAND`, `--msg COMMAND`, `-m COMMAND` (Env: `AIDER_MESSAGE`)

  * Specify a single message to send to the LLM, process the reply, and then exit (disables interactive chat mode).
* `--message-file MESSAGE_FILE`, `-f MESSAGE_FILE` (Env: `AIDER_MESSAGE_FILE`)

  * Specify a file containing the message to send.
* `--yes`, `-y` (Env: `AIDER_YES`)

  * Automatically say "yes" to all confirmation prompts.
* `--multiline` / `--no-multiline` (Env: `AIDER_MULTILINE`)

  * Enable/disable multiline input mode (swaps Enter and Meta-Enter behavior). Default is `False`.
* `--stream` / `--no-stream` (Env: `AIDER_STREAM`)

  * Enable/disable streaming responses. Default is `True`.
* `--user-input-color COLOR` (Env: `AIDER_USER_INPUT_COLOR`)

  * Color for user input.
* `--assistant-output-color COLOR` (Env: `AIDER_ASSISTANT_OUTPUT_COLOR`)

  * Color for assistant output.
* `--tool-output-color COLOR` (Env: `AIDER_TOOL_OUTPUT_COLOR`)

  * Color for tool output.
* `--tool-error-color COLOR` (Env: `AIDER_TOOL_ERROR_COLOR`)

  * Color for tool error output.
* `--speech-output` / `--no-speech-output` (Env: `AIDER_SPEECH_OUTPUT`)

  * Enable/disable speech output (text-to-speech). Default is `False`.
* `--speech-language LANG_CODE` (Env: `AIDER_SPEECH_LANGUAGE`)

  * Language for speech output (e.g., `en`).
* `--dark-mode` / `--no-dark-mode` (Env: `AIDER_DARK_MODE`)

  * Enable/disable dark mode for syntax highlighting. Default is `False`.
* `--light-mode` / `--no-light-mode` (Env: `AIDER_LIGHT_MODE`)

  * Enable/disable light mode. Default is `False`.
* `--pretty` / `--no-pretty` (Env: `AIDER_PRETTY`)

  * Enable/disable pretty printing of LLM responses. Default is `True`.
* `--show-diffs` / `--no-show-diffs` (Env: `AIDER_SHOW_DIFFS`)

  * Show diffs before applying changes. Default is `True`.
* `--show-commands` / `--no-show-commands` (Env: `AIDER_SHOW_COMMANDS`)

  * Show the commands being sent to the LLM. Default is `False`.
* `--show-repo-map` / `--no-show-repo-map` (Env: `AIDER_SHOW_REPO_MAP`)

  * Show the repo map if it's sent to the LLM. Default is `False`.
* `--input-history-file FILE_PATH` (Env: `AIDER_INPUT_HISTORY_FILE`)

  * File to store input history (default: `~/.aider.input.history`).
* `--chat-history-file FILE_PATH` (Env: `AIDER_CHAT_HISTORY_FILE`)

  * File to store chat history (default: `.aider.chat.history.md`).
* `--restore-chat-history` / `--no-restore-chat-history` (Env: `AIDER_RESTORE_CHAT_HISTORY`)

  * Restore chat history from the history file on startup. Default is `False`.
* `--llm-history-file FILE_PATH` (Env: `AIDER_LLM_HISTORY_FILE`)

  * File to log all LLM prompt/response messages (default: `.aider.llm.history.json`).

## Editing & Code Context

* `--edit-format EDIT_FORMAT_NAME` (Env: `AIDER_EDIT_FORMAT`)

  * Specify the edit format to use (e.g., `diff`, `whole`, `search_replace`).
* `--repo-map-tokens VALUE` (Env: `AIDER_REPO_MAP_TOKENS`)

  * Max tokens to use for the repository map (default: 1024).
* `--map-refresh VALUE` (Env: `AIDER_MAP_REFRESH`)

  * Force refresh of repo map if older than VALUE seconds.
* `--map-tokens VALUE` (Alias for `--repo-map-tokens`)
* `--map-multiplier-no-files VALUE` (Env: `AIDER_MAP_MULTIPLIER_NO_FILES`)

  * Multiplier for repo map tokens when no files are in chat (default: 4).
* `--read-only-files GLOB_PATTERN` (Env: `AIDER_READ_ONLY_FILES`)

  * Specify files to be read-only using a glob pattern. Can be used multiple times.
* `--allowed-edits-glob GLOB_PATTERN` (Env: `AIDER_ALLOWED_EDITS_GLOB`)

  * Only allow edits to files matching this glob. Can be used multiple times.
* `--disallowed-edits-glob GLOB_PATTERN` (Env: `AIDER_DISALLOWED_EDITS_GLOB`)

  * Disallow edits to files matching this glob. Can be used multiple times.
* `--watch-files` / `--no-watch-files` (Env: `AIDER_WATCH_FILES`)

  * Watch files for "AI" comments and respond. Default is `False`.

## Architect & Editor Model

* `--architect` / `--no-architect` (Env: `AIDER_ARCHITECT`)

  * Use architect/editor mode with two different models.
* `--editor-model MODEL_NAME` (Env: `AIDER_EDITOR_MODEL`)

  * Specify the model for the editor role in architect mode.
* `--auto-accept-architect` / `--no-auto-accept-architect` (Env: `AIDER_AUTO_ACCEPT_ARCHITECT`)

  * Automatically accept changes proposed by the architect model. Default is `True`.

## Other Settings

### Configuration

* `--config FILE_PATH`, `-c FILE_PATH`: Specify a YAML configuration file.
* `--env-file FILE_PATH`: Load environment variables from this file.
* `--set-env VAR=VALUE`: Set an environment variable for the aider session.

### SSL and Warnings

* `--verify-ssl` / `--no-verify-ssl` (Env: `AIDER_VERIFY_SSL`): Verify SSL certs when connecting to models. Default is `True`.
* `--show-model-warnings` / `--no-show-model-warnings` (Env: `AIDER_SHOW_MODEL_WARNINGS`): Show warnings about model capabilities. Default is `True`.
* `--check-model-accepts-settings` / `--no-check-model-accepts-settings` (Env: `AIDER_CHECK_MODEL_ACCEPTS_SETTINGS`): Check if the model likely supports provided settings. Default is `True`.

### Output and Instructions

* `--verbose`, `-v`: Enable verbose output.
* `--show-instructions` / `--no-show-instructions` (Env: `AIDER_SHOW_INSTRUCTIONS`): Show system prompts/instructions sent to the LLM. Default is `False`.

### Execution Control

* `--dry-run` / `--no-dry-run` (Env: `AIDER_DRY_RUN`): Run without making any changes. Default is `False`.
* `--apply FILE_PATH`: Apply a diff file to the current git repo.
* `--cwd DIRECTORY`: Set the current working directory.

### Versioning and Updates

* `--version`: Show aider version and exit.
* `--help`, `-h`: Show this help message and exit.
* `--check-update` (Env: `AIDER_CHECK_UPDATE`): Check for updates on startup.
* `--just-check-update`: Check for updates and exit.
* `--show-release-notes`: Show release notes for the latest version.
* `--upgrade`: Upgrade to the latest version of aider.
* `--install-main-branch`: Install the latest version from the main branch on GitHub.

### Analytics

* `--analytics` / `--analytics-disable` (Env: `AIDER_ANALYTICS`): Enable/disable anonymous analytics.
* `--analytics-log FILE_PATH` (Env: `AIDER_ANALYTICS_LOG_FILE`): Log analytics events to this file.
