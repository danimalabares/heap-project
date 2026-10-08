# Project latexmk configuration for the Heap Project.
#
# Every HP document reads the .aux files of the
# other documents through xr-hyper.  When several
# documents are compiled at the same time (for
# example with `latexmk -pvc`), one pdflatex run
# could read another document's .aux while that
# file was being rewritten, and fail with
# "File ended within \read".
#
# To avoid this, after each pdflatex pass we
# publish a snapshot of the .aux file in
# tmp/xref/ by writing a temporary file and
# renaming it, which is atomic.  preamble.tex
# reads these snapshots instead of the live .aux
# files.  A snapshot is only published when the
# .aux file is complete, i.e. when its last line
# is the \gdef \@abspage@last{...} line that
# LaTeX writes at \end{document}.

use File::Basename qw(fileparse);
use File::Compare qw(compare);
use File::Copy qw(copy);
use File::Path qw(make_path);

$pdf_mode = 1;
$pdflatex = 'internal hp_pdflatex pdflatex %O %S';

sub hp_pdflatex {
    my @cmd = @_;
    my $status = system(@cmd);
    hp_publish_aux($cmd[-1]);
    return $status;
}

sub hp_publish_aux {
    my ($source) = @_;
    my ($base) = fileparse($source, qr/\.[^.]*/);
    my $dir = $aux_dir || $out_dir || '.';
    my $aux = "$dir/$base.aux";
    return unless hp_aux_complete($aux);

    my $xref = 'tmp/xref';
    make_path($xref) unless -d $xref;
    my $target = "$xref/$base.aux";
    return if -e $target && compare($aux, $target) == 0;

    my $tmp = "$xref/.$base.aux.$$";
    if (copy($aux, $tmp) && rename($tmp, $target)) {
        return;
    }
    unlink $tmp;
    warn "hp_publish_aux: could not publish $target: $!\n";
}

sub hp_aux_complete {
    my ($aux) = @_;
    open(my $fh, '<', $aux) or return 0;
    my $last = '';
    while (my $line = <$fh>) {
        $last = $line if $line =~ /\S/;
    }
    close $fh;
    return $last =~ /^\\gdef \\\@abspage\@last\{\d+\}\s*$/;
}
