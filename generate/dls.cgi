#!/usr/bin/perl
use Math::Trig 'great_circle_destination';
use Geo::Calc;
use Data::Dumper;

print "Content-Type:application/octet-stream; name=\"FileName.osm\"\r\n";
print "Content-Disposition: attachment; filename=\"FileName.osm\"\r\n\n";
use strict;
my $cycle = 5;
my $count = 0;

my $way = 1;
my $node = 1;

my $start_township = 1;
my $start_range = 1;
my $start_meridian = 4;
#$start_nw_lat = 53.65719314626632;
#$start_nw_lon = -110.59564046463835;
#$start_ne_lat = 53.56974815534198;
#$start_ne_lon = -110.0;
#$start_se_lat = 49.0;
#$start_se_lon = -110.0;
#$start_sw_lat = 49.0;
#$start_sw_lon = -110.59564046463835;

my $pre_1881_ns = 0.3552237;
#$post_1881_ns = 0.3464566929133858;
my $post_1881_ns = ((60 - 49) / 126) * 4;
my $first_baseline = 49;
my $last_baseline = 60;


#starting point for individual township lines;
my $offset1 = 1629.0;
my @township = (
	{ Name => "1", OffsetW => 0, OffsetN => 0 },
	{ Name => "2", OffsetW => 1, OffsetN => 0 },
	{ Name => "3", OffsetW => 2, OffsetN => 0 },
	{ Name => "4", OffsetW => 3, OffsetN => 0 },
	{ Name => "5", OffsetW => 4, OffsetN => 0 },
	{ Name => "6", OffsetW => 5, OffsetN => 0 },
	{ Name => "7", OffsetW => 5, OffsetN => 1 },
	{ Name => "8", OffsetW => 4, OffsetN => 1 },
	{ Name => "9", OffsetW => 3, OffsetN => 1 },
	{ Name => "10", OffsetW => 3, OffsetN => 1 },
	{ Name => "11", OffsetW => 1, OffsetN => 1 },
	{ Name => "12", OffsetW => 0, OffsetN => 1 },
	{ Name => "13", OffsetW => 0, OffsetN => 2 },
	{ Name => "14", OffsetW => 1, OffsetN => 2 },
	{ Name => "15", OffsetW => 2, OffsetN => 2 },
	{ Name => "16", OffsetW => 3, OffsetN => 2 },
	{ Name => "17", OffsetW => 4, OffsetN => 2 },
	{ Name => "18", OffsetW => 5, OffsetN => 2 },
	{ Name => "19", OffsetW => 5, OffsetN => 3 },
	{ Name => "20", OffsetW => 4, OffsetN => 3 },
	{ Name => "21", OffsetW => 3, OffsetN => 3 },
	{ Name => "22", OffsetW => 2, OffsetN => 3 },
	{ Name => "23", OffsetW => 1, OffsetN => 3 },
	{ Name => "24", OffsetW => 0, OffsetN => 3 },
	{ Name => "25", OffsetW => 0, OffsetN => 4 },
	{ Name => "26", OffsetW => 1, OffsetN => 4 },
	{ Name => "27", OffsetW => 2, OffsetN => 4 },
	{ Name => "28", OffsetW => 3, OffsetN => 4 },
	{ Name => "29", OffsetW => 4, OffsetN => 4 },
	{ Name => "30", OffsetW => 5, OffsetN => 4 },
	{ Name => "31", OffsetW => 5, OffsetN => 5 },
	{ Name => "32", OffsetW => 4, OffsetN => 5 },
	{ Name => "33", OffsetW => 3, OffsetN => 5 },
	{ Name => "34", OffsetW => 2, OffsetN => 5 },
	{ Name => "35", OffsetW => 1, OffsetN => 5 },
	{ Name => "36", OffsetW => 0, OffsetN => 5 }
);

# 4th Meridian was supposed to be on 110Deg but it's a little ways off.
my @meridians = (
	{ Name => "1st Meridian", Lon => -97.4578916666667 },
	{ Name => "2nd Meridian", Lon => -102.0067659 },
	{ Name => "3rd Meridian", Lon => -106 },
	{ Name => "4th Meridian", Lon => -110.0051061 },
	{ Name => "5th Meridian", Lon => -114 },
	{ Name => "6th Meridian", Lon => -118 } );

