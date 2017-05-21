#!/usr/bin/perl
use CGI;
#use strict;
use Time::Local;
use Switch;
use Storable;
use POSIX;
use List::Util qw[min max];

require "./server-config.pl";
#my $SL_session_dir     = "/home/oasis/data/webcomp/web-session";

my $q = new CGI;
my $JOBID;
my $JOBDIR;

if (defined $q->param('JOBID')){ # retreive a existing job
  $JOBID = $q->param('JOBID');
  $JOBDIR = "$SL_session_dir/$JOBID"
}

open(TMP, "$JOBDIR/$JOBID.conf");
my ($ll, %confs);
while ($ll=<TMP>){
  chomp($ll);
  my ($key, $value) = split(/=/,$ll);
  $confs{$key} = $value;
}

print $q->header("text/html"),
      $q->start_html (-title=>"CD-HIT Suite");

print $q->p("The x-axis is the cluster size. Number of clusters >= this size is plotted using
            line-point style against left y-axis. Percentage of total sequences within clusters
            >= this size is plotted using line style against right y-axis.");
print $q->br, $q->br;
if ($confs{'program'} eq 'cd-hit-2d' or $confs{'program'} eq 'cd-hit-est-2d'){
  print $q->p("<b>Distribution of clusters and sequences at ".($confs{"lc1"}*100).'% level</b>');
  print $q->img({-src=>"../output/$JOBID/$JOBID.fas.db2novel.clstr.1.png",-height=>"400"}), $q->br;
}
else{
  for (my $i=1;$i<=$confs{'level'};$i++){
    print $q->p("<b>$i. Distribution of clusters and sequences at ".($confs{"lc$i"}*100).'% level</b>');
    print $q->img({-src=>"../output/$JOBID/$JOBID.fas.$i.clstr.1.png",-height=>"400"}), $q->br;
  }    
}

print $q->end_html();
