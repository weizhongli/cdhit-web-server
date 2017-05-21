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
my $store_file;
my $sortbywhat = "len";

if (defined $q->param('JOBID')){ # retreive a existing job
  $JOBID = $q->param('JOBID');
  if (defined $q->param('sorting')){ $sortbywhat = $q->param('sorting') }
  $store_file = "$SL_session_dir/$JOBID/$JOBID.clstr_$sortbywhat.dump"
}
my @clstr = @{retrieve($store_file)};

# add by ying huang
my $anno = 0;
my %clstr_anno = ();
my $store_file1 = "$SL_session_dir/$JOBID/$JOBID.fas.1.clstr.anno_$sortbywhat.dump";
if (-f $store_file1){  # anno info included
  $anno = 1;
  %clstr_anno = %{retrieve($store_file1)};
}
#

my $batchsize = 50;
my $totalpage = ceil(scalar(@clstr)/$batchsize);
my $pageno = 1;
if (defined $q->param('pageno')) {$pageno = $q->param('pageno');}
if ($pageno > $totalpage) {print $q->redirect($q->url()."?pageno=1");}
my $start = ($pageno-1)*$batchsize;
my $end = min(scalar(@clstr), $start+$batchsize);

print
  $q->header("text/html"),
  $q->start_html(-title=>"CD-HIT Suite",
                 -style=>{-src=>"../css/main.css"},
                 -script=>{-language=>"javascript",-src=>"../js/util.js"});

  my $help_info1 = ($sortbywhat eq "no") ? "their No. sequences":"length of the representative";
  my $help_info = <<EOD;
  In this webpage, we show the sequence cluster by a hierarchical tree structure. 
  Every cluster is represented by its representative sequence, click icon plus to
  show the sequences belong to the cluster. 
  
  For h-cd-hit or h-cd-hit-est running, the sequences are represenative sequences 
  from previous clustering, we can further explore the cluster information. 

  The clusters are sorted by $help_info1.
EOD

  $help_info =~ s/\n/\\n/g;
  $help_info =~ s/\"//g;

#### page
print $q->start_form(-action=>$q->url());
print <<EOD;
<P align="left">&nbsp; &nbsp; <input type=button value="More info" OnClick="alert('$help_info');"><p>
EOD
my $nextpage = $pageno + 1;
my $prevpage = $pageno - 1;

print $q->a({-href=>$q->url()."?pageno=1&JOBID=$JOBID&sorting=$sortbywhat"}, $q->img({-src=>"../css/images/pg-first.gif",-border=>"0"}));
if ( $prevpage <= 0 ) { print $q->a({-href=>$q->url()."?pageno=1&JOBID=$JOBID&sorting=$sortbywhat"}, $q->img({-src=>"../css/images/pg-prev.gif",-border=>"0"}));}
else { print $q->a({-href=>$q->url()."?pageno=$prevpage&JOBID=$JOBID&sorting=$sortbywhat"}, $q->img({-src=>"../css/images/pg-prev.gif",-border=>"0"})); }

print "<font size='+1'>Page ";
print $q->textfield(-name => 'pageno',-id => 'pageno', -size=>'+1',-value => $pageno,-size => 3,-onchange=>"submit()" ); 
print " of $totalpage</font>";

if ($nextpage > $totalpage) { print $q->a({-href=>$q->url()."?pageno=$totalpage&JOBID=$JOBID&sorting=$sortbywhat"}, $q->img({-src=>"../css/images/pg-next.gif",-border=>"0"}));}
else {print $q->a({-href=>$q->url()."?pageno=$nextpage&JOBID=$JOBID&sorting=$sortbywhat"}, $q->img({-src=>"../css/images/pg-next.gif",-border=>"0"}))};
print $q->a({-href=>$q->url()."?pageno=$totalpage&JOBID=$JOBID&sorting=$sortbywhat"}, $q->img({-src=>"../css/images/pg-last.gif",-border=>"0"}));
print $q->hidden({-name=>"JOBID",-value=>$JOBID});
print $q->hidden({-name=>"sorting",-value=>$sortbywhat});
print $q->end_form();

