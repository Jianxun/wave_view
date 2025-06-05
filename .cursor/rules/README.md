# Cursor Rules System

This directory contains a set of MDC-formatted rules that provide consistent guidance for the AI assistant when working with this project.

## Rules Overview

- **project-setup.mdc**: Guidelines for initializing and structuring Python projects - request when setting up new projects or discussing project structure
- **context-management.mdc**: Comprehensive guidelines for maintaining project continuity between chat sessions - applied to all conversations
- **development-guidelines.mdc**: Python development workflow with test-driven development and multi-session continuity - reference when planning tasks, writing tests, or implementing features
- **tools.mdc**: Documentation for utility tools including LLM API, web scraping, search, and screenshot capabilities - reference when needing specialized tool functionality
- **lessons.mdc**: A growing collection of project-specific lessons learned that should be referenced and updated throughout development

## When to Use Each Rule

- **Always-Applied Rules**: 
  - `context-management.mdc`: Critical for maintaining project state across sessions

- **Agent-Requested Rules**:
  - `project-setup.mdc`: When initializing or discussing project structure
  - `development-guidelines.mdc`: When implementing features or performing development tasks
  - `tools.mdc`: When needing specialized tools for development
  - `lessons.mdc`: When seeking best practices or adding new lessons from experience

## How These Rules Work

Each rule file is written in MDC format with metadata at the top and content below. The rules are applied based on:

1. **Metadata Structure**:
   ```
   ---
   description: Concise description of the rule's purpose and when to use it
   globs: [Optional] File patterns that trigger the rule
   alwaysApply: true/false (whether rule is always included)
   ---
   ```

2. **Application Method**:
   - **alwaysApply: true**: Rule content is always included in AI context
   - **alwaysApply: false**: Rule is available on request or when triggered by matching files
   - **globs**: File patterns (e.g., "*.py") that automatically include the rule when matching files are referenced

## Maintaining Rules

- Keep rule descriptions clear and concise in the metadata section
- Include explicit guidelines for when AI agents should reference the rule
- Organize content with clear headings and examples
- Update rules when project practices evolve
- Document any significant changes to rules in `context/memory.md`

## Adding New Rules

To add a new rule:
1. Create a new `.mdc` file in this directory
2. Add appropriate metadata at the top (description, globs, alwaysApply)
3. Include a section explaining when AI agents should use this rule
4. Organize content with clear headings and examples
5. Update this README.md to include the new rule
6. Commit the rule to the repository
