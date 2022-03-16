export const defaultValue = `${`
openapi: 3.0.0
info:
  version: 1.0.0
  title: Pet Store
servers:
- url: http://example.com
paths:
  /apis/v1/pets:
    post:
      summary: Add new pet
      tags:
      - pets
      description: Add new pet
      operationId: addPet
      requestBody:
        description: Add new pet
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/addPet'
      responses:
        '201':
          description: Pet added successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  pet_id:
                    description: pet_id
                    type: string
                    pattern: ^w+$
                    maxLength: 20
                  message:
                    description: message
                    type: string
                    pattern: ^w+$
                    maxLength: 30
        '400':
          $ref: '#/components/responses/BadRequest'
  /apis/v1/pets:{pet_id}:
    get:
      description: Get pet from store
      summary: Get pet from store
      operationId: getPet
      tags:
      - pets
      parameters:
      - name: pet_id
        in: path
        required: true
        description: Unique pet_id
        schema:
          type: string
          pattern: ^w+$
          maxLength: 40
          minLength: 0
      responses:
        '200':
          description: Pet retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  name:
                    description: pet name
                    type: string
                    pattern: ^w+$
                    maxLength: 20
        '400':
          $ref: '#/components/responses/BadRequest'
components:
  schemas:
    addPet:
      type: object
      required:
      - pet_name
      - breed
      properties:
        pet_name:
          type: string
          pattern: ^w+$
          maxLength: 30
          minLength: 0
          description: Pet name.
        breed:
          pattern: ^w+$
          type: string
          minLength: 0
          maxLength: 30
          description: Pet breed.
  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            type: object
            required:
            - error
            properties:
              error:
                description: error
                type: object
                required:
                - code
                - message
                properties:
                  code:
                    description: code
                    type: string
                    pattern: ^w+$
                    maxLength: 10
                  message:
                    description: message
                    type: string
                    pattern: ^w+$
                    maxLength: 20
tags:
- name: pets
  description: Everything about pets  
`}`;
