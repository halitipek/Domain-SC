# Project Tracking Guide

This document outlines how we track progress, manage issues, and coordinate development for Domain-SC.

## Project Management Tools

We use the following tools to track progress:

1. **GitHub Issues**: Primary task tracking
2. **GitHub Projects**: Kanban board for visualization
3. **Roadmap.md**: High-level planning document
4. **Milestones**: Group related issues for releases

## Issue Categories

Issues are categorized with the following labels:

### Type Labels
- `feature`: New functionality
- `bug`: Something isn't working as expected
- `docs`: Documentation-related tasks
- `test`: Testing-related tasks
- `refactor`: Code improvements without changing functionality
- `enhancement`: Improvements to existing features
- `roadmap`: Tasks from the official roadmap
- `tech-debt`: Technical debt that needs to be addressed

### Priority Labels
- `priority:critical`: Must be fixed immediately
- `priority:high`: Should be fixed in the current sprint
- `priority:medium`: Should be addressed soon
- `priority:low`: Nice to have

### Status Labels
- `status:backlog`: Not yet started
- `status:ready`: Ready to be worked on
- `status:in-progress`: Currently being worked on
- `status:review`: Ready for review
- `status:blocked`: Blocked by another issue

## GitHub Projects Structure

We use a GitHub Projects board with the following columns:

1. **Backlog**: Issues that are not yet scheduled
2. **Ready**: Issues that are ready to be worked on
3. **In Progress**: Issues currently being worked on
4. **Review**: Pull requests and issues ready for review
5. **Blocked**: Issues blocked by dependencies
6. **Done**: Completed issues and merged PRs

## Creating New Issues

When creating a new issue:

1. Use one of the issue templates:
   - Bug Report
   - Feature Request
   - Roadmap Task

2. Apply appropriate labels
3. Add to the project board
4. Assign to a milestone if applicable
5. Link to related issues if any

## Tracking Roadmap Progress

Roadmap tasks are tracked as follows:

1. Each roadmap task has a corresponding GitHub issue
2. The issue references the specific section in ROADMAP.md
3. Progress is updated in both the issue and the roadmap document
4. Completed tasks are marked with ✅ in the roadmap

## Prioritization Process

We prioritize issues based on:

1. Strategic importance (alignment with roadmap)
2. User impact (how many users are affected)
3. Implementation complexity (effort required)
4. Dependencies (blocking other important work)

Prioritization decisions are made during planning meetings and documented in meeting notes.

## Release Planning

Releases are planned as follows:

1. Define a milestone with a target date
2. Assign issues to the milestone
3. Track progress on the milestone page
4. Create a release branch when ready
5. Deploy and create a GitHub release with release notes

## Development Workflow

1. **Select an issue**: Choose an issue from the "Ready" column
2. **Move to "In Progress"**: Update the status and assign to yourself
3. **Create a branch**: Use the format `<type>/<issue-number>-<short-description>`
4. **Implement changes**: Make the necessary code changes
5. **Submit a PR**: Reference the issue in the PR description
6. **Review**: Address feedback from code reviews
7. **Merge**: Once approved, merge the PR
8. **Close the issue**: The issue is automatically moved to "Done"

## Progress Reporting

We track and report progress in the following ways:

1. **Daily updates**: Team members update their in-progress issues
2. **Weekly summary**: Posted as a comment on a tracking issue each Friday
3. **Monthly report**: A more comprehensive update on roadmap progress
4. **Release notes**: Detailed notes for each release

## Additional Notes

- All discussions related to an issue should happen in the issue comments
- Major decisions should be documented in comments or linked ADRs
- Use issue references (e.g., #123) to link related issues
- Blocked issues should clearly state what they're blocked by