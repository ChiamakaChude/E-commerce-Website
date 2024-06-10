<h3>E-commerce Web Application</h3>

<p>This project contains codes designed to build an e-commerce web application</p>

<p>It aims to create a platform that is resilient, flexible, scalable and modular with the use of modern techniques and tools, aligning with the principles and expectations of cloud native software. In order to meet and exceed users expectations</p>


<h3>Components</h3>

<p><b>It consists of 2 Microservices:</b><br>
1. User Microservice: this handles user related functions of the application such as log in, sign up, profile management, and logout.<br>
2. Product Microservice: it handles product related functions such as viewing products, creating a new product, adding and viewing product reviews.<br>

<p><b>Messaging service</b><br>
The projet also makes use of the Apache Kafka event streaming platform for asynchronour communication between the microservices<br><br>


<p><b>Docker</b><br>
The Components were containerised with docker. Each microservice consists of a Dockerfile used to build images. A compose file was also created to pull all the images from the Docker Hub to run on the same network.
</p>
