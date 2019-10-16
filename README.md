# PathFinding
Image processing path finding algorithm 

[Este projeto foi desenvolvido em outra plataforma de controle de versionamento e exportada para o GitHub após o término da disciplina Introdução ao Processamento de Imagens - UnB]

O projeto consiste na detecção do melhor caminho para uma sonda que navega em ambientes irregulares. O objetivo é utilizar técnicas de processamento de imagem em um mapa de altitude (cuja altura está registrada em um mapa de calor espacial RGB).

Após uma etapa de equalização, o método "look4path" é utilizado para a determinação da trajetória, que consiste em, a cada pixel, determinar a distância euclidiana entre os 8 vizinhos mais próximos e o ponto alvo (borda direita inferior da imagem), dentre os 3 pontos mais próximos ao alvo, o que possui o menor valor, em escala de cinza, é escolhido.

![Mars](images/Mars_final.bmp?raw=true)

## Instalação e uso

Install python
```
sudo apt-get update
sudo apt-get install python3.6
```

Create a virtual environment called "venv" and activate it
```
python3 -m venv venv
source venv/bin/activate
```

Install the required packages
```
python3 -m pip install -r requirements.txt
```

Run 
```
python3 pathFinder.py
```
