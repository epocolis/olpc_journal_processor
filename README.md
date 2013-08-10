This script allows you to extract Journal metadata from a Sugar Journal backup or several journal backups. These are usually found on the OLPC XS School Server under /library/users/


Running the script:
#####################

The scripts expects the directory structure to be "ROOT_DIRECTORY/users/*/*/*/*/metadata/*"

At the terminal prompt run the script by typing:

>> python olpc_dataprocessor.py -r ROOT_DIRECTORY_PATH  -o  OUTPUT_FILE_PATH

for example to process journals backups that are in a root folder called data and has the directory structure 
"data/users/*/*/*/*/metadata/*"", you would run the script by typing the following at the prompt: 

>> python olpc_dataprocessor.py -r data  -o  journals_data.csv

The script would process the all the journal backups found in the users/*  directories and output a file call journals_data.csv. 


Viewing the output csv file
###########################

For this example the created file will be journals_data.csv. To view the contents of the file, you can open it in a spreadsheet or text editor etc or your favorite statistical analysis package. P.S the delimiter for the csv file is an "*"

Comma Separated Values (CSV), OpenDocument Spreadsheet (ODS), and Microsoft Excel (XLS) formats of sample data are included. These were extracted from three OLPC XO laptops with arbitrary data. The source data are also included(see the data folder).

Email 
Leotis Buchanan at LeotisBuchanan@exterbox.com
Sameer Verma at sverma@sfsu.edu

References
http://wiki.sugarlabs.org/go/Human_Interface_Guidelines/The_Laptop_Experience/The_Journal
http://wiki.laptop.org/go/Journal_Activity
http://olpcjamaica.org.jm
