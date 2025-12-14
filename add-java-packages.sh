#!/bin/bash
# Add java_package options to all proto files

echo "Adding java_package options to proto files..."

# Find all .proto files and add java_package option after the package declaration
find . -name "*.proto" -type f | while read file; do
    echo "Processing $file"

    # Extract the package name
    package=$(grep "^package " "$file" | sed 's/package //; s/;//')

    # Convert to java package format
    # croupier.xxx.v1 -> cuihairu.github.io.croupier.xxx.v1
    java_package="cuihairu.github.io.$package"

    # Check if java_package already exists
    if grep -q "option java_package" "$file"; then
        echo "  java_package already exists, skipping..."
        continue
    fi

    # Add java_package option after the package declaration
    sed -i '' "/^package /a\\
option java_package = \"$java_package\";\\
" "$file"

    echo "  Added: option java_package = \"$java_package\";"
done

echo "Done!"