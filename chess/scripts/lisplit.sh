#!/bin/bash

# Check if all required parameters are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <year> <month> <target_folder>"
    exit 1
fi

# Assign parameters to variables
YEAR=$1
MONTH=$2
SOURCE_FOLDER=$3
TARGET_FOLDER=$4

# Construct the file name
FILE_NAME="${SOURCE_FOLDER}/lichess_db_standard_rated_${YEAR}-${MONTH}.pgn.zst"

# Check if the file exists
if [ ! -f "$FILE_NAME" ]; then
    echo "Error: File $FILE_NAME not found!"
    exit 1
fi

# Create the target folder if it doesn't exist
mkdir -p "$TARGET_FOLDER"

# Decompress and split the file
zstd -d --stdout "$FILE_NAME" | split -b 1000m - "$TARGET_FOLDER/lichess_${YEAR}-${MONTH}_"

# Print completion message
echo "Decompression and splitting completed. Files are saved in $TARGET_FOLDER."
