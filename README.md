# CI workflows used by Terraform-(AWS|Azure|GCP)-modules-vmseries repositories.

This is a repository for hosting all reusable workflows used by the *code* repositories:

* [terraform-aws-vmseries-modules](https://github.com/PaloAltoNetworks/terraform-aws-vmseries-modules)
* [terraform-azurerm-vmseries-modules](https://github.com/PaloAltoNetworks/terraform-azurerm-vmseries-modules)
* [terraform-google-vmseries-modules](https://github.com/PaloAltoNetworks/terraform-google-vmseries-modules)

All GitHub actions workflows stored on the target/code repositories are only stubs calling reusable workflows stored here. Since the workflows stored here are used for generic actions like release/PR management this repository provides a way to have common code for actions that should be the same for each repository.

Notice, that those workflows match the way we work with the code repositories. They do not have to necessarily match any use case around releasing and PRs.

## Workflow diagram

### Generic 

The generic diagram below is to visualize dependencies and relationships between workflows in the code and this repository.

```mermaid
flowchart
  trig[/Incoming trigger/] --> t_start
  subgraph T [Terraform Code Repository]
    direction TB
    t_start(Start a workflow)-->t_init(Set workflows permissions)
    t_init-->t_call(Call a reusable workflow)
    t_call-..-t_stop(Workflow end)
  end
  subgraph G [Generic Workflows Repository]
    direction TB
    g_start(Init point of a reusable workflow)-->g_init(Set workflow permissions)
    g_init-->g_jobs(Run jobs and subworkflows)
    g_jobs-->g_stop(Reusable workflow end)
  end
    t_call-->g_start
    g_stop-->t_stop
```

### Pull Requests

The diagram below shows detailed dependencies between both repositories using the [`PR CI`](./.github/workflows/pr_ci.yml) workflow.

```mermaid
flowchart
  trig(Pull Request GH trigger) --> t_start
  subgraph Terraform Code Repository
    subgraph T [Pull Request Workflow]
        direction TB
        t_start(Start a workflow)-->t_init(Set workflows permissions)
        t_init-->t_call(Call a reusable workflow)
        t_apply_action(Run the cloud dedicated\nPlan and Apply action)
        t_stop(Workflow end)
    end
  end
  subgraph Reusable Workflows Repository
    subgraph G [Pull Request Reusable Workflow]
        direction TB
        g_start(Init point of a reusable workflow)-->g_init(Set workflow permissions)
        g_init-->g_diff(Discover differences in Terraform code\n between trunk and base branches)
        g_junction(Sub-workflow junction point\nfor branch protection)
    end
    subgraph V [Validate Sub-Workflow]
        direction TB
        v_start(Init point of a sub-workflow)-->v_unpack(Unpack inputs to JSON\nfor matrix strategy use)
        v_unpack-->v_validate(Run validation\nstrategy: matrix)
    end
    subgraph A [Plan and Apply Sub-Workflow]
        direction TB
        a_start(Init point of a sub-workflow)-->a_unpack(Unpack inputs to JSON\nfor matrix strategy use)
        a_unpack-->a_apply(Run Plan and Apply\nstrategy: matrix)
    end
    subgraph P [Pre-Commit Sub-Workflow]
        direction TB
        p_start(Init point of a sub-workflow)-->p_prereq(Install pre-commit prerequisites)
        p_prereq-->p_pre_commit(Execute pre-commit hooks based on input parametrization)
    end
  end
  t_call-->g_start
  g_diff-->v_start
  g_diff-...->a_start
  g_init-->p_start
  g_init-->c_start

  v_validate-->a_start

  a_apply-->t_apply_action

  t_apply_action-->g_junction
  p_pre_commit-->g_junction
  c_checkov-->g_junction
  v_validate-->g_junction
  g_junction-->t_stop
```

## Usage

The code stored here is using Semantic Versioning and follows the GitHub actions way of providing tags for major releases. Therefore one can pin to a tag i.e. `v1` which will follow all minor and patch releases.

Please keep in mind that all workflows stored here use `permissions` property. Keep that in mind when referencing a workflow from this repository in your code - the permission you give to a reusable workflow in your code should match a summary of permissions used by all jobs in that particular reusable workflow.

An example of calling a reusable workflow.

```yaml
name: Lint PR Title
run-name: "Lint PR - (#${{ github.event.number }}) ${{ github.event.pull_request.title }}"

permissions:
  pull-requests: read

on:
  pull_request_target:
    types:
      - opened
      - edited
      - synchronize

jobs:
  lint_pr_title:
    name: Lint PR
    uses: PaloAltoNetworks/terraform-modules-vmseries-ci-workflows/.github/workflows/lint_pr_title.yml@v0
```

## Inputs/Outputs

None of the workflows takes any input nor they produce artifacts as output.
