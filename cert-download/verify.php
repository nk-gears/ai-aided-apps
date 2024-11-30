<?php

ini_set('display_startup_errors', 1);
ini_set('display_errors', 1);
error_reporting(-1);

function fetchNameByRegNo($regNo, $filePath) {
    try {
        // Check if the file exists
        if (!file_exists($filePath)) {
            throw new Exception("Error: File not found.");
        }

        // Open the file for reading
        $file = fopen($filePath, 'r');
        if (!$file) {
            throw new Exception("Error: Unable to open the file.");
        }

        // Read the file line by line
        while (($line = fgets($file)) !== false) {
            // Skip the header line
            if (stripos($line, 'RegNo Name') !== false) {
                continue;
            }

            // Split the line by whitespace
            $columns = preg_split('/\s{2,}|\t/', trim($line));

            // Check if the RegNo matches
            if (isset($columns[0]) && $columns[0] === $regNo) {
                // Close the file and return the Name
                fclose($file);
                return isset($columns[1]) ? $columns[1] : "Name not found.";
            }
        }

        // Close the file
        fclose($file);

        // If no match is found
        throw new Exception("Error: RegNo not found.");

    } catch (Exception $e) {
        echo $e->getMessage();
        // Return the error message if an exception is caught
        return $e->getMessage();
    }
}

$filePath = 'reg.txt'; // Ensure this path is correct for your server
$regNo = isset($_GET["regNo"]) ? $_GET["regNo"] : ''; // Handle missing regNo parameter

// Fetch the name from the text file
$name = fetchNameByRegNo($regNo, $filePath);

$userInfo = [];
$userInfo["name"] = $name;

// Return the data as JSON
header("Content-type: application/json");
echo json_encode($userInfo);
?>
