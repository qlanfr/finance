terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 2.0"
    }
  }
}

provider "docker" {}

# MySQL 컨테이너 설정
resource "docker_image" "mysql_image" {
  name = "mysql:latest"
}

resource "docker_container" "mysql_container" {
  image = docker_image.mysql_image.latest
  name  = "mysql_container"
  env = [
    "MYSQL_ROOT_PASSWORD=yourpassword",
    "MYSQL_DATABASE=stock_db",
    "MYSQL_USER=user",
    "MYSQL_PASSWORD=password"
  ]
ports {
  internal = 3306
  external = 3307
}

}

# FastAPI 컨테이너 설정
resource "docker_image" "fastapi_image" {
  name = "tiangolo/uvicorn-gunicorn-fastapi:python3.8"
}

resource "docker_container" "fastapi_container" {
  image = docker_image.fastapi_image.latest
  name  = "fastapi_container"
  ports {
    internal = 80
    external = 8000
  }
  depends_on = [docker_container.mysql_container]
}

