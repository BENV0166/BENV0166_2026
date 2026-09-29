# Git Exercise

This is a markdown file. To view its contents in a readable form, right-click on the file and select *open preview*.

## 1. Purpose of Exercise
To learn how to pull changes from the remote repository, make commits, create branches to save weekly exercises, and to generally learn the capabilities of Git.

You are expected to already have the Git repository for this module cloned to your machine.

## 2. Pull Changes
Before you every weeks exercises, it is best practice to pull any changes that have been made since you last opened VS Code.
* In VS Code, select the *Source Control* icon on the left toolbar. 
    * Under the repositories or changes tab, select the three dots button and select pull.
    * Depending on whether any updates have been made, updates will be made or nothing will happen.

## 3. Creating a branch
For this module, creating branches for each week's activities will help keep your workspace uncluttered, avoid duplication, and avoid conflicts if code needs to be updated to address some bugs.
1. Before creating a branch ensure you are on the main branch. You can tell in the repositories tab or in the bottom left corner of the screen which branch you are currently on next to the *Source Control* icon.

![](/src/images/Git_Screenshot_1.png)

2. Select the three dots button > Branch > Create Branch From
3. You should see a pop-up menu. Select the main branch as the one we want to branch from
4. Give a name to the branch such as *Example*

You should now see that the branch name has changed 

![](/src/images/Git_Screenshot_2.png)

In VS Code, you can switch easily between branches by clicking on the *Source Control* icon

## 4. Adding, Modifying and Commiting Files
In this step, we will show how to commit files

1. Go back to the explorer tab using the left side toolbar
2. Create a new file in the project root called Test_1.txt
3. Create another new file in the *outputs* directory called Test_2.csv
4. Open the *Exercise 1.ipynb* notebook and correct the title to read Exercise 1.
5. You should notice some activity in the source control toolbar. Git has logged that files have been created or modified. The next step will be to commit the changes:
    * You should see three files listed under changes. If there are only two, it likely means you forgot to save the changes made to the notebook.
    * It is a question of when, not if, you will forget to save changes to a notebook before committing.
6. The next step is that we need to stage changes by clicking the plus symbol. You can choose to stage all files or specific files.

![](/src/images/Git_Screenshot_3.png)

7. You should notice next to each file a letter indicating whether a file is untracked (U), modified (M), or added (A). Youcan also click on the file to see what changes were made. This is known as a **diff** in software lingo. The red highlights indicate what was changed or deleted and the green highlights indicate what has changed or added.

![](/src/images/Git_Screenshot_4.png)

8. Before committing, you need to add a descriptive message indicating what changes were made. For example *Added two new files and modified the title of Exercise_1*
To finish commiting changes click the blue commit button.
9. We quickly make another commit by adding text to one of the newly created test files. In the *graph* tab you should see that you have two commits registered and that they belong to the example branch

![](/src/images/Git_Screenshot_5.png)

## 5. Observing changes to the main branch
Switch back to the main branch. You should see that the two new files are missing and that the title of Exercise 1 is incorrect.  Furthermore if you open your computer's file explorer you will find the files are not there. This is expected as the changes made were isolated to the *Example* Branch and git has recorded the changes for you. 

## 6. Merging changes
You are able to merge the changes from the *Example* branch to the *main* branch easily using the merge function in VS Code.
1. From the *main* branch, from the menu button, select Branch > Merge
2. Select the branch you want to merge from ie. *Example*
3. You should now the see the added files in the main branch.
4. You may now deleted the two Test files as they are no longer needed and commit their deletion.

## 7. Preparing for Week 1
Repeat the necessary steps to create a branch for Week 1.

## 8. Additional Git Featuress
* Another important Git feature (that we will not be using for this module) is the git push command. This allows you to push updated code from your machine to the remote repository where others collaborators can access it. This is disabled for this repository. Avoid using the commit & push button in VS Code.
* There are some useful add-ons in VS Code that help you manage Git projects. Git Graph is one that I use and outlines the history of who made each commit and when and gives a visual of all of the branches
