This application, built on the Flask framework, demonstrates how a server application can seamlessly integrate with serverless computing to optimize performance and cost. By leveraging Amazon EC2 for hosting, the application benefits from a scalable and flexible virtual server environment that supports diverse workloads, making it ideal for consistent traffic and complex integrations. The application combines biometric authentication, real-time content updates, and monitoring with serverless technologies such as AWS Lambda, S3, SNS, and SQS. EC2 plays a critical role in hosting the main application server, providing a robust foundation for continuous uptime and reliability.


Serverless features complement the EC2 hosting by offloading specific tasks like handling metrics and event-driven operations to AWS Lambda. For instance, Lambda processes metrics for tracking actions such as adding movies, ensuring lightweight and cost-effective operations. This hybrid architecture strikes a balance between performance and expenses, using RDS MySQL for efficient data storage. The advantages of serverless computing within the application include high availability and scalability, as AWS Lambda automatically adjusts to varying loads without user intervention. It also lowers operating expenses since billing is based on actual usage, avoiding costs from underutilized servers. By abstracting infrastructure complexities, the application focuses on delivering user-centric features and usability while benefiting from the reliability of EC2 hosting for its core operations. This hybrid approach highlights the strengths of both traditional hosting and serverless solutions in creating a modern, efficient application ecosystem.


The application itself can be viewed as a SaaS solution for its users, providing secure access to services like content management, file uploads, and real-time metrics through a web-based interface. Additionally, AWS SNS acts as a SaaS tool by delivering notifications to users and administrators via managed endpoints like email or SMS.

![Blank diagram](https://github.com/user-attachments/assets/e51df1da-be2d-45ed-938a-53e0b30c3a0a)



Although serverless computing is as dynamic as it sounds, other static components used in the application include the RDS MySQL for structured data. This combination of an application and a new serverless architecture guarantees that the application uses the potential of the relational database for tasks such as the management of the user credentials and movie records; At the same time, the event-driven and auxiliary functions like the management of metrics and notifications will be observed by the serverless technologies. Serverless computing in this application is supported by other services from AWS. AWS SNS used for notifications for instance user logs in or new movie uploads, eliminates the need for dedicated messaging services. In the same way, AWS SQS provides a means for asynchronous messaging so the processing of movie-related data may run separately and independently enhancing the system’s speed and reliability. Some of these integrations largely explain how serverless computing simply escalates the functionality of a conventional architecture. Cloud computing is not a single technological device, like the smartphone or even microprocessors. As opposed to this, the system is mostly made up of three services: PaaS, IaaS as well as SaaS.


In the light of this application, AWS S3,RDS MySQL and SQS are the examples of IAAS services. These services facilitate the consumption of infrastructure level abstracts such as storage, databases or messaging without having to own or provision hardware. AWS S3 serves as an extremely resizable and fault-tolerant storage medium because any files uploaded by users are safely stored and accessed. RDS MySQL serves a relational database of recognized suitability for use in a Performance, reliable user authentication, with no need to handle the hardware directly for content handling. Like any other reliable messaging service, Amazon’s AWS SQS provides sturdy queuing system to enable asynchronous and scalable communications between the application parts. Collectively these services explain how IaaS relates to the fundamental application infrastructure support services.


The Application part of PaaS offerings is primarily implemented by AWS Lambda which delivers a platform for executing application logic and AWS CloudWatch, which implements the capabilities for monitoring system performance. AWS Lambda is an example of serverless computing as it runs code in response to events while not need to worry about servers, operating systems or runtimes. The application itself can be seen as an example of SaaS because it offers its users a means to securely access and use a number of services and functions via a web browser interface such as content management, file uploads, real-time analytics, and more. Moreover, AWS SNS acts as a SaaS tool by sending notifications to the user or the administrator through a managed subscriber that includes; email or Text Messages. Some of the ways that the application has been designed demonstrates a combination of IaaS, PaaS and SaaS as follows. IaaS elements provide for a solid and elastic infrastructure containing storage, databases, and queues. Services of PaaS like AWS Lambda and AWS CloudWatch helps to make computation and monitoring easier and flexible. SaaS solutions allow the end-users of the managed system to communicate with it effectively, using services such as notifications and file exchange. Collectively, this layered approach shows the advantage of integrating all these service models in fashioning a wealthy, outcome-oriented, and client-centric web application.


The architecture of this application is the combination of the serverless function and the conventional parts, which are provided and integrated with the AWS services. At the center of all this is the business application which communicates with several AWS elements for its operations, contents update, notification and data storages. When a user inputs a movie, the input is stored in Amazon RDS since it is the application’s relation database and any images related to the input will also be stored in the database too. The concept of the RDS instance is that it provides proper storage of all the film descriptions as well as the user credentials. At the same time, the image file is stored on Amazon S3, a very reliable and elastic web-based storage service to obtain public URLs. 


As a result of this flexibility, a movie details message is sent to Amazon SQS where it waits for consumption by other components of the application. From the queue, it is envisioned that AWS Lambda process the message so that lightweight function could be run without needing to manage servers. Lambda also writes data to Amazon CloudWatch for instance, the number of movies uploaded will be logged hence the administrators can analyze system efficiency.


Amazon SNS is in used within the application for notification services in real-time. Some activities include e-mail notification when a user logs in, new movies’ addition, etc…was due to the notification generated and sent by SNS to inform both the users and the administrators. This event-based design enhances the user interactions and organizational visibility.
The means they interconnect users, the application, and AWS services to provide a smooth flow of operations. It was important that the users of the application interact directly with the management of movies and viewing of the images they’ve uploaded while AWS services provide support to deliver the needed reliability, scalability, and performance to the application. This kind of hybrid architecture ensures strong grounding that will allow for smooth handling of the users and their information.
