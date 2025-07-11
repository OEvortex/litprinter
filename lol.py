from litprinter import lit
# Automatically pretty-formats different data types
data = {
    "users": ["alice", "bob", "charlie"],
    "active": True,
    "settings": {
        "theme": "dark",
        "notifications": True
    }
}
lit(data)  # Formatted with proper indentation and syntax highlighting