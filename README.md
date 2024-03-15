# Automatically create links and tags in your Obsidian vault

## Introduction

This script is designed for those of us using Obsidian to pen down thoughts, compose books, or compile resources with an eye towards eBook creation. If you're like me, you appreciate a bit of automation to streamline the tedious bits of formatting and linking. This script is here to assist in that, subtly enhancing your Markdown files without getting in the way of your creative process.  Plus, if you're brainstorming keywords, why not have a chat with ChatGPT? It might offer you some insights based on your work's themes.  

## What the Script Does

This script lends a hand by tackling a few specific tasks:

1. Copy Folder to Desktop: Works on a safe copy of your original vault.
2. Initialize Glossary Files: Sets up blank Markdown files for each term in your glossary, waiting for your wisdom.
3. Clean Filenames: Turns file names into cleaner, web-friendly versions.
4. Manage Markdown Links: Clears out old Markdown links and tags, then introduces fresh ones based on your chosen keywords, keeping your pages interconnected.
5. Tagging Content: Searches your Markdown content for certain keywords and tags them appropriately, helping you organize and categorize your writing.
6. Folder Exclusion: Keeps specific folders, like "glossary," untouched during the tagging and linking process.

## How to Use the Script

Here's how to get started:

    Make sure Python is installed on your computer.
    Gather your list of keywords. This can be a brainstorming session with yourself, or maybe ChatGPT can help generate a list based on your content's themes.
    Place the script in a location you find convenient.
    Adjust the original_vault_path and vault_path to fit your project's directory.
    Run the script through your terminal or command line: python run-me.py
    Check your project graph, tags and links and be seriously amazed.

## Contributing

Got ideas on how to make this script even better? Feel free to fork the repository, tweak to your heart's content, and submit a pull request. All contributions are welcomed and appreciated!

## License

This script is released under the MIT License. This means you are free to use, modify, distribute, and sell it as you see fit. I hope it serves your Obsidian life well and makes your process a bit smoother.
