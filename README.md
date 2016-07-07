# github-visitors

Tool to retrieve visitors count from github, to store it, and to plot it.

## Usage

usage: github-visitors.py [-h] --username USERNAME --repository REPOSITORY
                          [--password PASSWORD] [--archive ARCHIVE] [--plot]

Retrieve and store github traffic logs.

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME   github username
  --repository REPOSITORY
                        github repository (ie. pamela-project/slambench)
  --password PASSWORD   Not recommanded, if not set, it will be asked.
  --archive ARCHIVE     file where to load and save data.
  --plot                A plot will be generate if set.


## Example

The first time you run it, you should have a warning about the archive file, but this should stop once the archive file exists :

```
[toky@zebulon github-visitors]$ ./github-visitors.py --username bbodin --repository pamela-project/slambench --archive slambench.dat --plot

*********************************
** GitHub data retrieving tool **
*********************************

Please type your password for bbodin: 

Initialisation...
Read-only operation failed on the archive file 'slambench.dat'.

Generate Token...
Token OK

Open session...
Session OK

Retrieve data...
Data OK
Data is 14 elements
```

## Licence

See LICENCE file.

