import os
import shutil
import random

pasta_dataset = '.'  # Como você está na pasta do projeto, pode usar '.'

pasta_images = os.path.join(pasta_dataset, 'images')
pasta_labels = os.path.join(pasta_dataset, 'labels')

os.makedirs(os.path.join(pasta_images, 'train'), exist_ok=True)
os.makedirs(os.path.join(pasta_images, 'val'), exist_ok=True)
os.makedirs(os.path.join(pasta_labels, 'train'), exist_ok=True)
os.makedirs(os.path.join(pasta_labels, 'val'), exist_ok=True)

imagens = [f for f in os.listdir(pasta_images) if f.endswith(('.jpg', '.png', '.jpeg'))]

random.shuffle(imagens)

num_val = int(len(imagens) * 0.2)

val_images = imagens[:num_val]
train_images = imagens[num_val:]

def mover_arquivo(nome_arquivo, pasta_origem, pasta_destino):
    origem = os.path.join(pasta_origem, nome_arquivo)
    destino = os.path.join(pasta_destino, nome_arquivo)
    shutil.move(origem, destino)

for img in train_images:
    mover_arquivo(img, pasta_images, os.path.join(pasta_images, 'train'))
    label = os.path.splitext(img)[0] + '.txt'
    mover_arquivo(label, pasta_labels, os.path.join(pasta_labels, 'train'))

for img in val_images:
    mover_arquivo(img, pasta_images, os.path.join(pasta_images, 'val'))
    label = os.path.splitext(img)[0] + '.txt'
    mover_arquivo(label, pasta_labels, os.path.join(pasta_labels, 'val'))

print(f'Treinamento: {len(train_images)} imagens')
print(f'Validação: {len(val_images)} imagens')

yaml_content = f"""
train: {os.path.abspath(os.path.join(pasta_images, 'train'))}
val: {os.path.abspath(os.path.join(pasta_images, 'val'))}

nc: 1
names: ['carro']
"""

with open(os.path.join(pasta_dataset, 'dataset.yaml'), 'w') as f:
    f.write(yaml_content)

print('Arquivo dataset.yaml criado com sucesso!')
