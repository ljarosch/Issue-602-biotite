# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

__author__ = "Patrick Kunzmann"
__all__ = ["ClustalOmegaApp"]

from ..msaapp import MSAApp
from ..application import AppState, requires_state
from ...sequence.sequence import Sequence
from ...sequence.seqtypes import NucleotideSequence, ProteinSequence
from ...sequence.io.fasta.file import FastaFile
from ...sequence.align.alignment import Alignment


class ClustalOmegaApp(MSAApp):
    """
    Perform a multiple sequence alignment using Clustal-Omega.
    
    Parameters
    ----------
    sequences : iterable object of ProteinSequence or NucleotideSequence
        The sequences to be aligned.
    bin_path : str, optional
        Path of the Custal-Omega binary.
    
    Examples
    --------

    >>> seq1 = ProteinSequence("BIQTITE")
    >>> seq2 = ProteinSequence("TITANITE")
    >>> seq3 = ProteinSequence("BISMITE")
    >>> seq4 = ProteinSequence("IQLITE")
    >>> app = ClustalOmegaApp([seq1, seq2, seq3, seq4])
    >>> app.start()
    >>> app.join()
    >>> alignment = app.get_alignment()
    >>> print(alignment)
    -BIQTITE
    TITANITE
    -BISMITE
    --IQLITE
    """
    
    def __init__(self, sequences, bin_path="clustalo"):
        if isinstance(sequences[0], NucleotideSequence):
            self._seqtype = "DNA"
        else:
            self._seqtype = "Protein"
        super().__init__(sequences, bin_path)
    
    def run(self):
        self.set_arguments(
            ["--in", self.get_input_file_path(),
             "--out", self.get_output_file_path(),
             "--seqtype", self._seqtype,
             # Tree order for get_alignment_order() to work properly 
             "--output-order=tree-order"]
        )
        super().run()
