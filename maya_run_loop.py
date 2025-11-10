# -*- coding: utf-8 -*-
# @Time    : 2025/11/8/周六 23:30
# @Author  : alun
# @File    : maya_run_loop.py
# !/usr/bin/env python3

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from snac import SNAC
import soundfile as sf
import numpy as np
import re

CODE_START_TOKEN_ID = 128257
CODE_END_TOKEN_ID = 128258
CODE_TOKEN_OFFSET = 128266
SNAC_MIN_ID = 128266
SNAC_MAX_ID = 156937
SNAC_TOKENS_PER_FRAME = 7

SOH_ID = 128259
EOH_ID = 128260
SOA_ID = 128261
BOS_ID = 128000
TEXT_EOT_ID = 128009


def split_text(text: str, max_length: int = 50) -> list:
    """Split text into chunks while preserving emotion tags."""
    if len(text) <= max_length:
        return [text]

    # Split by sentence boundaries while keeping emotion tags
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def build_prompt(tokenizer, description: str, text: str) -> str:
    """Build formatted prompt for Maya1."""
    soh_token = tokenizer.decode([SOH_ID])
    eoh_token = tokenizer.decode([EOH_ID])
    soa_token = tokenizer.decode([SOA_ID])
    sos_token = tokenizer.decode([CODE_START_TOKEN_ID])
    eot_token = tokenizer.decode([TEXT_EOT_ID])
    bos_token = tokenizer.bos_token

    formatted_text = f'<description="{description}"> {text}'

    prompt = (
            soh_token + bos_token + formatted_text + eot_token +
            eoh_token + soa_token + sos_token
    )

    return prompt


def extract_snac_codes(token_ids: list) -> list:
    """Extract SNAC codes from generated tokens."""
    try:
        eos_idx = token_ids.index(CODE_END_TOKEN_ID)
    except ValueError:
        eos_idx = len(token_ids)

    snac_codes = [
        token_id for token_id in token_ids[:eos_idx]
        if SNAC_MIN_ID <= token_id <= SNAC_MAX_ID
    ]

    return snac_codes


def unpack_snac_from_7(snac_tokens: list) -> list:
    """Unpack 7-token SNAC frames to 3 hierarchical levels."""
    if snac_tokens and snac_tokens[-1] == CODE_END_TOKEN_ID:
        snac_tokens = snac_tokens[:-1]

    frames = len(snac_tokens) // SNAC_TOKENS_PER_FRAME
    snac_tokens = snac_tokens[:frames * SNAC_TOKENS_PER_FRAME]

    if frames == 0:
        return [[], [], []]

    l1, l2, l3 = [], [], []

    for i in range(frames):
        slots = snac_tokens[i * 7:(i + 1) * 7]
        l1.append((slots[0] - CODE_TOKEN_OFFSET) % 4096)
        l2.extend([
            (slots[1] - CODE_TOKEN_OFFSET) % 4096,
            (slots[4] - CODE_TOKEN_OFFSET) % 4096,
        ])
        l3.extend([
            (slots[2] - CODE_TOKEN_OFFSET) % 4096,
            (slots[3] - CODE_TOKEN_OFFSET) % 4096,
            (slots[5] - CODE_TOKEN_OFFSET) % 4096,
            (slots[6] - CODE_TOKEN_OFFSET) % 4096,
        ])

    return [l1, l2, l3]


