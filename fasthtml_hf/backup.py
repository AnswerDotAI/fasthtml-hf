from fastcore.utils import *
import os, shutil, datetime
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
from huggingface_hub import snapshot_download, upload_folder, create_repo, repo_exists, whoami

def _token(): return os.getenv("HF_TOKEN")

def get_cfg():
    return Config('.', 'config.ini',
                  types=dict(dataset_id=str, db_dir=str, private_backup=bool),
                  create=dict(dataset_id='todos-backup', db_dir='data', private_backup=True))

def get_dataset_id(cfg):
    token,dataset_id = _token(),cfg.dataset_id
    if "/" in dataset_id or token is None: return dataset_id
    return f"{whoami(token)['name']}/{dataset_id}"

def download():
    cfg = get_cfg()
    dataset_id = get_dataset_id(cfg)
    if os.getenv("SPACE_ID") and repo_exists(dataset_id, repo_type="dataset", token=os.getenv("HF_TOKEN")):
        cache_path = snapshot_download(repo_id=dataset_id, repo_type='dataset',
                                       token=_token())
        shutil.copytree(cache_path, cfg.db_dir, dirs_exist_ok=True)

def upload():
    cfg = get_cfg()
    if not os.getenv("SPACE_ID"): return
    dataset_id = get_dataset_id(cfg)
    create_repo(dataset_id, token=_token, private=True, repo_type='dataset', exist_ok=True)
    upload_folder(folder_path=cfg.db_dir, token=_token(),
                repo_id=dataset_id, repo_type='dataset',
                commit_message=f"backup at {datetime.datetime.now()}")
