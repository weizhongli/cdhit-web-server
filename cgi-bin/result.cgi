#!/usr/bin/perl -w
use CGI::Pretty qw( *table);
use Time::Local;
use Switch;

my $q = new CGI;

require "./server-config.pl";
#my $SL_session_dir     = "/home/oasis/data/webcomp/web-session";
my $N_refresh = 15;

my %fail_codes = ();
   $fail_codes{"Long"} = <<EOD;
<PRE>
Our server can not effectively clustering very long sequences, e.g. genomes. Your job took
too long time, it was killed to allow other jobs to run.

Please modify your job by removing very long sequences. We are sorry, but we are developing
tools to allow clustering genome-sized sequences, maybe available in near future.

CD-HIT team.
</PRE>
EOD
  $fail_codes{"Bin"} = <<EOD;
<PRE>
The file you uploaded is binary, please check your file
</PRE>
EOD
  $fail_codes{"DNA"} = <<EOD;
<PRE>
Your input file is DNA, you need to use cd-hit-est, but you used cd-hit, please resubmit
</PRE>
EOD

my $base_cgi = "/cgi-bin/index.cgi";
my $JOBID = $q->param('JOBID');
$JOBID =~ s/\s+//g;
 
security_check($JOBID);

if (defined $q->param('side')){
  if ($q->param('side') eq 'left' ) {result_left($JOBID);}
  else                              {result_right($JOBID);}
  exit(0);
}

if (-e "$SL_session_dir/$JOBID/$JOBID.fail") { failed_job($JOBID); }
if (-f "$SL_session_dir/$JOBID/$JOBID.ok") { completed_job($JOBID);} 
if (-d "$SL_session_dir/$JOBID") { running_job($JOBID); }
unknown_job($JOBID);

sub security_check{
  my $JOBID = shift;
  if ($JOBID =~ /\D/) {
    print $q->header("text/html");
    print "Invalid job id";
    print $q->end_html;

    exit();
  }
}

sub failed_job{
  my $JOBID = shift;
  print $q->header("text/html");
  print $q->title("You job $JOBID is failed");
  print "We are sorry, but your job $JOBID is failed:", $q->br;
  open(TMP, "$SL_session_dir/$JOBID/$JOBID.fail");
  my $ll;
  while ($ll=<TMP>) { 
    my $txt = $ll;
    if ($ll =~ /^Error_code\s+(\w+)/) {
      $txt = $fail_codes{$1};
    }
    print $txt.$q->br; 
  }
  close(TMP);
  print_google_analytics();
  print $q->end_html;
  exit(0);
}

sub completed_job{
  my $JOBID = shift;
  print $q->header("text/html");
  print $q->title("You job $JOBID is finished");
  print $q->frameset({-cols=>'15%,85%'},
    $q->frame({-name=>'left',-src=>"result.cgi?JOBID=$JOBID&side=left"}),
    $q->frame({-name=>'right',-src=>"result.cgi?JOBID=$JOBID&side=right"})
  );
  exit(0);
}

sub running_job{
  my $JOBID = shift;
  my $tmp_url = $q->url()."?JOBID=$JOBID";
  print $q->header(-type=>"text/html",-refresh=>$N_refresh);
  print $q->start_html(-title=>"You job $JOBID is still runnnig");
  print "You job $JOBID has been submitted", $q->br;
  print "You job $JOBID is still running", $q->br;
  print "This page will be refreshed every $N_refresh seconds", $q->br;
  print "You can also use this link to retrieve your job:", $q->br;
  print $q->a({-href=>$tmp_url}, $tmp_url), $q->br;
  print_google_analytics();
  print $q->end_html;
  exit(0)
}

sub unknown_job{
  my $JOBID = shift;
  print $q->header(-type=>"text/html",-refresh=>$N_refresh);
  print $q->start_html(-title=>"You job $JOBID not found");
  print "We can't recognize JOBID \"$JOBID\" you submitted", $q->br;
  print "Perhaps your job haven't entered the queue yet, be patient", $q->br;
  print "Or you submitted a wrong JOBID", $q->br;
  print_google_analytics();
  print $q->end_html;
  exit(0);
}

sub print_google_analytics {
  print <<EOD;
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-13149047-1");
pageTracker._trackPageview();
} catch(err) {}</script>
EOD
}

sub result_left{
  my $JOBID = shift;
  print $q->header(-type=>"text/html");
  print $q->start_html(-title=>"You job $JOBID is finished",-bgcolor=>"#dff0ff", -style=>{-src=>"../css/main.css"});
  print <<EOD;
<table width="100%">
<table align="left" style="border-bottom: 1px solid rgb(128, 128, 128);" width="100%" bgcolr="#f0f8ff">
<tr>
  <td bgcolor="#dff0ff" height="80" style="border-bottom: 1px solid rgb(161, 161, 161);" align="left">
  <a href="../cgi-bin/result.cgi?JOBID=$JOBID&side=right",    target='right'>Raw output</A><BR>
  <a href="../output/$JOBID/$JOBID.result.tar.gz"                           >Download all files</A><BR>
  <a href="../cgi-bin/get_tree.cgi?JOBID=$JOBID&sorting=no",  target='right'>Browse clusters by size</A><BR>
  <a href="../cgi-bin/get_tree.cgi?JOBID=$JOBID&sorting=len", target='right'>Browse clusters by length</A><BR>
EOD

  print <<EOD;
  <a href="../cgi-bin/get_plot.cgi?JOBID=$JOBID",             target='right'>Distribution of clusters</A><BR>
  </td>
</tr>
</table>
EOD

  print_google_analytics();
  print $q->end_html;
}

