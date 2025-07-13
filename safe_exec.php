<?php
$descriptorspec = array(
   0 => array("pipe", "r"),
   1 => array("pipe", "w"),
   2 => array("file", "/tmp/error-output.txt", "a"),
);

$cwd = null;
$env = null;

$python = '/home/mkn/.rye/shims/python';
$script = 'safe_exec.py';
$cmd = [$python, $script];
$process = proc_open($cmd, $descriptorspec, $pipes, $cwd, $env);
if (is_resource($process)) {
    echo stream_get_contents($pipes[1]);
    $return_value = proc_close($process);
    if ($return_value != 0):
        echo "Command returned error value: $return_value\n";
    endif;
}
else {
    echo "Failed to run Python!\n";
}