To upload test data:

1. Delete existing postgres volumes:
    - `docker volume ls`
    - `docker volume rm ${volume_name}`
2. Start backend:
    - `docker-compose up`
3. Install `jq` if not installed
    - `brew install jq` or `apt-get install jq`
4. Upload:
    - `cd` to this directory
    - `chmod +x upload.sh`
    - `./upload.sh`
