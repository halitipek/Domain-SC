# Test Case Guide for Domain-SC

This guide explains how to test the Domain-SC system with real-world test cases.

## Directory Structure

- `data/test_cases/`: Place your test case files here
- `data/output/`: The system will save outputs here

## How to Add Test Cases

1. Create a new directory in `data/test_cases/` for your test case:

```bash
mkdir -p data/test_cases/test_case_1
```

2. Add your input files to the test case directory:

**Example files:**
- Requirements documents (.md, .txt)
- API specifications (.json)
- Technology specifications (.md)
- Any other relevant documentation

## Running a Test Case

Use the `run_test_case.py` script to process a test case:

```bash
python run_test_case.py data/test_cases/test_case_1
```

This will:
1. Process all files in the test case directory
2. Index them in the RAG system
3. Initialize a workflow
4. Test a basic query
5. Save all outputs to a timestamped directory in `data/output/`

### Additional Options

- Enable debug mode for more detailed logging:
  ```bash
  python run_test_case.py data/test_cases/test_case_1 --debug
  ```

- Specify a custom output directory:
  ```bash
  python run_test_case.py data/test_cases/test_case_1 --output-dir ./my_results
  ```

## Test Case Examples

### Basic System Design Document Test

Create a test case with basic architectural requirements:

1. Create the test case directory:
   ```bash
   mkdir -p data/test_cases/architecture_design_1
   ```

2. Create a requirements file:
   ```bash
   # In data/test_cases/architecture_design_1/requirements.md
   # System Requirements
   
   ## Functional Requirements
   - User authentication system
   - Product catalog management
   - Order processing system
   - Payment processing integration
   
   ## Non-Functional Requirements
   - High availability (99.9% uptime)
   - Response time < 500ms for all API calls
   - Support for 10,000 concurrent users
   ```

3. Create a technology constraints file:
   ```bash
   # In data/test_cases/architecture_design_1/tech_constraints.md
   # Technology Constraints
   
   ## Approved Technologies
   - Backend: Python, Django/Flask
   - Frontend: React
   - Database: PostgreSQL
   - Infrastructure: AWS
   
   ## Integration Requirements
   - Must integrate with Stripe for payments
   - Must support OAuth 2.0 for authentication
   ```

4. Run the test case:
   ```bash
   python run_test_case.py data/test_cases/architecture_design_1
   ```

## Analyzing Results

Results are saved in the output directory and include:
- Metadata about processed documents
- RAG indexing results
- Query test results
- Generated architecture documents

## Debugging

When using the `--debug` flag, the system will produce more detailed logs. You can find these logs in:
- `logs/test_case_runner.log`
- Other component-specific logs in the `logs/` directory