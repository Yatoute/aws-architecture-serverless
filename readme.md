
---

# 📸 Postagram — Projet final : Déployement d'une API REST 100% Serverless sur AWS

Ce projet est réalisé dans le cadre de projet de cloud computing à l'ENSAI. Il consiste à développer la partie backend d’un réseau social de partage de photos, **Postagram**, en exploitant une architecture 100 % serverless et en déployant les ressources AWS avec Terraform.

Voici une version **cohérente et bien structurée** de la section "Objectif du projet", qui aligne bien les exigences fonctionnelles avec l’architecture déployée :

---

## 🧱 Objectif du projet

> Concevoir et déployer une API REST complète pour un réseau social de partage de photos, **Postagram**, reposant sur une architecture cloud **100 % serverless côté traitement des images** et **scalable côté backend**.

Cette API backend doit permettre de :

* Créer une publication (`POST /posts`)
* Supprimer une publication (`DELETE /posts/{id}`)
* Lire toutes les publications (`GET /posts`)
* Lire les publications d’un utilisateur (`GET /posts?user=username`)
* Générer une URL signée pour uploader une image (`GET /getSignedUrlPut`)
* Déclencher automatiquement une analyse d’image via **Amazon Rekognition** à chaque dépôt dans un bucket S3, et stocker les **labels détectés** dans une base **DynamoDB**

> L’infrastructure est déployée sur AWS en deux temps :

* Une **architecture serverless** pour gérer le stockage des images, la détection automatique des labels (via Lambda + S3 + DynamoDB)
* Une **architecture de backend web scalable**, composée d’instances **EC2** managées par un **Auto Scaling Group** derrière un **Load Balancer**, avec les ressources AWS injectées via des **variables d’environnement**

---

## 🧰 Technologies utilisées

- **Langage backend** : Python (FastAPI, boto3)
- **Infrastructure as Code** : Terraform avec CDKTF (Python)
- **Base de données** : Amazon DynamoDB
- **Stockage fichiers** : Amazon S3
- **Reconnaissance d’images** : AWS Rekognition (via Lambda)
- **Déploiement webservice** : EC2 + Auto Scaling Group + Load Balancer

---
