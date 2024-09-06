#!/bin/bash

# simple check . one day ill make a proper check endpoint
if curl -s http://localhost:8000 | grep "Ethan"; then
	  echo "App is running successfully"
	    exit 0
    else
	      echo "App validation failed"
	        exit 1
fi

