<?php

header('Content-type: application/json');
$url = "http://localhost:5000/";

$fromtime = isset($_GET['fromtime']);
$totime = isset($_GET['totime']);
$latest = isset($_GET['latest']);
$callback = isset($_GET['callback']);

$fromorto = $fromtime || $totime;
$frotolat = $fromorto || $latest;

if( $frotolat || $callback ) {

	$url .= '?';

	if( $fromtime ) { $url .= "fromtime=" . $_GET['fromtime']; }
	if( $totime ) { $url .= ( $fromtime ? '&' : '' ) . "totime=" . $_GET['totime']; }
	if( $latest ) { $url .= ( $fromorto ? '&' : '' ) . "latest=" . $_GET['latest']; }
	if( $callback ) { $url .= ( $frotolat ? '&' : '') . "callback=" . $_GET['callback']; }

}

echo file_get_contents($url);

?>
