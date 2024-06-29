import datetime
from huggingface_hub import create_repo, upload_folder, add_space_secret, whoami
from fastcore.utils import *
from fastcore.script import *

def _mk_docker(python_ver):
    fn = Path('Dockerfile')
    if fn.exists(): return
    packages = Path('packages.txt')
    pkg_line = ''
    reqs = Path('requirements.txt')
    if not reqs.exists(): reqs.write_text('python-fasthtml')
    req_line = f'RUN pip install --no-cache-dir -r requirements.txt'
    if packages.exists():
        pkglist = ' '.join(packages.readlines())
        pkg_line = f'RUN apt-get update -y && apt-get install -y {pkglist}'

    cts = f"""FROM python:{python_ver}
WORKDIR /code
COPY --link --chown=1000 . .
RUN mkdir -p /tmp/cache/
RUN chmod a+rwx -R /tmp/cache/
ENV HF_HUB_CACHE=HF_HOME
{req_line}
{pkg_line}
ENV PYTHONUNBUFFERED=1 PORT=7860
CMD ["python", "main.py"]
"""
    fn.write_text(cts)

@call_parse
def deploy(
    token:str=None, # Hugging Face token for authentication
    space_id:str="fasthtml-todos", # ID of the space to upload to
    python_ver:str='3.10', # Version of python to use
    upload:bool_arg=True, # Set to `false` to skip uploading files
    private:bool_arg=False): # Make the repository private
    "Upload current directory to Hugging Face Spaces"
    if not token: token=os.getenv('HF_TOKEN')
    if not token: return print('No token available')
    if "/" not in space_id: space_id = f"{whoami(token)['name']}/{space_id}"
    _mk_docker(python_ver)
    url = create_repo(space_id, token=token, repo_type='space',
                      space_sdk="docker", private=private, exist_ok=True)
    if not upload: return print('Repo created; upload skipped')
    upload_folder(folder_path=Path("."),
                repo_id=space_id, repo_type='space',
                ignore_patterns=['__pycache__/*', '.sesskey', 'deploy_hf.py', 'data/*'],
                commit_message=f"deploy at {datetime.datetime.now()}",
                token=token)
    add_space_secret(space_id, token=token, key="HF_TOKEN", value=token)
    print(f"Deployed space at {url}")

