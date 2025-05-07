"""
LLM-related commands for the Domain-SC CLI.
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from src.services.optimized_llm_service import OptimizedLLMService
from src.prompts.adaptive_prompt_system import AdaptivePromptSystem
from src.utils.logger import setup_logger

# Set up logging
logger = setup_logger("cli.llm")


def register_commands(subparsers: argparse._SubParsersAction) -> None:
    """
    Register LLM-related commands.
    
    Args:
        subparsers: Subparser group to add to
    """
    # LLM command group
    llm_parser = subparsers.add_parser("llm", help="LLM-related commands")
    llm_subparsers = llm_parser.add_subparsers(dest="llm_command", help="LLM command to execute")
    
    # LLM generate command
    llm_generate_parser = llm_subparsers.add_parser("generate", help="Generate text using the LLM")
    llm_generate_parser.add_argument("--prompt", "-p", help="Prompt string (if not provided, will read from stdin)")
    llm_generate_parser.add_argument("--model", "-m", help="Model name")
    llm_generate_parser.add_argument("--temperature", "-t", type=float, help="Temperature")
    llm_generate_parser.add_argument("--max-tokens", "-k", type=int, help="Max tokens")
    llm_generate_parser.add_argument("--streaming", "-s", action="store_true", help="Enable streaming output")
    
    # LLM prompt command
    llm_prompt_parser = llm_subparsers.add_parser("prompt", help="Generate text using a prompt template")
    llm_prompt_parser.add_argument("--template", "-t", required=True, help="Template name")
    llm_prompt_parser.add_argument("--variables", "-v", help="Variables for the prompt (JSON string)")
    llm_prompt_parser.add_argument("--vars-file", "-f", help="JSON file containing variables")
    llm_prompt_parser.add_argument("--model", "-m", help="Model name")
    llm_prompt_parser.add_argument("--temperature", "-T", type=float, help="Temperature")
    llm_prompt_parser.add_argument("--max-tokens", "-k", type=int, help="Max tokens")
    llm_prompt_parser.add_argument("--streaming", "-s", action="store_true", help="Enable streaming output")
    
    # LLM templates command
    llm_templates_parser = llm_subparsers.add_parser("templates", help="List available prompt templates")
    llm_templates_parser.add_argument("--template", "-t", help="Specific template to show details for")
    llm_templates_parser.add_argument("--format", "-f", choices=["json", "text"], default="text", 
                                     help="Output format (json or text)")
    
    # LLM models command
    llm_subparsers.add_parser("models", help="List available LLM models")
    
    # LLM benchmark command
    llm_benchmark_parser = llm_subparsers.add_parser("benchmark", help="Benchmark LLM performance")
    llm_benchmark_parser.add_argument("--models", "-m", nargs="+", help="Models to benchmark")
    llm_benchmark_parser.add_argument("--prompt", "-p", help="Prompt to use for benchmarking")
    llm_benchmark_parser.add_argument("--iterations", "-i", type=int, default=3, help="Number of iterations")
    llm_benchmark_parser.add_argument("--output", "-o", help="Output file for benchmark results")


def print_json(data: Any) -> None:
    """
    Print data as formatted JSON.
    
    Args:
        data: Data to print
    """
    print(json.dumps(data, indent=2))


async def handle_commands(args: argparse.Namespace, config: Any) -> int:
    """
    Handle LLM-related commands.
    
    Args:
        args: Parsed command line arguments
        config: CLI configuration
        
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    # Initialize services
    llm_service = OptimizedLLMService()
    prompt_system = AdaptivePromptSystem()
    
    if args.llm_command == "generate":
        # Get model, temperature and max_tokens with defaults from config
        model = args.model or config.get("llm", "default_model")
        temperature = args.temperature if args.temperature is not None else config.get("llm", "default_temperature")
        max_tokens = args.max_tokens or config.get("llm", "default_max_tokens")
        
        # Get prompt
        if not args.prompt:
            # If prompt not provided as argument, read from stdin
            print("Enter prompt (Ctrl+D to finish):")
            prompt_lines = []
            try:
                for line in sys.stdin:
                    prompt_lines.append(line)
                prompt = "".join(prompt_lines)
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return 1
        else:
            prompt = args.prompt
        
        if not prompt.strip():
            print("Error: Empty prompt.")
            return 1
        
        # Generate text
        print(f"Generating response using model: {model}...")
        if args.streaming:
            # Stream response
            async for chunk in llm_service.generate_text_stream(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            ):
                print(chunk, end="", flush=True)
            print()  # Add newline at the end
        else:
            # Generate complete response
            response = await llm_service.generate_text(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            print("\n----- Generated Response -----\n")
            print(response)
            print("\n-----------------------------\n")
        
        return 0
        
    elif args.llm_command == "prompt":
        # Get model, temperature and max_tokens with defaults from config
        model = args.model or config.get("llm", "default_model")
        temperature = args.temperature if args.temperature is not None else config.get("llm", "default_temperature")
        max_tokens = args.max_tokens or config.get("llm", "default_max_tokens")
        
        # Get variables
        variables: Dict[str, Any] = {}
        
        if args.vars_file:
            # Load variables from file
            try:
                with open(args.vars_file, 'r') as f:
                    variables = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading variables file: {e}")
                return 1
                
        elif args.variables:
            # Parse variables JSON string
            try:
                variables = json.loads(args.variables)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format for variables.")
                return 1
        
        # Generate with template
        print(f"Generating response using template '{args.template}' with model: {model}...")
        if args.streaming:
            # Stream response
            async for chunk in prompt_system.generate_with_template_stream(
                template_name=args.template,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **variables
            ):
                print(chunk, end="", flush=True)
            print()  # Add newline at the end
        else:
            # Generate complete response
            response = await prompt_system.generate_with_template(
                template_name=args.template,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **variables
            )
            
            print("\n----- Generated Response -----\n")
            print(response)
            print("\n-----------------------------\n")
        
        return 0
        
    elif args.llm_command == "templates":
        # List templates
        templates = await prompt_system.list_templates()
        
        if args.template:
            # Show specific template details
            template_details = await prompt_system.get_template_details(args.template)
            if not template_details:
                print(f"Template '{args.template}' not found.")
                return 1
                
            if args.format == "json":
                print_json(template_details)
            else:
                print(f"Template: {args.template}")
                print(f"Description: {template_details.get('description', 'N/A')}")
                print(f"Variables:")
                for var in template_details.get("variables", []):
                    print(f"  - {var.get('name')}: {var.get('description', 'N/A')}")
                print(f"Version: {template_details.get('version', 'N/A')}")
                print(f"Performance Score: {template_details.get('performance_score', 'N/A')}")
                
        else:
            # List all templates
            if args.format == "json":
                print_json({"templates": templates})
            else:
                print("Available templates:")
                for template in templates:
                    print(f"  - {template}")
        
        return 0
        
    elif args.llm_command == "models":
        # List available models
        models = await llm_service.list_available_models()
        print_json({"available_models": models})
        
        return 0
        
    elif args.llm_command == "benchmark":
        # Get models to benchmark
        models = args.models or [config.get("llm", "default_model")]
        
        # Get prompt
        if not args.prompt:
            # If prompt not provided as argument, use a default one
            prompt = "Explain the concept of microservices architecture in 3 paragraphs."
        else:
            prompt = args.prompt
        
        # Run benchmark
        print(f"Running benchmark with {args.iterations} iterations for each model...")
        results = await llm_service.benchmark_models(
            models=models,
            prompt=prompt,
            iterations=args.iterations
        )
        
        # Display results
        print("\nBenchmark Results:")
        print_json(results)
        
        # Save results if output file specified
        if args.output:
            try:
                with open(args.output, 'w') as f:
                    json.dump(results, f, indent=2)
                print(f"Benchmark results saved to {args.output}")
            except IOError as e:
                print(f"Error saving benchmark results: {e}")
                return 1
        
        return 0
    
    else:
        print("Unknown LLM command. Use 'domain-sc llm --help' for available commands.")
        return 1