sub result_right{
  my $JOBID = shift;
  print $q->header("text/html");
  print $q->start_html(-title=>"You job $JOBID is finished",-bgcolor=>"#dff0ff");
  print "You job $JOBID is finished.";
  open(TMP, "$SL_session_dir/$JOBID/$JOBID.conf");
  my ($ll, %confs, $i);

  while ($ll=<TMP>){
    chomp($ll);
    my ($key, $value) = split(/=/,$ll);
    $confs{$key} = $value;
  }
  print $q->br, "Program you ran: ".$confs{'program'};

  if (defined($confs{'input'})){
    print $q->hr,
          "You input file is ".$confs{'input'}." and we named it as "
         .$q->a({-href=>"../output/$JOBID/$JOBID.fas.0"},"$JOBID.fas.0"), $q->br;
    print "Summary information for $JOBID.fas.0 included in "
              .$q->a({-href=>"../output/$JOBID/$JOBID.fas.0.stat"},"$JOBID.fas.0.stat"), $q->br;
    print "You required ".$confs{'level'}." runs for sequence clustering",$q->br;
    my $space1 = "&nbsp;&nbsp;&nbsp;&nbsp;";
    my $space2 = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
    for ($i=1;$i<=$confs{'level'};$i++){
      my $str1 = ($i > 1) ? "(only representative sequences from pervious run included)":"";
      print "$space1 $i. Fasta file for representative sequences at " .($confs{"lc$i"}*100).'% identity is '
            .$q->a({-href=>"../output/$JOBID/$JOBID.fas.$i"},"$JOBID.fas.$i"), $q->br;
      print "$space2 Summary information for $JOBID.fas.$i included in "
            .$q->a({-href=>"../output/$JOBID/$JOBID.fas.$i.stat"},"$JOBID.fas.$i.stat"), $q->br;
      print "$space2 Corresponding cluster file $str1 is"
            .$q->a({-href=>"../output/$JOBID/$JOBID.fas.$i.clstr"},"$JOBID.fas.$i.clstr"), $q->br;
      print "$space2 Sorted cluster file by size is "
            .$q->a({-href=>"../output/$JOBID/$JOBID.fas.$i.clstr.sorted"},"$JOBID.fas.$i.clstr.sorted"), $q->br;
      if ($i > 1){
        print "$space2 Cluster file where all sequences are included is "
              .$q->a({-href=>"../output/$JOBID/$JOBID.fas.$i-0.clstr"},"$JOBID.fas.$i-0.clstr"),$q->br;
        print "$space2 Sorted cluster file by size is "
              .$q->a({-href=>"../output/$JOBID/$JOBID.fas.$i-0.clstr.sorted"},"$JOBID.fas.$i-0.clstr.sorted"),$q->br;
      }
    }
  }
  else{
    if ($confs{'local'} eq 1){
      print "You db1 file is sequence database ".$confs{'db1'}.$q->br;
    }
    else{
      print "You db1 file is ".$confs{'db1'}." and we named it as "
            .$q->a({-href=>"../output/$JOBID/$JOBID.fas.db1"},"$JOBID.fas.db1"), $q->br;
      print "&nbsp;&nbsp;&nbsp;&nbsp;Summary information for $JOBID.fas.db1 included in "
            .$q->a({-href=>"../output/$JOBID/$JOBID.fas.db1.stat"},"$JOBID.fas.db1.stat"), $q->br;
    }
    print "You db2 file is ".$confs{'db2'}." and we named it as "
          .$q->a({-href=>"../output/$JOBID/$JOBID.fas.db2"},"$JOBID.fas.db2"), $q->br;
    print "&nbsp;&nbsp;&nbsp;&nbsp;Summary information for $JOBID.fas.db2 included in "
          .$q->a({-href=>"../output/$JOBID/$JOBID.fas.db2.stat"},"$JOBID.fas.db2.stat"), $q->br;
    print "Sequences in db2 that are matched to db1 are stored in a cluster file "
          .$q->a({-href=>"../output/$JOBID/$JOBID.fas.db2novel.clstr"},"$JOBID.fas.db2novel.clstr"), $q->br;
    print "cluster file (sorted by size) is "
          .$q->a({-href=>"../output/$JOBID/$JOBID.fas.db2novel.clstr.sorted"},"$JOBID.fas.db2novel.clstr.sorted"), $q->br;
    print "Sequences in db2 that are not matched to db1 are stored in a fasta file "
          .$q->a({-href=>"../output/$JOBID/$JOBID.fas.db2novel"},"$JOBID.fas.db2novel"), $q->br;
  }
  print $q->hr;
  print "Generated shell script is "
        .$q->a({-href=>"../output/$JOBID/run-$JOBID.sh"},"run-$JOBID.sh")
        .$q->br.$q->br;
  open(TMP,"$SL_session_dir/$JOBID/run-$JOBID.sh");
  while (my $ll=<TMP>) { next unless($ll=~/^cd-hit/ or $ll=~/\.pl/ or $ll=~/\.py/); print $ll.$q->br; }
  print_google_analytics();
  print $q->end_html;
}
