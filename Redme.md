Image Sorting and Face Recognition System
This project is focused on developing an Image Sorting and Face Recognition System that enables the automatic organization of images based on known faces. The program uses machine learning techniques to recognize faces in images and sort them into respective folders. The main goal is to facilitate the management of large collections of images and provide a simple user interface to perform sorting operations efficiently.
Synopsis
1. Introduction
The Image Sorting and Face Recognition System leverages facial recognition technology to automatically categorize images by person. The system is designed to read images from a specified directory, process each image to detect faces, and then sort them into corresponding directories based on recognized individuals. The application provides a graphical user interface (GUI) that simplifies the image sorting process.

2. Objectives
The primary objectives of this project are:
1. To implement facial recognition technology to identify known faces in a set of images.
2. To organize images based on detected faces by sorting them into respective folders.
3. To provide a user-friendly GUI for users to interact with the program, select directories, and start the sorting process.
4. To ensure the program handles errors gracefully and provides feedback through a log system.

3. Methodology
The project follows a methodical approach:
1. Face Recognition: The system uses the `face_recognition` library to detect and compare faces in images against a database of known faces stored in a specific directory.
2. Image Sorting: Based on the recognized faces, the system organizes the images into different directories. Each directory corresponds to a specific person. If no match is found, the image is moved to a "NoKnownFaces" directory.
3. Graphical User Interface (GUI): The user interacts with the system through a GUI built using Tkinter. The interface allows users to select directories, view progress, and initiate sorting operations.
4. Error Handling: The program handles errors like missing directories or unrecognized faces by displaying appropriate messages to the user.

4. Features
The key features of the system include:
1. Directory Selection: The user can select directories for known faces, images to process, and the destination sorted directory.
2. Real-Time Log Updates: During image processing, the application logs each processed image in real-time, ensuring transparency.
3. Automatic Directory Creation: If the sorted directory does not exist, the system automatically creates it to ensure proper image sorting.
4. Asynchronous Processing: The sorting process runs on a separate thread to prevent the application from becoming unresponsive during heavy processing.
5. Face Matching and Sorting: The system matches faces and moves images into directories corresponding to recognized individuals.

5. Conclusion
This project successfully demonstrates the use of facial recognition and image sorting techniques to automate the management of image collections. By utilizing machine learning and Tkinter for the GUI, the system offers an intuitive and efficient solution for sorting images based on recognized faces. The system can be further enhanced to handle more complex scenarios and provide additional features like bulk image uploads or integration with cloud-based storage for large-scale implementations.

Submitted by: Mohd Salman Quadri(Project Head), Kirti Solanki(Team Member),Priyansh Sharma(Team Member)
College: Engineering College Bikaner
Department: BCA 3rd Year
Date: 18 November 2024
