import os

# ========================= GLOBAL VARIABLES ========================
outputsDirectory = os.path.join("data", "output")
folders_in_directory = os.listdir(outputsDirectory)
directory_list =[]
outputFile_list = []
for folders in folders_in_directory:
    directory_list.append(os.path.join(outputsDirectory, folders))
    outputFile_list.append(folders + ".json")
print(
# ======================== VARIABLES END =============================
def deleteOutPutFiles(file):
    # DELETE PREVIOUS OUTPUT FILES
    if os.path.exists(file):
        os.remove(file)


def writeContentsToFile(filePath, content):
    file = open(filePath, 'a')
    for lines in content:
        file.write(lines)
    file.close()


def deleteNonJSONFiles(directory, files_in_directory):
    # DELETE FILES WITH EXTENSION OTHER THAN .TXT

    filtered_files_delete = [file for file in files_in_directory if not file.endswith(".json")]
    for file in filtered_files_delete:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)


def writeFinalFile(directory, files_in_directory, outputFile):
    # WRITE THE CONTENTS OF TXT PART FILES INTO INE SINGLE FILE
    filtered_files_write = [file for file in files_in_directory if (file.endswith(".json") and file != outputFile)]

    for file in filtered_files_write:
        path_to_file = os.path.join(directory, file)
        path_to_write_file = os.path.join(directory, outputFile)
        with open(path_to_file, 'r') as firstfile, open(path_to_write_file, 'a') as secondfile:
            # read content from first file
            for line in firstfile:
                # append content to second file
                secondfile.write(line)
        # DELETE THE REDUNDANT TEXT FILES
        os.remove(path_to_file)


def squashFiles():
    # ITERATE OVER FILES IN DIRECTORY LIST
    for index, directory in enumerate(directory_list):
        # GET FILES IN DIRECTORY
        files_in_directory = os.listdir(directory)

        # DELETE NON TEXT FILES - SO THAT WE CAN SQUASH ALL PART FILES INTO ONE
        deleteNonJSONFiles(directory, files_in_directory)

        # SQUASH ALL FILES INTO ONE
        writeFinalFile(directory, files_in_directory, outputFile_list[index])

def main():

    for index, dir in enumerate(directory_list):
        deleteOutPutFiles(os.path.join(dir, outputFile_list[index]))

    # SQUASH FILES
    squashFiles()

main()