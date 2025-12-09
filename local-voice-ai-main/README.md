STT: Deepgram Nova 2    || whisper large v3 turbo  || nova 3 || sarvam STT (with translate) ||  Flux(best)
LLM: Groq Llama maverick || gemini 2.5 flash lite || gpt 5.1 mini || flagship model with ow latency
TTS: Sarvam(Hindi)(vidya manisha)  ---> audio quality 24kHz || Gemini 2.5 TTS (hindi) ||
sarvam hindi is little cheaper than gemini hindi i think || english cheap model -> Murf and Gemini
in a min-> 17 sec input 13sec silence 30sec ouput
gemini making problem from its own end
zyada shade mt bana kro ai already jaanta h kya kese krna h or issue ata h toh sbse best h documentation
docker compose logs -f agent

i dont want to change current logic or frontend i want to add twilio sip trunking to my agent for inbound call
i have purchased a US number on twilio and enabled sip trunk on it

i want that when i call on that us number agent should speak in hindi so use nova 2 hindi and sarvam for it 
here is github link if required: https://github.com/ShayneP/livekit-sip-python-example

kai faste ho toh perplexity use krlia kro cchota se modify krwane k liye
# For running without docker:

1. CD to livekit server binary file
--> livekit-server --dev --bind 0.0.0.0 --node-ip 127.0.0.1 

2. in agent dir, .env should have: LIVEKIT_URL=ws://localhost:7880
CD to agent dir and run
--> python myagent.py dev 

3. cd voice-assistant-frontend
setup .env.local
install pnpm and npm (if not): pnpm install
--> pnpm run dev

# For running with docker:
1. docker-compose down
2. docker-compose up --build    // for starting and building


frontend, features, conenct to number
document to adil

tahajjud
clothes for day 1 and 2
here to airport
self drive car book 
airport procedure and things to keep in mind
how to go to car shop
car to hotel how to drive
shops nearby to purchase stuff
decoration of room
first meet gift
flowers
lights
Ring
Gift for her
Gift for mother, gift for kitchen
Chocolates
Diary with hand written
last meet gift

If want to use local models, dockerfile:
services:
  # kokoro:
  #   image: ghcr.io/remsky/kokoro-fastapi-cpu:latest
  #   ports:
  #     - "8880:8880"
  #   networks:
  #     - agent_network

  livekit:
    image: livekit/livekit-server:latest
    ports:
      - "7880:7880"
      - "7881:7881"
    command: --dev --bind "0.0.0.0"
    networks:
      - agent_network

  # whisper:
  #   build:
  #     context: ./whisper
  #   volumes:
  #     - whisper-data:/data
  #   ports:
  #     - "11435:80"
  #   networks:
  #     - agent_network

  # ollama:
  #   build:
  #     context: ./ollama
  #   ports:
  #     - "11434:11434"
  #   volumes:
  #     - ollama:/root/.ollama
  #   networks:
  #     - agent_network
  #   deploy:
  #     resources:
  #       limits:
  #         memory: 8G
  #       reservations:
  #         memory: 6G

  agent:
    build:
      context: ./agent
    environment:
      - LIVEKIT_HOST=ws://livekit:7880
      - LIVEKIT_API_KEY=devkey
      - LIVEKIT_API_SECRET=secret
      - LIVEKIT_AGENT_PORT=7880
      - DEEPGRAM_API_KEY=4cdc8cd7e079558e3a7d7da663001d476ae82fda
      - GROQ_API_KEY=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
      - SARVAM_API_KEY=sk_fc3eym9d_g2cxeyhj3cqz2jxacKUgSVjs
    depends_on:
      - livekit
      - kokoro
      - whisper
      - ollama
    networks:
      - agent_network

  frontend:
    build:
      context: ./voice-assistant-frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
      - LIVEKIT_URL=ws://livekit:7880
      - LIVEKIT_API_KEY=devkey
      - LIVEKIT_API_SECRET=secret
      - NEXT_PUBLIC_LIVEKIT_API_KEY=devkey
    depends_on:
      - livekit
    networks:
      - agent_network

volumes:
  ollama:
  whisper-data:

networks:
  agent_network:
    driver: bridge