use CGI::Pretty qw(:standard *table);
#use CGI;
use Time::Local;
use Switch;

my $help_image = {-src=>"../css/images/help.gif", -border=>"0", -alt=>"."};
my $whole_width = "900";
my $table_l1 = "500";


sub print_header{
  print   header("text/html"),
    start_html(-title=>"CD-HIT Suite",
               -style=>{-src=>"../css/main.css"},
               -script=>{-language=>"javascript",-src=>"../js/util.js"},
               -bgcolor=>"grey"),
    br, br,
    start_table({-style=>"border-bottom: 1px solid rgb(128, 128, 128);", -align=>"center", -bgcolr=>"#f0-f8ff", -width=>$whole_width}),
    Tr(
      td({-style=>"border-bottom: 1px solid rgb(161, 161, 161);",-bgcolor=>"#dff0ff",-height=>"80"},
        table({-align=>"center",-width=>"90%"},
          Tr([ td(font({-size=>"+2"},"CD-HIT Suite: Biological Sequence Clustering and Comparison")) ])
        )
      )
    ),
    end_table();
}

sub print_content{
  my $cmd = shift;
  my $JOBID = shift;
  print start_table({-style=>"border-bottom: 1px solid rgb(128, 128, 128);", -align=>"center", -bgcolr=>"#f0-f8ff", -width=>$whole_width}),
          Tr([
            td({-align=>"center",-valign=>"top",-bgcolor=>"white"},
                br
                .div({-class=>"menu1box"}, menu_list($cmd))
                .div({-class=>"main1box"}, main_content($cmd, $JOBID).br)
                .br
              )
          ]),
        end_table();
}


