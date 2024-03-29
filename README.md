<a name="back-to-top"></a>

# Buda Spread API

[![Github Follow][github-follow-badge]][github-follow-url]
[![Ask Me Anything][ama-badge]][ama-url]
[![Say Thanks!][say-thanks-badge]][say-thanks-url]
[![License][license-badge]][license-url]
![coverage](assets/coverage.svg)

<!-- *********************************************************************** -->
<!-- I) ABOUT THE PROJECT -->
<!-- *********************************************************************** -->

## About The Project

This API is designed for Buda.com to calculate and manage the spread across various markets. Key features include:

- Retrieving the spread of all markets in a single API call.
- Managing a 'spread alert' system, enabling users to set and check spread thresholds.

The API supports polling to determine if the current spread is above or below these thresholds.

The service has been deployed in [Vercel](https://vercel.com) and configured with documentation with two user interfaces

- **SwaggerUI** served at [https://buda-spread-api-sandy.vercel.app/api/docs](https://buda-spread-api-sandy.vercel.app/api/docs)
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
![Postman Badge](https://img.shields.io/badge/Postman-FF6C37?logo=postman&logoColor=fff&style=for-the-badge)
![Swagger Badge](https://img.shields.io/badge/Swagger-85EA2D?logo=swagger&logoColor=000&style=for-the-badge)
<img src="https://raw.githubusercontent.com/Redocly/redoc/main/docs/images/redoc.png" alt="Swagger Badge" style="height: 28px; width: auto;">
![Docker Badge](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge)
![Vercel Badge](https://img.shields.io/badge/Vercel-000?logo=vercel&logoColor=fff&style=for-the-badge)

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

If you want to run the API using [Docker](https://www.docker.com/) in your local environment, then `docker` and `docker-compose` will be required. The best and easiest way to install Docker in your local environment is by installing [Docker Desktop](https://docs.docker.com/desktop/).

<!-- 3.2) Installation -->
<!-- ----------------------------------------------------------------------- -->

### Installation

To get a copy of this project and run it in your local environment, follow the steps listed below.

1. Clone the repo
   ```sh
   git clone git@github.com:BigSamu/Buda_Spread_API.git
   ```
2. Go into the repository
   ```sh
   cd Buda_Spread_API
   ```
3. Install required python packages or dependencies
   ```sh
   pipenv install
   ```
4. Create a .env file and add the following related environmental variables

   ```sh
   BUDA_API_SECRET=[YOUR_MAILGUN_API_KEY]
   BUDA_API_KEY=[YOUR_MAILGUN_DOMAIN_NAME]
   ```

  To create these variables please visit the related Buda API documentation in this [link](https://api.buda.com/en/#rest-api-private-endpoints)

5. Activate virtual environment
   ```sh
   pipenv shell
   ```

<p align="right">(<a href="#back-to-top">back to top</a>)</p>

<!-- ----------------------------------------------------------------------- -->
<!-- 3.3) Usage -->
<!-- ----------------------------------------------------------------------- -->

### Usage

After successful installation in your local environment, you can run the API running the command `pipenv run start`. Once done you can test the API either using [Postman](https://www.postman.com/) or by visiting the Swagger UI documentation at [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

For setting up an alert value in your local environment you need to send a POST request to the endpoint below and the respective body request:

- POST Request
  - endpoint: `http://localhost:8000/api/v1/alerts`
  - body request:
    ```json
      {"value":"<your-value>"}
    ```

For polling alert analysis two endpoints can be used with GET request to get the information:

- GET Request
  - endpoint: `http://localhost:8000/api/v1/alerts`
- GET Request
  - endpoint:`http://localhost:8000/api/v1/alerts/{market_id}`
  - path parameter: `market_id`

The first GET request is for getting alert analysis from all markets and the second, for a specific market (i.e. `btc-clp`). If you want to test the polling directly with the deployed version, you can use directly these routes instead for the respective POST and GET requests:

- POST and GET requests: `https://buda-spread-api-sandy.vercel.app/api/v1/alerts`
- GET request: `https://buda-spread-api-sandy.vercel.app/api/v1/alerts/{market_id}`

If you prefer to use [Docker](https://www.docker.com/) in your local environment please run `docker-compose up -d`. Then you can use [Postman](https://www.postman.com/) or visit the Swagger UI URL given above.

More details can be found in the documentation user interfaces that the current API has:

- **SwaggerUI** served at [https://buda-spread-api-sandy.vercel.app/api/docs](https://buda-spread-api-sandy.vercel.app/api/docs)
- **ReDoc** served at [https://buda-spread-api-sandy.vercel.app/api/redoc](https://spread-api-sandy.vercel.app/api/redoc)


<p align="right">(<a href="#back-to-top">back to top</a>)</p>

---

<!-- ----------------------------------------------------------------------- -->
<!-- 3.4) Testing -->
<!-- ----------------------------------------------------------------------- -->

### Testing and Coverage

For checking unit tests in the developed API on your local environment you can run `pipenv run test`. Likewise, for checking the coverage of those tests, you can run `pipenv run coverage`

## Contact Me

<!-- ![GitHub Follow](https://img.shields.io/github/followers/BigSamu.svg?style=social&label=Follow)
![GitHub Star](https://img.shields.io/github/stars/BigSamu?affiliations=OWNER%2CCOLLABORATOR&style=social&label=Star) -->

Feel free to contact me if you have any doubt!

Samuel Valdes Gutierrez

[![Gmail][gmail-badge]][gmail-url]
[![LinkedIn][linkedin-badge]][linkedin-url]

<p align="right">(<a href="#back-to-top">back to top</a>)</p>

---

## License

This project is licensed under the terms of the MIT license.

> You can check out the full license [here](./LICENSE.md)

<p align="right">(<a href="#back-to-top">back to top</a>)</p>

---


<!-- *********************************************************************** -->
<!-- VIII) FOOTER -->
<!-- *********************************************************************** -->

<p align="center">
Developed with ❤️ in Chile 🇨🇱
</p>

<!-- *********************************************************************** -->
<!-- A) MARKDOWN LINKS & IMAGES -->
<!-- *********************************************************************** -->

<!-- ----------------------------------------------------------------------- -->
<!-- Contact -->
<!-- ----------------------------------------------------------------------- -->

<!-- Gmail -->
[gmail-badge]: https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white
[gmail-url]: mailto:valdesgutierrez@gmail.com

<!-- LinkedIn -->
[linkedin-badge]: https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-badge-small]: https://img.shields.io/badge/--linkedin?label=LinkedIn&logo=LinkedIn&style=social
[linkedin-url]: https://www.linkedin.com/in/samuel-valdes-gutierrez

<!-- Ask Me Anything -->
[ama-badge]: https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg
[ama-url]: #contact-me

<!-- Say Thanks -->
[say-thanks-badge]: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
[say-thanks-url]: https://saythanks.io/to/BigSamu

<!-- ----------------------------------------------------------------------- -->
<!-- GitHub
<!-- ----------------------------------------------------------------------- -->

<!-- License -->

[license-badge]: https://img.shields.io/badge/license-MIT-green
[license-url]: ./LICENSE.md

<!-- Follow -->

[github-follow-badge]: https://img.shields.io/github/followers/BigSamu.svg?style=social&label=Follow
[github-follow-url]: https://github.com/BigSamu?tab=followers