def generate_audio_chunk(model, tokenizer, snac_model, description: str, text: str, device: str) -> np.ndarray:
    """Generate audio for a single text chunk."""
    prompt = build_prompt(tokenizer, description, text)

    inputs = tokenizer(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    with torch.inference_mode():
        outputs = model.generate(
                **inputs,
                max_new_tokens=2048,
                min_new_tokens=28,
                temperature=0.4,
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=True,
                eos_token_id=CODE_END_TOKEN_ID,
                pad_token_id=tokenizer.pad_token_id,
        )

    generated_ids = outputs[0, inputs['input_ids'].shape[1]:].tolist()
    snac_tokens = extract_snac_codes(generated_ids)

    if len(snac_tokens) < 7:
        print(f"Warning: Not enough SNAC tokens for chunk: {text[:30]}...")
        return np.array([])

    levels = unpack_snac_from_7(snac_tokens)
    codes_tensor = [
        torch.tensor(level, dtype=torch.long, device=device).unsqueeze(0)
        for level in levels
    ]

    with torch.inference_mode():
        z_q = snac_model.quantizer.from_codes(codes_tensor)
        audio = snac_model.decoder(z_q)[0, 0].cpu().numpy()

    # Trim warmup samples
    if len(audio) > 2048:
        audio = audio[2048:]

    return audio


def main():
    print("\n[1/4] Loading Maya1 model...")
    model = AutoModelForCausalLM.from_pretrained(
            "maya-research/maya1",
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(
            "maya-research/maya1",
            trust_remote_code=True
    )
    print(f"Model loaded: {len(tokenizer)} tokens in vocabulary")

    print("\n[2/4] Loading SNAC audio decoder...")
    snac_model = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.cuda.is_available():
        snac_model = snac_model.to("cuda")
    print("SNAC decoder loaded")

    # description = "Realistic male voice in the 30s age with american accent. Normal pitch, warm timbre, conversational pacing."
    description = "The voice of US President Trump giving an exciting and passionate speech. Deep pitch, authoritative tone, energetic pacing."
    text = '''
    What is up, my creative legends?! <laugh_harder> Welcome back to the channel! <whisper>Today, we are diving headfirst into the beast that is ComfyUI! Now, <whisper>if you're stuck in the dark ages of linear AI generation—you know, <laugh_harder>just typing a prompt and hoping for the best—then get ready for a paradigm shift!
<laugh_harder> No, I am NOT talking about Automatic1111! <laugh_harder> That's for n00bs who don't want to see the magic happen! <laugh_harder>
ComfyUI is a node-based interface for Stable Diffusion, and trust me, it's where the pros live. <whisper> Think of it like a visual coding environment for AI art! Instead of a single box, you get a canvas where you connect different colored nodes—Load Checkpoint, CLIP Text Encode, KSampler, VAE Decode... <whisper> It sounds complicated, right? <whisper> It is! <whisper> But that's the fun part! <whisper>
Why put yourself through this? Control, my friends, absolute control!
With ComfyUI, you see the entire image generation pipeline laid out in front of you. You can literally watch the image being rendered in real-time. <laugh_harder> You can grab the latent noise at any point, inject a LoRA only into the foreground, use one prompt for the background and another for the subject... <laugh_harder> It’s like having a digital laboratory!
    '''

    print("\n[3/4] Splitting and generating speech...")
    print(f"Original text length: {len(text)} characters")
    print(f"Original text: {text}")

    # Split text into chunks
    text_chunks = split_text(text, max_length=50)
    print(f"\nSplit into {len(text_chunks)} chunks:")
    print("=" * 80)
    for i, chunk in enumerate(text_chunks, 1):
        print(f"\nChunk {i}/{len(text_chunks)}:")
        print(f"  Length: {len(chunk)} characters")
        print(f"  Content: {chunk}")
        print("-" * 80)

    # Generate audio for each chunk
    audio_chunks = []
    print("\n" + "=" * 80)
    print("Starting audio generation for each chunk...")
    print("=" * 80)
    for i, chunk in enumerate(text_chunks, 1):
        print(f"\n>>> Generating chunk {i}/{len(text_chunks)}:")
        print(f"    Text: {chunk}")
        audio = generate_audio_chunk(model, tokenizer, snac_model, description, chunk, device)
        if len(audio) > 0:
            audio_chunks.append(audio)
            print(f"    ✓ Generated {len(audio)} samples ({len(audio)/24000:.2f}s)")
        else:
            print(f"    ✗ Failed to generate audio for this chunk")

    print("\n[4/4] Merging audio chunks...")
    # Merge all audio chunks
    if audio_chunks:
        merged_audio = np.concatenate(audio_chunks)
        total_duration = len(merged_audio) / 24000
        print(f"Total audio: {len(merged_audio)} samples ({total_duration:.2f}s)")

        # Save merged audio
        output_file = "output_loop_1.wav"
        sf.write(output_file, merged_audio, 24000)
        print(f"\nVoice generated successfully: {output_file}")
    else:
        print("Error: No audio chunks generated")


if __name__ == "__main__":
    main()
    print("\nAll done!")
