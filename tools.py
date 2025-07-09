def read_file(file_path)->str:
  with open(file_path, 'r', encoding='utf-8') as file:
    return file.read()
  
from datetime import datetime
import os

def save_application(resume:str,cover_letter:str,job_title:str):
  timestamp = datetime.now().strftime("%Y%m%d_%H%M")
  folder = "applications"
  os.makedirs(folder, exist_ok=True)
  base_filename =os.path.join(folder,f"{job_title.replace(' ', '_')}_{timestamp}")
  with open(base_filename +"_resume.txt", 'w', encoding='utf-8') as f:
    f.write(resume)
  with open(base_filename +"_cover_letter.txt", 'w', encoding='utf-8') as f:
    f.write(cover_letter)

  return f"Saved resume and cover letter for '{job_title}'"


from langchain.tools import Tool

read_tool =Tool(
  name= "read_file",
  func = read_file,
  description ="Reads plain text from a given file path"
  
)
save_tool =Tool(
  name = "save_application",
  func = "save_application",
  description="Saves Tailored resume and cover letter to files"
)

tools = [read_tool,save_tool]


from pydantic import BaseModel,Field
from typing import List

class ApplicationOutput(BaseModel):
  job_title:str
  tailored_resume:str
  cover_letter:str
