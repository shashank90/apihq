import json
import re
import yaml
import resource
import ruamel.yaml
from ruamel.yaml.main import round_trip_load as yaml_load, round_trip_dump as yaml_dump


def test1():
    audit_output = "\n[Warning] No .validaterc file found. The validator will run in default mode.\nTo configure the validator, create a .validaterc file.\n\nerrors\n\n  Message :   API definition must have an `swagger` field\n  Path    :   swagger\n  Line    :   1\n\nwarnings\n\n  Message :   The provided document does not match any of the registered formats [OpenAPI 3.x, OpenAPI 2.0 (Swagger), OpenAPI 3.0.x, OpenAPI 3.1.x]\n  Path    :   \n  Line    :   1\n\n"
    temp = re.sub(
        r"(^\n[Warning\]\s+[a-zA-Z\s.,\n]*).validaterc file.\n\n", "", audit_output
    )
    print(temp)


def test():
    json_str = "\nopenapi: \"3.0.0\"\ninfo:\n  version: 1.0.0\n  title: Swagger Petstore\n  description: A sample API that uses a petstore as an example to demonstrate features in the OpenAPI 3.0 specification\nservers:\n  - url: http://petstore.swagger.io/api\n  paths:\n  /pets:\n    get:\n      description: |\n        Returns all pets from the system that the user has access to\n        Nam sed condimentum est. Maecenas tempor sagittis sapien, nec rhoncus sem sagittis sit amet. Aenean at gravida augue, ac iaculis sem. Curabitur odio lorem, ornare eget elementum nec, cursus id lectus. Duis mi turpis, pulvinar ac eros ac, tincidunt varius justo. In hac habitasse platea dictumst. Integer at adipiscing ante, a sagittis ligula. Aenean pharetra tempor ante molestie imperdiet. Vivamus id aliquam diam. Cras quis velit non tortor eleifend sagittis. Praesent at enim pharetra urna volutpat venenatis eget eget mauris. In eleifend fermentum facilisis. Praesent enim enim, gravida ac sodales sed, placerat id erat. Suspendisse lacus dolor, consectetur non augue vel, vehicula interdum libero. Morbi euismod sagittis libero sed lacinia.\n        Sed tempus felis lobortis leo pulvinar rutrum. Nam mattis velit nisl, eu condimentum ligula luctus nec. Phasellus semper velit eget aliquet faucibus. In a mattis elit. Phasellus vel urna viverra, condimentum lorem id, rhoncus nibh. Ut pellentesque posuere elementum. Sed a varius odio. Morbi rhoncus ligula libero, vel eleifend nunc tristique vitae. Fusce et sem dui. Aenean nec scelerisque tortor. Fusce malesuada accumsan magna vel tempus. Quisque mollis felis eu dolor tristique, sit amet auctor felis gravida. Sed libero lorem, molestie sed nisl in, accumsan tempor nisi. Fusce sollicitudin massa ut lacinia mattis. Sed vel eleifend lorem. Pellentesque vitae felis pretium, pulvinar elit eu, euismod sapien.\n      operationId: findPets\n      parameters:\n        - name: tags\n          in: query\n          description: tags to filter by\n          required: false\n          style: form\n          schema:\n            type: array\n            items:\n              type: string\n        - name: limit\n          in: query\n          description: maximum number of results to return\n          required: false\n          schema:\n            type: integer\n            format: int32\n      responses:\n        '200':\n          description: pet response\n          content:\n            application/json:\n              schema:\n                type: array\n                items:\n                  $ref: '#/components/schemas/Pet'\n        default:\n          description: unexpected error\n          content:\n            application/json:\n              schema:\n                $ref: '#/components/schemas/Error'\n    post:\n      description: Creates a new pet in the store. Duplicates are allowed\n      operationId: addPet\n      requestBody:\n        description: Pet to add to the store\n        required: true\n        content:\n          application/json:\n            schema:\n              $ref: '#/components/schemas/NewPet'\n      responses:\n        '200':\n          description: pet response\n          content:\n            application/json:\n              schema:\n                $ref: '#/components/schemas/Pet'\n        default:\n          description: unexpected error\n          content:\n            application/json:\n              schema:\n                $ref: '#/components/schemas/Error'\ncomponents:\nschemas:\n  Pet:\n    allOf:\n      - $ref: '#/components/schemas/NewPet'\n      - type: object\n        required:\n        - id\n        properties:\n          id:\n            type: integer\n            format: int64\n\n  NewPet:\n    type: object\n    required:\n      - name  \n    properties:\n      name:\n        type: string\n      tag:\n        type: string    \n\n  Error:\n    type: object\n    required:\n      - code\n      - message\n    properties:\n      code:\n        type: integer\n        format: int32\n      message:\n        type: string "
    try:
        # json.loads(json_str)
        content = json.loads(json.dumps(json_str))
        # print(content)
        ff = open("test.yaml", "w+")
        print(content)
        # print(yaml_dump(content))

        # with open("data.yml", "w") as outfile:
        # yaml.dump(content, outfile, default_flow_style=False)

        # open text file
        text_file = open("data.yaml", "w")

        # write string to file
        n = text_file.write(content)

        # close file
        text_file.close()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    test1()
