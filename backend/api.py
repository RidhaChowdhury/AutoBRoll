from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import openai
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from io import BytesIO
import base64

app = FastAPI()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    openai.api_key = api_key
else:
    raise ValueError("OpenAI API key not found in environment variable.")

device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16")
pipe.to(device)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/generate_broll")
def generate_broll(prompts: List[str]):
    completions = []
    for prompt in prompts:
        completions.append(
            {"role": "user", "content": prompt}
        )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Generate stable diffusion prompt strings to create engaging b-roll for the following prompts."}] + completions
    )

    generated_prompts = []
    for choice in response.choices:
        generated_prompts.append(choice.message.content)

    generated_images = []
    for prompt in generated_prompts:
        with autocast(enabled=device == "cuda"):
            image = pipe(prompt, guidance_scale=8.5).images[0]

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        imgstr = base64.b64encode(buffer.getvalue()).decode("utf-8")
        generated_images.append(imgstr)

    return {"prompts": generated_prompts, "images": generated_images}
