# QUESTION 

  This is a group project work that students will do throughout the semester. This is to enable them do a practical exhibition of all the technologies learnt during the course of study. Students have the right to choose any organization to use as a case study.

# Title: Blood Bank Management System

Blood bank management is a useful application for organizations (managing blood bank) and the hospitals to maintain the records of blood unit, serve the donation and blood request.

Students are to use Tkinter for GUI development and MySQL for database management to implement this project.

Blood bank system tracks the availability of different blood types in real-time, ensuring hospitals and organizations can access the required data quickly, facilitate the management of blood donors, including registration, donation history, and scheduling for future donations, provide a platform for hospitals to request specific blood types and track the status of their requests efficiently and implement a secure and well-structured database using MySQL for storing and managing sensitive data such as donor details, blood inventory, and transaction records.

• The system should fetch all the records from the BloodBank table and displaying the same on the screen using mysql connector.
• The entries consist of blood group, the units of blood available of the particular blood group, and two tkinter buttons to perform the functionalities (donate, and request) and as per user requirement.
• The user to enter the required blood group and amount using the Tkinter entry widget and then it offers a submit button to call the request_dbase() method which checks availability and updates data correspondingly.
• Connects with the database and checks if the asked amount of blood is available or not. If not, it displays the required message. Otherwise, it completes the request and reduces the units of the particular blood group in the database, and flashes the corresponding message box.
• Two methods (donate and donate_dbase) just increase the units of blood donated by the user.
 

# SYSTEM FEATURES

▪ The admin login
▪ Homepage display blood groups and unit with donate and request options.
▪ Register Donors with their blood groups
▪ Blood request button to enter the units of blood required with date
▪ Donate blood button to enter blood group to donate with date
▪ Blood donation history
▪ Logout


# NB: I used Postgresql for the databse instead of mysql
