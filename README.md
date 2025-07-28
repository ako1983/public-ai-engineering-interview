# Running the AI Engineering Interview Repo

## Step 1 - Obtain and Set Credentials

The first step is to obtain your credentials from the Vital/Junction Dashboard and OpenAI.

**IMPORTANT NOTE:** I will provide you with `VITAL_API_KEY` and `OPENAI_API_KEY` at the start of our interview; you are more than welcome to generate your own if you desire.

Once you have done this:

```
# Copy the .env.example file:
cp .env.example .env

# Fill all the env variables in the .env file
VITAL_API_KEY=..
VITAL_ENV=sandbox
VITAL_REGION=us
OPENAI_API_KEY=..
```

## Step 2 - Run using Docker 

```
# Run fixenv.sh this copies the environment variables into the correct locations
./fixenv.sh

# Run Docker 
docker compose up --build
```