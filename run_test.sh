#!/bin/sh

BASE_NAME=$1

TEST_FILE="test_${BASE_NAME}.py"

FOUND_PATH=$(find tests -type f -name "$TEST_FILE")

if [ -n "$FOUND_PATH" ]; then
    echo "$FOUND_PATH"
else
    echo "Test file not found: ${TEST_FILE}"
fi
python -m pytest -vvv -s $FOUND_PATH