## 4. Data Models / Structures

This section defines the key data structures, formats, and conventions used for communication between agents, tool interactions, and overall state management within PoC 5.

### Session State (context.state):

Stores JSON strings representing structured outcomes from agents.
State Keys: Defined in `sleepy_ai_agent/constants/constants.py` (e.g., `constants.TASK_PARSING_OUTCOME_KEY`).

### Standard Agent Outcome JSON Structure:

Agents (`TaskParsingAgent`, `FileLocatorAgent`, `GitSetupAgent`, `AiderExecutionAgent`) output a JSON string:

```json
{
  "status": "success" | "failure",
  "message": "Optional: Human-readable message.",
  // Agent-specific result fields, e.g.:
  // For TaskParsingAgent: "target_file_name", "change_description", "branch_slug"
  // For FileLocatorAgent: "target_file_full_path"
  // For GitSetupAgent: "branch_name"
  // For AiderExecutionAgent: "details"
}
```

`TaskParsingAgent` must output `status: "failure"` if essential fields cannot be extracted.

### Standard "Skipped" JSON Structure (set by callbacks):

```json
{
  "status": "skipped",
  "message": "Skipped due to [reason]."
}
```

### Prompt Injection for ReportingAgent:

Uses ADK's `{state_key_from_constants}` syntax to receive prior JSON string outcomes.

### task_description.md (Source of Task Input):

Located in "Goal" folder (path constructed from `constants.DEFAULT_WORKSPACE_PATH` and `constants.DEFAULT_GOAL_FOLDER_NAME`).
Contains a literal string (user's backlog item).
`TaskParsingAgent` uses LLM to parse this string for `target_file_name`, `change_description`, `branch_slug`.

### changelog.md (Output File):

Located in "Goal" folder. Maintained by `ChangelogAgent`.
Format for entries:

```markdown
## <Calling Agent Name from constants.py>
YYYY-MM-DD HH:MM:SS

- <Detail 1 of the action or result.>
- <Detail 2 if applicable.>
```

`ReportingAgent` reads this to check for inconsistencies.

### Tool Input/Output (Custom FunctionTools):

Return Python dictionary: `{"status": "success" | "failure", "result": <data> | "message": <error>}`.

### constants.py File Content:

Defines state output keys, file names (`constants.TASK_DESCRIPTION_FILE`, `constants.CHANGELOG_FILE`), pre-configured paths (`constants.DEFAULT_WORKSPACE_PATH`, `constants.DEFAULT_GOAL_FOLDER_NAME` - relative), agent friendly names, and default LLM model names.
