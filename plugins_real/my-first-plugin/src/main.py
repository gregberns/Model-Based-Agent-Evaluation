# src/main.py

def greet(name: str) -> str:
    """Generates a greeting message."""
    # This is a placeholder. A real implementation would have more logic.
    # A bug could be that it doesn't handle empty names, for example.
    if not name:
        return "Hello, anonymous!"
    return f"Hello, {name}!"

if __name__ == "__main__":
    # This allows the plugin to be run directly for testing.
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="World", help="The name to greet.")
    args = parser.parse_args()
    print(greet(args.name))
