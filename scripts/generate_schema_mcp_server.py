""""Generate a PandasSchemaster schema class from a DataFrame file using MCP server utilizing SSE transport."""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from pandasschemaster import SchemaGenerator

# This is the shared MCP server instance
mcp = FastMCP(
    "pandasschemaster-mcp",
    instructions="Use the PandasSchemaster MCP Server to generate and validate DataFrame schemas.",
    help_text="This server provides functionality to generate and validate DataFrame schemas using PandasSchemaster.",
    version="1.0.1",
)

@mcp.tool(
    name="pandasschemaster.generate_schema",
    description="Generate a PandasSchemaster schema class from a DataFrame file.",
)
async def generate_schema(
    absolute_path: str,
    class_name: str = "TestSchema",
    output_path: Optional[str] = None,
    sample_size: int = 42,
) -> str:
    """Generate a schema class from a DataFrame.

    Args:
        absolute_path (str): The absolute path to the input file.
        class_name (str, optional): The name of the generated schema class. Defaults to "TestSchema".
        output_path (Optional[str], optional): The path to the output file. Defaults to None.

    Returns:
        str: The generated schema class as a string.
    """

    schema_generator = SchemaGenerator(infer_nullable=True, sample_size=sample_size)
    schema_class = schema_generator.generate_from_file(
        absolute_path,
        output_path=output_path,
        class_name=class_name,
    )

    return schema_class


# Entry point to run the server
if __name__ == "__main__":
     mcp.run(
        transport="sse"  # Use Server-Sent Events for real-time updates
    )
