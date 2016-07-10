<?php

header('Content-type: application/json');
$url = "http://localhost:5000/";

$fromtime = isset($_GET['fromtime']);
$totime = isset($_GET['totime']);
$interval = isset($_GET('interval']);
$latest = isset($_GET['latest']);
$callback = isset($_GET['callback']);

$fromorto = $fromtime || $totime;
$fromorin = $fromorto || $interval;
$frominla = $fromorin || $latest;

if( $fromorin || $callback ) {

	$url .= '?';

	if( $fromtime ) { $url .= "fromtime=" . $_GET['fromtime']; }
	if( $totime ) { $url .= ( $fromtime ? '&' : '' ) . "totime=" . $_GET['totime']; }
	if( $interval ) { $url .= ($fromorto ? '&' : '' ) . "interval=" . $_GET['interval']; } 
	if( $latest ) { $url .= ( $fromorin ? '&' : '' ) . "latest=" . $_GET['latest']; }
	if( $callback ) { $url .= ( $frominla ? '&' : '') . "callback=" . $_GET['callback']; }

}

echo file_get_contents($url);

?>
