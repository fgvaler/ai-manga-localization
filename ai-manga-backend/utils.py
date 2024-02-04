import tiktoken

def num_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def load_source_text(file_path: str) -> str:
    source_text = ""
    with open(file_path, "r") as file:
        for line in file:
            source_text += line.strip()
            source_text += '\n'
    return source_text

def chunk_source_text(source_text: str, max_tokens: int = 8192) -> list[str]:
    """Chunk the source text into chunks with a maximum number of tokens."""
    chunks = []
    chunk = ""
    
    for line in source_text.split('\n'):
        line_token_count = num_tokens(line)
        
        if line_token_count > max_tokens:
            raise ValueError(f"Line with more than {max_tokens} tokens")
        
        chunk_token_count = num_tokens(chunk)

        cut_here = (line.strip() == "" and chunk_token_count > max_tokens/8) \
            or (chunk_token_count + line_token_count > max_tokens)
        
        if cut_here:
            chunks.append(chunk)
            chunk = line + '\n'
        else:
            chunk += line + '\n'
    
    chunks.append(chunk)  # Append the last chunk
    return chunks