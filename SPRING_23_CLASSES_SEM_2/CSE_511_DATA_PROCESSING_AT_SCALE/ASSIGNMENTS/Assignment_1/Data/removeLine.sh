// read the file into an array    
$fileAsArray = file($FileName);

// the line to delete is the line number minus 1, because arrays begin at zero
$lineToDelete = $_GET['remove'] - 1;

// check if the line to delete is greater than the length of the file
if ($lineToDelete > sizeof($fileAsArray)) {
    throw new Exception("Given line number was not found in file.");
}

//remove the line
unset($fileAsArray[$lineToDelete]);

// open the file for reading
if (!is_writable($fileName) || !$fp = fopen($fileName, 'w+')) {
    // print an error
    throw new Exception("Cannot open file ($fileName)");
}

// if $fp is valid
if ($fp) {
    // write the array to the file
    foreach ($fileAsArray as $line) {
        fwrite($fp, $line);
    }

    // close the file
    fclose($fp);
}