#!/usr/bin/perl

# my $host="quagga-host";         #quagga router name
my $logpass="bgpuser";            #login password
my $enable="zebra";             #enable password
my $myasn="100";              #local AS number
my $router_id="172.0.1.1";     #bgp router-id
my $remote_as="101";          #remote-as number
my $remote_ip="172.0.2.1";     #BGP neighbor ip address
my $route_count=0;
my $max_routes=300000;              #max number of routers to generate

open (BGPCONF,'>bgpd.conf')|| die "Can not open bgpd.conf for writing";
# print BGPCONF "hostname $host\npassword $logpass\nenable password $enable\nline vty \n";
print BGPCONF "log file /var/log/quagga/bgpd.log\npassword $logpass\n";
print BGPCONF "router bgp $myasn\n  bgp router-id $router_id\n  neighbor $remote_ip remote-as $remote_as\n";
MAXR: while ($route_count <= $max_routes ) { 
$octet1=int(rand(223))+1; #generate 1st octet randomly in 1-223 range, 224 and up is multicust and class E  
if ($octet1 ==127) {next;} #need to make sure that 127.X.X.0/24 is excluded 
$octet2=0;  
while ( $octet2 <= 255 ){
$octet3=0;
while ( $octet3 <= 255 ) {
print BGPCONF "  network $octet1\.$octet2\.$octet3\.0/24\n";
$octet3++;
$route_count++;
if ($route_count == $max_routes) {last MAXR;}
}
$octet2++;
}
}
close BGPCONF;
