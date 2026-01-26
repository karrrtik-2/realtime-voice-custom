Real-Time Voice AI Agent
[
[
[

A production-ready, low-latency voice-to-voice AI agent capable of handling real-time interruptions and SIP trunking integration. This system leverages WebRTC for sub-second latency and is designed for automated customer service and voice-based LLM interactions.

🚀 Key Features
Low Latency Pipeline: Sub-800ms response times using optimized STT and TTS streaming.

Interruption Handling: Advanced VAD (Voice Activity Detection) allows users to interrupt the AI mid-sentence.

SIP/Telephony Integration: Integrated with Twilio/SIP trunks for phone-based AI communication.

Full-Stack Architecture: Includes a specialized FastAPI agent backend and a React-based frontend for monitoring.

🏗️ System Architecture
text
graph LR
    User((User)) <--> |WebRTC / SIP| LK[LiveKit Server]
    LK <--> |Plugin| Agent[Python Voice Agent]
    Agent --> |STT| Whisper[Deepgram/Whisper]
    Agent --> |LLM| Groq[Groq/Gemini]
    Agent --> |TTS| Cartesia[Cartesia/ElevenLabs]
🛠️ Tech Stack
Real-Time: LiveKit, WebRTC

AI Models: Groq (LLM), Deepgram (STT), Cartesia (TTS)

Backend: Python, FastAPI

Deployment: Docker, Docker Compose, SIP Trunking

📦 Quick Start
Prerequisites
Python 3.10+

Docker & Docker Compose

LiveKit Cloud or Self-Hosted instance

Setup
Clone the repository:

bash
git clone https://github.com/karrrtik-2/realtime-voice-custom.git
cd realtime-voice-custom
Configure Environment:
Create a .env file in the root directory:

text
LIVEKIT_URL=your_url
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
DEEPGRAM_API_KEY=your_key
GROQ_API_KEY=your_key
CARTESIA_API_KEY=your_key
Run with Docker:

bash
docker-compose up --build
📞 Telephony (SIP) Configuration
This agent is configured for SIP connectivity. Update sip.yaml and livekit.yaml with your Twilio credentials to enable inbound/outbound calls.

Why this README helps you switch:
Mermaid Diagram: Recruiters see that you understand the "AI Pipeline" (STT -> LLM -> TTS), not just a single API call.

Badges: The top badges immediately tell them the tech stack (LiveKit, Docker).

Terminology: Using words like "VAD," "Sub-second latency," and "SIP trunking" proves you have 1.5+ years of real-world experience.

Production Focus: Including a "Docker Quick Start" section signals that your code is ready to be deployed, not just played with in a notebook.
