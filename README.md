# S3Extract - Square Product Development Division 3 PS1 File Extractor

# Overview

File extractor for the custom filesystem implementation used for the PlayStation 1 games developed by Square Product Development Division 3.

Supported games include
- Xenogears
- Chrono Cross
- Dewprism ( Threads of Fate )

# Usage
Extract the filesystem contained within the .BIN file for retails copies of Xenogears, Chrono Cross and Dewprism / Threads of Fate.

```main.py -b *.BIN```

Extract the filesystem contained within the .IMG file found in demo copies of Chrono Cross and Dewprism / Threads of Fate.

```main.py -hei *.HED *.EXE *.IMG```

Extract the filesystem contained within the .IMG file found in the 1997 Taikenban demo of Xenogears.

```main.py -ei *.EXE *.IMG```

# Project Structure
```
S3Extract
│   debug_args.py         - Debug Dictionary of input files when developing.
│   def_square_file.py    - Definitions for all the different structures used in Square entries.
│   extract.py            - Main file extractor logic.
│   id_hash_bin.py        - Identifiers using hashes for .BIN files.
│   id_hash_img.py        - Identifiers using hashes for .IMG files.
│   main.py               - CLI Tool for extracting Square filesystems.
│   mod_binary_reader.py  - Module with defs to make reading binary data easier.
│   mod_color.py          - Module for adding colored text output to the Windows terminal.
│   README.md             - You are reading this.
│   square_file_system.py - Classes for handling the file entries and filesystem.
│   tf_ext_guess.py       - File Entry transformer for guessing file extension based on pattern matching.
│   tf_hash.py            - File Entry transformer by matching hash of the file contents.
│   tf_index.py           - File Entry transformer by matching index in a index file.
│
├───data     - .csv files containing metadata as used by the transformers.
│
├───scripts  - Misc python files for small tasks
│       extract_fnd.py       - Small script for extracting the .fnd file found in PC release of Chrono Cross: The Radical Dreamers Edition
└       extract_load_data.py - Small script for extracting the file io reads from the log files copy pasted out of PCSX-Redux output
```

# Transformer Based Naming
The following challenges apply when extracting the filesystem
- No file name
- No file extension
- No folder structure ( Only Xenogears allows a file entry to act as a parent folder )
- Duplicates of the same file ( Loading optimization? )

The only exception is Chrono Cross where over 95% of the original folder and name structure
was able to be restored thanks to the debug files `cdrom.fnd` and `cdrom2.fnd` left over in the PC release of `Chrono Cross: The Radical Dreamers Edition`.

To solve this problem, naming is based on transformers to help annotate file entries.

If a file entry passes the transformers check metadata will be applied to that file when exported.
A transformer can provide one of, or all of the following...
- File name
- File extension
- Folder path

Multiple transformers are implemented to use a priority based approach to naming files. Higher priority transformers are chosen over lower.

1. Index - If there is a index file for the given game version, use the metadata provided.
2. Hash - Mainly used for duplicate files, if the hash of the file entry is found in the hashmap leverage the metadata provided
3. Extension Guess - When all else fails, a hueristic guess on what the file format is based on patterns in the file is used to give a rough estimate of what the file type could be.

# Credits
Thanks to Nocash for documenting the filesystem as described in the `Nocash PSXSPX Playstation Specifications` here
https://problemkaputt.de/psxspx-cdrom-file-archives-in-hidden-sectors.htm

Thanks to the Chrono Compendium for their documentation of the Chrono Cross files as described here
http://www.chronocompendium.com:8000/Term/Chrono_Cross_File_Structure.html