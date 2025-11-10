import re
text = """
Wow. This place looks even better than I imagined. How did they set all this up so perfectly? The lights, the music, everything feels magical. I can't stop smiling right now.
"""


def split_text(text: str, max_length: int = 50) -> list:
    """Split text into chunks while preserving emotion tags."""
    if len(text) <= max_length:
        return [text]

    # Split by sentence boundaries while keeping emotion tags
    sentences = re.split(r"(?<=[.!?])\s+", text)

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


chunks = split_text(text, max_length=100)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}")
