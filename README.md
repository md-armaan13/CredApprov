# Credit Approval Api's



The Credit Approval API project aims to provide a robust and efficient system for assessing and approving loans based on customers' creditworthiness. Leveraging the Python/Django stack, the API utilizes past data and future transactions to evaluate various parameters, including loan history, repayment behavior, and current financial status.

Ultimately, the Credit Approval API streamlines the loan approval process, providing a reliable solution for financial institutions to assess credit risk and make timely lending decisions. 

Credit Approval Api is available as a hosted service
at [https://myfavouritestunes.io/](http://20.193.151.75:8000/).

A [Swagger API documentaion for Credit Approval API](https://github.com/md-armaan13/My-Favourites-Tunes/blob/master/DockerFile) is 
available [].

Screenshots:

![Screenshot of Period/Grace dialog](/static/common/images/loginpage.png "Period/Grace Dialog")

##

![Screenshot of Cron dialog](/static/common/images/musicpage.png "Cron Dialog")



##

![Screenshot of Badges page](/static/common/images/artistpage.png "Status Badges")


## Setting Up for Development

To set up My Favourites Tunes development environment:

* Install dependencies (Debian/Ubuntu):

  ```sh
  sudo apt update
  sudo apt install -y gcc python3-dev python3-venv libpq-dev libcurl4-openssl-dev libssl-dev
  ```

* Prepare directory for project code and virtualenv. Feel free to use a
  different location:

  ```sh
  mkdir -p ~/babynama
  cd ~/babynam
  ```

* Prepare virtual environment
  (with virtualenv you get pip, we'll use it soon to install requirements):

  ```sh
  python3 -m venv venv
  source venv/bin/activate
  pip3 install wheel # make sure wheel is installed in the venv
  ```

* Check out project code:

  ```sh
  git clone https://github.com/md-armaan13/My-Favourites-Tunes.git
  ```

* Install requirements (Django, ...) into virtualenv:

  ```sh
  pip install -r requirements.txt
  ```


* Now create the .env in the root and copy the Environment Variables From Gist [here]( https://gist.github.com/md-armaan13/4791efb08d1f2d6d247cbdf938d27e74)

  ```sh
  https://gist.github.com/md-armaan13/4791efb08d1f2d6d247cbdf938d27e74
  ```




* Run development server:

  ```sh
  python manage.py runserver
  ```

The site should now be running at `http://localhost:8000`.
To access Django administration site, log in as a superuser, then
visit `http://localhost:8000/admin/`
* Defualt Login Credentials are:

  ```sh
  Email admin@gmail.com
  Pass  admin123
  ```

## Using Docker
To set up My Favourites Tunes development environment using docker :
* Now create the .env in the root and copy the Environment Variables From Gist [here]( https://gist.github.com/md-armaan13/4791efb08d1f2d6d247cbdf938d27e74)

  ```sh
  https://gist.github.com/md-armaan13/4791efb08d1f2d6d247cbdf938d27e74
  ```
* Make sure that the Dockerfile is in the same directory where you are running the docker build command.
  ```sh
  docker build -t my-favourite-tunes .
  ```
* To run a Docker container from the image you've built, you can use the docker run command.
  ```sh
  docker run -p 8000:8000 my-favourite-tunes
  ```
  After running this command, your Django application should be accessible at http://localhost:8000 in your web browser.