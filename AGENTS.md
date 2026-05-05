List of things to NOT do unless explicitly asked
  - Do NOT try to run the project's code
  - Do NOT 'git commit'

When asked on how to run stuff, you may first explain what is going on, then explain the commands, and at last you put all commands in a single chunk in the order they will be executed.

There is a docker-compose file with all services.
You have permission to access the .env. Any variables that must be synced across all services will read from it (mainly URLs).

There are `auxpy.py` and `auxmd.md`. They are scratchpads with throwaway code and notes. They are useful in short-term, hence why they are in the .gitignore. Do not edit these two files unless told to so.