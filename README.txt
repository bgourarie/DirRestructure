use TestCSV2.txt as an example to build a csv file.
It should have the following structure:
Each directory will be relative to a rootDirectory in the config file: 


oldDirectory*,newDirectoryName*, newDirectoryRoot*, newDirSub(Optional), newDirSub2 (optional)

*the OldDirectory should be a subdir of the oldRootDirectory from config file
*the first three values are required, the subdirectories are optional (blanks will be ignored)

each directory should have its own line (as the CSV format)


you can use the config file to specify a test run, which is very useful to make sure you didn't mess anything up before you do a massive operation!


Any errors will be recorded to the log (can be disabled in conf). Since the program uses python.os.copytree to perform the operation, any folders which already exist in the destination will be skipped- so it is enough to simply fix the faulty directory and run the script again without changing the csv file.

Enjoy
