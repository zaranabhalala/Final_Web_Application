# Final Web Application

## Team members
1. Zarana Bhalala
2. Jay Sorathiya

## Project feature 1
### Zarana Bhalala
1.  Created a login and registration process that includes email verification.
* Login Process - Log into your account by entering your email address and password.
* Registration Process - Create new account by clicking "Register" button and  submitting your account information.
* Upon a register, user will receive an Email with attached link to verify their login. Once the login is verified, the user will be able to login to view player's database.
* To view the feature working step by step [Click Here](Final%20Web%20Application.pdf). 

### Jay Sorathiya
2. Created API endpoints and from those endpoints created Charts of the available data using a Chart.js in Javascript
* Login Process - Log into your account by entering your email address and password.
* Click on Player Statistics (the Green button on top).
* Upon clicking, the page will display the statistics of Players according to their positions.
* As long as the new data is added, the statistics will change.
* To view this feature working step by step [Click Here](). 

# Installation instructions
### Prerequisites:
* Port 5000 and 3200 are open to use in system.
* Docker is installed and running.

### Steps:
* Clone the repository -
`git clone https://github.com/zaranabhalala/Final_Web_Application`
  
* Go to the Final_Web_Application folder - 
`cd Final_Web_Application`
  
* Build and run the code - 
`docker-compose up`
  
* It will start and run with MYSQL and Flask App and then open a browser and paste below URL - 
`http://localhost:5000/`
