---
layout: post
title: A Docker Compose Workflow For Teams
---

## Why Use Docker Compose

Docker can help you develop and distribute software. One of the ways it can help is by 
explicitly stating and formalizing build processes and configurations, allowing 
services to be distributed and run in _all_ dockerized environments.

[Docker Compose](https://docs.docker.com/compose/) allows multiple dockerized services 
to work together by both explicitly stating the ports on which the services present 
their functionality and defining the ways in which services can reach or reference each other.

Modern software development practices recommend accomplishing tasks in parallel whenever possible. 
By implementing services with specific functions, software architecture increasingly 
drives business logic. Frequently, these services are worked on by different individuals or teams, 
are written in different languages, and utilize different software stacks.

Because different people are working on different services with different languages and different
software stacks, software developers need access to diverse development environments. Their
development environments need to include a wide variety of services and support the developers as
they delivery ongoing work to the rest of their team to introducing blockers in their work.

A Docker Compose workflow allows software developers to work effectively in these modern
frameworks, effectively practice Agile development methodologies, and produce useful deliverables
to developers, quality assurance, and production deployment teams.

You can visualize the workflow like this:

![Docker Compose Workflow]({{ "/assets/docker_compose_workflow_diagram.jpg" | absolute_url }})

Development environments are contained and managable by a single individual or team. Each 
development environment is responsible for producing a deliverable component that can be
used by other development environments to provide the promised functionality, and used by
the QA environment for testing. 

Services can be tested both in isolation and in their production contexts. Build requirements, 
configuration details, and service interdependencies can be made explicit in the Docker build 
and compose files. This helps prevent technical debt, makes deployments details known factors,
and interfaces _exceptionally_ well with Continuous Integration/Continuous Deployment (CI/CD) 
pipelines in order to facilitate rapid development, testing, and deployment.

## Project Orchestration

Employing a Docker Compose workflow requires some project level orchestration in order to be
successful. The workflow involves minimal, but vital, infrastructure, as well as coherent 
project-level design.

### Project Design

Projects that follow best practices in software design are often easily mapped into Docker Compose
driven workflows. Keep in mind several additional factors when designing and managing projects 
in order to get the most out of these practices.

Separate projects into services that can be encapsulated in such a way that they present a cleanly
delineated interface. This interface must present functionality through standardized
interfaces with well-documented input requirements and specifications and output values. 
The project configuration must also be well documented, and configuration values must be 
set at run time in order to allow the service to be run in local, QA, and production environments.

Construct each service within a single software stack that does not duplicate requirements. Each service 
must also include debug-level logging understandable to those both without knowledge of the stack and with 
little knowledge of the source code beyond the fulfillment of the functionalities promised by the interface.

After these minimum requirements have been met, write each application so that it abides by the rules
of the [12 Factor App](https://12factor.net). This helps you follow industry best practices, and synergizes
excellently with the requirements for running each service within a properly dockerized environment,
and within a compose-based workflow.

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

Production deployments are often project specific, informed by architecture and infrastructure constraints,
preferences, requirements, and special considerations. Despite this, a docker-compose based workflow
can help make production deployment easier, whether you are deploying containers into production or not.

In the event that you deploying containers into production it is often optimal to make the production
deployment as similar as possible to the QA builds and even the local development builds, or (perhaps
more accurately) to make the QA and Local builds and environments as similar as possible to production.
If, for whatever reason, this isn't possible, production builds should be formalized and their differences
from the local and QA builds documented. If possible these builds should be formalized into alternate
base images for the application containers to be built on top of or within.

If you are not deploying containers to production the dockerization of the QA environment still serves
as valuable documentation as to the configuration of th services in a production-esque environment.
In combination with documentation detailing the differences between the QA environment and the production
environment, as well as documentation detailing any configuration of the hosts required beyond what is
required for the configuration of the docker machines, a formal production deployment can be had with
comparatively little work, leveraging work done in order to configure previous environments whenever
possible.

## Conclusion

Docker Compose workflows provide the tools to allow modern software development teams to work effectively
on large, service based, systems. The local development environments provide developers with the ability
to build services which are able to be built, tested, and deployed locally both in isolation and in the
context of the larger systems architecture which they are meant to participate in. The remote repository
serves as the glue which holds these developmenet enironments together, as well as a clean deliverable
specification for each team. The coupling of the build processes between the development environments
and the QA environments provides a delivery pipeline and an easy way to avoid common issues of
configuration and stack mismatch between developers and QA. Finally, the dockerization and delivery
mechanisms provide convenient methods for packaging software for delivery to production environments
as containers - or, if production is not containerized, implicitly provide a head start on standardizing
and documenting deployments into other environments.

These workflows can be applied to a greenfield projects at the offset, or existing projects (with a bit
of elbow grease) can be converted to utilize these workflows. I hope this post has demonstrated the
benefits and methodologies of a compose based workflow, and that you consider utilizing one for your
(or your team's) next project!
