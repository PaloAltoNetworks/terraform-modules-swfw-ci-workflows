# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps,
and credit will always be given.

## Areas of contribution

Contributions are welcome across the entire project:

- Code
- Documentation
- Testing

## Contributing workflow

### New Contributors

1. Search the [issues](https://github.com/PaloAltoNetworks/terraform-modules-vmseries-ci-workflows/issues) to see if there is an existing issue. If not, open an issue (note the issue ID).

1. Fork the repository to your personal namespace (only need to do this once).

1. Clone the repo from your personal namespace.

   `git clone https://github.com/{username}/terraform-modules-vmseries-ci-workflows.git`
   Ensure that `{username}` is _your_ user name.

1. Add the source repository as an upsteam.

   `git remote add upstream https://github.com/PaloAltoNetworks/terraform-modules-vmseries-ci-workflows.git`

1. Create a branch which corresponds to the issue ID created in step 1.

   For example, if the issue ID is 101:
   `git checkout -b 101-updating-wildfire-templates`

1. Make the desired changes and commit to your local repository.

1. [Test](#testing) the changes (preferably add tests for any code changes)

1. Push changes to _your_ repository

   `git push origin/101-updating-wildfire-templates`

1. Rebase with the upstream to resolve any potential conflicts.

   `git rebase upstream develop`

1. Open a Pull Request and link it to the issue (reference the issue, i.e. "fixes #233"). Do use [conventional commits format](https://www.conventionalcommits.org).

1. Once the PR has been merged, delete your local branch

   `git branch -D 101-updating-wildfire-templates`

### Existing Contributors

1. Search the [issues](https://github.com/PaloAltoNetworks/terraform-modules-vmseries-ci-workflows.git/issues) to see if there is an existing issue. If not, open an issue (note the issue ID).

1. Update from the source repository.

   `git pull upstream develop`

1. Create a branch which corresponds to the issue ID created in step 1.

   For example, if the issue ID is 101:
   `git checkout -b 101-updating-wildfire-templates`

1. Make any changes, and ensure the commit messages are clear and consistent (reference the issue ID and type of change in all commit messages)

1. [Test](#testing) the changes (preferably add tests for any code changes)

1. Document the changes (update the README and any other relevant documents)

1. Push changes to _your_ repository

   `git push origin/101-updating-wildfire-templates`
1. Rebase with the upstream to resolve any potential conflicts.

   `git rebase upstream develop`

1. Open a Pull Request and link it to the issue (reference the issue, i.e. "fixes #233"). Do use [conventional commits format](https://www.conventionalcommits.org).

1. Once the PR has been merged, delete your local branch

   `git branch -D 101-updating-wildfire-templates`

## Testing

Testing of reusable workflows is tricky. Since these actions are specific to the code that is stored on the code repos and are being triggered from there there is no easy way to test them directly. Hence the following scenario is proposed:

1. Create a fork of this repository as described in [Contributing workflow](#contributing-workflow). Create a branch and provide you changes to the code. Commit and push your changes.

1. Create a fork of a code repository. See `CONTRIBUTING.md` in your repository of choice. It does not matter which one you choose. Creating a fork of the code repository gives you an advantage of having access to branches that normally are protected (like the main/master branch). Some of the workflows do work only on those branches. Additionally you will have to change the reference to the reusable workflow in order to use the code you develop.

1. We will assume a scenario where one would like to change the code for a workflow that is being triggered on `pull_request`.

    1. Create a new branch on the forked code repository. Edit the workflow you would like to change and adjust the `uses` line in a way that it will point to your newly created branch on the reusable workflows fork repository.\
    Example:

        <!-- language: yaml -->

            name: PR CI
            
            run-name: "CI pipeline for PR - (#${{ github.event.number }}) ${{ github.event.pull_request.title }}"
            
            permissions:
              contents: read
              actions: read
            
            on:
              pull_request:
                branches: ['main']
            
            jobs:
              pr_ci_wrkflw:
                name: Run CI
                uses: {username}/terraform-modules-vmseries-ci-workflows/.github/workflows/pr_ci.yml@{branchname}

        <!-- -->

    1. Push your changes. This will trigger a workflow to run on the forked code repository, but the reusable workflow will be taken from your fork of the reusable workflows repository.

Of course each time you make changes on the reusable workflows repository is not enough to trigger the workflows on the code repository. You have to make a dummy change on the code repository each time you want to generate a trigger for the workflow to run.
