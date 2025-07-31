<?php
/*
 * Migr8 Test PHP Payload
 * Harmless reconnaissance payload for upload testing
 */

echo "<!-- Migr8 PHP Test Payload -->\n";
echo "<h2>PHP Upload Test Successful</h2>\n";
echo "<p>Server: " . $_SERVER['SERVER_SOFTWARE'] . "</p>\n";
echo "<p>PHP Version: " . phpversion() . "</p>\n";
echo "<p>Current Time: " . date('Y-m-d H:i:s') . "</p>\n";
echo "<p>Upload Directory: " . __DIR__ . "</p>\n";
echo "<p>File: " . __FILE__ . "</p>\n";

// Basic system info (non-harmful)
if (function_exists('php_uname')) {
    echo "<p>System: " . php_uname() . "</p>\n";
}

// Check if dangerous functions are disabled
$dangerous_functions = ['exec', 'shell_exec', 'system', 'passthru'];
foreach ($dangerous_functions as $func) {
    $status = function_exists($func) ? 'Available' : 'Disabled';
    echo "<p>Function $func: $status</p>\n";
}

echo "<!-- End Migr8 PHP Test Payload -->\n";
?>
