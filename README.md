# Cloud Thin Layer Test

This repository contains an application that can be interfaced using the sdrdm-workflow framework, which contains the following:

- Some script-like or software-like application that "does" something
- Specifications as markdown that are used to map values and classes to
- An entrypoint which is called within the container


## Thin layer services

Thin layers revolve around offering small services such as parameter estimation, visualisation or simulation in a "container" fashion. For this, sdRDM offers a generic Docker image which can be used as a "worker" to execute these services in a controlled and streamlined way. Secondly, software providers or researchers can wrap their works in such a container to make sure results are reproduced accordingly (as close as possible). 

Thin layer interfaces are defined as Markdown, such that researchers can "dock" data models using sdRDM linking templates without having to write code. See the ```specifications/model.md``` file for an example. Here the ```Calculator``` app takes in a number and an exponent to potentiate each other. In addition, the app also defines how results are given back (see the ```Result``` object). This adds advantages for bot researcher and developer, since the latter can make sure to use the software properly by providing logic, whereas the user has a clear documentation what to insert and what to expect.

The minimum requirement necessary to run such a service are two things:

- Provide an ```entrypoint.py``` and ```main()``` function to execute the code.
- Make sure that all dependencies are met by providing a ```requirements.txt``` - These will be installed within the container.

Other than that everything is up to your application logic.

## How to use the given service

### Image set up

In order to use the application, first install [Docker](https://docker.com/) and read this [tutorial](https://docs.docker.com/get-started/) to get started. When everything has been installed succesfully, build and start the container using the following commands.

```bash
# Build the image
docker build -t sdrdm-worker https://github.com/JR-1991/sdrdm-workflow-image.git

# Run the container
docker run -p 8000:80 -d sdrdm-worker
```

You can now access the docker image via ```localhost:8000```, which should lead to a (tiny) documentation. Next up, we are going to build an artifical data model, from which we'd like to send our data to the ```Calculator``` application to perform the service.

### Client-side data model

The data model in use here will be inferred from sdRDM's ```parse```-method, which, if no ```__source__``` for model reproduction is given, generates a model on the fly. Last, we will need a linking template to connect our model to the app's interface.

##### Code
```python
import requests

from sdRDM import DataModel

# The simple data model
raw_data = {
    "name": "Jan Range",
    "my_number": 20
}

# Parse it, using sdRDM
dataset, lib = DataModel.parse(data=raw_data, root_name="HostModel")

# Define a template on how to map data
template = {
        '__model__': 'HostModel',
        '__sources__': {'Calculator': 'https://github.com/JR-1991/application.git'},
        '__constants__': {
            'Calculator': {
                'exponent': 10
            }},
        'HostModel': {'my_number': 'Calculator.number'}
    }

# Finally, send everything to the application
result = requests.post(
        "http://localhost:8000",
        json={
            "data": dataset.dict(),
            "name": dataset.__class__.__name__,
            "template": template,
            "app": "https://github.com/JR-1991/cloud-sdrdm-test-app.git"
        }
    ).json() 

print(result)

# From this point on, write the results back to your model
# or send it to another application.
```

##### Output

```json
{
    "id": "calculator0",
    "number": 20.0,
    "exponent": 10,
    "results": [
        {"id": "result0", "number": 10240000000000.0}
    ]
}
```

--------
