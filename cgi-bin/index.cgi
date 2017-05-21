#!/usr/bin/perl -w
use CGI::Pretty qw(:standard *table);
require "./service-local.pl";

my $cmd = (defined param('cmd')) ? param('cmd') : 'Server home';
my $JOBID = (defined param('JOBID')) ? param('JOBID') : 0;

if ($cmd eq 'result' and $JOBID ne "0") { print redirect("result.cgi?JOBID=$JOBID");}

print_header();
print_content($cmd, $JOBID);
print_tail();		
