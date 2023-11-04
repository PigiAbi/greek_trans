<?php

ini_set('display_errors', 'On');
error_reporting(E_ALL | E_STRICT);

//connect to DB
require_once ('f_connect.php');
 
// get all of the "posted" and "get" vars
$variables = array('id');
foreach ($variables as $var) {
    $$var = $cid->real_escape_string($_REQUEST[$var]);		
}

//start HTML
echo "
<head>
	<title>Transcription</title>
</head>
<script src='javascript.js'></script>
<body>";

//how many transcriptions does this person need to do for this round?
$SQLtext = "SELECT currentround, numrequired FROM `transcription_user_details` where id='$id' LIMIT 1";
list($currentround, $numrequired) = executeSQL($SQLtext);

//how many transcriptions has this person done?
$SQLtext = "SELECT COUNT(*) FROM `transcription_user_transcriptions` where id='$id' LIMIT 1";
list($numfinished) = executeSQL($SQLtext);

//what was the last transcription this person did (we go in order to avoid repetition)
$SQLtext = "SELECT transcription_index FROM `transcription_user_transcriptions` where id='$id' ORDER BY timestamp LIMIT 1";
list($transcription_index) = executeSQL($SQLtext);
if ($transcription_index) {
	//if haven't ever done one, choose a random one.
	$transcription_index=($transcription_index%1000)+1;
} else {
	$transcription_index=rand(1,1000);
}

//what is the answer to the next transcription?
$SQLtext = "SELECT answer_key FROM `transcription_answerkey` where transcription_index='$transcription_index' LIMIT 1";
list($answer_key) = executeSQL($SQLtext);

//has person has finished?
if ($numfinished>=$numrequired) {
	echo "You have completed the necessary tasks. Thank you.";
//if not, needs to complete the tasks
} else {
	echo "You have completed $numfinished of the $numrequired necessary tasks. You have to do transcription $transcription_index.";

	//bring up transcription pic
	echo "<br><img src='../td3/pics/Pic".$transcription_index."' width=1050>";
	
	//create image holders for transcription
	echo "<table width=1050 cellpadding=0 cellspacing=0 border=0><tr>";
	for ($i=1;$i<=35;$i++) {
		echo "<td><img src='pics/placeholder.png' width=30 height=40></td>";
	}
	echo "</tr></table>";
	
	//create image holders for transcription
	$array = array("a","b","c","d","e","f","g","h","i","dot");
	echo "<center><table width=1050 cellpadding=0 cellspacing=0 border=0><tr>";
	foreach ($array as &$letter) {
		echo "<td><img src='pics/".$letter.".png' border='1'></td>";
		echo "<td><img src='pics/placeholder.png' width=10></td>";
	}
	echo "</tr></table></center>";
	
	//start form HTML:
	echo "
	<form name='mainForm' action='index.php?id=$id' onsubmit='return checkAccuracy()' method='post' > 
	text: <input type='text' name='transcription' value=''>";
	echo" <input type='text' name='transcription_' value='".$answer_key."'>
	<input type='submit' value='Submit'></form>";


	
}







//this executes SQL command to talk to DB
function executeSQL($SQL)
{
	global $cid, $db;
	$result = mysqli_query($cid,"$SQL");
	if (!$result) { echo("ERROR?: " . mysqli_error($cid) . "\n$SQL\n");   }
	$temp = mysqli_fetch_array($result);
	return $temp;
}


?>
