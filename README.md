# FastHTML on 🤗 Spaces

Deploy a FastHTML application to [Hugging Face Spaces](https://huggingface.co/spaces) for free with one command!

## Quickstart

1. Create a free account on [Hugging Face](https://huggingface.co)
2. Go to your account settings and create an access token with write access. Keep this token safe and don't share it.
3. Set the `HF_TOKEN` environment variable to that token
4. Install fasthtml-hf: `pip install fasthtml-hf`
5. HuggingFace needs `fasthtml-hf` to run your space, so add it to your requirements.txt file.
6. At the top of your `main.py` add `from fasthtml_hf import setup_hf_backup`, and just before you run uvicorn add `setup_hf_backup(app)`. If you run uvicorn in an `if __name__ == "__main__"` block, you'll need to call `setup_hf_backup(app)` *before* the `if` block.
7. Run `fh_hf_deploy <space_name>`, replacing `<space_name>` with the name you want to give your space.

By default this will upload a public space. You can make it private with `--private true`.

## Configuration

The space will upload a backup of your database to a [Hugging Face Dataset](https://huggingface.co/datasets). By default it will be private and its name will be `<your-huggingface-id>/space-backup`. You can change this behavior in the `config.ini` file. If not provided, a default file will be created with the contents (note that the `[DEFAULT]` line is required at the top):

```
[DEFAULT]
dataset_id = space-backup
db_dir = data
private_backup = True
interval = 15 # number of minutes between periodic backups
```

If you so choose, you can disable the automatic backups and use [persistent storage](https://huggingface.co/docs/hub/en/spaces-storage#persistent-storage-specs) instead for $5/month (USD). 
