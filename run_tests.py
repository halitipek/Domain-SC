#!/usr/bin/env python
"""
Test runner for Domain-SC.

This script runs all or selected tests for the Domain-SC system.
"""

import os
import sys
import argparse
import unittest
import coverage
from pathlib import Path


def run_tests(test_type="all", verbose=False, coverage_report=False):
    """Run the specified tests.
    
    Args:
        test_type: Type of tests to run (all, unit, integration, functional)
        verbose: Whether to show verbose output
        coverage_report: Whether to generate a coverage report
    
    Returns:
        True if all tests pass, False otherwise
    """
    # Add project root to Python path
    project_root = Path(__file__).resolve().parent
    sys.path.append(str(project_root))
    
    # Set up test discovery
    loader = unittest.TestLoader()
    
    if test_type == "all":
        print("Running all tests...")
        test_suite = loader.discover("tests")
        # Make sure we're finding tests
        if not test_suite.countTestCases():
            print("No tests discovered in 'tests' directory. Trying specific test files...")
            # Manually add specific test files if discovery isn't finding them
            doc_processor_tests = loader.loadTestsFromName("tests.unit.test_document_processor")
            test_suite.addTest(doc_processor_tests)
            print(f"Added {doc_processor_tests.countTestCases()} tests from document_processor")
    elif test_type == "unit":
        print("Running unit tests...")
        test_suite = loader.discover("tests/unit")
        # Make sure we're finding tests
        if not test_suite.countTestCases():
            print("No unit tests discovered. Trying specific test files...")
            doc_processor_tests = loader.loadTestsFromName("tests.unit.test_document_processor")
            test_suite.addTest(doc_processor_tests)
            print(f"Added {doc_processor_tests.countTestCases()} tests from document_processor")
    elif test_type == "integration":
        print("Running integration tests...")
        test_suite = loader.discover("tests/integration")
    elif test_type == "functional":
        print("Running functional tests...")
        test_suite = loader.discover("tests/functional")
    else:
        print(f"Unknown test type: {test_type}")
        return False
        
    print(f"Found {test_suite.countTestCases()} test cases")
    
    # Set up test runner
    verbosity = 2 if verbose else 1
    
    if coverage_report:
        # Set up coverage
        cov = coverage.Coverage(
            source=["src"],
            omit=[
                "*/tests/*",
                "*/venv/*",
                "*/__init__.py",
            ]
        )
        cov.start()
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(test_suite)
    
    if coverage_report:
        # Generate coverage report
        cov.stop()
        cov.save()
        
        print("\nCoverage Report:")
        cov.report()
        
        # Generate HTML report
        cov.html_report(directory="coverage_html")
        print(f"HTML coverage report generated in {project_root}/coverage_html/")
    
    # Return True if all tests pass
    return result.wasSuccessful()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run tests for Domain-SC")
    parser.add_argument(
        "--type", "-t",
        choices=["all", "unit", "integration", "functional"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output"
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Generate a coverage report"
    )
    
    args = parser.parse_args()
    
    success = run_tests(
        test_type=args.type,
        verbose=args.verbose,
        coverage_report=args.coverage
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()