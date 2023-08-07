#! usr/bin/env python

import os
import argparse
import sys
import re

##make parser for command line arguments
def create_arg_parser():
    # Creates and returns the ArgumentParser object

    parser = argparse.ArgumentParser(
                description='Small tool to parse and split data from fastqc output.')
    parser.add_argument('infile', type= argparse.FileType(mode='r'),
                    help='Path to the input file.')
    parser.add_argument('-o', '--outdir', nargs='?', default= None,
                    help='Path to output directory if alternate location to input file is desired. If the directory does not exist it will be made.')
    parser.add_argument('--fastaconvert', action='store_true',
                    help='Converts Overrepresented sequences text file into a fasta format file.')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.0',
                    help='Prints program version to screen.')
    return parser

##function to split fast_qc data by module into individual text files
def split_data(__infile__, __outdir__):
    #initialize mode variable. Program starts by searching for module headers
    #in read mode and then switches to write mode, outputting content to
    #sepparate text files. When it hits the >>END_MODULE marker it terminates
    #the current module type and returns to read mode to search for next
    #module header.
    mode = "read"
    type = "none"
    for line in __infile__.readlines():
        #read mode
        if mode == "read":
            #hit module header and switch modes
            if ((">>" in line) and ("END_MODULE" not in line)):
                mode = "write"
                type = (re.sub(r"(pass|fail|warn)", '', line.removeprefix(">>")).strip() )
                if parsed_args.verbose is not None:
                    print( "found start of %s! writing to file..." % type )
                #open module specific outfile
                __outfile__ = open(__outdir__ + "/" + re.sub(" ", "_", type) + ".txt", 'w' )
                continue
        #in write mode evaluates lines
        if mode == "write":
            #Hit end of module, closes out file and returns to read mode
            if (">>END_MODULE" in line):
                __outfile__.close()
                mode = "read"
                if parsed_args.verbose is not None:
                    print("%s information extracted!" % type)
                type= "none"
            #write output to designated outfile
            else:
                __outfile__.write( re.sub("#", '', line ) )
    #check just in case something broke
    if __outfile__.closed == False:
        __outfile__.close()
    __infile__.close()

##Function to extract sequences from Overrepresented sequences module and write
##them to a fasta format file to allow for use with bioinformatic tools.
def fasta_convert(__outdir__):
    __seqs__ = open(__outdir__ + "/Overrepresented_sequences.txt", 'r')
    __fasta__ = open(__outdir__ + "/Overrepresented_sequences.fasta", 'w')
    n= 0
    for line in __seqs__.readlines():
        if n ==  0:
            #skip header
            n+= 1
            continue
        __fasta__.write(">Overrepresented_sequences_%d\n" % n)
        __fasta__.write(line.split()[0] + "\n")
        n+=1
    __seqs__.close()
    __fasta__.close()

if __name__ == "__main__":
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])

    if parsed_args.verbose is not None:
        print("Being parsing of %s" % parsed_args.infile)

    if parsed_args.outdir is not None:
        if not os.path.exists(parsed_args.outdir):
            if parsed_args.verbose is not None:
                print("Specified outdir does not exist, creating outdir...")
            os.makedirs(parsed_args.outdir)

    if parsed_args.outdir is None:
        __outdir__= os.path.dirname(parsed_args.infile.name)
    else:
        __outdir__= parsed_args.outdir.rstrip("/")

    split_data(parsed_args.infile, __outdir__)

    if parsed_args.fastaconvert is not None:
        if parsed_args.verbose is not None:
            print("Fasta converter enabled. Generated Over represented sequences fasta...")
        fasta_convert(__outdir__)
        if parsed_args.verbose is not None:
            print("Overrepresented sequences fasta generated!")

    if parsed_args.verbose is not None:
        print("Process complete. Bye!")
