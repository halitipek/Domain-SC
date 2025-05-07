# Domain-SC Enhanced System Demo Guide

This guide explains how to run and understand the enhanced Domain-SC system's capabilities using the demonstration script.

## Overview

The `demo_enhanced_system.py` script showcases the full workflow of the Domain-SC system with all the enhanced components:

1. **Enhanced RAG Service** with semantic pre-evaluation
2. **Optimized LLM Service** with smart model selection and caching
3. **Adaptive Prompt System** with performance tracking
4. **Simulation-Based System Architect Agent** for better architecture design

The demo takes textual requirements as input and produces a complete system architecture design, using the enhanced components to improve quality, consistency, and cost-effectiveness.

## Running the Demo

### Prerequisites

Ensure you have all the required dependencies installed:

```bash
pip install -r requirements.txt
```

### Running the Complete Demo

To run the complete end-to-end demo with sample requirements:

```bash
python demo_enhanced_system.py
```

This will execute a complete workflow:

1. Index knowledge resources for RAG
2. Analyze the requirements text
3. Enhance requirements with relevant knowledge from the RAG system
4. Convert to a format suitable for architecture design
5. Generate a complete system architecture using the simulation-based approach

### Output Files

The demo generates several output files in the `data/output/demo_results` directory:

- `structured_requirements.json` - Analyzed and structured requirements
- `rag_results.json` - Knowledge retrieved from the RAG system
- `design_input.json` - Formatted input for the architecture agent
- `generated_architecture.json` - Complete architecture in JSON format
- `generated_architecture.md` - Human-readable architecture document in Markdown

## Customizing the Demo

### Using Your Own Requirements

To use your own requirements, modify the `sample_requirements` variable in the `main` function of `demo_enhanced_system.py`:

```python
sample_requirements = """
Your custom requirements text here.
"""
```

### Adding Custom Knowledge

To add custom knowledge for the RAG system, add Markdown (.md) files to the `resources` directory. These files will be automatically indexed and used to enhance the architecture design process.

## Understanding the Enhancements

### RAG Enhancement

The demo uses semantic pre-evaluation to filter documents before retrieval, ensuring better relevance and lower token costs. You can see the retrieved knowledge in the `rag_results.json` file.

### LLM Optimization

The demo uses smart model selection and semantic caching to reduce costs and improve response times. The `optimized_llm_service.py` component automatically selects the appropriate model based on task complexity.

### Simulation-Based Approach

The architect agent uses simulation to predict expected outputs for each stage of architecture design, then compares actual outputs to these simulations. When there are significant deviations, it re-runs with guidance to improve quality. This process is reflected in the architecture design file.

## Troubleshooting

If you encounter any issues:

1. Check the logs in the `logs/enhanced_demo.log` file for detailed information.
2. Ensure that all required files are present in the expected directories.
3. Verify that all dependencies are installed correctly.

For more detailed information on each component, refer to the `IMPROVEMENTS.md` document.