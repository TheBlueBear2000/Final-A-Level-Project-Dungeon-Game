import os

def generate_tree(directory, prefix=''):
    files = []
    dirs = []
    
    # List all items in the directory
    for item in os.listdir(directory):
        if not item.startswith('.') and item != '__pycache__':  # Ignore hidden files and __pycache__ directory
            if os.path.isfile(os.path.join(directory, item)):
                files.append(item)
            else:
                dirs.append(item)
    
    # Print files in current directory
    for i, file in enumerate(files):
        if i == len(files) - 1 and not dirs:  # Last file and no subdirectories
            print(prefix + '└──', file)
        else:
            print(prefix + '├──', file)
    
    # Recursively print subdirectories
    for i, dir in enumerate(dirs):
        path = os.path.join(directory, dir)
        if i == len(dirs) - 1:  # Last subdirectory
            print(prefix + '└──', dir)
            generate_tree(path, prefix + '    ')
        else:
            print(prefix + '├──', dir)
            generate_tree(path, prefix + '│   ')

# Ask user for directory
directory = input("Enter directory path: ")

# Generate and print tree
print(os.path.basename(directory))
generate_tree(directory)