my $file_contents = "";

my $file_header = "<?xml version='1.0' encoding='UTF-8'?>
<osm version='0.6' upload='true' generator='JOSM'>";
my $file_footer = "</osm>";


foreach (@meridians) {
	$file_contents .= "<node id='-" . ($node) ."' action='modify' visible='true' lat='" . $first_baseline .  "' lon='" . $_->{Lon} .  "' />" . "\n"
	. "<node id='-" . ($node + 1) . "' action='modify' visible='true' lat='" . $last_baseline . "' lon='" . $_->{Lon} . "' />" . "\n"
	. "  <way id='-" . $way . "' action='modify' visible='true'>" ."\n"
	. "    <nd ref='-" . $node . "' />" . "\n"
	. "    <nd ref='-" . ($node + 1) . "' />" . "\n"
	. "    <tag k='name' v='" . $_->{Name} . "' />" . "\n"
	. "  </way>" . "\n";
	$way++;
	$node = $node + 3;
}

# Output West of the 1st Meridian
my $current_lat = 49;
my $count = 1;
while ($current_lat <= $last_baseline) { 
	my ($string1, $node1) = &get_node($current_lat,$meridians[0]->{Lon});
	my ($string2, $node2) = &get_node($current_lat,$meridians[1]->{Lon});
	$file_contents .= $string1 . $string2 . &get_way($count . " From " . $meridians[0]->{Name} . " To " . $meridians[1]->{Name},
		($node1, $node2,$node1));
	$node = $node + 3;
	$count++;
	$current_lat = $current_lat + $pre_1881_ns / 4;
}

# Output West of the 2nd Meridian
$current_lat = 49;
$count = 1;
while ($current_lat <= $last_baseline) { 
	my ($string1, $node1) = &get_node($current_lat,$meridians[1]->{Lon});
	my ($string2, $node2) = &get_node($current_lat,$meridians[2]->{Lon});
	$file_contents .= $string1 . $string2 . &get_way($count . " From " . $meridians[1]->{Name} . " To " . $meridians[2]->{Name},
		($node1, $node2,$node1));
	$node = $node + 3;
	my $current_lon = $meridians[1]->{Lon};
	my $countinner = 1;
	$count++;
#	print STDERR "Current Lon: " . $current_lon . "Meridian 3: " . $meridians[2]->{Lon} . "\n";
	while ($current_lon >= $meridians[2]->{Lon}) {
		my $gc = Geo::Calc->new( lat => $current_lat, lon => $current_lon );
		my $result = $gc->destination_point( -90, 9778 );
		$current_lon = $result->{lon};
		if ($result->{lon} >= $meridians[2]->{Lon} ) {
		if ($count == 2) {
			my ($string1, $node1) = &get_node($current_lat,$current_lon);
			my ($string2, $node2) = &get_node($current_lat + ($post_1881_ns / 2), $current_lon);
			$file_contents .= $string1 . $string2 . &get_way("TEST",($node1,$node2));
		}
		elsif ($count % 4 != 0 && $count % 2 == 0) {
#			print STDERR "correction line";
			my ($string1, $node1) = &get_node($current_lat + ($post_1881_ns / 2),$current_lon);
			my ($string2, $node2) = &get_node($current_lat - ($post_1881_ns / 2), $current_lon);
			$file_contents .= $string1 . $string2 . &get_way("TEST",($node1,$node2));
		}
		else {
			last;
		}
		}
		print STDERR "Current Lon: " . $current_lon . "Meridian 3: " . $meridians[2]->{Lon} . "\n";
		$countinner++;
	}
	$current_lat = $current_lat + $post_1881_ns / 4;
}

