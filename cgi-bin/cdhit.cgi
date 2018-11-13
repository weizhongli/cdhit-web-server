#!/usr/bin/perl -w
use CGI;
#use strict;
use Time::Local;
use Switch;
$CGI::POST_MAX = 1024*1024*250;

my $script_name = $0;
my $script_dir = $0;
   $script_dir =~ s/[^\/]+$//;
   $script_dir = "./" unless ($script_dir);
   $script_dir =~ s/\/$//; #### remove last "/"
#### This should be /home/oasis/data/www/home/cdhit_suite/cgi-bin
my @d_path = split(/\//, $script_dir);
my $base_cgi = "/$d_path[-2]/$d_path[-1]/index.cgi";

require "./server-config.pl";

my $q = new CGI;
if ($q->cgi_error()){ size_error($q, "The files you uploaded are too big ".$q->cgi_error); }

my $program = $q->param('program');
if    ($program eq 'h-cd-hit')     {$program = 'cd-hit';}
elsif ($program eq 'h-cd-hit-est') {$program = 'cd-hit-est';}

my $JOBID;
my $parameters;

## get env 2010.02.17
my $env_fname;
#get date and time
my $dt_int;
my $dt_format;
my $key;
## end get env

## for mail job stat: added by Beifang Niu
my $M_ADDRESS;

if (defined $q->param('JOBID')){ # retreive a existing job
  $JOBID = $q->param('JOBID');
  print $q->redirect("$base_cgi?cmd=result&JOBID=$JOBID");
}
else{   # submit a new job
  $parameters = check_parameters();
  if ($parameters =~ /^Error/) { parameter_error(); }
  else {
    if ($program eq 'cd-hit-2d' or $program eq 'cd-hit-est-2d'){ $JOBID = prepare_input_2d();}
    else{ $JOBID = prepare_input();}

    $M_ADDRESS = $q->param('Mailaddress'); # for mail added by Beifang Niu
    print $q->redirect("$base_cgi?cmd=result&JOBID=$JOBID");
    send_mail($M_ADDRESS,$JOBID); # for mail added by Beifang Niu
  }
}
exit(0);


sub size_error{
  my ($q, $reason) = @_;
  print $q->header("text/html");
  print $q->start_html(-title=>"Error");
  print $q->p("You upload was not processed because the following error occured:");
  print $q->p($q->i($reason));
  print $q->end_html;
  exit(0);
}


sub parameter_error{
  print $q->header("text/html");
  print $q->start_html(-title=>"Error Parameters");
  print $parameters, $q->br;
  print "Please reset your parameters",$q->br;
  print $q->end_html;
}

#for mail added by Beifang Niu

sub send_mail {
  my $M_ADDRESS = shift;
  my $JOBID = shift;
  
  my $r_mail  = $M_ADDRESS;
  my $s_mail  = $admin_email;
  my $subject = 'CD-HIT webserver job status checking';
  my $tmpm_url = $q->url()."?JOBID=$JOBID";
  
  open(MAIL,"|/usr/lib/sendmail -t ");
  
  print MAIL "To: $r_mail\n";
  print MAIL "From: $s_mail\n";
  print MAIL "Subject: $subject\n\n";
  print MAIL "Job status link: \n";
  print MAIL $tmpm_url;
  
  close(MAIL);
  
  print<<END_TAG;

END_TAG
}


sub prepare_input_2d{
  my $ll;
  my $fh_db1 = $q->param('SeqDB1');
  my $fh_db2 = $q->param('SeqF');
  # create working directory and upload FASTA file
  my $JOBID = time();
  # use time to generate JOBID to avoid use a OLD id
  my $JOBDIR = "$SL_session_dir/$JOBID";
  while (-d $JOBDIR){ # an already exist JOBID, submitted at the same time
    sleep(5);
    $JOBID = time();
    $JOBDIR = "$SL_session_dir/$JOBID";
  }
  mkdir($JOBDIR);

  my ($input_fname,$db1_fname);
  if ($q->param('program') eq 'cd-hit-2d' and $q->param('which_db1') eq '1'){
    if    ($q->param('LocalDB1') eq 'SWISSPROT') { $db1_fname = $sw_db;}
    elsif ($q->param('LocalDB1') eq 'PDB'      ) { $db1_fname = $pdb_db;}
    $fh_db1 = $q->param('LocalDB1');
  }
  else{
    $input_fname = "$JOBDIR/$JOBID.fas.db1"; #upload sequence into $input_fname;
    open(UPLOADFILE, "> $input_fname");
    binmode(UPLOADFILE);
    while ($ll=<$fh_db1>) {print UPLOADFILE $ll;}
    close(UPLOADFILE);
    $db1_fname = "$JOBID.fas.db1";
  }
  $input_fname = "$JOBDIR/$JOBID.fas.db2"; #upload sequence into $input_fname;
  open(UPLOADFILE, "> $input_fname");
  binmode(UPLOADFILE);
  while ($ll=<$fh_db2>) {print UPLOADFILE $ll;}
  close(UPLOADFILE);

  my ($cmd_str, $iden, $wsize);
  $iden = $q->param("lc1");
  $wsize = get_wsize($iden);
  $cmd_str .= <<EOD;
#!/bin/sh
#\$ -S /bin/bash
#\$ -v PATH=$SL_bin_dir:$ENV{'PATH'}
$qsub_local

#\$ -e $JOBDIR/$JOBID.err
#\$ -o $JOBDIR/$JOBID.out
cd $JOBDIR
sed -i "s/\\x0d/\\n/g" $db1_fname
sed -i "s/\\x0d/\\n/g" $JOBID.fas.db2

EOD
  $cmd_str .= "faa_stat.pl $JOBID.fas.db1\n" if ($q->param('which_db1') ne "1");
  $cmd_str .= <<EOD;
faa_stat.pl $JOBID.fas.db2
$NGS_cdhit_dir/$program -i $db1_fname -i2 $JOBID.fas.db2 -o $JOBID.fas.db2novel -c $iden -n $wsize $parameters -T 4 -M 32000
$NGS_cdhit_dir/clstr_sort_by.pl no < $JOBID.fas.db2novel.clstr > $JOBID.fas.db2novel.clstr.sorted
$NGS_cdhit_dir/clstr_list.pl $JOBID.fas.db2novel.clstr $JOBID.clstr.dump
$NGS_cdhit_dir/clstr_list_sort.pl $JOBID.clstr.dump $JOBID.clstr_no.dump
$NGS_cdhit_dir/clstr_list_sort.pl $JOBID.clstr.dump $JOBID.clstr_len.dump len
$NGS_cdhit_dir/clstr_list_sort.pl $JOBID.clstr.dump $JOBID.clstr_des.dump des
gnuplot1.pl < $JOBID.fas.db2novel.clstr > $JOBID.fas.db2novel.clstr.1; gnuplot2.pl $JOBID.fas.db2novel.clstr.1 $JOBID.fas.db2novel.clstr.1.png
tar -zcf $JOBID.result.tar.gz * --exclude=*.dump --exclude=*.env
echo hello > $JOBID.ok
EOD

  my $sh_fname = "$JOBDIR/run-$JOBID.sh";
  open(SHELLFILE, "> $sh_fname");
  print SHELLFILE $cmd_str;
  close(SHELLFILE);
    
  #configuration file
  my $conf_fname = "$JOBDIR/$JOBID.conf";
  open(CONFILE, "> $conf_fname");
  print CONFILE "program=".$q->param("program")."\n";
  print CONFILE "level=1\n";
  print CONFILE "local=".$q->param("which_db1")."\n";
  print CONFILE "db1=$fh_db1\n";
  print CONFILE "db2=".$fh_db2."\n";
  print CONFILE "lc1=".$q->param("lc1")."\n";
  print CONFILE "parameters=$parameters\n";
  close(SHELLFILE);

	## env file
	$env_fname = "$JOBDIR/$JOBID.env";
	open(ENVFILE, "> $env_fname");
	print ENVFILE "PROGRAM = ".$q->param("program")."\n";
	#get date and time
	$dt_int = time;
	print ENVFILE "DATE_INT = ".$dt_int."\n";
	$dt_format = gmtime($dt_int);
	print ENVFILE "DATE = ".$dt_format."\n";
	foreach $key (sort keys(%ENV))
	{
		print ENVFILE "$key = $ENV{$key} \n";
	}
	#print ENVFILE $ENV('REMOTE_ADDR');
	close(ENVFILE);
	## end env file

  # submit the job
  #my $cmd = `/opt/gridengine/bin/lx26-amd64/qsub $sh_fname > $JOBDIR/$JOBID.qsub.dump`;
  my $cmd = `$qsub_exe $sh_fname 1>$JOBDIR/$JOBID.qsub.dump 2>$JOBDIR/$JOBID.qsub.err.dump`;

  # return jobid
  return $JOBID;
}

sub prepare_input{
  # prepare files and input for h-cd-hit or h-cd-est runs
  my $fh = $q->param('SeqF');
  # file handl for the input
  # create working directory and upload FASTA file
  my $JOBID = time();
  # use time to generate JOBID to avoid use a OLD id
  my $JOBDIR = "$SL_session_dir/$JOBID";
  while (-d $JOBDIR){ # an already exist JOBID, submitted at the same time
    sleep(5);
    $JOBID = time();
    $JOBDIR = "$SL_session_dir/$JOBID";
  }
  mkdir($JOBDIR);
  
  my $input_fname = "$JOBDIR/$JOBID.fas.0"; #upload sequence into $input_fname;
  open(UPLOADFILE, "> $input_fname");
  binmode(UPLOADFILE);
  my $ll;
  while ($ll=<$fh>) {print UPLOADFILE $ll;}
  close(UPLOADFILE);

  # create qsub script and configure files
  my $level = $q->param('level');
  my ($cmd_str, $iden, $wsize);
  $cmd_str .= <<EOD;
#!/bin/sh
#\$ -S /bin/bash
#\$ -v PATH=$SL_bin_dir:$ENV{'PATH'}
$qsub_local

#\$ -e $JOBDIR/$JOBID.err
#\$ -o $JOBDIR/$JOBID.out
cd $JOBDIR
sed -i "s/\\x0d/\\n/g" $JOBID.fas.0

faa_stat.pl $JOBID.fas.0

EOD

  my $i;
  for ($i=1; $i<=$level;$i++){
    my $im1 = $i-1;
    $iden = $q->param("lc$i");
    if ($iden >= 0.4){
      $wsize = get_wsize($iden);
      $cmd_str .= <<EOD;
$NGS_cdhit_dir/$program -i $JOBID.fas.$im1 -d 0 -o $JOBID.fas.$i -c $iden -n $wsize $parameters -T 4 -M 32000
EOD
    }
    elsif ($program eq 'cd-hit') { # use psi-cd-hit
      $cmd_str .=<<EOD;
$NGS_cdhit_dir/psi-cd-hit/psi-cd-hit.pl -i $JOBID.fas.$im1 -o $JOBID.fas.$i -c $iden -P $NGS_blast_dir -para 4
rm -rf $JOBID.fas.$im1-bl
EOD
    }
    $cmd_str .= <<EOD;
faa_stat.pl $JOBID.fas.$i
$NGS_cdhit_dir/clstr_sort_by.pl no < $JOBID.fas.$i.clstr > $JOBID.fas.$i.clstr.sorted
$NGS_cdhit_dir/clstr_list.pl $JOBID.fas.$i.clstr $JOBID.clstr.dump
gnuplot1.pl < $JOBID.fas.$i.clstr > $JOBID.fas.$i.clstr.1; gnuplot2.pl $JOBID.fas.$i.clstr.1 $JOBID.fas.$i.clstr.1.png
EOD
    $cmd_str .= <<EOD if  ($i == 2);
$NGS_cdhit_dir/clstr_rev.pl $JOBID.fas.1.clstr $JOBID.fas.2.clstr > $JOBID.fas.2-0.clstr
$NGS_cdhit_dir/clstr_sort_by.pl no < $JOBID.fas.2-0.clstr > $JOBID.fas.2-0.clstr.sorted
EOD
    $cmd_str .= <<EOD if ($i == 3);
$NGS_cdhit_dir/clstr_rev.pl $JOBID.fas.2-0.clstr $JOBID.fas.3.clstr > $JOBID.fas.3-0.clstr
$NGS_cdhit_dir/clstr_sort_by.pl no < $JOBID.fas.3-0.clstr > $JOBID.fas.3-0.clstr.sorted
EOD
  }
    
  $cmd_str .= <<EOD;
$NGS_cdhit_dir/clstr_list_sort.pl $JOBID.clstr.dump $JOBID.clstr_no.dump
$NGS_cdhit_dir/clstr_list_sort.pl $JOBID.clstr.dump $JOBID.clstr_len.dump len
$NGS_cdhit_dir/clstr_list_sort.pl $JOBID.clstr.dump $JOBID.clstr_des.dump des
EOD
  if ($level==1 && $q->param("anno")==1){ #for current version, only level 1 have annotion info incorporated
    $cmd_str .= <<EOD;
$NGS_cdhit_dir/FET.pl $JOBID.fas.1.clstr $JOBID.fas.1.clstr.anno $JOBID.fas.1.clstr.anno_len.dump 2>$JOBID.fas.1.clstr.anno.err
$NGS_cdhit_dir/FET.pl $JOBID.fas.1.clstr.sorted $JOBID.fas.1.clstr.sorted.anno $JOBID.fas.1.clstr.anno_no.dump 2>$JOBID.fas.1.clstr.sorted.anno.err
EOD
  }
  $cmd_str .= <<EOD;
tar -zcf $JOBID.result.tar.gz * --exclude=*.dump --exclude=*.env
echo hello > $JOBID.ok
EOD
  my $sh_fname = "$JOBDIR/run-$JOBID.sh";
  open(SHELLFILE, "> $sh_fname");
  print SHELLFILE $cmd_str;
  close(SHELLFILE);
    
  #configuration file
  my $conf_fname = "$JOBDIR/$JOBID.conf";
  open(CONFILE, "> $conf_fname");
  print CONFILE "program=".$q->param("program")."\n";
  print CONFILE "level=$level\n";
  print CONFILE "input=$fh\n";
  for ($i=1; $i<=$level; $i++){ print CONFILE "lc$i=".$q->param("lc$i")."\n"; }
  print CONFILE "parameters=$parameters\n";
  close(CONFILE);

	## env file
	$env_fname = "$JOBDIR/$JOBID.env";
	open(ENVFILE, "> $env_fname");
	print ENVFILE "PROGRAM = ".$q->param("program")."\n";
	#get date and time
	$dt_int = time;
	print ENVFILE "DATE_INT = ".$dt_int."\n";
	$dt_format = gmtime($dt_int);
	print ENVFILE "DATE = ".$dt_format."\n";
	foreach $key (sort keys(%ENV))
	{
		print ENVFILE "$key = $ENV{$key} \n";
	}
	#print ENVFILE $ENV('REMOTE_ADDR');
	close(ENVFILE);
	## end env file

  # submit the job
  my $cmd = `$qsub_exe $sh_fname 1>$JOBDIR/$JOBID.qsub.dump 2>$JOBDIR/$JOBID.qsub.err.dump`;

  # return jobid
  return $JOBID;
}


# decide word size based on seqence identity
sub get_wsize{
  my $iden = shift;
  if ($program eq 'cd-hit' or $program eq 'cd-hit-2d'){
    if    ( $iden >= 0.70 ) {return 5;}
    elsif ( $iden >= 0.60 ) {return 4;}
    elsif ( $iden >= 0.50 ) {return 3;}
    else                    {return 2;}
  }
  else{
    if    ( $iden >= 0.95 ) {return "10 -l 11";}
    elsif ( $iden >= 0.92 ) {return 9;}
    elsif ( $iden >= 0.90 ) {return 8;}
    elsif ( $iden >= 0.88 ) {return 7;}
    elsif ( $iden >= 0.85 ) {return 6;}
    elsif ( $iden >= 0.80 ) {return 5;}
    else                    {return 4;}
  }
}

# check parameters in the form
sub check_parameters{
  my $resu="";
  my $i;
  
  ###############
  # Data_Field
  if ( $q->param('program') eq 'cd-hit-2d' and $q->param('which_db1') eq '0' and $q->param('SeqDB1') eq ''){
    return "Error: please upload your search database in FASTA format";
  }
  if ( $q->param('program') eq 'cd-hit-est-2d' and $q->param('SeqDB1') eq ''){
    return "Error: please upload your search database in FASTA format";
  }
  if ( ($q->param('SeqF') eq '')){
    return "Error: please upload your sequences in FASTA format";
  }

  ###############
  # Iden_Field
  for ($i=1; $i<=$q->param('level'); $i++){
    if ($program eq 'cd-hit'){
      if (not ($q->param("lc$i") =~ /^\d+(\.\d+)?$/ and $q->param("lc$i")<=1 and $q->param("lc$i")>=0.1)){
        return "Error: -c of level $i for cd-hit or cd-hit-2d should be a float between 0.1 to 1";
      }
    }
    elsif ($program eq 'cd-hit-2d'){
      if (not ($q->param("lc$i") =~ /^\d+(\.\d+)?$/ and $q->param("lc$i")<=1 and $q->param("lc$i")>=0.4)){
        return "Error: -c of level $i for cd-hit or cd-hit-2d should be a float between 0.4 to 1";
      }
    }
    else{
      if (not ($q->param("lc$i") =~ /^\d+(\.\d+)?$/ and $q->param("lc$i")<=1 and $q->param("lc$i")>=0.75)){
        return "Error: -c of level $i for cd-hit-est or cd-hit-est-2d should be a float between 0.75 to 1";
      }
    }
  }

  for ($i=2; $i<=$q->param('level'); $i++){
    if ( $q->param("lc$i") >= $q->param("lc".($i-1)) ){
      return "Error: -c of level $i should be smaller than -c of level ".($i-1)
    }
  }

  ###############
  # Algo_Field
  if ($program eq 'cd-hit-est' or $program eq 'cd-hit-est-2d'){    $resu .= " -r ".$q->param('lr');  }
  $resu .= " -G ".$q->param('uG');
  $resu .= " -g ".$q->param('lg');

  if ($q->param('lb') =~ /^\d+$/){$resu .= " -b ".$q->param('lb'); }
  else{return "Error: -b should be an integer";}
  if ($q->param('ll') =~ /^\d+$/){$resu .= " -l ".$q->param('ll'); }
  else{return "Error: -l should be an integer";}

  ###############
  # Align_Field
  if ($q->param('ls') =~ /^\d+(\.\d+)?$/ and $q->param('ls') <= 1) { $resu .= " -s ".$q->param('ls'); }
  else { return "Error: -s should be a float between 0-1"; }

  if ($q->param('uS') =~ /^\d+$/ ){ $resu .= " -S ".$q->param('uS'); }
  elsif ($q->param('uS') ne 'unlimited'){ return "Error: -S should be an integer or unlimited";  }

  if ($q->param('lauL') =~ /^\d+(\.\d+)?$/ and $q->param('lauL') <=1) { $resu .= " -aL ".$q->param('lauL'); }
  else {return "Error: -aL should be a float between 0-1";}

  if ($q->param('uAuL') =~ /^\d+$/ ){ $resu .= " -AL ".$q->param('uAuL'); }
  elsif ($q->param('uAuL') ne 'unlimited'){ return "Error: -AL should be an integer or unlimited";  }

  if ($q->param('lauS') =~ /^\d+(\.\d+)?$/ and $q->param('lauS') <=1) { $resu .= " -aS ".$q->param('lauS'); }
  else {return "Error: -aS should be a float between 0-1";}

  if ($q->param('uAuS') =~ /^\d+$/ ){ $resu .= " -AS ".$q->param('uAuS'); }
  elsif ($q->param('uAuS') ne 'unlimited'){ return "Error: -AS should be an integer or unlimited";  }

  ###############
  # Length_Field
  
  if (defined($q->param('ls2'))){ # options used by cd-hit-2d or cd-hit-est-2d
    if ($q->param('ls2') =~ /^\d+(\.\d+)?$/ and $q->param('ls2') <=1) { $resu .= " -s2 ".$q->param('ls2'); }
    else { return "Error: -s2 should be a float between 0-1"; }
  }
  
  if (defined($q->param('uS2'))){ # options used by cd-hit-2d or cd-hit-est-2d
    if ($q->param('uS2') =~ /^\d+$/){ $resu .= " -S2 ".$q->param('uS2');}
    else { return "Error: -S2 should be an integer"; }
  }
  
  return $resu;
}