sub main_content{
  my $cmd = shift;
  my $JOBID = shift;
  if ($cmd eq "Server home"){

  my $intro_txt = <<EOD;

CD-HIT package can perform various jobs like clustering a protein database,
clustering a DNA/RNA database, comparing two databases (protein or DNA/RNA), and
generating protein families. 
More infomation is available at <a href="http://cd-hit.org">CD-HIT home page.</a>
EOD
  my $li_cdhit = "cd-hit";
  my $li_cdhit_txt = <<EOD;
CD-HIT clusters proteins that meet a similarity threshold, usually
a sequence identity. Each cluster has one representative sequence. The input is a protein
dataset in fasta format. It generates a fasta file of representative sequences
and a text file of list of clusters.
EOD
  my $li_cdhitest = "cd-hit-est";
  my $li_cdhitest_txt = <<EOD;
CD-HIT-EST clusters a nucleotide sequences that meet a similarity threshold, usually
a sequence identity. The input is a DNA/RNA dataset in fasta format
It generates a fasta file of representative sequences
and a text file of list of clusters. It can not be used for very long sequences, like full genomes.
EOD
  my $li_hcdhit = "h-cd-hit";
  my $li_hcdhit_txt = <<EOD;
Multiple CD-HIT runs. Proteins are first clustered at a high identity (like 90%), the non-redundant sequences
are further clustered at a low identity (like 60%). A third cluster can be performed at lower identity.
Multi-step run is more efficient and more accurate than a single run.
EOD
  my $li_hcdhitest = "h-cd-hit-est";
  my $li_hcdhitest_txt = <<EOD;
Multiple CD-HIT-EST runs.
EOD
  my $li_cdhit2d = "cd-hit-2d";
  my $li_cdhit2d_txt = <<EOD;
CD-HIT-2D compares 2 protein datasets (db1, db2). It identifies the sequences in db2 that
are similar to db1 at a certain threshold. The input are two protein datasets (db1, db2) in
fasta format and the output are two files: a fasta file of proteins in db2 that are not similar
to db1 and a text file that lists similar sequences between db1 & db2.
EOD
  my $li_cdhitest2d = "cd-hit-est-2d";
  my $li_cdhitest2d_txt = <<EOD;
Like CD-HIT-2D, CD-HIT-EST-2D compares 2 nucleotide datasets.
For same reason as CD-HIT-EST, CD-HIT-EST-2D is not good for very long sequences.
EOD
  my $li_result_txt = <<EOD;
Retrieve the result of you previous submitted jobs, download sample datasets, or view sample results.
EOD
  my $li_ftp_txt = <<EOD;
Use our FTP site to download pre-calcualted sequence
clusters for some popular databases, like NR, Swissprot and PDB
EOD
  my $li_server_txt = <<EOD;
We are glad if this server can help your research. Although cd-hit is very fast, but clustering is 
still very computationally intensive. We currently limit the file upload size to 100MB. cd-hit run slower with 
a low identity cutoff, we further limit the upload size to 20MB if the clustering cutoff is <60% identity
for protein sequences. 
We intent to increase the limit because we will upgrade our computer cluster. 
Also we provided pre-calcualted clusters from our FTP site. If you need to cluster larger dataset, please
contact us. 

<P>
We recommand that you download the zipped file after the job finished. We will delete
the jobs older than 90 days to save disk space.
<P>
Thank you for your understanding.
EOD
    return  
      br.div({-class=>"para"}, $intro_txt.br.br,
        ul( 
        li(font({-size=>"+2"},a({-href=>"index.cgi?cmd=cd-hit"},       $li_cdhit   )),  ul(li($li_cdhit_txt     .br.br))), 
        li(font({-size=>"+2"},a({-href=>"index.cgi?cmd=cd-hit-est"},   $li_cdhitest)),  ul(li($li_cdhitest_txt  .br.br))),
        li(font({-size=>"+2"},a({-href=>"index.cgi?cmd=h-cd-hit"},     $li_hcdhit)),    ul(li($li_hcdhit_txt    .br.br))),
        li(font({-size=>"+2"},a({-href=>"index.cgi?cmd=h-cd-hit-est"}, $li_hcdhitest)), ul(li($li_hcdhitest_txt .br.br))),
        li(font({-size=>"+2"},a({-href=>"index.cgi?cmd=cd-hit-2d"},    $li_cdhit2d)),   ul(li($li_cdhit2d_txt   .br.br))),
        li(font({-size=>"+2"},a({-href=>"index.cgi?cmd=cd-hit-est-2d"},$li_cdhitest2d)),ul(li($li_cdhitest2d_txt.br.br))),
        li(font({-size=>"+2"},a({-href=>"index.cgi?cmd=result"},       "result")),      ul(li($li_result_txt    .br.br))),
        li(font({-size=>"+2"},a({-href=>"index.cgi?cmd=calculated%20clusters"},"calculated clusters")), ul(li($li_ftp_txt .br.br))),
        li(font({-size=>"+2"},"server usage"),                                                          ul(li($li_server_txt .br.br)))
        ));
  }

  if ($cmd eq "calculated clusters"){
    return  br.br.div({-class=>"para"}, "<center>".font({-size=>"+3"}, "cdhit ftp")."</center>".br.br,
      ul(li(font({-size=>"+2"},a({-href=>"ftp://weizhong-lab.ucsd.edu/data"},"calculated clusters ftp")))));
  }

  if ($cmd eq "result"){
    if ($JOBID eq 0){
      my $sample_txt=<<EOD;

<Font color="red">
Results older than 180 days will be removed from the server to save disk space!
</Font>

<HR>
<B><font size=+2>Samples</font></B><BR>
Sample protein dataset:<BR> 
<A href="http://weizhong-lab.ucsd.edu/cdhit_suite/output/test1/test1.fas.0">download data</A>,
<A href="http://weizhong-lab.ucsd.edu/cdhit_suite/cgi-bin/result.cgi?JOBID=test1">view results 
by h-cd-hit at three levels: 90%, 60% and 30%</A> <P>

Sample protein dataset with annotation term:<BR>
This dataset contains proteins annotated with COG family. the defline of 
this fasta file looks like ">AF0017_1||COG1250" where the COG family ID is appended
after ">sequence_name||".
<A href="http://weizhong-lab.ucsd.edu/cdhit_suite/output/test4/test4.fas.0">download data</A>,
<A href="http://weizhong-lab.ucsd.edu/cdhit_suite/cgi-bin/result.cgi?JOBID=test4">view results 
by cd-hit clustered at 60% identity</A> <P>

Sample DNA dataset:<BR>
<A href="http://weizhong-lab.ucsd.edu/cdhit_suite/output/test3/test3.fas.0">download data</A>,
<A href="http://weizhong-lab.ucsd.edu/cdhit_suite/cgi-bin/result.cgi?JOBID=test3">view results by cd-hit-est at 95%</A> <P>

Sample DNA dataset with annotation term:<BR>
This dataset contains microbial rRNAs annotated with Taxonomy ID at genus rank, the defline of
this fasta file looks like ">NC_009925__1405528_1405648_5S||genus_taxid_15597", where the Taxonomy ID is appended
after ">sequence_name||".  
<A href="http://weizhong-lab.ucsd.edu/cdhit_suite/output/testRNA1/testRNA1.fas.0">download data</A>,
<A href="http://weizhong-lab.ucsd.edu/cdhit_suite/cgi-bin/result.cgi?JOBID=testRNA1">view results by 
cd-hit-est clustered at 95% identity</A> <P>

EOD
      return start_form({-id=>"myform",-action=>"cdhit.cgi",-method=>"post",-enctype=>"multipart/form-data"})
             .hidden({-name=>"program",-value=>$cmd})
             .div({-class=>"para"}, "Please input your job id to retrive the running result:"
                  ,textfield(-name=>"JOBID", -size=>"16", -value=>""), submit(-name=>"sub", -value=>"Submit", -style=>"font-size:120%"))
             .end_form(). div({-class=>"para"}, $sample_txt);
      }
    else {
      return start_form({-id=>"myform",-action=>"cdhit.cgi",-method=>"post",-enctype=>"multipart/form-data"})
             .hidden({-name=>"program",-value=>$cmd})
             .div({-class=>"para"}, iframe({-src=>"result.cgi?JOBID=$JOBID", -width=>"100%", -height=>"600"},"hello"))
             .end_form();
    }
  }

  my $Fields;
  if ($cmd eq "cd-hit-2d" or $cmd eq "cd-hit-est-2d"){
     $Fields = div({-class=>"para"},br, Data_Field($cmd),br,Iden_Field($cmd),br,Algo_Field($cmd),br,Align_Field($cmd),br,Length_Field($cmd),br,Mail_Field($cmd));
  }
  else{
     $Fields = div({-class=>"para"},br, Data_Field($cmd),br,Iden_Field($cmd),br,Algo_Field($cmd),br,Align_Field($cmd),br,Mail_Field($cmd));
  } 

  return start_form({-id=>"myform",-action=>"cdhit.cgi",-method=>"post",-enctype=>"multipart/form-data"})
         .hidden({-name=>"program",-value=>$cmd})
         .$Fields
         .div({-class=>"para_sub", -align=>"center"}, 
         submit(-name=>"sub", -value=>"Submit", -style=>"font-size:120%"), 
              "&nbsp;&nbsp;&nbsp;&nbsp;",
              reset(-name=>"clear",-value=>"Clear",-style=>"font-size:120%"))
         .end_form();
}
          
