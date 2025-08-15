# Custom web radio station

This is a custom web radio station built using Docker, Liquidsoap, and Icecast. It allows you to stream music and jingles.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/EncryptEx/radio.git
   cd radio
   ```

2. Place your music files in the `music` directory and your jingles in the `jingles` directory.

3. Create a `icecast.xml` to configure Icecast. You can use the provided `icecast.xml.template` as a starting point.

4. Change the password and make sure it matches the one in the Liquidsoap file `main.liq` (see last line).

## Running the Radio Station

To start the radio station, run:

```bash
docker-compose up -d
```

This will start the Icecast and Liquidsoap services.

## Accessing the Stream

You can access the stream at `http://localhost:8000/radio.ogg`.

## Accessing the Liquidsoap telnet

You can access the Liquidsoap via telnet: 

```bash
telnet localhost 1234
```