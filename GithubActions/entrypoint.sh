#!/bin/bash
set -e

# Check if the runner is already configured
if [ ! -f .runner ]; then
    echo "Configuring GitHub Actions Runner..."
    ./config.sh --url $REPO_URL --token $RUNNER_TOKEN --unattended --replace
fi

echo "Starting GitHub Actions Runner..."
exec ./run.sh
