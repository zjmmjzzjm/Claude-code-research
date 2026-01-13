# Claude Code Research & Tools

This repository is a comprehensive research project dedicated to analyzing **Claude Code**, its "Superpowers" skill library, and AI-assisted software development methodologies. It also contains practical utility tools, such as a Twitter data collector.

## Project Overview

This workspace serves two primary purposes:
1.  **Research Hub:** In-depth analysis, documentation, and notes on using Claude Code, focusing on advanced workflows like TDD, systematic debugging, and sub-agent collaboration.
2.  **Tooling:** A collection of Python-based utilities, currently featuring a robust Twitter data scraper.

## 🛠️ Tool: Twitter Collector

A Python script (`twitter_collector.py`) to harvest tweets and user data using `twscrape`.

### Setup
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements-twitter.txt
    ```
    *Note: Requires `twscrape`.*

2.  **Initialize `twscrape`:**
    You must add accounts to the `twscrape` pool before using the script.
    ```bash
    twscrape add_accounts
    ```

### Usage
Run the collector via the command line:

```bash
# Collect tweets from a single user
python twitter_collector.py @username -n 100

# Collect tweets from users followed by a specific account
python twitter_collector.py @username --following --max-users 20

# Save output in a specific format (json, markdown, csv, or all)
python twitter_collector.py @username --format csv
```

**Key Features:**
*   **User Info & Tweets:** Scrapes detailed user profiles and their timeline.
*   **Following Network:** Can crawl users followed by a target account.
*   **Multiple Formats:** Exports data to JSON (programmatic), Markdown (readable), and CSV (spreadsheet).
*   **Resilience:** Includes login handling and rate-limiting pauses.

## 📚 Research: Claude Code & Superpowers

The `docs/` and `notes/` directories contain extensive research on maximizing AI coding agents.

### Core Philosophies
*   **Progressive Disclosure:** AI should request info only as needed to save context window and improve focus.
*   **Systematization > Ad-hoc:** Development should follow strict workflows (Brainstorm -> Plan -> Execute) rather than random prompting.
*   **Evidence > Claims:** "It works" is insufficient; verification (tests, logs) is required.
*   **Sub-agent Driven Development:** Decomposing complex tasks into sub-tasks handled by specialized sub-agents with dual-phase review (Spec Compliance + Code Quality).

### Key Workflows (Superpowers)
This repo studies the "Superpowers" library for Claude Code. Key skills include:

| Skill | Description | Command |
| :--- | :--- | :--- |
| **Brainstorming** | Socratic questioning to refine requirements before coding. | `/superpowers:brainstorm` |
| **Git Worktrees** | Creating isolated environments for parallel task execution. | `/superpowers:using-git-worktrees` |
| **Writing Plans** | Generating detailed, atomic step-by-step implementation plans. | `/superpowers:write-plan` |
| **TDD** | Enforcing a Red-Green-Refactor cycle (deletes code written without tests). | `/superpowers:test-driven-development` |
| **Systematic Debugging** | A 4-stage process: Identification -> Hypothesis -> Testing -> Solution. | `/superpowers:systematic-debugging` |

### Directory Structure

*   `docs/`: Formal documentation on principles and best practices.
    *   `principles/`: Deep dives into architecture and core concepts.
    *   `best-practices/`: Guides on workflows (e.g., automated debugging).
*   `notes/`: Personal learning notes, summaries, and feasibility analyses.
    *   `claude-code-实用经验总结.md`: Practical summary of daily usage experiences.
*   `experiments/`: Sandboxed area for testing new AI coding features or prompts.
*   `resources/`: External references and crawled documentation (e.g., `skills-deeptoai-docs`).

## 🚀 Getting Started

1.  **Explore the Notes:** Start with `notes/claude-code-实用经验总结.md` for a high-level overview of effective AI coding patterns.
2.  **Use the Tools:** Check `twitter_collector.py` for data gathering needs.
3.  **Read the Research:** Dive into `docs/principles/` to understand the theoretical underpinnings of the "Superpowers" framework.
