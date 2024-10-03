# Automated-Testing-Deployment-of-NextCloud-on-Bare-Metal-Cloud
Automated deployment and testing of NextCloud on bare-metal Kubernetes, integrated with CI/CD for functional, security, and performance validation.
NextCloud Deployment on Bare-Metal Cloud Infrastructure
Overview

   ## Overview
This capstone project automates the deployment, testing, and documentation of NextCloud on a bare-metal Kubernetes infrastructure, integrating Continuous Integration/Continuous Deployment (CI/CD) practices to ensure quality, security, and scalability. The project received a final score of 17.5/20 and serves as a key demonstration of my skills in cloud computing, automation, and DevOps methodologies.

## Project Objectives
- **Automated Deployment**: Deploy NextCloud on Kubernetes clusters managed by Proxmox, with a focus on scalability and resilience.
- **Security Hardening**: Apply CIS benchmarks to enhance the security of the cloud infrastructure, ensuring data integrity and resistance to cyber threats.
- **Automated Testing**: Integrate functional, security, and performance tests into the CI/CD pipeline using tools like Selenium and Pytest for end-to-end validation.

## Features
- **Infrastructure Deployment**: Bare-metal infrastructure deployment using Kubernetes with MicroK8s and Juju.
- **Security Compliance**: Automated testing for security hardening using CIS benchmarks, Sonobuoy, and other CNCF tools.
- **CI/CD Integration**: Continuous integration for functional and security testing using GitLab pipelines, enabling early detection of vulnerabilities.

## Repository Structure
- `Failure_detection/`: Scripts for detecting cluster issues and generating CIS compliance reports.
- `infrastructure_deployment/`: Contains deployment scripts and configuration files for Kubernetes and Juju.
- `nextcloud_deployment/`: Helm charts, deployment templates, and functional testing files for NextCloud.
- `Reports/`: Documentation and reports for infrastructure deployment, functional testing, and security integration.
- `Tests/`: Automated test scripts for verifying the integrity, functionality, and security of the NextCloud instance.

## Technologies Used
- **Cloud & Infrastructure**: Kubernetes, Docker, Proxmox, Juju
- **Automation & CI/CD**: GitLab, Ansible, Helm
- **Testing**: Selenium, Pytest, Sonobuoy, CIS benchmarks
- **Programming Languages**: Python, Bash

