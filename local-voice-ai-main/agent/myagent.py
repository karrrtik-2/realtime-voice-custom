import logging
import asyncio
import json
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import deepgram, groq, sarvam, silero, google 

load_dotenv()

logger = logging.getLogger("local-agent")
logger.setLevel(logging.INFO)

class LocalAgent(Agent):
    def __init__(self, stt_instance, tts_instance, instructions) -> None:
        # LLM setup
        llm = groq.LLM(model="meta-llama/llama-4-maverick-17b-128e-instruct")
        vad_inst = silero.VAD.load()

        super().__init__(
            instructions=instructions,
            stt=stt_instance,
            llm=llm,
            tts=tts_instance,
            vad=vad_inst
        )
        
        # Metrics wrappers
        def llm_metrics_wrapper(metrics):
            asyncio.create_task(self.on_llm_metrics_collected(metrics))
        llm.on("metrics_collected", llm_metrics_wrapper)
        
        # Bind metrics only if the instance supports it
        if hasattr(stt_instance, "on"):
            stt_instance.on("metrics_collected", lambda m: asyncio.create_task(self.on_stt_metrics_collected(m)))
            stt_instance.on("eou_metrics_collected", lambda m: asyncio.create_task(self.on_eou_metrics_collected(m)))
        
        if hasattr(tts_instance, "on"):
            tts_instance.on("metrics_collected", lambda m: asyncio.create_task(self.on_tts_metrics_collected(m)))
            
        vad_inst.on("metrics_collected", lambda m: asyncio.create_task(self.on_vad_event(m)))

    async def on_llm_metrics_collected(self, metrics):
        logger.info(f"LLM Metrics: {metrics}")
    async def on_stt_metrics_collected(self, metrics):
        logger.info(f"STT Metrics: {metrics}")
    async def on_eou_metrics_collected(self, metrics):
        logger.info(f"EOU Metrics: {metrics}")
    async def on_tts_metrics_collected(self, metrics):
        logger.info(f"TTS Metrics: {metrics}")
    async def on_vad_event(self, event):
        pass

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    
    # Wait for participant to join
    participant = await ctx.wait_for_participant()
    logger.info(f"Participant joined: {participant.identity}")

    # --- 1. SET DEFAULTS ---
    selected_lang = "hi"
    selected_voice = "sarvam"

    # --- 2. DETECT SIP (PHONE) VS WEB ---
    is_sip_call = participant.identity.startswith("sip_") or participant.identity.startswith("+")

    if is_sip_call:
        logger.info("Detected SIP (Phone) Call. Forcing Hindi + Sarvam.")
        selected_lang = "hi"
        selected_voice = "sarvam"
    else:
        # Web User
        if participant.metadata:
            try:
                meta = json.loads(participant.metadata)
                selected_lang = meta.get("language", "hi")
                selected_voice = meta.get("voice", "sarvam")
                logger.info(f"Web User selected -> Lang: {selected_lang}, Voice: {selected_voice}")
            except Exception as e:
                logger.error(f"Failed to parse metadata: {e}")

    # --- 3. CONFIGURE STT ---
    stt_lang = "hi" if selected_lang == "hi" else "en"
    stt = deepgram.STT(model="nova-2", language=stt_lang)

    # --- 4. CONFIGURE TTS ---
    tts = None
    if selected_voice == "sarvam":
        tts = sarvam.TTS(
            target_language_code="hi-IN",  
            speaker="vidya",
            model="bulbul:v2"
        )
    elif selected_voice == "gemini":
        tts = google.beta.GeminiTTS(
            model="models/gemini-2.5-flash-preview-tts",
            voice_name="Zephyr",
            instructions="Speak.",
        )
    else:
        tts = sarvam.TTS(target_language_code="hi-IN", speaker="vidya")

    # --- 5. CONFIGURE INSTRUCTIONS ---
    instructions = ""
    if selected_lang == "hi":
        instructions = """
            You are a helpful agent who speaks primarily in Hindi.
            Never ever use emojis. Keep responses short and concise.
            Respond in Hindi.
        """
    else:
        instructions = """
            You are a helpful agent who speaks in English.
            Never ever use emojis. Keep responses short and concise.
            Respond in English.
        """

    # --- 6. START AGENT ---
    session = AgentSession()
    agent = LocalAgent(stt_instance=stt, tts_instance=tts, instructions=instructions)
    
    await session.start(agent=agent, room=ctx.room)

    # --- 7. INITIAL GREETING ---
    # Give a small delay to ensure audio channel is open
    await asyncio.sleep(1)
    
    if selected_lang == "hi":
        await session.generate_reply(
            instructions="Greet the caller in Hindi in one short, friendly sentence and offer help."
        )
    else:
        await session.generate_reply(
            instructions="Say 'Hello! How can I help you today?'"
        )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, job_memory_warn_mb=1500))