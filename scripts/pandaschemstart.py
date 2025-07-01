#!/usr/bin/env python3
"""
PandasSchemstart - Unified interface for PandasSchemaster CLI and MCP server.

This script provides a single entry point for both schema generation and MCP server functionality.

Usage:
    python pandaschemstart.py generate <input_file> [OPTIONS]    # Generate schema
    python pandaschemstart.py mcp-server [OPTIONS]              # Start MCP server
    python pandaschemstart.py --help                            # Show help

Examples:
    # Generate schema from CSV
    python pandaschemstart.py generate data.csv -o schema.py -c MySchema
    
    # Start MCP server
    python pandaschemstart.py mcp-server
    
    # Start MCP server with specific transport
    python pandaschemstart.py mcp-server --transport=sse

Commands:
    generate    Generate schema classes from data files (same as generate_schema.py)
    mcp-server  Start the MCP server for AI assistant integration

For detailed help on each command:
    python pandaschemstart.py generate --help
    python pandaschemstart.py mcp-server --help
"""

import sys
import os
import argparse
from typing import List, Optional

# Add the parent directory to Python path to find pandasschemaster package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)


def run_generate_command(args: List[str]) -> int:
    """Run the schema generation command."""
    # Import and run the main function from schema_generator
    try:
        # Save the original sys.argv
        original_argv = sys.argv.copy()
        
        # Set sys.argv to the arguments we want to pass
        sys.argv = ['generate_schema.py'] + args
        
        from pandasschemaster.schema_generator import main
        
        # Call main() which will use sys.argv
        result = main()
        
        # Restore original sys.argv
        sys.argv = original_argv
        
        return result if result is not None else 0
        
    except ImportError as e:
        print(f"Error: Failed to import schema generator: {e}", file=sys.stderr)
        return 1
    except SystemExit as e:
        # Handle sys.exit() calls from the schema generator
        return e.code if e.code is not None else 0
    finally:
        # Ensure sys.argv is restored even if an exception occurs
        if 'original_argv' in locals():
            sys.argv = original_argv


def run_mcp_server(transport: str = "sse") -> int:
    """Run the MCP server."""
    try:
        # Import the MCP server from the same directory
        import importlib.util
        import os
        
        # Get the path to the MCP server script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mcp_server_path = os.path.join(script_dir, "generate_schema_mcp_server.py")
        
        # Load the MCP server module
        spec = importlib.util.spec_from_file_location("mcp_server", mcp_server_path)
        mcp_server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mcp_server_module)
        
        # Get the mcp instance
        mcp = mcp_server_module.mcp
        
        print(f"🚀 Starting PandasSchemaster MCP server with {transport} transport...")
        print("📡 Server will be available for AI assistant tool calls")
        print("🔧 Available tool: pandasschemaster.generate_schema")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run the MCP server
        mcp.run(transport=transport)
        return 0
        
    except ImportError as e:
        print(f"Error: Failed to import MCP server: {e}", file=sys.stderr)
        print("Make sure 'mcp' package is installed: pip install mcp[cli]", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print("Error: MCP server script 'generate_schema_mcp_server.py' not found", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except Exception as e:
        print(f"Error: Failed to start MCP server: {e}", file=sys.stderr)
        return 1


def create_main_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog='pandaschemstart',
        description='Unified interface for PandasSchemaster CLI and MCP server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate data.csv -o schema.py -c MySchema
  %(prog)s mcp-server
  %(prog)s mcp-server --transport=sse

For more information on each command:
  %(prog)s generate --help
  %(prog)s mcp-server --help
        """.strip()
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='PandasSchemstart 1.0.0'
    )
    
    # Create subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        metavar='COMMAND'
    )
    
    # Generate command
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate schema classes from data files',
        description='Generate PandasSchemaster schema classes from data files',
        add_help=False  # We'll handle help ourselves to pass through to schema_generator
    )
    
    # MCP server command
    mcp_parser = subparsers.add_parser(
        'mcp-server',
        help='Start MCP server for AI assistant integration',
        description='Start the MCP server to enable AI assistants to generate schemas'
    )
    
    mcp_parser.add_argument(
        '--transport',
        choices=['sse'],
        default='sse',
        help='Transport protocol for MCP server (default: sse)'
    )
    
    return parser


def main() -> int:
    """Main entry point."""
    parser = create_main_parser()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    
    # Parse known args to handle the case where generate command has its own help
    args, remaining = parser.parse_known_args()
    
    if args.command == 'generate':
        # For generate command, pass all arguments after 'generate' to the schema generator
        generate_args = sys.argv[2:]  # Skip 'pandaschemstart.py' and 'generate'
        return run_generate_command(generate_args)
    
    elif args.command == 'mcp-server':
        # Parse the remaining arguments for mcp-server
        if remaining:
            print(f"Warning: Unknown arguments for mcp-server: {remaining}", file=sys.stderr)
        return run_mcp_server(args.transport)
    
    else:
        # This handles the case where --help or --version was used
        if hasattr(args, 'help') or not args.command:
            parser.print_help()
            return 0
        
        print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
