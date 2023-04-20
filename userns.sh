#!/bin/bash

# Configuration file
CONFIG_FILE="/etc/userns-namespaces.conf"

# Lookup function to get the name of a user namespace
lookup_namespace_name() {
    local nsid="$1"
    local name="$(grep -w "$nsid" "$CONFIG_FILE" | awk '{print $2}')"
    echo "$name"
}

# Example usage: lookup the name of namespace with NSID 1001
namespace_name="$(lookup_namespace_name 1001)"
echo "Namespace name: $namespace_name"