sub print_tail{
  print table({-style=>"border-bottom: 1px solid rgb(128, 128, 128);",-align=>"center",-width=>$whole_width},
          Tr({-bgcolor=>"#dff0ff"},[
            td(div({-class=>"para"}, "<center><b>Reference:</b></center>",
              ol(li('Ying Huang, Beifang Niu, Ying Gao, Limin Fu and Weizhong Li. '
                     ."CD-HIT Suite: a web server for clustering and comparing biological sequences. "
                     ."Bioinformatics, 2010(26): 680-682.".a({-href=>"http://bioinformatics.oxfordjournals.org/content/26/5/680"},"full text")),
                 li('Weizhong Li and Adam Godzik. '
                     ."Cd-hit: a fast program for clustering and comparing large sets of protein or nucleotide sequences. "
                     ."Bioinformatics, 2006(22): 1658-1659. ".a({-href=>"http://bioinformatics.oxfordjournals.org/cgi/content/full/22/13/1658"},"full text")),
                 li('Weizhong Li, Lukasz Jaroszewski and Adam Godzik. '
                     ."Tolerating some redundancy significantly speeds up clustering of large protein databases. "
                     ."Bioinformatics, 2002(18): 77-82. ".a({-href=>"http://bioinformatics.oxfordjournals.org/cgi/reprint/18/1/77"},"full text")),
                 li('Weizhong Li, Lukasz Jaroszewski and Adam Godzik. '
                     ."Clustering of highly homologous sequences to reduce the size of large protein databases. "
                     ."Bioinformatics, 2001(17): 282-283. ".a({-href=>"http://bioinformatics.oxfordjournals.org/cgi/reprint/17/3/282"},"full text"))
                 ))),
            td({-align=>"center",-bgcolor=>"#dff0ff",-height=>"50"},
                'Contact @<a href="mailto:liwz@sdsc.edu"><u>Weizhong Li</u></a>')
            ]) 
          );

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

</BODY>

EOD
}

