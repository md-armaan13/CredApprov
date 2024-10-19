# Credit Approval Api's



The Credit Approval API project aims to provide a robust and efficient system for assessing and approving loans based on customers' creditworthiness. Leveraging the Python/Django stack, the API utilizes past data and future transactions to evaluate various parameters, including loan history, repayment behavior, and current financial status.

Ultimately, the Credit Approval API streamlines the loan approval process, providing a reliable solution for financial institutions to assess credit risk and make timely lending decisions. 

Credit Approval Api is available as a hosted service
at [https://mycreditapi/](http://15.206.171.158:3000/api/docs/).

A [Swagger API documentaion for Credit Approval API](http://15.206.171.158:3000/api/docs/) is 
available Here [http://15.206.171.158:3000/api/docs/](http://15.206.171.158:3000/api/docs/).



## Using Docker
* To set up 'Credit Approval Api' environment using docker :
Prepare directory for project code and virtualenv. Feel free to use a
  different location:

   ```sh
   mkdir -p ~/creditApprov
   cd ~/CreditApprov
   ```
* Check out project code:

  ```sh
  git clone https://github.com/md-armaan13/CredApprov.git
  ```
   ```sh
  cd CredApprov
  ```

* Make sure that the docker and docker-compose is already installed in the system . Run below command to build images context
  ```sh
  docker-compose build
  ```
* To run a Docker containers from the image you've built, you can use the docker run command.
  ```sh
  docker-compose up
  ```
  After running this command, your Django application should be accessible at http://localhost:3000 in your web browser.

