
# SumVibes

Vibe coding development environment.

----------------------------------------------------------------------

# RLC - Run Log Concat

*Run*/Test/Release - Quality testing and reporting are put into production.  
*Log*/Deploy/Production - Keep track of your project and make sure it is constantly optimised.  
*Concat*/Review/Retirement - End-of-life activities.

----------------------------------------------------------------------

`concat_macro.sh` is the heart of RLC, it's goal is to create a 
semi-reproducible log of the problem at hand. There is still non 
deterministic things like time and system information, which may be 
pertinent to the current issue, like process `X` takes this long or 
we're having trouble with hardware `Y`.

## Issue Management

The whole idea of RLC is to create a prompt for a developer and/or an 
LLM where they can read the logs of the problem at hand, and the files 
that are pertinent to  the issue.

And either work on the solution immediately or ask for more information.

## task list / tracking

every Issue will have a task List

the 1st job will be RLC itself and it's executor should be 
`current-system` but we may set that up to be `remote-systems` later

The following task-List is added to every issue:

|name|executor|
|PDD|JuniorLM and User|
|IssueQC|JuniorLM and User|
|RLC|current-system and Liaison|
|summarization|current-system-sumtree|
|cut-out|JuniorLM and User|
|diagnostics|SeniorLM|
|patching|JuniorLM on the output from the SeniorLM|

## json
The task list will be json.

## issue.md

Files that might be pertinent should have ther own summary, if their 
entire text is included in the issue.md there should be no summary 
provided.

other files like icons and other doodads should be moved to a dir like 
`/rsrcs` and a summary of the folder should be included.

again the goal is shortening our issue.md so if the whole file is 
included we don't need a summary, but if we really need just 1 
function out of it we might do a partial include, and the summary.

most of the work is designed to be done by a junior developer, where 
diagnostics and patching should be set up so if there is trouble at 
that stage the people doing the work will be saying something like can 
you give me the whole file `Z`.

Remember we're trying to conserve bandwidth on this channel, so we can 
use more tokens for solving other issues. The entities doing 
diagnostics and patching shouldn't see any of this unless they are 
working on RLC.

## cut-out gui

There will be a file list, where the user and the JuniorLM will vote 
on what files should be included in the issue. only the user votes 
will count, but they should view the JuniorLM votes and summaries will 
also be shown to the user here to influence their decision making 
process so they can work faster.

## Branch Management

Each Issue should have a unique number, and the response from the 
issue.md being given to the SeniorLM should be parsed by the JuniorLM 
to create and apply the patch.

When a patch is a applied it will create a new branch, possibly new issues 

In the event the issue isn't solved, 

----------------------------------------------------------------------

`concat_macro.sh` file:

```
run_and_log() { # run a script $1 and log to output $2
    utcupdate
    echo "Running $1 at $utc"
    sumtree
    nix-shell "$3" --run "bash $1" 2>&1 | tee "$2"
    utcupdate
    echo "Completed $1 at $utc"
}

combine_files() {
  shift
  rm $1
  # Loop through remaining args (the input files)
  for file in "$@"; do
    filename=$(basename "$file")
    # Print header with 10 # chars before and after
    {
      echo -e "#####\nFile: $filename\n######\n\n\`\`\`"
      # Escape triple backticks in file content
      sed 's/```/\\```/g' "$file"
      echo -e "\n\`\`\`"
    } >> "$1"
  done
}

cd $owd

run_and_log "./issue67.sh" "./issue67.log" "./devShells.nix"

combine_files concat67.md ./devShells.nix ./issue67.log ./test67.py ./issue67.md
```

## PDD Liaisons

As a liaison between a large set of senior & junior developers, 
managing a context-management-workflow, where we have several tasks 
that constitute the job.

### `issue.sh` and VLORI

Our goal here is to reproduce the issue.

VLORI or verbose_log_of_running_issue.sh.txt is the result of the 
issue.sh commands used to run all commands and programs, only we will 
have access to the files tagged with [-]

note issue.sh is included in VLORI that is why only the liaisons have access

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

# PDD - Plan Design Develop

There are 3 Liaisons, 1 each for plan design development.

*Plan Liaison* manages review, requirements, and readme. They are in 
charge of deciding status of the project or subtask, and asking the 
user/client for more information if necessary. they are also in charge 
of benchmarks and tests.

*Design Liaison* manages dependency resolution and timing this 
includes issuing new subtasks and waiting for them to complete before 
moving to Dev-stage the junior dev will act as a senior-dev until all 
libraries are installed, after dependencies are resolved they are to 
make a list of files from the VLORI that are pertient to the issue.

IF dependencies or other libs or pathing issues or system issues were 
solved etc. from subtasks The VLORI will be recreated at this point by 
running RLC. note this happens in a subtask.

At this point a junior dev will make a list of candidates of files 
causing the issue by processing the VLORI. SumIssueSumFile() will be 
recursively run on files starting with the VLORI, and output a tree 
that may contain duplicates.

*Senior Developer* after the VLORI is failing not because of 
dependencies or other libraries not passing tests, list of files 
created by the *Design Liaison* along with the VLORI will be sent to 
the Senior-Dev to suggest possible solutions.

*Development Liaison* processes the output of the senior dev, and 
prepares a patch to be applied to the project. They are in charge of 
applying edits as described by the senior dev.

