import gradio as gr
import subprocess
import os
import uuid
import shutil

def separate_vocals(audio_path):
    if audio_path is None:
        return None, None
    
    job_id = str(uuid.uuid4())
    os.makedirs("tmp", exist_ok=True)
    
    input_path = f"tmp/{job_id}.wav"
    shutil.copy(audio_path, input_path)
    
    try:
        subprocess.run([
            "demucs",
            "--two-stems=vocals",
            "-o", f"tmp/out_{job_id}",
            input_path
        ], check=True)
    except subprocess.CalledProcessError:
        return None, None
    
    base = os.path.splitext(os.path.basename(input_path))[0]
    vocals_path = f"tmp/out_{job_id}/htdemucs/{base}/vocals.wav"
    inst_path = f"tmp/out_{job_id}/htdemucs/{base}/no_vocals.wav"
    
    return vocals_path, inst_path


with gr.Blocks(title="AI Vocal Remover") as demo:
    gr.Markdown("# 🎤 AI Vocal Remover")
    gr.Markdown("သီချင်း Upload လုပ်ပါ။ AI က vocal နဲ့ instrumental ခွဲပေးမယ်။")
    
    with gr.Row():
        audio_in = gr.Audio(type="filepath", label="သီချင်း Upload")
    
    btn = gr.Button("🎵 ခွဲမယ်", variant="primary")
    
    with gr.Row():
        vocals_out = gr.Audio(label="🎙️ Vocals")
        inst_out = gr.Audio(label="🎸 Instrumental")
    
    btn.click(
        fn=separate_vocals,
        inputs=audio_in,
        outputs=[vocals_out, inst_out]
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
