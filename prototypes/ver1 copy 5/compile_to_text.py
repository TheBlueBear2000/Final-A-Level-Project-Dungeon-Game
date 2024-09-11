
import os

file_string = "CODE:"
file_count = 0

directory = 'projects/prototypes/ver1/'
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if filename.endswith('.py')  or  filename.endswith('.json'):
            with open(os.path.join(dirpath, filename)) as f:
                file_string += "\n\n\n\n" + dirpath + '/' + filename + "\n"
                file_string += f.read()
                file_count += 1
                #print(f.read())

file_string += f"\n\n\n\nTotal files: {file_count}\n"

#print(file_string)

with open("projects/prototypes/ver1/saved_text.txt", 'w') as f:
    f.write(file_string)


