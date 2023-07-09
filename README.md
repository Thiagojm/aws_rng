# aws_rng

## Introduction
Python code to record bits using TrueRNG3 on Rapsberry Pi and send to an AWS Bucket.

## Usage
The rng_collect.py file writes the data to a .csv and a .bin (control) file.
The send_aws.py file sends the data to a Bucket in AWS and then deletes it locally.
