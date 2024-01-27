# Processor Integration Box

This is a simple script to emulate a processor that takes in a file via sftp and can output multiple files.

### Config file
```json5
{
  // input filename matching follows the unix filename globbing standard
  // like * would mean match everything and *.txt would mean match everything 
  // that ends with .txt
  "*": {
    "output_files": ["example.txt"],
    // Optional bytes in hex to check for some validation bytes in the input files
    "input_byte_match": ""
  },
  // Will only run if the input filename matches this name
  "example_input.txt": {
    "output_files": ["example.txt"],
    "input_byte_match": ""
  }
}
```

### Example Running
```shell
docker build -f dockerfiles/centos7.Dockerfile -t centos7-sftp .
docker run -it -p 2222:22 --rm centos7-sftp

docker build -f dockerfiles/rockylinux8.Dockerfile -t rockylinux8-sftp .
docker run -it -p 2222:22 --rm rockylinux8-sftp

docker build -f dockerfiles/rockylinux9.Dockerfile -t rockylinux9-sftp .
docker run -it -p 2222:22 --rm rockylinux9-sftp

# sshing which is disabled would be accomplished via
ssh -p 2222 sftp_user@localhost
# Using sftp
sftp -P 2222 sftp_user@localhost
```