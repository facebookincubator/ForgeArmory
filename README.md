# ForgeArmory
[![License](https://img.shields.io/github/license/facebookincubator/ForgeArmory?label=License&style=flat&color=blue&logo=github)](https://github.com/facebookincubator/ForgeArmory/blob/main/LICENSE)
[![🚨 Semgrep Analysis](https://github.com/facebookincubator/ForgeArmory/actions/workflows/semgrep.yaml/badge.svg)](https://github.com/facebookincubator/ForgeArmory/actions/workflows/semgrep.yaml)
[![Pre-Commit](https://github.com/facebookincubator/ForgeArmory/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/facebookincubator/ForgeArmory/actions/workflows/pre-commit.yaml)

ForgeArmory is a repository of attacker Tactics, Techniques, and Procedures (TTPs) that you can download and run with Meta's [TTPForge](https://github.com/facebookincubator/TTPForge) attack simulation engine. Our catalog presently focuses on macOS and Cloud TTPs.

## Setup
To get started, [install TTPForge](https://github.com/facebookincubator/TTPForge/blob/main/README.md#installation) and then browse the ForgeArmory [TTP catalog](https://github.com/facebookincubator/ForgeArmory/tree/main/ttps) to find cyberattacks to simulate.

### Additional Setup for Development
To set up ForgeArmory for development or to contribute to the project, ensure you have Node.js (version 12.0 or higher) and Yarn (version 1.0 or higher) installed.

#### Windows Installation:
1. Clone the repository:
   git clone https://github.com/Your_Username_/ForgeArmory.git
2. Navigate to the project directory:
   cd ForgeArmory
3. Install dependencies:
   yarn install
4. Run the project:
   yarn start
5. Open your browser and go to http://localhost:3000 to access ForgeArmory.

#### macOS/Linux Installation:
1. Clone the repository:
   git clone https://github.com/Your_Username_/ForgeArmory.git
2. Navigate to the project directory:
   cd ForgeArmory
3. Install dependencies:
   yarn install
4. Run the project:
   yarn start
5. Open your browser and go to http://localhost:3000.

## Usage

Once set up, you can use ForgeArmory in conjunction with Foundry VTT for your tabletop role-playing games or for attack simulation. Here’s an example of initializing ForgeArmory:

import { ForgeArmory } from 'forge-armory';

const setup = ForgeArmory.initialize({ config });
setup.run();

To customize ForgeArmory, you can modify the config.js file in the root directory. An example configuration might look like:

const config = {
  port: 3000,
  defaultGame: 'Dungeons & Dragons 5e',
};

## Adding New TTPs

You can add new TTPs to ForgeArmory by forking this repository and adding your TTP YAML files to the appropriate directories in the catalog. Check out the TTPForge documentation to learn the syntax for writing TTPs and explore TTPForge's attack simulation features.

## Submitting Pull Requests

Once your TTPs are ready, feel free to send us a pull request. Our automation will run various linters and checks against new pull requests. Several linters may be used as pre-commit hooks. You can install and set up pre-commit according to the official instructions.

For quick ad hoc runs, you may want to run pre-commit in a virtual environment:

python3 -m venv venv
. venv/bin/activate
pip3 install pre-commit
pre-commit run --all-files

## Contributing

We welcome contributions to ForgeArmory! To contribute, first fork the repository on GitHub, and create a new branch:

git checkout -b feature-name

Make your changes and commit them:

git commit -m "Add feature description"

Push your changes to your fork:

git push origin feature-name

Open a Pull Request (PR) from your fork's branch to the main repository. Ensure that your changes pass the existing tests before submitting your PR. Run tests using:

yarn test

Feel free to submit issues or suggest new features by creating a GitHub issue.

## Glossary

Foundry VTT refers to a virtual tabletop application used to play role-playing games like Dungeons & Dragons. Forge is a hosting service that supports Foundry VTT modules and systems, making it easier to manage and run games without dealing with infrastructure manually.