The VLORI will be recreated at this point by running RLC

At this point a junior dev will make a list of candidates of files 
causing the issue by processing the VLORI. SumIssueSumFile() will be 
recursively run on files starting with the VLORI, and output a tree 
that may contain duplicates.

Process will restart at plan/review Liaison

----------------------------------------------------------------------

 just a list of all files executed in the VLORI, 

From the candidates it will read them 1 by 1 and decide if there is any documentation or source from other files that needs to be included to answer the issue at hand.

on all candidates.

, for the 
Planner to review, 

test deploy review will be automated with RLC
----------------------------------------------------------------------

this should really only happen at the begining of a project or issue

and the VLORI has failed at least 1x for the current issue. on the 0th iteration the junior dev will work with the user to prepare 

Making certain VLORI is not failing because of library or other dependency either isn't installed or passing tests.
that way subtask can be issued to handle the installation and evaluation of dependencies. This process makes certain the system is working as planned

----------------------------------------------------------------------

## Plan/Concept - Projects and the viability are envisioned and prioritised.

*Plan Liaison* manages review, requirements, and readme. They are in 
charge of deciding status of the project or subtask, and asking the 
user/client for more information if necessary. they are also in charge 
of benchmarks and tests.

If we are here are previous step was concatenate. This is when we review the VLORI, if there is no VLORI this task has just begun.

Project-Description

errors/bugs create new subtasks if they don't exist already

fail early, and fail often. our first goal is to make an output immediately.

unless we received input from a senior-dev in the review we will not edit the `exe.md` and `libs.md` design files the client and junior-dev made, or will make in the next step.

This will look like lib `X` or feature `Y` is unavailable on this system. for instance if the senior-dev said backpropagation isn't supported in vulkan based pytorch.

At this point we would edit the libs.md add a message and let the Design liaison would handle that.

Planning Liaison is to figure out what job completion looks like, and handle senior-dev requests on design changes.

----------------------------------------------------------------------

## Design/Inception - Initial requirements are discussed and decided.

*Design Liaison* manages dependency resolution and timing this 
includes issuing new subtasks and waiting for them to complete before 
moving to Dev-stage the junior dev will act as a senior-dev until all 
libraries are installed, after dependencies are resolved they are to 
make a list of files from the VLORI that are pertient to the issue.

Design Liaison manages design patterns, and waits for subtasks to complete before moving to Dev-stage
the junior dev will act as a senior-dev until all libraries are installed.

library installation creates subtasks for each library.

tests are assumed to be done by libraries not part of the prject.

### exe.md

list of names of standalone executables within the project.

markdown for each exe will be in a sub dir, the version we are using it's src and doc and 1 to 3 example calls.

VLORI dir will not be seen by RLC.

### libs.md

src/doc may not exist, if the customer asks for it we make it.

#### tasks & subtasks

This changes based on the state of each exe, if tests need to be written etc.

Tasks for an issue can include subtasks.

After definitions and descriptions of exe and libs are managed, this is where choices on adding libraries and or tests may be used in deciding on what additional tasks or subtasks may be needed.

example - runing an example pytorch benchmark to make sure it is installed correctly on the current system etc. it would get added to exe.md as torch_test as a new subissue.

Remember while the requirements.md and readme.md of the issue we receive are priority #2, but our #1 priority or job is to manage context for any issues leading up to the task. Remember we are taking small steps in a journey towards the finish line, we must make sure the ground doesn't break beneath us, there must be testing or example outputs.

Remember errors are part of the development, we will the junior-devs and the client/customer will pick the libs and exe for the project and if they make a bad choice the seniors will tell them later.

### library and exe installation failure

if the junior dev fails after 3 tries the user will be prompted to view the VLORI and be asked if it can be sent for development to the senior dev.

### after the VLORI 

after the VLORI is generated for the current task 

Design Liaison will make a list of candidate files from the VLORI, just a list of all files executed in the VLORI, 

From the candidates it will read them 1 by 1 and decide if there is any documentation or source from other files that needs to be included to answer the issue at hand.

SumIssueSumFile() on all candidates.

#### SumIssueSumFile

`SumIssueSumFile(issue, file, target_dir)`

VLORI will have the sumtree output
, the issue we are working on, and the entire 
current file, along with a json yes/no dialog for if the current file 
is pertinent to our issue; returns true or false

once the Design Liaison is done selecting pertinent source code, this will start the RLC_COG gui with the selected files/code highlighted. so the client/user can assist in selecting/deselecting pertinent code to be handed to the senior dev along with the VLORI.

----------------------------------------------------------------------

At this point the VLORI is given to the senior or Junior-Dev

and when the response is received it is handed to the Development Liaison.

processes the output of the senior dev, and prepares a patch to be applied to the project.

----------------------------------------------------------------------

## Develop/Iteration - The project team begins to work on the project's development.

Development Liaison processes the output of the senior dev, and prepares a patch to be applied to the project.

After exe is running with error, then we run the RLC suite and the senior devs get notified of the error.

If the RLC suite is run and the review is more work needs to be done.

this stage is where the senior-dev steps in


if there are no errors, but there is missing functionality

our job is to create the file directory skeleton of the project, manage library versions, make calls to the programs as described in the issue.

if there needs to be more verbose output etc. needs to be a question the senior dev will ask us to ask the client/user/customer.

----------------------------------------------------------------------
