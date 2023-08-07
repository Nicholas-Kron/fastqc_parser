# fastqc_parser
A little script that takes the output of the read quality control tool [FastQC](https://github.com/s-andrews/FastQC) and splits it so that each module has its own output text file. Optionally, can also convert the `overrepresented sequences` module into a fasta file, mostly to use as input for BLAST.

usage:

```
fastqc_parser.py [-h] [-o [OUTDIR]] [--fastaconvert] [-v] [--version] infile
```

options:

  ```
  -h, --help            show this help message and exit
  -o [OUTDIR], --outdir [OUTDIR]
                        Path to output directory if alternate location to input file is desired. If the directory does not exist it will be made.
  --fastaconvert        Converts Overrepresented sequences text file into a fasta format file.
  -v, --verbose         
  --version             Prints program version to screen.
  ```

  Example usage:
  
  ```
  #generate fastqc report for fastq file.
  fastqc my_file.fastq
  unzip my_file_fastqc.zip

  ##OR##
  
  #generate fastqc report for fastq file. Set --extract flag to have results file available for immediate processing. 
  fastqc --extract my_file.fastq

  #extract modules from fastqc data directory. 
  python fastqc_parser.py my_file_fastqc/fastqc_data.txt
  ```

  which gives the following output:
  
  ```
  my_file_fastqc/Adapter_Content.txt
  my_file_fastqc/Basic_Statistics.txt
  my_file_fastqc/Overrepresented_sequences.txt
  my_file_fastqc/Per_base_N_content.txt
  my_file_fastqc/Per_base_sequence_content.txt
  my_file_fastqc/Per_base_sequence_quality.txt
  my_file_fastqc/Per_sequence_GC_content.txt
  my_file_fastqc/Per_sequence_quality_scores.txt
  my_file_fastqc/Per_tile_sequence_quality.txt
  my_file_fastqc/Sequence_Duplication_Levels.txt
  my_file_fastqc/Sequence_Length_Distribution.txt
  ```
