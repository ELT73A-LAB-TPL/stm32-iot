# Stack smartband — Node-RED + Mosquitto + Ntfy

Backend completo self-hosted para o sistema de detecção de quedas.
Substitui Firebase (Realtime Database + FCM) por serviços open source.

## Estrutura de arquivos

```
smartband-stack/
├── docker-compose.yml
├── .env.example          → copiar para .env e ajustar
├── mosquitto/
│   └── config/
│       └── mosquitto.conf
└── sqlite/               → criada automaticamente (banco de dados)
```

## Subindo a stack

```bash
# 1. Criar estrutura de diretórios
mkdir -p mosquitto/config sqlite

# 2. Copiar arquivos de configuração
cp mosquitto.conf mosquitto/config/mosquitto.conf
cp .env.example .env

# 3. Editar .env com seus valores
nano .env

# 4. Subir todos os serviços
docker compose up -d

# 5. Verificar status
docker compose ps
docker compose logs -f
```

## Acessos

| Serviço    | URL                        | Uso                        |
|------------|----------------------------|----------------------------|
| Node-RED   | http://localhost:1880       | Editor de fluxos           |
| Ntfy       | http://localhost:8080       | Interface de notificações  |
| Mosquitto  | mqtt://localhost:1883       | Broker MQTT                |
| WebSocket  | ws://localhost:8765         | App Flutter (tempo real)   |

## Configuração do Node-RED após subir

1. Acessar http://localhost:1880
2. Instalar paletas necessárias (Menu → Manage Palette):
   - `node-red-node-sqlite`
   - `node-red-contrib-websocket` (já incluso no Node-RED 3.x)
3. Importar o fluxo (Menu → Import) com o JSON do fluxo de quedas

## Configuração do Ntfy

```bash
# Criar usuário para o cuidador
docker exec -it smartband-ntfy ntfy user add cuidador

# Conceder permissão de leitura no tópico de alertas
docker exec -it smartband-ntfy ntfy access cuidador cuidador-alertas read

# Criar usuário para o Node-RED publicar
docker exec -it smartband-ntfy ntfy user add nodered
docker exec -it smartband-ntfy ntfy access nodered cuidador-alertas write
```

## URL do Ntfy no nó http request do Node-RED

```
http://ntfy:80/publish
```

> Dentro da rede Docker, os serviços se comunicam pelo nome do container.
> O Node-RED acessa o Ntfy como `http://ntfy:80`, não `http://localhost:8080`.

## Reiniciar um serviço

```bash
docker compose restart nodered
docker compose restart mosquitto
docker compose restart ntfy
```

## Parar tudo

```bash
docker compose down          # mantém volumes (dados preservados)
docker compose down -v       # remove volumes (dados apagados)
```

## Rodando em Raspberry Pi

A stack é compatível com ARM64 (Raspberry Pi 4/5).
Todas as imagens (`eclipse-mosquitto`, `nodered/node-red`,
`binwiederhier/ntfy`) publicam imagens multi-arch.

Para expor na rede local, substituir `localhost` pelo IP fixo
da Raspberry Pi ou configurar um hostname mDNS (ex: `smartband.local`).
