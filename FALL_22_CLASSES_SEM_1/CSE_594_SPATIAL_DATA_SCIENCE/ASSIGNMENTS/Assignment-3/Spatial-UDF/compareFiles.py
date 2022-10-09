import os

# ========================= GLOBAL VARIABLES ========================
outputsDirectory = os.path.join("data", "outputs")
trueOutputsDirectory = os.path.join("data", "true-outputs")
directory_list = [outputsDirectory, trueOutputsDirectory]
outputFile = 'Output.txt'
outputSorted = 'OutputSorted.txt'

# COMPARE BOTH FINAL OUTPUT TEXT FILES
outputs_file = os.path.join(outputsDirectory, outputFile)
true_outputs_file = os.path.join(trueOutputsDirectory, outputFile)

outputs_file_sorted = os.path.join(outputsDirectory, outputSorted)
true_outputs_file_sorted = os.path.join(trueOutputsDirectory, outputSorted)


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


def deleteNonTextFiles(directory, files_in_directory):
    # DELETE FILES WITH EXTENSION OTHER THAN .TXT

    filtered_files_delete = [file for file in files_in_directory if not file.endswith(".txt")]
    for file in filtered_files_delete:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)


def writeFinalFile(directory, files_in_directory):
    # WRITE THE CONTENTS OF TXT PART FILES INTO INE SINGLE FILE
    filtered_files_write = [file for file in files_in_directory if (file.endswith(".txt") and file != outputFile)]

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
        deleteNonTextFiles(directory, files_in_directory)

        # SQUASH ALL FILES INTO ONE
        writeFinalFile(directory, files_in_directory)


# DEFINE FILE COMPARE LOGIC
def createSortedFilesAndComapare():
    udfFile = open(outputs_file, 'r')
    UDFlines = sorted(udfFile.readlines())
    writeContentsToFile(outputs_file_sorted, UDFlines)
    udfFile.close()
    deleteOutPutFiles(outputs_file)

    TrueFile = open(true_outputs_file, 'r')
    Truelines = sorted(TrueFile.readlines())
    writeContentsToFile(true_outputs_file_sorted, Truelines)
    TrueFile.close()
    deleteOutPutFiles(true_outputs_file)

    flag = True
    for line in UDFlines:
        if line not in Truelines:
            flag = False
            print(f"{line} is missing from {true_outputs_file}")
            break

    if flag:
        print("No difference in the files found")


def main():
    # IF FILES PRESENT ALREADY BEFORE EXECUTING DELETE THEM
    deleteOutPutFiles(outputs_file_sorted)
    deleteOutPutFiles(true_outputs_file_sorted)

    # SQUASH FILES
    squashFiles()

    # SORT FILES AND DELETE INTERMEDIATE FILES
    createSortedFilesAndComapare()

main()