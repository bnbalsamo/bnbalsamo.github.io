---
layout: page
---


- get a basic understanding of all the exciting acronyms, APIs, REST, etc
- once we know what they are, figure out how to use them
- Use an API!
- Quickly discuss webhooks if there's time.


- The majority of this talk is meant to be interacting with the API!
- Please participate, or at least look over someone elses shoulder!

---

- APIs are how programs expose functionality to outside systems
    - Useful for integration and extension!
- APIs are interfaces for machines, not people!
    - But the first step to building a program to use them
      is using one yourself!
- APIs vs RPA
    - RPA is teaching machines to use human interfaces
    - APIs are an interface built for machines
    - Both are appropriate in different scenarios

- Not all APIs are web APIs, some expose their functionality through
  a different medium, like a programming language or a non-http socket
  connection, but for the rest of this talk whenever I say API it's safe
  to assume that I'm discussing a web API.

---

- Lots of companies have APIs
- Useful for interoperability, exposing functionality, supporting extension, etc.
- Becoming more prevalent in environments with microservices, distributed architectures,
  single page applications, multiple front ends based on the same data, etc.
- We're going to discuss REST APIs. Not every API is a REST API, but plenty of them are. 
  APIs are organized based on what their intended use is.

---

- REST is a method of organizing APIs
- **State**
    - You tell the API what state you want the objects in
        - You DON'T tell it how to get there.


- There are other kinds of APIs
    - SOAP: Precursor to REST, kind of, but didn't live up to its _simple_ name.
    - RPC: Less often implemented over HTTP, still relevant, but mostly for distributed computing.


- REST organizes information about application state into three general types.
    - Collection
    - Object
    - Subcollection


- A collection is like the whole spreadsheet
- An object is like a single row
- A subcollection is... like some rows from the spreadsheet with some quality

---

- Web APIs utilize HTTP to communicate.

- HTTP is the same thing your browser uses

- HTTP is a request/responses protocol.
    - Client sends request to server
    - Server processes request
    - Server sends response to client

Requests and responses have a variety of ways to store data or metadata.
- Header
- Query params (url)
- The request body

HTTP requests are split up into different methods based on what the action is meant
to do.

In different contexts these methods might mean slightly different things.

In the context of APIs...

---

REST maps the HTTP verbs onto different ways to change object state.

**CRUD**

This means that a single endpoint can serve multiple purposes depending on the 
kind of request you send to it!

---

What does our service do?

Stores data about authors and quotes.

---

Data schema + relations

---

Endpoints to park our collections and objects at...

---

Live demo/walkthrough of ths one.

---

Ask people to try on their own.

---

Tricky one - PUT or PATCH can both work, but operate differently.

---
