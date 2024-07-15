# Reprodução de Roubo de Sessão TCP inspirado no Mitnick Attack usando Docker
## 👨‍💻🕵️ UFPR - CI1007 - Segurança

## Disponível também em: https://hackmd.io/@gustavo-prado/HkEyitW_0 para leitura mais fácil!!

## 💡 Ideia do Trabalho
* Usando Arp Spoofing, derrubar o Trusted Server e capturar ISN
* Forjar pacotes TCP do three-way-handshake
* Forjar conexão RSH
* Usar RSH para executar comandos na outra máquina e conseguir acesso para a máquina atacante

## 🐋 Docker
* Temos 3 containers:
    * *seed-attacker* - Container com sistema que será o atacante
    * *x-terminal* - Container com o terminal que deve ser invadido (IP 10.9.0.5)
    * *trusted-server* - Container com o sistema confiável que tem acesso ao terminal (10.9.0.6)
* Eles estão em uma rede interna (IP 10.9.0.0)
* Comando para iniciar os containeres: `docker compose up -d`
* Para entrar em um container: `docker exec -it <nome do container> bash`

## 🦹 ARP
### Usamos o pacote *scapy* do Python para criar todos os pacotes que usaremos nesses scripts.
O que fazemos para envenenar a tabela ARP do *x-terminal* é mandar pacotes ARP, dizendo que o endereço MAC do IP 10.9.0.6 é o endereço do *seed-attacker* e não mais o do *trusted-server*. Mandamos esse pacote em broadcast pra rede, assim o terminal irá receber esse pacote e atualizar sua tabela com os valores que mandamos.
Mandamos também um pacote para o *trusted-server* dizendo que o endereço MAC do *x-terminal* (10.9.0.5) é **ff:ff:ff:ff:ff:aa**, ou seja, um endereço inválido, então quando ele tentar mandar responder os pacotes do *x-terminal*, os pacotes enviados por ele não irão ser recebidos por ninguém.
Fazemos algo parecido no próprio *seed-attacker*, colocando o mesmo MAC inválido para o *trusted-server* (10.9.0.6), assim nenhuma mensagem será repassada para ele.

## 🤝 TCP
Tendo executado o envenenamento da tabela ARP, nos passando pelo Trusted-Server, vamos iniciar uma conexão TCP com o *x-terminal*.
Fazemos então o seguinte:
* Mandamos pela porta 1023 para porta 514 do *x-terminal* um pacote SYN
* Desviamos o pacote SYN+ACK do *trusted-server* para nós
* Respondemos com um ACK, capturando a sequência do pacote recebido

Após isso a conexão foi iniciada e podemos mandar o pacote RSH para executar o comando que desejamos.

## 🚪 RSH
Após iniciada a conexão, podemos o pacote do RSH com o seguinte formato:

| Porta Secundária | Usuário do Cliente | Usuário do Servidor | Comando a ser executado |
| -------- | -------- | -------- | -------- |
| 1022     | root     | root     | echo "+" > /root/.rhosts |

O RSH usa uma porta secundária, no nosso caso a 1022, para enviar erros que ocorram durante a execução. Os usuários são os padrão do sistema (o user *root*) e o comando que queremos executar substitui o arquivo *.rhosts* do *x-terminal* por um novo, que permite qualquer host adentrar o sistema (símbolo '+' libera acesso a qualquer máquina).
Após mandar esse pacote, temos que capturar na porta 1022 o pacote mandado pelo *x-terminal*, pegar o número de sequência do pacote e responder com um SYN+ACK para a porta 1023 do terminal.
### Depois disso tudo, o comando será executado na máquina terminal, nos dando acesso como queríamos.


## 📂 Arquivos
* *arp.py* - Arquivo com o código das funções que executam o envenenamento de tabela ARP das máquinas
* *main.py* - Arquivo com o código principal, que chama as funções ARP, mandar os pacotes para forjar a conexão TCP e mandar o pacote RSH

## ▶️ Execução
* **!! IMPORTANTE !!** Antes de rodar os scripts para o trabalho é preciso entrar no container do *x-terminal* e criar um arquivo *.rhosts* dentro da pasta `/root` com o seguinte conteúdo:
`10.9.0.6 root` 
Assim permitindo o acesso rsh pelo *trusted-server*
* Depois, basta entrar no container do *seed-attacker*:
`docker exec -it seed-attacker bash` e entrar na pasta `/volumes`
* Dentro da pasta volumes, basta executar o *main.py* : `python3 main.py`