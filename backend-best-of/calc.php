<?php
ini_set('memory_limit', '-1');

define("NORTH_WEST_LON", 11.979071);
define("NORTH_WEST_LAT", 54.189192);
define("SOUTH_EAST_LON", 12.246176);
define("SOUTH_EAST_LAT", 54.051561);
define("RASTER_SIZE", 0.001);

$data = array();
$envpriorities = array();
//$missedtypes = array();
$raster = array();

function downloadData() {
	global $data, $envpriorities;
	$dataSources = json_decode(file_get_contents("data-sources.json"));
	for ($i = 0; $i < count($dataSources->sources); $i++) { 
		$json = getDataFromURL($dataSources->sources[$i]->url);
		if (!is_object($json)) {
			echo "Cannot get data source ".$dataSources->sources[$i]->name;
			continue;
		}
		array_push($data, $json);
		array_push($envpriorities, $dataSources->sources[$i]->envpriority);
		echo "Downloaded Source '".$dataSources->sources[$i]->name."'\n\r";
		if ($data[count($data) - 1]->type != "FeatureCollection") {
			trigger_error("Source is not of type 'FeatureCollection'", E_USER_WARNING);
		}
	}
}

function calcBestOf() {
	for ($i = NORTH_WEST_LON; $i < SOUTH_EAST_LON; $i += RASTER_SIZE) { 
		for ($j = SOUTH_EAST_LAT; $j < NORTH_WEST_LAT; $j += RASTER_SIZE) {
			calcScore($i, $j);
		}
	}
}

function calcScore($lon, $lat) {
	global $data, $envpriorities, $missedtypes, $raster;
	$score = 0;
	for ($i = 0; $i < count($data); $i++) { 
		if ($data[$i]->type == "FeatureCollection") {
			for ($j = 0; $j < count($data[$i]->features); $j++) { 
				if ($data[$i]->features[$j]->geometry->type == "Point" && 
					checkPoint($lon, $lat, $data[$i]->features[$j]->geometry->coordinates)) {
					$score += $envpriorities[$i] * 0.0001 / RASTER_SIZE;
				} /*else {
					if (!array_search($data[$i]->features[$j]->geometry->type, $missedtypes)) {
						array_push($missedtypes, $data[$i]->features[$j]->geometry->type);
					}
				}*/
			}
		}
	}
	$raster[$lon."-".$lat] = $score;
}

function checkPoint($lon, $lat, $point) {
	return $point[0] >= $lon && $point[1] >= $lat && $point[0] <= ($lon + RASTER_SIZE) && $point[1] <= ($lat + RASTER_SIZE);
}

function getDataFromURL($url) {
	return json_decode(file_get_contents($url));
}

function print10Best() {
	global $raster;
	$i = 0;
	foreach ($raster as $key => $value) {
		echo $key." -> ".$value."\n\r";
		$i++;
		if ($i >= 10) {
			break;
		}
	}
}

function writeToFile() {
	global $raster;
	$geoJSON = array();
	$geoJSON["type"] = "FeatureCollection";
	$geoJSON["features"] = array();
	foreach ($raster as $key => $value) {
		if ($value <= 0) {
			continue;
		}
		$geoJSONFeature = array();
		$geoJSONFeature["type"] = "Feature";
		$geoJSONFeature["geometry"]["type"] = "Point"; 
		$geoJSONFeature["geometry"]["coordinates"][0] = floatval(explode("-", $key)[0] + RASTER_SIZE / 2);
		$geoJSONFeature["geometry"]["coordinates"][1] = floatval(explode("-", $key)[1] + RASTER_SIZE / 2);
		$geoJSONFeature["properties"]["envpriority"] = $value;
		array_push($geoJSON["features"], $geoJSONFeature);
	}
	file_put_contents("best-places-".RASTER_SIZE.".json", json_encode($geoJSON, JSON_PRETTY_PRINT));
}

$beginTime = time();
echo "Start...\n\r";
echo "Download Data...\n\r";
downloadData();
if (count($data) <= 0) {
	echo "No Connection. Abort";
	die();
}
echo "Calc best of...\n\r";
calcBestOf();

arsort($raster);
print10Best();

echo "Write to file...\n\r";
writeToFile();

/*echo "This types counld be calculated: ";
for ($i = 0; $i < count($missedtypes); $i++) { 
	echo $missedtypes[$i].($i < count($missedtypes) - 1 ? ", " : "");
}*/

$finishedTime = time();
echo "Finished in ".(($finishedTime-$beginTime))."s.";
?>