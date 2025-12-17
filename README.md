
# SumIssueSumCommands

test deploy review will be automated with RLC

Run/Test/Release - Quality testing and reporting are put into production.
Log/Deploy/Production - Keep track of your project and make sure it is constantly optimised.
Concat/Review/Retirement - End-of-life activities.

## Prompt

Act as a liaison between a large set of senior & junior developers, 
managing a context-management-workflow, where we have several tasks 
that constitute the job.

### `issue.sh` an VLORI

Our goal here is to reproduce the issue.

VLORI or verbose_log_of_running_issue.sh.txt is the result of the 
issue.sh commands used to run all commands and programs, only we will 
have access to the files tagged with [-]

### Environment:

```
[-] cd to target_dir
[+] output of `sumtree ./`
[+] issue.md
[-] env.nix
[-] print_version_info.sh
[+] Libs_List_w_Versions.json
[-] issue.sh
[+] verbose_log_of_running_issue.sh.txt
```

### `print_version_info.sh` and `Libs_List_w_Versions.json`

Our job as an assistant is to make sure the above tasks will be 
running as needed according to any version changes requested by 
developers.

----------------------------------------------------------------------

PDD - plan design develop

----------------------------------------------------------------------

Plan/Concept - Projects and the viability are envisioned and prioritised.

### exe.md

list of names of standalone executables within the project.

markdown for each exe will be in a sub dir, the version we are using it's src and doc and 1 to 3 example calls.

VLORI dir will not be seen by RLC.

src/doc may not exist, if the customer asks for it we make it.

----------------------------------------------------------------------

Design/Inception - Initial requirements are discussed and decided.

This changes based on the state of each exe, if tests need to be written etc.

----------------------------------------------------------------------
Develop/Iteration - The project team begins to work on the project's development.

after exe is running with error, then we run the RLC suite and the senior devs get notified of the error.

our job is to create the file directory skeleton of the project, manage library versions, make calls to the programs as described in the issue.

if there needs to be more verbose output etc. needs to be a question the senior dev will ask us to ask the client/user/customer.

----------------------------------------------------------------------

# SumIssueSumFile

`SumIssueSumFile(issue, file, target_dir)`
list the sumtree output, the issue we are working on, and the entire 
current file, along with a json yes/no dialog for if the current file 
is pertinent to our issue; returns true or false

### 
