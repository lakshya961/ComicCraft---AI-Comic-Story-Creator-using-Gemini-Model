
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"story": None, "idea": ""}
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, idea: str = Form(...)):

    comic_prompt = f"""
You are ComicCraft, an AI Comic Story Creator using Gemini Models.

Create an original comic story based on this idea:

{idea}

Include:

Title:
Genre:

Main Characters:
- Character 1
- Character 2

PANEL 1:
Setting:
Caption:
Dialogue:

PANEL 2:
Setting:
Caption:
Dialogue:

PANEL 3:
Setting:
Caption:
Dialogue:

PANEL 4:
Setting:
Caption:
Dialogue:

PANEL 5:
Setting:
Caption:
Dialogue:

PANEL 6:
Setting:
Caption:
Dialogue:

PANEL 7:
Setting:
Caption:
Dialogue:

PANEL 8:
Setting:
Caption:
Dialogue:

Ending:

Make the story creative, family-friendly and easy to understand.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=comic_prompt
        )

        story = response.text

    except Exception as e:
        story = f"Error generating comic: {str(e)}"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"story": story, "idea": idea}
    )
