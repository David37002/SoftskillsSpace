# Soft Skill Space

An educational platform to facilitate both tutoring and online courses

## Useful links

- [Gitlab repo](https://gitlab.com/tushortz/softskillspace)
- [Theme](https://eduport.webestica.com/index.html)

## Requirements

- Python / Django

## Project setup

If not using docker, you can setup a virtual environment using the command below

```sh
python -m venv env
```

then activate it with

```sh
./env/Scripts/activate   # windows or
source env/bin/activate  # linux or mac
```

## Install required packages

Run the command below

```sh
python -m pip install -r requirements-dev.txt
```

Once the virtual environment has been activated, install the necessary requirements by using the command below

```sh
python manage.py migrate
```

##  Setting up default data

Run the code to pre-populate your database with default data

```sh
python manage.py loaddata ./softskillspace/fixtures/subject.json

python manage.py loaddata ./softskillspace/fixtures/location.json
```


## Important steps

- Go to the Gitblab issue board (https://gitlab.com/tushortz/softskillspace/-/boards/4073022)
- In the backlog lane, choose a ticket an assign to yourself
- Move the chosen ticket to in progress
- Create a branch in your local pc but branching from the develop branch.
- Once coding is done, run the `scripts.sh` script.
- If successful, push your code to Gitlab
- Notify two colleagues to perform code reviews
- If code review is successful, move ticket to `closed` lane on Gitlab


## Contribution

Pick a ticket on the [Gitlab repository](https://gitlab.com/tushortz/softskillspace). If you haven't cloned the repository, use the command to clone from the terminal

```sh
git clone https://gitlab.com/tushortz/softskillspace
```

When creating a new branch, **ENSURE** that the branch name starts with the format **SSS-&lt;issue-no&gt;-&lt;short-description&gt;** e.g. **SSS-1-project-setup** and the main branch is from develop. use the command below when creating a new branch.

```
git checkout develop
git branch -m <branch name>
```

When creating a pull request, please select the target branch as `develop`.

- After writing your code, make sure to run the `scripts.sh` file and **ENSURE** it passes before pushing to the git repository. Use the command below to run the test.

```sh
sh ./scripts.sh
```

## Pushing to the repository

Run the following command

```sh
 # if pushing for the first time
$ git push -u origin <branchname>

# if pushing normally
$ git push
```
