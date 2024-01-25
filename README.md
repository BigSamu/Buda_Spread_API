<a name="back-to-top"></a>

# Buda Spread API

<!-- *********************************************************************** -->
<!-- I) ABOUT THE PROJECT -->
<!-- *********************************************************************** -->

## About The Project

This API is designed for Buda.com to calculate and manage the spread across various markets. Key features include:

- Retrieving the spread of all markets in a single API call.
- Managing a 'spread alert' system, enabling users to set and check spread thresholds.

The API supports polling to determine if the current spread is above or below these thresholds.

The service has been deployed in [Vercel](https://vercel.com) and configured with documentation with two user interfaces

- **SwaggerUI** served at [https://buda-spread-api-sandy.vercel.app/api/doc](https://spread-api-sandy.vercel.app/api/doc)
- **ReDoc** served at [https://buda-spread-api-sandy.vercel.app/api/redoc](https://spread-api-sandy.vercel.app/api/redoc)

---

<!-- *********************************************************************** -->
<!-- II) TECHNOLOGIES -->
<!-- *********************************************************************** -->

## Technologies

The following technologies are used for the implementation of this project:

![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![PyPI Badge](https://img.shields.io/badge/PyPI-3775A9?logo=pypi&logoColor=fff&style=for-the-badge)
![FastAPI Badge](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=for-the-badge)
![Docker Badge](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge)
![Vercel Badge](https://img.shields.io/badge/Vercel-000?logo=vercel&logoColor=fff&style=for-the-badge)
![Swagger Badge](https://img.shields.io/badge/Swagger-85EA2D?logo=swagger&logoColor=000&style=for-the-badge)
<img src="https://raw.githubusercontent.com/Redocly/redoc/main/docs/images/redoc.png" alt="Swagger Badge" style="height: 28px; width: auto;">


<p align="right">(<a href="#back-to-top">back to top</a>)</p>

---

<!-- *********************************************************************** -->
<!-- III) GETTING STARTED -->
<!-- *********************************************************************** -->

## Getting Started

<!-- ----------------------------------------------------------------------- -->
<!-- 3.1) Prerequisites -->
<!-- ----------------------------------------------------------------------- -->

### Prerequisites

For setting up your local environment `Python3` and a `pip3` are required for running the API locally.

For easy management of packages and environment `pipenv` is used. To install this tool globally run:

```sh
pip3 install pipenv
```

<!-- 3.2) Installation -->
<!-- ----------------------------------------------------------------------- -->

### Installation

To get a copy of this project and run it in your local environment, follow the steps listed below.

1. Clone the repo
   ```sh
   git clone git@github.com:BigSamu/SuperhereoAPI_Simulation.git
   ```
2. Go into the repository
   ```sh
   cd SuperhereoAPI_Simulation
   ```
3. Install required pyhon packages or dependencies
   ```sh
   pipenv install
   ```
4. Create a .env file and add the following related API Keys and Domains

   ```sh
   SUPERHERO_API_KEY=[YOUR_SUPERHERO_API_KEY]
   MAILGUN_API_KEY=[YOUR_MAILGUN_API_KEY]
   MAILGUN_DOMAIN_NAME=[YOUR_MAILGUN_DOMAIN_NAME]
   ```
5. Activate virtual environemnt
   ```sh
   pipenv shell
   ```

6. Run application
   ```sh
   python -m app.main [-email <email address>]
   ```

<p align="right">(<a href="#back-to-top">back to top</a>)</p>

<!-- ----------------------------------------------------------------------- -->
<!-- 3.3) Usage -->
<!-- ----------------------------------------------------------------------- -->

### Usage

After successful installation and execution, you will be able to experience the simulation in your terminal. If an email address is provided, you will receive the results of the simulation in your email.

> **NOTE:** The email address provided has to be registered in your domain in Mailgun API, so the script can send the results of the simulation that particular email.

<p align="right">(<a href="#back-to-top">back to top</a>)</p>

---

<!-- *********************************************************************** -->
<!-- VIII) FOOTER -->
<!-- *********************************************************************** -->

<p align="center">
Developed with ❤️ in Chile 🇨🇱
</p>
