# Running the AI Engineering Interview Repo

## Step 1 - Obtain and Set Credentials
**IMPORTANT NOTE:** I will provide you with `VITAL_API_KEY` and `OPENAI_API_KEY` at the start of our interview; you are more than welcome to generate your own if you desire.

```
# Copy the .env.example file:
cp .env.example .env

# Fill all the env variables in the .env file
VITAL_API_KEY=""
VITAL_ENV=sandbox
VITAL_REGION=us
OPENAI_API_KEY=""
```

```
# Run fixenv.sh; this copies the environment variables into the correct locations
./fixenv.sh
```

## Step 2 - Run using Docker 

```
# Run Docker 
docker compose up --build
```

## Step 3 - Specific to Interview
Please review `CANDIDATE_GUIDE_README.md`

**IMPORTANT NOTE:** You will want to run the steps above and build the Docker container in advance. However, the backend will error out on the initial build given the lack of `VITAL_API_KEY` and `OPENAI_API_KEY`. Once I provide you with the API keys, you will copy/paste them into the root `.env` and execute:
```
./fixenv.sh
docker compose restart
docker compose up
```