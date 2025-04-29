import gradio as gr
from pytube import YouTube
from pydub import AudioSegment
import os

def convert_youtube_to_mp3(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=".")
    new_file = os.path.splitext(out_file)[0] + ".mp3"
    AudioSegment.from_file(out_file).export(new_file, format="mp3")
    os.remove(out_file)
    return new_file

def convert_audio(uploaded_file, output_format):
    audio = AudioSegment.from_file(uploaded_file.name)
    output_filename = f"converted_audio.{output_format}"
    audio.export(output_filename, format=output_format)
    return output_filename

with gr.Blocks() as demo:
    gr.Markdown("# Conversor de Áudio e YouTube para MP3")
    
    with gr.Tab("Converter Áudio"):
        with gr.Row():
            audio_input = gr.File(label="Selecione um arquivo de áudio")
            format_output = gr.Dropdown(choices=["mp3", "wav", "ogg"], label="Formato de saída")
            audio_btn = gr.Button("Converter")
            audio_output = gr.File(label="Download do áudio convertido")
        audio_btn.click(convert_audio, inputs=[audio_input, format_output], outputs=audio_output)

    with gr.Tab("Converter YouTube para MP3"):
        with gr.Row():
            yt_url = gr.Textbox(label="URL do YouTube")
            yt_btn = gr.Button("Converter")
            yt_output = gr.File(label="Download do MP3")
        yt_btn.click(convert_youtube_to_mp3, inputs=yt_url, outputs=yt_output)

import os
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