my %node2size = ();
my $clstr_level = 0;
for (my $i=$start; $i<$end; $i++){
  my $node1 = "$i";
  my $j = 0;
  $clstr_level=1 if ($clstr_level<1);

  foreach my $seq1 (@{$clstr[$i][3]}) {
    if ($$seq1[2]) { # can be futher expanded
      my $node2 = "$i.$j";
      my $k = 0;
      $clstr_level=2 if ($clstr_level<2);
      foreach my $seq2(@{$$seq1[3]}) {
        if ($$seq2[2]) {  
          my $node3 = "$i.$j.$k";
          my $nn = scalar(@{$$seq2[3]});
          $clstr_level=3 if ($clstr_level<3);
          $node2size{$node1} += $nn;
          $node2size{$node2} += $nn;
          $node2size{$node3} += $nn;
        }
        else {
          $node2size{$node1}++;
          $node2size{$node2}++;
        }
        $k++;
      }
    }
    else {
      $node2size{$node1}++;
    }
    $j++;
  }
}

for (my $i=$start; $i<$end; $i++){
  print "\n<div class=\"treenode1\">";
  my $branch_str = ($clstr_level>1)? ", No. branches:". scalar(@{$clstr[$i][3]}) : "";
  print $q->a({-href=>"javascript: hideShow('hello$i')"}, $q->img({-id=>"ihello$i",-src=>"../css/images/plus.png",-border=>"0"}));
  print "Cluster $i", $branch_str, ", No. sequences: ", $node2size{"$i"}, ", Representative: $clstr[$i][0], length:$clstr[$i][1] ";
######################################## # add by ying huang for annotation present
  if ($anno == 1){
    print "<BR>&nbsp;&nbsp;&nbsp;&nbsp;Check over-represented function annotation term in the cluster";
    print $q->a({-href=>"javascript: toggle('anno$i')"}, $q->img({-id=>"ianno$i",-src=>"../css/images/help.gif",-border=>"0"}));
    print "<div style='display: none;' id='anno$i' class='treenode1'>";
    my @columns = ();
    my $header = ["Annotation Term", "# of Seq in Cls", "Cls Percentage", "# of Seq in Input", "Background Percentage", "Enrichment", "Pvalue"];
    push @columns, $q->td($header);
    foreach my $tmp (@{$clstr_anno{$clstr[$i][0]}}){
      push @columns, $q->td($tmp);
    }
    print $q->table({-cellpadding => 3, -border => 1}, $q->Tr(\@columns));
    print "<BR><BR></div>";
  }
  print "</div>\n";
#######################################

  print "<div style='display: none;' id='hello$i' class='treenode2'>";
  my $j=0;
  foreach my $seq1 (@{$clstr[$i][3]}) {
    print "<div class='treenode1'>";
    if ($$seq1[2]) { # can be futher expanded
      $branch_str = ($clstr_level>2)? ", No. branches:". scalar(@{$$seq1[3]})  : "";
      print $q->a({-href=>"javascript: hideShow('hello$i.$j')"},$q->img({-id=>"ihello$i.$j",-src=>"../css/images/plus.png",-border=>"0"}));
      print "Cluster $i.$j", $branch_str, ", No. sequences:", $node2size{"$i.$j"}, ", Representative: $$seq1[0], length: $$seq1[1] </div>\n";
      print "<div style='display: none;' id='hello$i.$j' class='treenode2'>";
      my $k=0;
      foreach my $seq2(@{$$seq1[3]}) { 
        print "<div class='treenode1'>";
        if ($$seq2[2]){
          print $q->a({-href=>"javascript: hideShow('hello$i.$j.$k')"},$q->img({-id=>"ihello$i.$j.$k",-src=>"../css/images/plus.png",-border=>"0"}));
          print "Cluster $i.$j.$k, No. sequences: ", $node2size{"$i.$j.$k"}, ", Representative: $$seq2[0], length:$$seq2[1] </div>\n";
          print "<div style='display: none;' id='hello$i.$j.$k' class='treenode2'>";
          my $k1 = 0;
          foreach my $seq3(@{$$seq2[3]}) { 
            print "<div class='treenode1'>";
            print "$k1. $$seq3[0], length: $$seq3[1], identity: $$seq3[4] </div>\n";
            $k1++;
          }
          print "</div>";
        }
        else{
          print "$k. $$seq2[0], length: $$seq2[1], identity: $$seq2[4]</div>\n";
        }
        $k = $k+1;
      }
      print "</div>";
    }
    else{
      print "$j. $$seq1[0], length: $$seq1[1], identity: $$seq1[4]</div>\n";
    }
    $j = $j+1;
  }
  print "</div></div>";
}

print $q->end_html();

