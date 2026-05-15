name: Build APK

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install Buildozer
        run: |
          sudo apt update
          sudo apt install -y git zip unzip openjdk-17-jdk python3-pip
          pip install --upgrade pip