sub Length_Field{
# this is a field specific to 2d comparison
  my $mcd = shift;
  return fieldset({-id=>"LenPara"}, legend("Length Control Parameters"),
           table(Tr( td({-width=>$table_l1}, "Length difference cutoff (fraction)".help_object('ls2'))
                     .td(textfield(-name=>"ls2", -size=>"4", -value=>"1.0"))),
                 help_box("ls2", "length difference cutoff, default 1.0.
                         by default, the length of seqs in db1 >= seqs in db2 in the same cluster.
                         if set to 0.9, the length of seqs in db1 may only need to be >= 0.9 x seq lengthes in db2"),
                 Tr( td({-width=>$table_l1}, "Length difference cutoff (amino acids/bases)".help_object('uS2'))
                     .td(textfield(-name=>"uS2", -size=>"4", -value=>"0"))),
                 help_box("uS2", "length difference cutoff, default 0.
                         by default, the length of seqs in db1 >= seqs in db2 in the same cluster.
                         if set to 60, seqs in db2 may be up to 60 amino acid/bases longer than seqs in db1")
         
           )
         );
}
        

sub Data_Field{
  my $cmd = shift;
  my @columns = ();
#  push @columns, td("Load Fasta file from your computer:".filefield({-name=>"SeqF"}));
#  push @columns, td("Click ".a({-href=>"#"},"here")." for an example file");
  
  if ($cmd eq "cd-hit-2d"){
    push @columns, td("CD-HIT-2D compares 2 protein datasets (db1, db2). It identifies the sequences in db2 that
                            are similar to db1 at a certain threshold.".br);
    push @columns, td("<b>Choose db1</b>");
    push @columns, td("&nbsp;&nbsp;&nbsp;&nbsp;"#<input name='which_db1' type='radio' checked='checked' value='0'>"
                    ."Load  search database (in Fasta format) :"
                    ."<input name='SeqDB1' type='file'>"); # onchange='document.forms[0].elements[\"which_db1\"][0].checked=\"checked\";'>");
#    push @columns, td("&nbsp;&nbsp;&nbsp;&nbsp;<input name='which_db1' type='radio' value='1'>"
#                    ."Use a commonly used sequence database:"
#                    ."<select onchange='document.forms[0].elements[\"which_db1\"][1].checked=\"checked\"' name='LocalDB1'>"
#                    ."<option value='NR' selected='selected'>NR</option><option value='SWISSPROT'>SWISSPROT</option><option value='PDB'>PDB</option></select>");
    push @columns, td("<b>Choose db2</b>");
  }
  elsif ($cmd eq "cd-hit-est-2d"){
    push @columns, td("CD-HIT-EST-2D compares 2 nucleotide datasets (db1, db2). It identifies the sequences in
                            db2 that are similar to db1 at a certain threshold.");
    push @columns, td("<b>Choose db1</b>");
    push @columns, td("&nbsp;&nbsp;&nbsp;&nbsp;"#<input name='which_db1' type='radio' checked='checked' value='0'>"
                    ."Load  search database (in Fasta format) :"
                    ."<input name='SeqDB1' type='file'>");
#    push @columns, td("&nbsp;&nbsp;&nbsp;&nbsp;<input name='db2' type='radio' value='1'>"
#                    ."Use a commonly used sequence database:"
#                    ."<select name='level' onchange='document.forms[0].elements[\"db2\"][1].checked=\"checked\"' name='LocalDB2'>"
#                    ."<option value='NT' selected='selected'>NT</option><option value='ENV_NT'>ENV_NT</option></select>");
    push @columns, td("<b>Choose db2</b>");
  }
#    push @columns, td("<b>Choose db2</b>");
    push @columns, td("&nbsp;&nbsp;&nbsp;&nbsp;Load Query Fasta file from your computer:".filefield({-name=>"SeqF"}));
    if ($cmd eq "cd-hit" || $cmd eq "cd-hit-est"){
        push @columns, td("&nbsp;&nbsp;&nbsp;&nbsp;<input name='anno' type='checkbox' value='1'>
                        &nbsp;&nbsp;Incorporate annotation info at header line".help_object('anno'));
        push @columns, help_box("anno", "If this option is checked, the header lines of the input fasta file
                        should have format: '>SequenceID||term1,term2', here term1, term2 is the function
                        annotation of corresponding input sequence, seperated by comma (no space). The user can leave 
                        it blank if the sequence has not been annotated. You can click result tab for sample data.");
    }

    return fieldset({-id=>"DataPara"}, legend("Sequence file and databases".help_object('File_Size')),table( help_box("File_Size", "In current version, the maximu size
                of uploaded files is 50MB"), Tr(\@columns)));
}


sub Iden_Field{
  my $cmd = shift;
  if ($cmd eq "h-cd-hit" or $cmd eq "h-cd-hit-est"){
    return fieldset({-id=>"IdenPara"}, legend("Sequence Identity Parameters"),
             table(
               Tr(td({-width=>$table_l1}, "Number of CD-HIT runs".help_object('BasicHelp'))
                 .td(popup_menu(-name=>"level",-onchange=>"SetIden()",-values=>["1","2","3"], -labels=>{"1"=>"1","2"=>"2","3"=>"3"}, -default=>"1"))
               ),
               help_box("BasicHelp", "try basic help"),
               Tr(td({-width=>$table_l1}, "<input id='y1' type='radio' checked='checked' disabled>"
                   ."Sequence identity cut-off for 1st run".help_object('Iden1')).td(iden_text("1"))
               ),
               help_box("Iden1", "Sequence identity cut-off for 1st run, should be a float between 0 to 1"),
               Tr(td({-width=>$table_l1}, "<input id='y2' type='radio' disabled>"
                   ."Sequence identity cut-off for 2nd run".help_object('Iden2')).td(iden_text("2"))
               ),
               help_box("Iden2", "Sequence identity cut-off for 2nd run, should be a float between 0 to cut-off for 1st run"),
               Tr(td({-width=>$table_l1}, "<input id='y3' type='radio' disabled>"
                                     ."Sequence identity cut-off for 3rd run".help_object('Iden3')).td(iden_text("3"))
               ),
               help_box("Iden3", "Sequence identity cut-off for 3rd run, should be a float between 0 to cut-off for 2nd run")
             )
          );
  }
  else{
    return  fieldset({-id=>"IdenPara"}, legend("Sequence Identity Parameters"),
              hidden({-name=>"level",-value=>"1"}),
              table(
                Tr(td({-width=>$table_l1}, "<input id='y1' type='radio' checked='checked' disabled>"
                  ."Sequence identity cut-off".help_object('Iden1')).td(iden_text("1"))
                ),
                help_box("Iden1", "Sequence identity cut-off should be a float between 0 to 1, 0.9 means 90% identity")
              )
    );
  }
}



sub Algo_Field{
  my $cmd = shift;
  my @columns = ();
  if ($cmd eq "cd-hit-est" or $cmd eq "h-cd-hit-est" or $cmd eq "cd-hit-est-2d"){
    push @columns, Tr(td({-width=>$table_l1}, "-r: comparing both strands".help_object('Both'))
                      .td("<input name='lr' value='0' type='radio' checked='checked'>No<input name='lr' value='1' type='radio'>Yes")
                     );
    push @columns, help_box("Both", "Whether reverse complementary strand of the nucleotides should be included in comparison?");
  }
  
  push @columns, Tr(td({-width=>$table_l1}, "-G: use global sequence identity".help_object('Global'))
                   .td("<input name='uG' value='0' type='radio'>No<input name='uG' value='1' type='radio' checked='checked'>Yes")
                   );
  push @columns, help_box("Global", "Use global sequence identity or local sequence identity, local sequence identity was calculated as :
                           number of identical amino acids in alignment divided by the length of the alignment");
  push @columns, Tr(td({-width=>$table_l1}, "-g: sequence is clustered to the best cluster that meet the threshold".help_object('Similar'))
                   .td("<input name='lg' value='0' type='radio'>No<input name='lg' value='1' type='radio' checked='checked'>Yes")
                   );
  push @columns, help_box("Similar", "By cd-hit's default algorithm, a sequence is clustered to the first cluster that meet the threshold (fast mode). 
                           If set to yes, the program will cluster it into the most similar cluster that meet the threshold (accurate but slow mode)");
  push @columns, Tr(td({-width=>$table_l1}, "-b: bandwidth of alignment".help_object("Alignment"))
                   .td(textfield(-name=>"lb", -size=>"4", -value=>"20")));
  push @columns, help_box("Alignment", "Band width of alignment, should be a positive integer");
  
  return fieldset({-id=>"AlgoPara"}, legend("Algorithm Parameters"), table( join(" ",@columns)));
}  



sub Align_Field{
  return
    fieldset({-id=>"AlignPara"}, legend("Alignment Coverage Parameters".help_object('Coverage')),
      table(
        Tr({-style=>"display:none", -id=>"Coverage"}, 
          td("<div  class='helpbox'><img src='../css/images/coverage.gif' border='0' alt='.' width='100%'>
              <font size='+1'>
              aL = R<sub>a</sub> / R, AL = R- R<sub>a</sub> <br>  aS = S<sub>a</sub> / S, AS = S- S<sub>a</sub> <br>
              s = S<sub>a</sub> /  R<sub>a</sub>, S = R - S</font></div>")),
        Tr([
          td({-width=>$table_l1}, "-aL: minimal alignment coverage (fraction) for the longer sequence")      .td(textfield(-name=>"lauL", -size=>"6", -value=>"0.0")), 
          td({-width=>$table_l1}, "-AL: maximum  unaligned part (amino acids/bases) for the longer sequence") .td(textfield(-name=>"uAuL", -size=>"6", -value=>"unlimited")),
          td({-width=>$table_l1}, "-aS: minimal alignment coverage (fraction) for the shorter sequence")     .td(textfield(-name=>"lauS", -size=>"6", -value=>"0.0")), 
          td({-width=>$table_l1}, "-AS: maximum  unaligned part (amino acids/bases) for the shorter sequence").td(textfield(-name=>"uAuS", -size=>"6", -value=>"unlimited")), 
          td({-width=>$table_l1}, "-s:  minimal length similarity (fraction)")                               .td(textfield(-name=>"ls",   -size=>"6", -value=>"0.0")), 
          td({-width=>$table_l1}, "-S:  maximum  length difference in amino acids/bases(-S)")                 .td(textfield(-name=>"uS",   -size=>"6", -value=>"unlimited"))
        ])
      )
    );
}

## for sending job stat link: added by Beifang Niu
sub Mail_Field{
  return fieldset({-id=>"Mail"}, legend("Mail address for job checking".help_object('Mailnotice')),
         table( Tr({-style=>"display:none", -id=>"Mailnotice"}, 
           td("<div  class='helpbox'> Your job running stat link will be sent to your mail box")), 
           Tr([ td({-width=>$table_l1}, "Give your mail address: ".textfield(-name=>"Mailaddress", -size=>"25", -value=>" "))])
         ));
}


sub help_object{
  return a({-href=>"javascript: toggle('".$_[0]."')"}, img($help_image));
}

sub help_box{
  return Tr({-style=>"display:none",-id=>$_[0]}, td(div({-class=>"helpbox"}, $_[1])));
}

sub iden_text{
  return textfield(-name=>"lc$_[0]", -size=>"4", -value=>"0.9");
}

sub menu_list{
  my $cmd = shift;
  my $relative_url  = url(-relative=>1);
  my @cmds = ('Server home', 'cd-hit', 'cd-hit-est', 'h-cd-hit', 'h-cd-hit-est', 'cd-hit-2d', 'cd-hit-est-2d', 'result','calculated clusters');
  my @li_list = ();
  foreach (@cmds){
    my $lab = $_; 
    if ($_ eq $cmd){
      push @li_list, li({-class=>"hover"},a({-href=>"$relative_url?cmd=$_"}, $lab));
    }
    else{
      push @li_list, li(a({-href=>"$relative_url?cmd=$_"}, $lab));
    }
  }
  return  ul({-id=>"menu1"}, join(" ",@li_list));
}
