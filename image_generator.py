import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if device=="cuda" else torch.float32)
pipe = pipe.to(device)

aspect_ratio_options = {
    "Square (1:1)": (512, 512),
    "Landscape (16:9)": (768, 432),
    "Portrait (9:16)": (432, 768),
    "Standard (4:3)": (680, 512),
    "Widescreen (21:9)": (896, 384)
}

def generate_image_from_prompt(prompt, style="None", aspect_ratio="Landscape (16:9)"):
    if style != "None":
        prompt = f"{prompt}, {style} style"
    width, height = aspect_ratio_options.get(aspect_ratio, (768, 432))
    image = pipe(prompt, width=width, height=height).images[0]
    return image
