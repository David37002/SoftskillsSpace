git add . > /dev/null 2>&1

black --exclude=".*/migrations/,.*/env/" $(git ls-files '*.py') > /dev/null 2>&1
echo "- Black format complete"

autopep8 --in-place --exclude="**/migrations/,**/env/" --aggressive --aggressive $(git ls-files '*.py') > /dev/null 2>&1
echo "- Autopep 8 format complete"

isort $(git ls-files '*.py') > /dev/null 2>&1
echo "- Isort format complete"

PYLINT_RESULT=$(pylint $(git ls-files '*.py'))
pylint $(git ls-files '*.py')
echo "Pylint run complete"
echo

UNIT_TEST_OUTPUT=`python manage.py test --keepdb -v 2`
echo "UNIT TEST RUN COMPLETE"
echo

PYLINT_SCORE=$(echo $PYLINT_RESULT | grep -Eo 'at [0-9.]{0,4}' | grep -Eo '[0-9.]{0,4}')
if [[ $PYLINT_SCORE = *10* && $UNIT_TEST_OUTPUT != *FAILED* ]]
then
    git add . > /dev/null 2>&1
    BRANCH_NAME=$(git branch --show-current)
    GIT_STATUS="$(git status -s)"

    if [[ "$GIT_STATUS" = *'M'* ]]
    then
        echo "Please enter commit message for $BRANCH_NAME"
        read COMMIT_MESSAGE
        git commit -m "$COMMIT_MESSAGE"
    fi

    git push -u origin $BRANCH_NAME
    echo "SUCCESS"
else
    echo "FAILURE. Please check the comments above. Fix the issue and re-run script"
fi