# Output West of the 3nd Meridian
$current_lat = 49;
$count = 1;
while ($current_lat <= $last_baseline) { 
	my ($string1, $node1) = &get_node($current_lat,$meridians[2]->{Lon});
	my ($string2, $node2) = &get_node($current_lat,$meridians[3]->{Lon});
	$file_contents .= $string1 . $string2 . &get_way($count . " From " . $meridians[2]->{Name} . " To " . $meridians[3]->{Name},
		($node1, $node2,$node1));
	$node = $node + 3;
	my $current_lon = $meridians[2]->{Lon};
	my $countinner = 1;
	$count++;
#	print STDERR "Current Lon: " . $current_lon . "Meridian 4: " . $meridians[3]->{Lon} . "\n";
	while ($current_lon >= $meridians[3]->{Lon}) {
		my $gc = Geo::Calc->new( lat => $current_lat, lon => $current_lon );
		my $result = $gc->destination_point( -90, 9778 );
		$current_lon = $result->{lon};
		if ($result->{lon} >= $meridians[3]->{Lon} ) {
		if ($count == 2) {
			my ($string1, $node1) = &get_node($current_lat,$current_lon);
			my ($string2, $node2) = &get_node($current_lat + ($post_1881_ns / 2), $current_lon);
			$file_contents .= $string1 . $string2 . &get_way("TEST",($node1,$node2));
		}
		elsif ($count % 4 != 0 && $count % 2 == 0) {
#			print STDERR "correction line";
			my ($string1, $node1) = &get_node($current_lat + ($post_1881_ns / 2),$current_lon);
			my ($string2, $node2) = &get_node($current_lat - ($post_1881_ns / 2), $current_lon);
			$file_contents .= $string1 . $string2 . &get_way("TEST",($node1,$node2));
		}
		else {
			last;
		}
		}
		print STDERR "Current Lon: " . $current_lon . "Meridian 4: " . $meridians[3]->{Lon} . "\n";
		$countinner++;
	}
	$current_lat = $current_lat + $post_1881_ns / 4;
}

# Output West of the 4th Meridian
$current_lat = 49;
$count = 1;
while ($current_lat <= $last_baseline) { 
	my ($string1, $node1) = &get_node($current_lat,$meridians[3]->{Lon});
	my ($string2, $node2) = &get_node($current_lat,$meridians[4]->{Lon});
	$file_contents .= $string1 . $string2 . &get_way($count . " From " . $meridians[3]->{Name} . " To " . $meridians[4]->{Name},
		($node1, $node2,$node1));
	my $current_lon = $meridians[3]->{Lon};
	my $countinner = 1;
	$count++;
#	print STDERR "Current Lon: " . $current_lon . "Meridian 5: " . $meridians[4]->{Lon} . "\n";
	my $range = 1;
	while ($current_lon >= $meridians[4]->{Lon}) {
		my $gc = Geo::Calc->new( lat => $current_lat, lon => $current_lon );
		if ($current_lon >= $meridians[4]->{Lon} ) {
			if ($count == 2) {
				# This only matches the first row at the South side.
				#my ($string1, $node1) = &get_node($current_lat,$current_lon);
				#my ($string2, $node2) = &get_node($current_lat + ($post_1881_ns / 2), $current_lon);
				#$file_contents .= $string1 . $string2 . &get_way("TEST",($node1,$node2));
				&get_township_grid("Range: " . $range . "Baseline: " . $count . " W4", $current_lat,$current_lon,$offset1);
				&get_township_grid("Range: " . $range+1 . "Baseline: " . $count . " W4", $current_lat + ($post_1881_ns / 4), $current_lon,$offset1);
			}
			elsif ($count % 4 != 0 && $count % 2 == 0) {
				# This matches the ranges that the townships are squared against.
				#my ($string1, $node1) = &get_node($current_lat + ($post_1881_ns / 2),$current_lon);
				#my ($string2, $node2) = &get_node($current_lat - ($post_1881_ns / 2), $current_lon);
				#$file_contents .= $string1 . $string2 . &get_way("TEST",($node1,$node2));
				&get_township_grid($count . "-" . $range . " W4" . $current_lat,$current_lat, $current_lon,$offset1);
				&get_township_grid($count . "-" . $range . " W4", $current_lat + ($post_1881_ns / 4 * 1), $current_lon,$offset1);
				&get_township_grid($count . "-" . $range . " W4", $current_lat - ($post_1881_ns / 2), $current_lon,$offset1);
				&get_township_grid($count . "-" . $range . " W4", $current_lat - ($post_1881_ns / 4 * 1), $current_lon,$offset1);
			}
			else {
				last;
			}
		}
		my $result = $gc->destination_point( -90, 9778 );
		$current_lon = $result->{lon};
		print STDERR "Current Lon: " . $current_lon . "Meridian 5: " . $meridians[4]->{Lon} . "\n";
		$range = $range + 4;
		$countinner++;
	}
	$current_lat = $current_lat + $post_1881_ns / 4;
}

