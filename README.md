# DevOps 주가 예측 및 자원 모니터링 프로젝트

이 프로젝트는 주가 예측 모델을 개발하고, CPU 및 메모리 자원 사용량을 모니터링하여 텔레그램으로 알림을 보내는 시스템입니다. FastAPI와 Docker, Kubernetes, Terraform을 사용하여 구축되었습니다.

---

## 프로젝트 개요

- **주가 예측 모델**: 데이터를 기반으로 한 선형 회귀 모델을 사용하여 하루 뒤 주가를 예측하고 MySQL에 저장.
- **자원 모니터링**: `psutil`을 사용해 CPU와 메모리 사용량을 주기적으로 확인하고, 일정 조건을 충족할 때 오토스케일링 알림을 텔레그램으로 전송.
- **텔레그램 봇 통합**: `/predict` 명령어로 최근 예측값을 요청하거나, 1시간마다 자원 사용량 보고를 수신할 수 있는 기능.
- **컨테이너화 및 클러스터링**: Docker와 Kubernetes로 컨테이너를 배포하고, Terraform을 통해 자동화된 인프라 구성.

---
##주요 기능 설명
#주가 예측 모델:

            stock_predictor.py에서 주가 예측 모델을 생성하고, 예측 결과를 MySQL에 저장합니다.
#자원 모니터링:

            telegram_alert.py에서 CPU 및 메모리 사용량을 주기적으로 확인하여, 자원 사용량이 70%를 넘길 경우 오토스케일링 알림을 전송합니다.
#텔레그램 명령어:

            /predict 명령어로 가장 최근의 주가 예측값을 확인할 수 있습니다.

---

## 설치 및 실행 가이드

### 1. 필수 도구 설치

1. **Python 3.8 이상**
2. **Docker** 및 **Docker Compose**
3. **Terraform**
4. **Minikube**

#### 설치 명령어 예시 (Ubuntu 기준)

```bash
# Python 설치
sudo apt update && sudo apt install python3 python3-pip

# Docker 설치
sudo apt install -y docker.io

# Terraform 설치
wget https://releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_linux_amd64.zip
unzip terraform_1.0.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Minikube 설치
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube


my_devops_project/
├── telegram_alert.py           # 자원 모니터링 및 텔레그램 알림 코드
├── terraform_setup/            # Terraform 설정 폴더
│   └── main.tf                 # Terraform 설정 파일
├── kubernetes_setup/           # Kubernetes 설정 파일 폴더
│   ├── deployment.yaml         # FastAPI 배포 설정 파일
│   └── service.yaml            # FastAPI 로드 밸런서 설정 파일
├── stock_predictor.py          # 주가 예측 모델 코드
├── main.py                     # FastAPI 서버 코드
└── README.md                   # 프로젝트 문서화 파일
---
###파드 확인


### 파드 확인

![pod](./%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202024-10-31%2018-44-36.png)

### api 서버 확인

![api동작](./%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202024-10-31%2018-45-51.png)



-----




