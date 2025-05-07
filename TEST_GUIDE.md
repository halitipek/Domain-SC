# Domain-SC Testing Guide

This document describes how to run and extend the test suite for the Domain-SC system.

## Running Tests

The test suite can be run using the `run_tests.py` script:

```bash
# Run all tests
python run_tests.py

# Run only unit tests
python run_tests.py --type unit

# Run only integration tests
python run_tests.py --type integration

# Run only functional tests
python run_tests.py --type functional

# Run with verbose output
python run_tests.py --verbose

# Generate a coverage report
python run_tests.py --coverage
```

## Test Structure

The tests are organized into three categories:

### Unit Tests

Unit tests verify the functionality of individual components in isolation. These tests mock dependencies and focus on testing the behavior of a single class or function.

**Location**: `tests/unit/`

Key unit tests:
- `test_document_processor.py`: Tests the document loading and chunking functionality
- `test_prompt_manager.py`: Tests the prompt template management
- `test_base_agent.py`: Tests the core agent functionality

### Integration Tests

Integration tests verify that different components work together correctly. These tests focus on the interactions between components.

**Location**: `tests/integration/`

Key integration tests:
- `test_rag_integration.py`: Tests the complete RAG pipeline
- `test_agent_interaction.py`: Tests interactions between agents

### Functional Tests

Functional tests verify the system's behavior from an external perspective. These tests interact with the system through its public interfaces.

**Location**: `tests/functional/`

Key functional tests:
- `test_cli.py`: Tests the command-line interface

## Writing Tests

### Unit Tests

When writing unit tests, follow these guidelines:

1. Each test should focus on a single functionality
2. Mock external dependencies
3. Use descriptive test names that explain what is being tested
4. Include assertions that verify the expected behavior

Example unit test:

```python
def test_document_loading(self):
    """Test loading a document."""
    # Arrange
    processor = DocumentProcessor()
    test_file = "test.txt"
    
    # Act
    result = processor.load_document(test_file)
    
    # Assert
    self.assertIsNotNone(result)
    self.assertGreater(len(result), 0)
```

### Integration Tests

When writing integration tests, follow these guidelines:

1. Test interactions between components
2. Set up realistic test data
3. Verify that components work together correctly
4. Clean up test resources after tests

Example integration test:

```python
def test_rag_query_pipeline(self):
    """Test the complete RAG pipeline."""
    # Arrange
    rag_service = RagService()
    rag_service.index_documents(["test.txt"])
    
    # Act
    result = rag_service.query("test query")
    
    # Assert
    self.assertIsNotNone(result.answer)
    self.assertGreater(len(result.retrieved_documents), 0)
```

### Functional Tests

When writing functional tests, follow these guidelines:

1. Test from an external perspective
2. Use public interfaces only
3. Test realistic user scenarios
4. Make tests independent of each other

Example functional test:

```python
def test_cli_workflow(self):
    """Test the CLI workflow."""
    # Arrange
    test_file = "test.txt"
    
    # Act
    result = subprocess.run(
        ["python", "cli.py", "workflow", "create", "--name", "test", "--files", test_file],
        capture_output=True, text=True
    )
    
    # Assert
    self.assertEqual(result.returncode, 0)
    self.assertIn("workflow_id", result.stdout)
```

## Coverage Report

To generate a coverage report, run:

```bash
python run_tests.py --coverage
```

This will generate a report showing which parts of the code are covered by tests. The report will be displayed in the console and also saved as an HTML report in the `coverage_html` directory.

To view the HTML report, open `coverage_html/index.html` in a web browser.

## Continuous Integration

The test suite is designed to be run in a CI environment. The tests will skip certain parts that require external dependencies if they are run in a CI environment (detected by the presence of a `CI` environment variable).

## Troubleshooting

If tests are failing, check for these common issues:

1. **Missing Dependencies**: Make sure all required packages are installed
2. **File Permissions**: Ensure the test has permission to create and modify files
3. **Network Issues**: Some tests may require network access
4. **Environment Variables**: Check if required environment variables are set
5. **File System Issues**: Tests that create temporary files may fail if disk space is limited