# Output West of the 5th Meridian
$current_lat = 49;
$count = 1;
while ($current_lat <= $last_baseline) { 
	my ($string1, $node1) = &get_node($current_lat,$meridians[4]->{Lon});
	my ($string2, $node2) = &get_node($current_lat,$meridians[5]->{Lon});
	$file_contents .= $string1 . $string2 . &get_way($count . " From " . $meridians[4]->{Name} . " To " . $meridians[5]->{Name},
		($node1, $node2,$node1));
	$node = $node + 3;
	$count++;
	$current_lat = $current_lat + $post_1881_ns / 4;
}

print $file_header . "\n";
print $file_contents . "\n";
print $file_footer . "\n";


sub get_node() {
	my ($lat, $lon) = @_;
	$node++;
	my $string = "<node id='-" . $node . "' action='modify' visible='true' lat='" . $lat . "' lon='" . $lon . "' />" . "\n";
	return ($string, $node);
}

sub get_way() {
	my ($name, @nodes) = @_;
	$way++;
	my $string = "  <way id='-" . $way . "' action='modify' visible='true'>" ."\n";
	foreach my $node (@nodes) {
		$string .= "    <nd ref='-" . $node . "' />" . "\n";
	}
	$string .= "    <tag k='name' v='" . $name . " ' />" . "\n"
	. "  </way>" . "\n";
	return $string;
}

sub get_calc_position() {
	my ($lat, $lon, $direction, $distance) = @_;
	my $gc = Geo::Calc->new( lat => $lat, lon => $lon );
	my $result = $gc->destination_point( $direction, $distance );
	return ($result->{Lat}, $result->{Lon})
}

sub get_calc_position_nw() {
	my ($lat, $lon, $offsetn, $offsetw) = @_;
#	print STDERR "LAT: " . $lat . " LON: " . $lon . "\n";
	if ($offsetn > 0) {
#		print STDERR "Offset N: " . $offsetn . "\n";
		my $gc = Geo::Calc->new( lat => $lat, lon => $lon );
		my $result = $gc->destination_point( 0, $offsetn );
		$lat = $result->{lat};
		$lon = $result->{lon};
#		print STDERR "LAT: " . $lat . " LON: " . $lon . "\n";
#		print STDERR Dumper($result) . "\n";
	}
	if ($offsetw > 0 ) {
#		print STDERR "Offset W: " . $offsetw . "\n";
		my $gc = Geo::Calc->new( lat => $lat, lon => $lon );
		my $result = $gc->destination_point( -90, $offsetw );
		$lat = $result->{lat};
		$lon = $result->{lon};
#		print STDERR "LAT: " . $lat . " LON: " . $lon . "\n";
#		print STDERR Dumper($result) . "\n";
	}
	return ($lat, $lon)
}


sub get_township_grid() {
	my ($desc, $lat,$lon,$size) = @_;
	foreach (@township) {
		my $string;
		my ($se_lat, $se_lon) = &get_calc_position_nw($lat, $lon, $_->{OffsetN} * $size, $_->{OffsetW} * $size);
		my ($nw_lat, $nw_lon) = &get_calc_position_nw($se_lat, $se_lon, $size, $size);
		my ($string1, $node1) = &get_node($se_lat, $se_lon); 
		my ($string2, $node2) = &get_node($se_lat, $nw_lon); 
		my ($string3, $node3) = &get_node($nw_lat, $nw_lon); 
		my ($string4, $node4) = &get_node($nw_lat, $se_lon); 
		my $way_string = &get_way("Township: " . $_->{Name} . " " . $desc, ($node1, $node2, $node3, $node4, $node1));
		$file_contents .= $string1 . $string2 . $string3 . $string4 . $way_string;
#		print STDERR $way_string;
	}
}

#sub NESW { deg2rad($_[0]), deg2rad(90 - $_[1]) }

1;
