#!/bin/bash
# This script creates symlinks for the .gemini directory and GEMINI.md file
# into a target directory and updates the git exclude file.

set -e

# Check for target directory argument
if [ -z "$1" ]; then
  echo "Usage: $0 <target-directory>"
  exit 1
fi

# Define source and destination paths
SOURCE_DIR_PATH=$(pwd)
TARGET_DIR_PATH="$1"

# Ensure the target directory exists
if [ ! -d "$TARGET_DIR_PATH" ]; then
  echo "Error: Target directory '$TARGET_DIR_PATH' not found."
  exit 1
fi

# Create symlinks using -f to overwrite if they exist and -n to handle directory links correctly
echo "Creating symlinks in $TARGET_DIR_PATH..."
ln -sfn "$SOURCE_DIR_PATH/.gemini" "$TARGET_DIR_PATH/.gemini"
ln -sfn "$SOURCE_DIR_PATH/GEMINI.md" "$TARGET_DIR_PATH/GEMINI.md"
echo "Symlinks created successfully."

# Update .git/info/exclude in the target repository
EXCLUDE_FILE="$TARGET_DIR_PATH/.git/info/exclude"

# Ensure the .git/info directory exists
mkdir -p "$(dirname "$EXCLUDE_FILE")"

# Add entries to the exclude file if they don't already exist
echo "Updating git exclude file: $EXCLUDE_FILE"
grep -qxF '.gemini' "$EXCLUDE_FILE" || echo '.gemini' >> "$EXCLUDE_FILE"
grep -qxF 'GEMINI.md' "$EXCLUDE_FILE" || echo 'GEMINI.md' >> "$EXCLUDE_FILE"

echo "Script finished successfully."
