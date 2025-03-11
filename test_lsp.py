import sys
from pathlib import Path
import json
from pylsp import uris
from pylsp.workspace import Document, Workspace
from pylsp.python_lsp import PythonLSPServer
from pyls_jsonrpc.streams import JsonRpcStreamReader, JsonRpcStreamWriter
import io

def setup_workspace(root_path):
    """Initialize a workspace with the given root path"""
    # Create transport using in-memory streams
    reader = JsonRpcStreamReader(io.StringIO())
    writer = JsonRpcStreamWriter(io.StringIO())
    tx = (reader, writer)
    
    # Define config
    config = {
        'pylsp': {
            'plugins': {
                'pycodestyle': {'enabled': False},
                'mccabe': {'enabled': False},
                'pyflakes': {'enabled': False},
                'rope_completion': {'enabled': True}
            }
        }
    }
    
    # Create workspace instance
    ws = Workspace(root_path, config)
    
    # Initialize server with transport and config
    server = PythonLSPServer(tx, config)
    
    # Set workspace
    server.workspace = ws

    # Convert root_path to URI format
    root_uri = uris.from_fs_path(root_path)
    
    # Initialize the server
    server.m_initialize(
        processId=None,
        rootUri=root_uri,
        workspaceFolders=None,
        capabilities={},
        initializationOptions=None
    )
    
    # Complete initialization
    server.m_initialized()
    
    return server

def find_references(server, file_path, line, character):
    """Find references for symbol at given position"""
    # Convert file path to URI format
    uri = uris.from_fs_path(file_path)
    
    # Create position dictionary
    position = {'line': line, 'character': character}
    
    # Find references (include declarations by default)
    return server.references(uri, position, exclude_declaration=False)

def main():
    # Example usage
    if len(sys.argv) != 4:
        print("Usage: python test_lsp.py <file_path> <line> <character>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    # Check if file exists
    if not Path(file_path).is_file():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
        
    try:
        line = int(sys.argv[2])
        character = int(sys.argv[3])
    except ValueError:
        print("Error: Line and character must be integers")
        sys.exit(1)
    
    # Setup workspace using the file's parent directory as root
    root_path = str(Path(file_path).parent)
    server = setup_workspace(root_path)
    
    try:
        # Create document in workspace
        uri = uris.from_fs_path(file_path)
        server.workspace.put_document(uri, source=Path(file_path).read_text())
        
        # Find references
        refs = find_references(server, file_path, line, character)
        
        # Print results
        print(json.dumps(refs, indent=2))
    except Exception as e:
        print(f"Error finding references: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
