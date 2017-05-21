$NGS_cdhit_dir = "/home/oasis/data/NGS-ann-project/apps/cd-hit";
$NGS_blast_dir = "/home/oasis/data/NGS-ann-project/apps/bin";
$SL_session_dir     = "/home/oasis/data/webcomp/web-session";
$SL_rammcap_dir     = "/home/oasis/data/webcomp/RAMMCAP-ann";
$SL_bin_dir         = "$SL_rammcap_dir/bin";

$qsub_exe = "/opt/sge6/bin/linux-x64/qsub";
$admin_email = "liwz\@sdsc.edu";
$sw_db = "/home/oasis/data/webcomp/RAMMCAP-ann/database/swissprot";
$pdb_db = "/home/oasis/data/webcomp/RAMMCAP-ann/database/pdbaa";

$qsub_local = <<EOD;
#\$ -v BLASTMAT=/home/oasis/data/webcomp/RAMMCAP-ann/blast/bin/data
#\$ -v LD_LIBRARY_PATH=/home/oasis/data/webcomp/RAMMCAP-ann/gnuplot-install/lib
#\$ -v PERL5LIB=/home/hying/programs/Perl_Lib
#\$ -q all.q
#\$ -pe orte 4
EOD
