# Triige Backend

## Summary
Triige is able to quickly assess the severity of each victim’s condition and assign each person a priority for immediate treatment. It does this by attaching QR codes preprogrammed with SHA-256 encryption hashes to patients at the scene. First responders scan the QR code and input a patient’s data either manually or by using voice commands. Entered inputs are stored on a Flask server in the IBM Cloud. This information can be retrieved from the IBM Cloud by GET & POST requests. Our user interface (UI) is simple and easy to use while allowing for first responders to see a variety of aggregate data such as the amount of blood needed. We comply with the HIPPA standards since all data is stored on the IBM Cloud along with leveraging all the security features provided by the cloud. Additionally, no patient health information is stored on QR codes to protect the patient’s privacy.

## What it Does
The backend server allows the mobile application to add new patients and get patient medical information already entered into the database. The database stores everything from a pateint's age to their exact gps location at any given time.

In order to keep all this very sensitive data safe, we implemented a very secure token authentication system along with leveraging all the security features of the cloud. During every step of the process, we made sure that we were strictly adhereing to all the professional standards specifically the HPPA security standard. 

## Getting Started
If you want the username and password to login and use the Flask server then please email me at: pauljprogrammer@gmail.com. 

Otherwise, you can access the a basic implementation of the server at: https://repl.it/@pauljprogrammer/Tech-to-Protect-10-Backend. More isntructions are provided in repl.

## How it's Built
The backend server is built using Flask and hosted on the IBM Cloud. It stores all patient and responder data in a SQLite database.

- [Demo Slides](https://github.com/dhruvilp/triige/blob/master/screenshots/demo_slides.pdf)


## Triige Mobile App Repository
- [Triige Mobile App Repository](https://github.com/dhruvilp/triige)


If you have any questions about our project and want to gain access to our backend server feel free to email Paul (pauljprogrammer@gmail.com) or Dhruvil (atdhruvilpatel@gmail.com). Thanks!
