![build and test status](https://github.com/DigitalCommons/mykomap-monolith/actions/workflows/node-build-test.yml/badge.svg)

# LRU

A project by the LondonRentersUnion Data and Research Coworking Group to repurpose the Digital Commons Cooperative Mykomap's project to highlight housing licence data.

## SETUP

The original .README had some perhaps outdated local setup data - you might need WSL if you're on Windows to run bash lines.

1. npm ci
2. Duplicate the .env.examples in both the backend and frontend, then rename to .env, remember to insert a MapTiler API key.
3. npm run build
4. npm run dev in both backend and frontend

Navigate to `localhost:5173/?datasetId=cwm-latest` in the browser to see the map. Replace `cwm-latest` with `powys-eng` or any other dataset name from the `cwm-test-data` repo to see it on the map.

The LRU licensing data is in `/apps/back-end/test/data/datasets/lru-licensing`
Items are not stored in this repo, ask around for them if you're part of LRU.

## RUNNING STORYBOOK

Just run the static version.

Everything past this line is from the original Digital Commons Cooperative .README.

---

# Mykomap Mono-Repo

Mono-repo home to the FE/BE applications and libraries comprising Mykomap.

See the full technical documentation [here](https://digitalcommons.github.io/mykomap-monolith/).

This is a Digital Commons Cooperative project, please follow the [contribution guidelines](https://github.com/DigitalCommons#-contributing) if you wish to participate in building Mykomaps.

## Applications

- [Front-end](./apps/front-end/)
- [Back-end](./apps/back-end/)

## Libraries

- [Common](./libs/common/), which contains the OpenAPI spec and ts-rest contract.
- [Node Utils](./libs/node-utils), which contains file manipulation functions.

## How to install a dependency

```
npm i <package> -w <workspace name> --save
```

e.g.

```
npm i @fastify/cors -w @mykomap/back-end --save
```

## Installation

See [deployment docs](https://digitalcommons.github.io/mykomap-monolith/deployment/).

## Quick Local Set-up

There are 4 codebases and 1 data source to setup. Follow the order as written here.

Note: users on windows will need to use WSL as some of the build steps are unix-like.

### Data

1. Download data by cloning this repository: https://github.com/DigitalCommons/cwm-test-data
1. Navigate into the directory and do `git checkout dev` to use the dev branch of the data
1. Note the path to the datasets directory from the Mykomap directory because you'll need this later for the back-end .env file

### Node Utils & Common Types

1. `cd libs/node-utils`
1. `npm ci`
1. `npm run build`
1. `cd ../common`
1. `npm ci`
1. `npm run build`

### Back-end

1. `cd apps/back-end`
1. Copy .env file contents from BitWarden under Mykomap Back End .env Variables. The values in Bitwarden assume that you created `cwm-test-data` in a directory next to `mykomap-monolith`. If you did something different update the SERVER_DATA_ROOT env variable.
1. Create `.env` next to `.env.example`
1. `npm ci`
1. `npm run dev`

### Front-end

1. `cd apps/front-end`
1. Copy .env file contents from BitWarden under Mykomap Front End .env Variables
1. Create `.env` next to `.env.example`
1. `npm ci`
1. `npm run dev`

Navigate to `localhost:5173/?datasetId=cwm-latest` in the browser to see the map. Replace `cwm-latest` with `powys-eng` or any other dataset name from the `cwm-test-data` repo to see it on the map.
