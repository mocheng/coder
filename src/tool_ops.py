"""Tool Operations - File reading and basic operations"""

from pathlib import Path
from typing import Optional


def read_file_content(file_path: str) -> Optional[str]:
    """
    Read file content safely with proper error handling.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File content as string, or None if error occurred
        
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If no read permission
        UnicodeDecodeError: If file encoding is not supported
    """
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found")
    
    # Check if it's actually a file
    if not path.is_file():
        raise ValueError(f"'{file_path}' is not a file")
    
    # Try to read with common encodings
    encodings = ['utf-8', 'utf-16', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except PermissionError:
            raise PermissionError(f"Permission denied reading '{file_path}'")
    
    # If all encodings failed
    raise UnicodeDecodeError(f"Could not decode file '{file_path}' with supported encodings")


def is_text_file(file_path: str) -> bool:
    """
    Check if file is likely a text file based on extension.
    
    Args:
        file_path: Path to check
        
    Returns:
        True if likely a text file
    """
    text_extensions = {
        '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp',
        '.txt', '.md', '.rst', '.json', '.xml', '.yaml', '.yml',
        '.html', '.css', '.scss', '.sass', '.sql', '.sh', '.bash',
        '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala'
    }
    
    path = Path(file_path)
    return path.suffix.lower() in text_extensions
