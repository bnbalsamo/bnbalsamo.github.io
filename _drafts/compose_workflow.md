---
layout: post
title: A Docker Compose Workflow For Teams
---

## Introduction

Docker provides a variety of benefits to both the software development
and distribution pipelines. One such benefit is explicitly stating and formalizing
build processes and configurations - allowing for services to be distributed and
run in _all_ dockerized environments.

Docker compose allows for multiple dockerized services to be arranged to work together,
explicitly stating the ports on which the services present their functionality. And
defining the ways in which services can reach/reference each other.

Modern software development practices, like Agile and associated methodologies, require
accomplishing tasks in parallel whenever possible. Software architectures increasingly
accomplish business logic by implementing several services which deliver functionality. 
Frequently, these services are worked on by different individuals or teams, are written in 
different languages, and utilize different software stacks.

In combination, these factors mean that software developers need access to development
environments which include a wide variety of services, and need to be able to deliver ongoing
work to the rest of their team in order to avoid serializing workflows and introducing blockers.

A Docker Compose workflow allows for software developers to work effectively in these modern
frameworks, and effectively employ Agile development methodologies while producing deliverables
appropriate for use by other developers, quality assurance, and production deployment teams.

When all is said and done the workflow can be visualized like so:

![Docker Compose Workflow]({{ "/assets/docker_compose_workflow_diagram.jpg" | absolute_url }})

Development environments are cleanly contained and made managable by a single individual or team.
Each development environment is responsible for producing a deliverable component which can be
utilized by all other development environments to provide the promised functionality, as well as
the QA environment for testing. This means that services can scale

Services can be tested in isolation as well as in their production
contexts, and build requirements, configuration details, and service interdependencies are made
explicit in the docker build and compose files. This drastically reduces the generation of technical
debt, makes deployments details know factors, and interfaces _exceptionally_ well with Continuous 
integration pipelines in order to facilitate rapid development, testing, and deployment.

## Project Orchestration

Employing a Docker Compose workflow requires some project level orchestration in order to be
successful. The workflow involves minimal, but vital, infrastructure, as well as coherent project
level design.

### Project Design

Projects which abide by best software design practices are often easily mapped into docker compose
driven workflows. There are several factors which should be kept in mind, however, when designing
and managing projects in order to get the most out of these practices.

Projects should be split into services which can be encapsulated such that they present a cleanly
delineated interface. This interface should present functionality through standardized
interfaces with well documented input requirements and specifications, as well as output values. 
Project configuration must also be well documented, and configuration values should be 
set at run time in order to allow the service to be run in local, QA, and production environments.

Each service should, ideally, be constructed within a single software stack which does not duplicate
requirements. Also, each service should include debug logging understandable to those without knowledge
of the stack, and with minimal knowledge of the source code beyond the fulfillment of the functionalities
promised by the interface.

### The Infrastructure

In order to utilize a compose driven workflow a project _must_ have a docker repository to utilize.
Different projects come with different constraints - for some the public Docker Hub will be an acceptable
repository, for others you will have to utilize a private repository. After a repository location is selected
the repository details must be made available to all of the teams working on the project. Additionally,
a minimal tagging structure must be put into place. The tagging structure should describe images
which fulfill the stated contracts of the service, as well as potentially 'development' versions of those
services.

In addition to the image repository and tagging specifications, the project must have a way to 
distribute pieces of information and documentation. This information includes certain 'specification' 
like information (eg, the interfaces and contracts that each service supports) as well as certain 
'base' artifacts - the most important of which is the base docker-compose upon which the QA environment 
will be built directly, and which each development environment should be based on. A centralized
source code version control repository (eg, git) is often the most appropriate place to coordinate
the sharing of knowledge and documentation.

Management of this centralized knowledge, as well as the generation of tagging structures and workflows
can be handled by different teams or individuals depending on the project management methodology which
is being employed, but a coherent plan regarding who manages these aspects of the project, and what
responsibilities and capabilities are held by each team (dev teams, QA teams, project managers, etc)
is essential.

## The Local Development Environments

The crux of the docker compose workflow is the development environments for each individual service - and
each of these development environments is built by the project specific docker-compose.yml file. This
file has two very important attributes:

1. It defines an image _and_ a build context for the local service
2. It pulls all the other services from the image repository

This allows the local development environment to pull all the other portions of the project from the
centralized repository, and builds the local service from the build context - allowing the developer to
run it in the _actual_ context it will operate in within the production environment, as well as in isolation.

Once a service is fulfilling a new requirement or providing another interface/functionality this information
can be communicated back to the centralized information store, and each environment can be used in order
to push the most recent version of the service back to the centralized image repository.
If allowed by the tagging structure (for example, if each development environment is pulling the 
"latest" tag of the others) the new functionality can be transparently integrated into the other 
development environments on their next build.

This workflow also means that the development environment is entirely owned by the developer or development
team working in it - provided the requirement that the image builds in all the other development environments
and the QA build is maintained.

## Quality Assurance Builds

The quality assurance build of the project then is _exceptionally_ simple to configure - it is simply
the docker-compose file which is being used in all of the development environments, with the exception
that it defines **no** build contexts. This docker compose should pull all of the published build artifacts,
from each of the development environments, and they should work together.

This should, provided each project presents the proper interfaces, give QA the ability to run unit tests
against each separate project in isolation, as well as integration tests with all of the services in concert.
It also provides the opportunity for QA teams to devise their own tests to be run against the current latest
builds of each development service and run them at any time.

## Production Deployment

- Productionization
- Pinned requirements
- Pinned tags
- Equivalent of "merge to master"

## Conclusion

