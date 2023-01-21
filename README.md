# OctoTools
[![Loading the packages](/images/helpCard.png)](/images/helpCard.png)
A purpose built Houdini Package for use in a show/shot/task workflow. This package is for use with Houdini 19.x.x

- [OctoTools](#houdini-package-template)
  - [Overview](#overview)
  - [Getting Started](#getting-started)
  - [Installing The Package](#installing-the-package)

## Overview

This repo is meant to house generic shot tools and otl/hda libraries from various 3rd party vendors, making it easy to distribute tools studio wide.

## Getting Started

1. Download the latest release onto a network location / server

    [![Loading the packages](/images/octoSplash_01.jpg)](/images/octoSplash_01.jpg)


## Installing the package

1. Copy the 'OctoTools.json' file to your houdini packages directory. Once this has been done, launch houdini and you should see an OctoTools menu. If you would like to check that the packages have loaded, switch to the '!OctoTools' desktop and go to the package broswer tab.

    [![Installing the packages](/images/packages.png)](/images/packages.png)

## Mermaid Examples
```mermaid
gitGraph
    commit
    commit
    branch tools
    checkout tools
    commit
    commit
    commit
    commit
    commit
    commit
    commit
    commit
    commit
    checkout main
    merge tools
    commit
    commit
```

```mermaid
journey
title My working day
section Go to work
Make tea: 5: Me
Go upstairs: 3: Me
Do work: 1: Me, Cat
section Go home
Go downstairs: 5: Me
Sit down: 3: Me
```

Markdown Sequence Diagram temp:
```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

Markdown Flowchart temp:
```mermaid
graph LR
A[Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D
```
